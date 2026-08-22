/**
 * 20. Chat Panel — floating site-assistant backed by the blog-chat-agent
 * cloud function (hunyuan-exp, server-side key, rate-limited). Zero deps.
 * Markup is created lazily on first open so pages without interaction
 * never pay for it.
 */
var CHAT_ENDPOINT = 'https://hunyuan-d2gk9echy7cc73225.service.tcloudbase.com/api/chat';

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
        }
    }

    fab.addEventListener('click', function () { toggle(panel.hidden); });
    closeBtn.addEventListener('click', function () { toggle(false); });
    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && !panel.hidden) toggle(false);
    });

    form.addEventListener('submit', async function (e) {
        e.preventDefault();
        var text = input.value.trim();
        if (!text || sendBtn.disabled) return;
        input.value = '';
        bubble('user', text);
        setPending(true);
        var pending = bubble('assistant', isZh ? '思考中…' : 'Thinking…');
        try {
            // No custom Content-Type: keeps this a CORS "simple request" so the
            // gateway never has to answer a preflight OPTIONS round-trip.
            var res = await fetch(CHAT_ENDPOINT, {
                method: 'POST',
                body: JSON.stringify({ message: text, history: history, lang: isZh ? 'zh' : 'en' }),
            });
            var data = await res.json().catch(function () { return {}; });
            if (!res.ok || !data.reply) throw new Error(data.error || String(res.status));
            pending.textContent = data.reply;
            history.push({ role: 'user', content: text }, { role: 'assistant', content: data.reply });
        } catch (err) {
            pending.classList.add('chat-error');
            pending.textContent = isZh
                ? '出错了，稍后再试。（' + (err && err.message ? err.message : 'network') + '）'
                : 'Something went wrong, try again later. (' + (err && err.message ? err.message : 'network') + ')';
        } finally {
            setPending(false);
            log.scrollTop = log.scrollHeight;
        }
    });
}

chatInit(); // functional UI, not decoration — init regardless of reduced motion
