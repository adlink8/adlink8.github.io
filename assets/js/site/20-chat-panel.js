/**
 * 20. Chat Panel — floating site-assistant backed by the blog-chat-agent
 * cloud function (hunyuan-exp, server-side key, rate-limited). Zero deps.
 * Markup is created lazily on first open so pages without interaction
 * never pay for it.
 *
 * Replies stream: the request body carries {"stream":true} and the same
 * endpoint answers text/event-stream (chunk/done/error frames). Any failure
 * before the stream starts — network error, non-SSE response — retries once
 * against STREAM_FALLBACK (same endpoint minus the flag, classic JSON).
 */
var CHAT_ENDPOINT = 'https://hunyuan-d2gk9echy7cc73225.service.tcloudbase.com/api/chat';
var STREAM_FALLBACK = CHAT_ENDPOINT; // same route; omitting {"stream":true} selects the JSON reply

function chatBuildPanel() {
    var wrap = document.createElement('div');
    wrap.className = 'chat-widget';
    wrap.innerHTML =
        '<button class="chat-fab" type="button" aria-expanded="false" aria-haspopup="dialog">' +
            '<span class="chat-fab-icon" aria-hidden="true">💬</span>' +
        '</button>' +
        '<div class="chat-panel" role="dialog" aria-modal="false" hidden>' +
            '<div class="chat-head">' +
                '<span class="chat-title"></span>' +
                '<button class="chat-close" type="button" aria-label="close">×</button>' +
            '</div>' +
            '<div class="chat-log" aria-live="polite"></div>' +
            '<form class="chat-form">' +
                '<input class="chat-input" type="text" maxlength="2000" autocomplete="off" />' +
                '<button class="chat-send" type="submit"></button>' +
            '</form>' +
        '</div>';
    return wrap;
}

