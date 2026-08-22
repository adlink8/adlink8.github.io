/**
 * blog-chat-agent — web-function chat endpoint for adlink8.github.io
 *
 * Runs as a CloudBase HTTP (web) function: scf_bootstrap launches this
 * server on $PORT. Security posture:
 * - Model access stays entirely server-side (hunyuan-exp, free inspire-pack quota)
 * - CORS locked to the blog's own origins; kill switch via AGENT_ENABLED=false
 * - Per-IP minute limiter + global daily cap (in-memory, best-effort across
 *   instances; upgrade path is a NoSQL counter when drift matters)
 * - Prompts/answers are never logged — only token counts and truncated IPs
 */
const http = require('http');
const tcb = require('@cloudbase/node-sdk');

const app = tcb.init({ env: 'hunyuan-d2gk9echy7cc73225' });
const ai = app.ai();
const model = ai.createModel('hunyuan-exp');
const MODEL_ID = 'hunyuan-2.0-instruct-20251111';

const ALLOWED_ORIGINS = [
    'https://adlink8.github.io',
    'http://127.0.0.1:1313',
    'http://localhost:1313',
];
const MAX_MESSAGE_CHARS = 2000;
const MAX_HISTORY_MESSAGES = 12; // prior turns kept in context
const RATE_PER_MINUTE = 6;       // per IP
const DAILY_GLOBAL_CAP = 500;

const SYSTEM_PROMPTS = {
    zh: [
        '你是 Li Shuo Yan 个人博客（adlink8.github.io）的站内助手。',
        '他的方向是 DevOps × AI 工程：CI/CD、云基础设施、RAG/LLM 系统；',
        '代表项目 novel-mind 是面向中文长文本的 RAG 平台，另有 t5ai-codex-quota IoT 设备监控器等。',
        '只回答与站主、博客内容、项目和技术学习相关的问题；话题无关时礼貌拒绝并引导回站点内容。',
        '不编造未提及的事实；回答保持简洁（一般不超过 200 字），使用中文。',
    ].join('\n'),
    en: [
        "You are the on-site assistant of Li Shuo Yan's personal blog (adlink8.github.io).",
        'His focus is DevOps × AI engineering: CI/CD, cloud infrastructure, RAG/LLM systems;',
        'his flagship project novel-mind is a long-text Chinese RAG platform, plus an IoT device monitor (t5ai-codex-quota).',
        'Answer only questions about the site owner, the blog content, his projects, and technical learning; politely decline unrelated topics.',
        'Never invent facts not present here; keep answers concise (under 150 words), and reply in English.',
    ].join('\n'),
};

// --- rate limiting via NoSQL counters (shared across instances) ---
// Keys: "m:<ip>:<minute-slot>" and "d:global:<date>". Old docs are tiny and
// pruned lazily; a dedicated TTL sweep is not worth it at blog traffic levels.
const db = app.database();
const rateCol = db.collection('agent_rate');

async function bumpCounter(key) {
    const _ = db.command;
    try {
        const r = await rateCol.doc(key).update({ count: _.inc(1), ts: Date.now() });
        if (!r.stats || r.stats.updated === 0) throw new Error('missing');
    } catch {
        await rateCol.add({ _id: key, count: 1, ts: Date.now() }).catch(() => {});
    }
    try {
        const d = await rateCol.doc(key).get();
        const arr = Array.isArray(d.data) ? d.data : [d.data];
        return (arr[0] && arr[0].count) || 1;
    } catch {
        return 1;
    }
}

async function isRateLimited(ip) {
    const minuteSlot = Math.floor(Date.now() / 60_000);
    const todayUTC = new Date().toISOString().slice(0, 10);
    const [minuteCount, dayCount] = await Promise.all([
        bumpCounter(`m:${ip}:${minuteSlot}`),
        bumpCounter(`d:global:${todayUTC}`),
    ]);
    return minuteCount > RATE_PER_MINUTE || dayCount > DAILY_GLOBAL_CAP;
}

function send(res, status, origin, payload) {
    res.writeHead(status, {
        'Content-Type': 'application/json; charset=utf-8',
        'Cache-Control': 'no-store',
    });
    res.end(JSON.stringify(payload));
}

function readBody(req) {
    return new Promise((resolve, reject) => {
        let size = 0;
        const chunks = [];
        req.on('data', (c) => {
            size += c.length;
            if (size > 64 * 1024) { reject(new Error('body too large')); req.destroy(); return; }
            chunks.push(c);
        });
        req.on('end', () => resolve(Buffer.concat(chunks).toString('utf8')));
        req.on('error', reject);
    });
}

const server = http.createServer(async (req, res) => {
    const origin = req.headers.origin || '';
    const cors = {
        // NOTE: intentionally NO Access-Control-* headers here. The CloudBase
        // gateway (cross-domain check on) appends its own; adding ours too
        // yields "origin,origin" which browsers must reject.
    };

    try {
        if (req.method === 'OPTIONS') {
            res.writeHead(204, cors);
            res.end();
            return;
        }
        if (!ALLOWED_ORIGINS.includes(origin)) return send(res, 403, origin, { error: 'origin not allowed' });
        if (req.method !== 'POST') return send(res, 405, origin, { error: 'method not allowed' });

        if (process.env.AGENT_ENABLED === 'false') {
            return send(res, 503, origin, { error: 'assistant temporarily disabled' });
        }

        // The edge proxy sets these from the actual TCP peer; x-real-ip here is
        // an internal hop address. x-envoy-external-address cannot be spoofed by
        // the client; the x-forwarded-for head is the real client unless they
        // forge the header outright (acceptable residual risk for v1 limiting).
        const ip = req.headers['x-envoy-external-address']
            || String(req.headers['x-forwarded-for'] || '').split(',').map((s) => s.trim()).filter(Boolean)[0]
            || 'unknown';
        if (await isRateLimited(ip)) return send(res, 429, origin, { error: 'too many requests, slow down' });

        let body;
        try {
            body = JSON.parse(await readBody(req));
        } catch {
            return send(res, 400, origin, { error: 'invalid JSON body' });
        }

        const message = typeof body.message === 'string' ? body.message.trim() : '';
        const lang = body.lang === 'en' ? 'en' : 'zh';
        if (!message || message.length > MAX_MESSAGE_CHARS) {
            return send(res, 400, origin, { error: `message must be 1..${MAX_MESSAGE_CHARS} chars` });
        }

        // keep at most N most-recent prior turns, each role-validated and length-capped
        const history = Array.isArray(body.history) ? body.history.slice(-MAX_HISTORY_MESSAGES) : [];
        const cleanHistory = history
            .filter((m) => m && (m.role === 'user' || m.role === 'assistant') && typeof m.content === 'string')
            .map((m) => ({ role: m.role, content: m.content.slice(0, MAX_MESSAGE_CHARS) }));

        const result = await model.generateText({
            model: MODEL_ID,
            messages: [
                { role: 'system', content: SYSTEM_PROMPTS[lang] },
                ...cleanHistory,
                { role: 'user', content: message },
            ],
            temperature: 0.6,
        });

        console.log(`chat ok ip=${ip.slice(0, 8)} tokens=${result.usage?.total_tokens ?? '?'}`);
        send(res, 200, origin, { reply: result.text, usage: { total_tokens: result.usage?.total_tokens ?? null } });
    } catch (err) {
        console.error('request failed:', err && err.message ? err.message : err);
        if (!res.headersSent) send(res, 502, origin, { error: 'model call failed' });
        else res.end();
    }
});

server.listen(process.env.PORT || 9000, () => {
    console.log('blog-chat-agent listening on', process.env.PORT || 9000);
});
