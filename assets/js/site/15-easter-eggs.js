    /**
     * 12. Easter Eggs
     * - Konami code ↑↑↓↓←→←→BA : meteor storm (dark) / sunlight party (light)
     * - Click the moon / sun   : celestial reaction
     * - Oct 25 (birthday)      : toast + golden Scorpius
     */
    var isZh = (document.documentElement.lang || '').indexOf('zh') === 0;
    var eggToastTimer = null;
    var showToast = function(text, ms) {
        var t = document.querySelector('.egg-toast');
        if (!t) {
            t = document.createElement('div');
            t.className = 'egg-toast';
            t.setAttribute('role', 'status');
            document.body.appendChild(t);
        }
        t.textContent = text;
        t.classList.add('show');
        clearTimeout(eggToastTimer);
        eggToastTimer = setTimeout(function() { t.classList.remove('show'); }, ms || 3500);
    };

    var meteorBurst = function(count) {
        if (!sky || reduceMotion) return;
        for (var i = 0; i < count; i++) {
            (function(n) {
                setTimeout(function() {
                    var m = document.createElement('div');
                    m.className = 'meteor burst';
                    m.style.top = (Math.random() * 40 - 5) + '%';
                    m.style.left = (20 + Math.random() * 90) + '%';
                    m.style.width = (90 + Math.random() * 140) + 'px';
                    var dur = 0.7 + Math.random() * 0.9;
                    m.style.animationDuration = dur + 's';
                    m.style.animationIterationCount = '1';
                    sky.appendChild(m);
                    setTimeout(function() { m.remove(); }, dur * 1000 + 150);
                }, n * 120);
            })(i);
        }
    };

    var KONAMI = ['ArrowUp', 'ArrowUp', 'ArrowDown', 'ArrowDown',
                  'ArrowLeft', 'ArrowRight', 'ArrowLeft', 'ArrowRight', 'b', 'a'];
    var kIdx = 0;
    document.addEventListener('keydown', function(e) {
        var k = e.key.length === 1 ? e.key.toLowerCase() : e.key;
        kIdx = (k === KONAMI[kIdx]) ? kIdx + 1 : (k === KONAMI[0] ? 1 : 0);
        if (kIdx === KONAMI.length) {
            kIdx = 0;
            if (document.documentElement.dataset.theme === 'dark') {
                meteorBurst(30);
            } else {
                document.body.classList.add('party-sky');
                setTimeout(function() { document.body.classList.remove('party-sky'); }, 8000);
            }
            showToast(isZh ? '🌠 隐藏咒语生效！' : '🌠 Konami unlocked!');
        }
    });

    var moonEl = document.querySelector('.moon');
    var sunEl = document.querySelector('.sun');
    if (moonEl) {
        moonEl.addEventListener('click', function() {
            meteorBurst(6);
            showToast(isZh ? '🌙 你戳了一下月亮' : '🌙 You poked the moon');
        });
    }
    if (sunEl) {
        sunEl.addEventListener('click', function() {
            document.body.classList.add('party-sky');
            setTimeout(function() { document.body.classList.remove('party-sky'); }, 3000);
            showToast(isZh ? '☀️ 小心刺眼' : '☀️ Careful, it\'s bright');
        });
    }

    var today = new Date();
    if (today.getMonth() === 9 && today.getDate() === 25) {
        var con = document.querySelector('.constellation');
        if (con) con.classList.add('birthday');
        setTimeout(function() {
            showToast(isZh ? '🎂 今天是博主的生日，天蝎座 full power！'
                           : '🎂 It\'s the author\'s birthday — Scorpius at full power!', 6000);
        }, 1500);
    }