function chatInit() {
    var root = chatBuildPanel();
    document.body.appendChild(root);
    var fab = root.querySelector('.chat-fab');
    var panel = root.querySelector('.chat-panel');
    var log = root.querySelector('.chat-log');
    var form = root.querySelector('.chat-form');
    var input = root.querySelector('.chat-input');
    var sendBtn = root.querySelector('.chat-send');
    var closeBtn = root.querySelector('.chat-close');

    var title = isZh ? '站内助手' : 'Site Assistant';
    var placeholder = isZh ? '问我关于这个站的问题…' : 'Ask about this site…';
    var sendLabel = isZh ? '发送' : 'Send';
    var greeting = isZh
        ? '你好！我是站内助手，可以聊聊站长的方向、novel-mind 项目或博客里的文章。'
        : "Hi! I'm the site assistant — ask about the owner's work, the novel-mind project, or anything on this blog.";
    root.querySelector('.chat-title').textContent = title;
    input.placeholder = placeholder;
    sendBtn.textContent = sendLabel;
    sendBtn.setAttribute('aria-label', sendLabel);

    var history = []; // {role, content} prior turns sent with each request
    var activeAbort = null; // AbortController of the in-flight request, if any
    var thinking = isZh ? '思考中…' : 'Thinking…';

    function bubble(role, text) {
        var el = document.createElement('div');
        el.className = 'chat-msg chat-' + role;
        el.textContent = text;
        log.appendChild(el);
        log.scrollTop = log.scrollHeight;
        return el;
    }

    function setPending(on) {
        sendBtn.disabled = on;
        input.disabled = on;
        sendBtn.textContent = isZh ? (on ? '…' : '发送') : (on ? '…' : 'Send');
    }

    function toggle(open) {
        panel.hidden = !open;
        fab.setAttribute('aria-expanded', String(open));
        if (open && !log.childNodes.length) bubble('assistant', greeting);
        if (open) {
            requestAnimationFrame(function () { panel.classList.add('on'); });
            // rAF stays suspended in some embedded webviews (in-app browsers);
            // without this fallback the panel would sit at opacity:0 with
            // pointer-events:none forever. classList.add is idempotent.
            setTimeout(function () { panel.classList.add('on'); }, 60);
            input.focus();
        } else {
            panel.classList.remove('on');
            if (activeAbort) activeAbort.abort(); // keep whatever text already streamed
        }
    }

    fab.addEventListener('click', function () { toggle(panel.hidden); });
    closeBtn.addEventListener('click', function () { toggle(false); });
    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && !panel.hidden) toggle(false);
    });

    // Reads the SSE body via fetch (EventSource can't POST), splitting on the
    // blank-line frame boundary. Chunks render into `pending` as they arrive;
    // the returned promise settles with the full text on done, throws on
    // error/abort. err.streamed=true marks failures after content arrived —
    // those must not trigger the JSON fallback (the question was answered).
    async function readAssistantStream(res, pending) {
        var reader = res.body.getReader();
        var decoder = new TextDecoder();
        var buf = '';
        var out = '';
        var sawFrame = false;
        function handleFrame(frame) {
            var lines = frame.split('\n');
            for (var j = 0; j < lines.length; j++) {
                if (lines[j].indexOf('data:') !== 0) continue;
                var evt;
                try { evt = JSON.parse(lines[j].slice(5).trim()); } catch (e) { continue; }
                sawFrame = true;
                if (evt.type === 'chunk') {
                    out += evt.text || '';
                    pending.textContent = out;
                    log.scrollTop = log.scrollHeight;
                } else if (evt.type === 'done') {
                    if (!out) { // done with zero chunks — don't store an empty turn
                        var empty = new Error('empty reply');
                        empty.streamed = true; // question was consumed — no retry
                        throw empty;
                    }
                    return out;
                } else if (evt.type === 'error') {
                    var err = new Error(evt.message || 'stream error');
                    err.streamed = out !== '';
                    throw err;
                }
            }
            return null;
        }
        try {
            for (;;) {
                var r = await reader.read();
                if (r.done) break;
                buf += decoder.decode(r.value, { stream: true });
                var frames = buf.split('\n\n');
                buf = frames.pop(); // incomplete tail stays buffered
                for (var i = 0; i < frames.length; i++) {
                    var done = handleFrame(frames[i]);
                    if (done !== null) return done;
                }
            }
        } catch (e) {
            if (out !== '' || sawFrame) e.streamed = true;
            throw e;
        }
        if (!out) throw new Error('stream ended without content');
        return out; // stream closed early — partial text beats an error
    }

    // Classic single-shot JSON reply — the fallback and pre-stream behavior.
    async function askJSON(text, controller) {
        var res = await fetch(STREAM_FALLBACK, {
            method: 'POST',
            body: JSON.stringify({ message: text, history: history, lang: isZh ? 'zh' : 'en' }),
            signal: controller.signal,
        });
        var data = await res.json().catch(function () { return {}; });
        if (!res.ok || !data.reply) throw new Error(data.error || String(res.status));
        return data.reply;
    }

    form.addEventListener('submit', async function (e) {
        e.preventDefault();
        var text = input.value.trim();
        if (!text || sendBtn.disabled) return;
        input.value = '';
        bubble('user', text);
        setPending(true);
        var pending = bubble('assistant', thinking);
        var controller = new AbortController();
        activeAbort = controller;
        var reply = '';
        try {
            try {
                // No custom Content-Type: keeps this a CORS "simple request" so the
                // gateway never has to answer a preflight OPTIONS round-trip.
                var res = await fetch(CHAT_ENDPOINT, {
                    method: 'POST',
                    body: JSON.stringify({ message: text, history: history, lang: isZh ? 'zh' : 'en', stream: true }),
                    signal: controller.signal,
                });
                var ct = (res.headers.get('content-type') || '').toLowerCase();
                if (!res.ok || ct.indexOf('json') !== -1) {
                    // validation / rate-limit / kill-switch errors are plain JSON
                    var data = await res.json().catch(function () { return {}; });
                    throw new Error(data.error || String(res.status));
                }
                reply = await readAssistantStream(res, pending);
            } catch (err) {
                if (controller.signal.aborted) throw err; // user closed the panel
                if (err && err.streamed) throw err; // mid-stream failure — no retry
                reply = await askJSON(text, controller); // stream unusable → legacy retry
            }
            pending.textContent = reply;
            history.push({ role: 'user', content: text }, { role: 'assistant', content: reply });
        } catch (err) {
            if (controller.signal.aborted) {
                // keep partial text; nothing streamed yet → say it was cut short
                pending.textContent = pending.textContent === thinking
                    ? (isZh ? '（已中断）' : '(interrupted)')
                    : pending.textContent;
            } else {
                var partial = pending.textContent !== thinking ? pending.textContent + '\n' : '';
                pending.classList.add('chat-error');
                pending.textContent = partial + (isZh
                    ? '出错了，稍后再试。（' + (err && err.message ? err.message : 'network') + '）'
                    : 'Something went wrong, try again later. (' + (err && err.message ? err.message : 'network') + ')');
            }
        } finally {
            activeAbort = null;
            setPending(false);
            log.scrollTop = log.scrollHeight;
        }
    });
}

chatInit(); // functional UI, not decoration — init regardless of reduced motion
