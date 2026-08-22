/**
 * retrieval.js — blog article grounding for blog-chat-agent.
 *
 * Pulls the site's existing search index (/index.json, /zh/index.json —
 * regenerated on every Hugo build, so articles update with each deploy),
 * caches it per warm instance, scores posts against the question with
 * weighted term overlap (CJK bigrams + latin words), and returns a
 * references block for the system prompt. Zero extra services.
 */
const ARTICLES_URL = {
    zh: 'https://adlink8.github.io/zh/index.json',
    en: 'https://adlink8.github.io/index.json',
};
const ARTICLES_TTL = 10 * 60_000;
const REF_TOP_K = 3;
const REF_SNIPPET_CHARS = 400;
const REF_TOTAL_CHARS = 3000;

let articlesCache = { lang: '', ts: 0, list: [] };

function stripHtml(html) {
    return String(html)
        .replace(/<[^>]+>/g, ' ')
        .replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>')
        .replace(/&quot;/g, '"').replace(/&#39;/g, "'")
        .replace(/\s+/g, ' ')
        .trim();
}

function tokenize(text) {
    const terms = {};
    const latin = String(text).toLowerCase().match(/[a-z0-9][a-z0-9-]{1,}/g) || [];
    for (const w of latin) terms[w] = 1;
    const han = String(text).match(/[\u4e00-\u9fff]+/g) || [];
    for (const run of han) {
        if (run.length === 1) terms[run] = 1;
        for (let j = 0; j + 2 <= run.length; j++) terms[run.slice(j, j + 2)] = 1;
    }
    return Object.keys(terms);
}

function countOccurrences(hay, needle) {
    if (!needle) return 0;
    let n = 0;
    let idx = hay.indexOf(needle);
    while (idx !== -1) { n += 1; idx = hay.indexOf(needle, idx + needle.length); }
    return n;
}

async function fetchIndex(lang) {
    // Direct github.io access from mainland egress is slow/flaky — generous
    // timeout plus one retry; failure degrades to un-grounded answers.
    for (let attempt = 0; attempt < 2; attempt++) {
        try {
            const res = await fetch(ARTICLES_URL[lang], { signal: AbortSignal.timeout(10_000) });
            if (res.ok) return await res.json();
        } catch { /* retry */ }
    }
    return null;
}

async function loadArticles(lang) {
    const now = Date.now();
    if (articlesCache.lang === lang && now - articlesCache.ts < ARTICLES_TTL && articlesCache.list.length) {
        return articlesCache.list;
    }
    const pages = await fetchIndex(lang);
    if (!pages) return articlesCache.lang === lang ? articlesCache.list : [];
    const list = (Array.isArray(pages) ? pages : pages.pages || [])
        .map((p) => ({ title: p.title || '', permalink: p.permalink || '', text: stripHtml(p.content || '') }))
        .filter((a) => a.title && a.text);
    articlesCache = { lang, ts: now, list };
    return list;
}

function bestParagraph(text, terms) {
    const paras = text.split(/(?<=[。！？!?])\s/).concat(text.split(/\s{3,}/));
    let best = '';
    let bestHits = 0;
    for (const p of paras) {
        if (p.length < 40) continue;
        let hits = 0;
        for (const t of terms) hits += countOccurrences(p, t);
        if (hits > bestHits) { bestHits = hits; best = p; }
    }
    return bestHits > 0 ? best : '';
}

async function buildSystemReferences(lang, query) {
    const articles = await loadArticles(lang);
    if (!articles.length) return '';
    const terms = tokenize(query);
    if (!terms.length) return '';

    const scored = articles
        .map((a) => {
            const titleL = a.title.toLowerCase();
            let score = 0;
            for (const t of terms) {
                score += 3 * countOccurrences(titleL, t);
                score += countOccurrences(a.text, t) / 50; // damped body hits
            }
            return { a, score, para: bestParagraph(a.text, terms) };
        })
        .filter((s) => s.score > 0 && s.para)
        .sort((x, y) => y.score - x.score)
        .slice(0, REF_TOP_K);
    if (!scored.length) return '';

    const lines = [
        '',
        lang === 'zh'
            ? '以下是站内文章检索结果(可能相关)。回答相关问题请优先依据它们,不确定就明说,并在有帮助时给出原文链接:'
            : 'Retrieved blog articles (possibly relevant). Ground relevant answers in them, say so when unsure, and link the source when helpful:',
        '',
    ];
    let used = 0;
    for (let k = 0; k < scored.length; k++) {
        const s = scored[k];
        let snippet = s.para.slice(0, REF_SNIPPET_CHARS);
        if (used + snippet.length > REF_TOTAL_CHARS) snippet = snippet.slice(0, Math.max(0, REF_TOTAL_CHARS - used));
        if (!snippet) break;
        used += snippet.length;
        lines.push('[' + (k + 1) + '] ' + s.a.title + '\n' + (lang === 'zh' ? '链接: ' : 'link: ') + s.a.permalink + '\n' + (lang === 'zh' ? '片段: ' : 'snippet: ') + snippet);
    }
    return lines.length > 3 ? lines.join('\n') : '';
}

module.exports = { buildSystemReferences };
