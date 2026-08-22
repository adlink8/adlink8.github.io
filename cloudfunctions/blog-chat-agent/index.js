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
const { buildSystemReferences } = require('./retrieval');

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

// Depth is inferred by the model from the question's wording — no UI tiers.
// Server-side quick-tier detection: prompt-only guides proved too soft for
// this model, so explicit trigger words force a hard per-request constraint.
const QUICK_TRIGGERS = [
    /一句话/, /简短/, /简单说/, /只要结论/, /速览/, /快速了解/, /长话短说/,
    /in one sentence/i, /briefly/i, /in short/i, /just the (?:point|answer)/i, /tl;?dr/i, /quick(?:ly)? answer/i,
];
const QUICK_HARD = {
    zh: '\n[本次硬性要求]提问者要求极速版:回答必须 1~2 句、总计不超过 60 字,禁止使用列表和"要点"段。',
    en: '\n[HARD RULE for this reply] The asker wants the quick version: answer in 1-2 sentences, under 40 words total, no lists.',
};

function quickAsked(text) {
    return QUICK_TRIGGERS.some(function (re) { return re.test(text); });
}

// Deterministic tier-1 enforcement: the model tends to append a "要点" block
// even when told not to, so keep only leading complete sentences up to ~60 chars.
function quickTruncate(text) {
    var parts = text.replace(/^[-*•]\s*/gm, '').split(/(?<=[。！？!?])/);
    var out = '';
    for (var i = 0; i < parts.length; i++) {
        var s = parts[i].trim();
        if (!s) continue;
        if (out && (out + s).length > 60) break;
        out += (out ? '' : '') + s;
        if (out.length >= 40) break;
    }
    return out || text.slice(0, 60);
}

const DEPTH_GUIDE = {
    zh: [
        '回答深度自适应提问者意图,自主判断三类:',
        '① 极速了解——措辞含"一句话""简短""简单说""快速""只要结论""速览"任一时,必须执行:1~2 句、合计不超过 60 字、禁止列表;',
        '② 轻微了解(一般性提问)→ 约 100~150 字,先结论后要点;',
        '③ 深入了解(明确要细节、原理、做法、架构)→ 分层展开:结论 → 背景/原理 → 关键细节或例子,可用小标题与列表,至多约 400 字。',
        '依据提问措辞与上下文自行判断,不要反问用户想要哪种深度。',
    ].join('\n'),
    en: [
        'Adapt answer depth to the asker\u2019s intent, self-classified into three tiers:',
        '(1) quick skim — when wording contains "in one sentence", "briefly", "quick", "just the point", or similar, this tier is MANDATORY: 1-2 sentences, under 40 words total, no lists;',
        '(2) light understanding (ordinary questions) -> ~100-150 words, conclusion first;',
        '(3) deep dive (explicitly asks for details, how it works, architecture) -> layered: conclusion -> context -> key details/examples, headings/lists allowed, up to ~300 words.',
        'Judge from the wording and context yourself; never ask which depth the user wants.',
    ].join('\n'),
};

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
                { role: 'system', content: SYSTEM_PROMPTS[lang] + '\n' + DEPTH_GUIDE[lang] + (quickAsked(message) ? QUICK_HARD[lang] : '') + '\n' + await buildSystemReferences(lang, message) },
                ...cleanHistory,
                { role: 'user', content: message },
            ],
            temperature: 0.6,
        });

        var reply = result.text;
        if (quickAsked(message)) reply = quickTruncate(reply);
        console.log(`chat ok ip=${ip.slice(0, 8)} tokens=${result.usage?.total_tokens ?? '?'}`);
        send(res, 200, origin, { reply: reply, usage: { total_tokens: result.usage?.total_tokens ?? null } });
    } catch (err) {
        console.error('request failed:', err && err.message ? err.message : err);
        if (!res.headersSent) send(res, 502, origin, { error: 'model call failed' });
        else res.end();
    }
});

server.listen(process.env.PORT || 9000, () => {
    console.log('blog-chat-agent listening on', process.env.PORT || 9000);
});
