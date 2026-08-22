    /**
     * 13. More Eggs — Van Gogh "Starry Night" (canvas), typed words,
     * logo disco, late-night owl, copy toast
     *
     * Starry Night flow:
     *   1. GATHER (~5s) — faint stars light up one by one on a jittered
     *      grid (even coverage, neither dense nor sparse)
     *   2. SWIRL — stars orbit the nearest swirl center along SEMICIRCLE
     *      arcs, leaving fading trails; angular speed ramps up gradually;
     *      after ~180° of travel a star respawns elsewhere (brush-stroke feel)
     */
    var starryTimer = null;
    var starry = null; // active canvas session

    var stopStarry = function() {
        if (!starry) return;
        var s = starry;
        starry = null;
        if (s.raf) cancelAnimationFrame(s.raf);
        sky.classList.remove('starry');
        s.canvas.classList.add('starry-out');
        setTimeout(function() { s.canvas.remove(); }, 3200);
    };

    var startStarry = function() {
        var canvas = document.createElement('canvas');
        canvas.className = 'starry-canvas';
        sky.appendChild(canvas);
        var ctx = canvas.getContext('2d');
        var W = canvas.width = window.innerWidth;
        var H = canvas.height = window.innerHeight;

        // swirl centers — randomized positions every activation,
        // kept ≥220px apart and away from the edges
        var centers = [];
        var nC = 4 + Math.floor(Math.random() * 2); // 4–5 centers
        var tries = 0;
        while (centers.length < nC && tries < 80) {
            tries++;
            var cx = W * (0.1 + Math.random() * 0.8);
            var cy = H * (0.1 + Math.random() * 0.8);
            var ok = centers.every(function(c) {
                var dx = c.x - cx, dy = c.y - cy;
                return dx * dx + dy * dy > 220 * 220;
            });
            if (ok) centers.push({ x: cx, y: cy, dir: Math.random() < 0.5 ? 1 : -1 });
        }
        var nearest = function(x, y) {
            var best = centers[0], bd = Infinity;
            centers.forEach(function(c) {
                var d = (x - c.x) * (x - c.x) + (y - c.y) * (y - c.y);
                if (d < bd) { bd = d; best = c; }
            });
            return best;
        };

        // jittered grid: exactly one potential star per cell -> even spread
        var area = W * H;
        var count = Math.max(90, Math.min(230, Math.round(area / 7500)));
        var cell = Math.sqrt(area / count);
        var cols = Math.ceil(W / cell), rows = Math.ceil(H / cell);
        var cells = [];
        for (var r = 0; r < rows; r++)
            for (var q = 0; q < cols; q++)
                cells.push([q, r]);
        // shuffle, keep ~85% for a natural (not mechanical) coverage
        for (var i = cells.length - 1; i > 0; i--) {
            var j = Math.floor(Math.random() * (i + 1));
            var tmp = cells[i]; cells[i] = cells[j]; cells[j] = tmp;
        }
        cells = cells.slice(0, Math.round(cells.length * 0.85));

        var GATHER_MS = 5000;
        // blue-only trail palette
        var palette = [
            [120, 170, 255], [160, 200, 255], [100, 190, 255],
            [180, 215, 255], [140, 220, 255]
        ];
        var mkStar = function(cellXY, appearAt) {
            var x = cellXY[0] * cell + Math.random() * cell;
            var y = cellXY[1] * cell + Math.random() * cell;
            var c = nearest(x, y);
            var ang = Math.atan2(y - c.y, x - c.x);
            var dist = Math.sqrt((x - c.x) * (x - c.x) + (y - c.y) * (y - c.y));
            var col = palette[Math.floor(Math.random() * palette.length)];
            return {
                c: c, ang: ang, rad: Math.max(24, dist),
                size: 0.8 + Math.random() * 1.4,
                col: col,
                tw: Math.random() * Math.PI * 2,       // twinkle phase
                twF: 0.0015 + Math.random() * 0.0025,  // twinkle freq
                omega: (0.25 + Math.random() * 0.3) / Math.max(0.5, dist / 90), // inner faster
                traveled: 0,
                appearAt: appearAt,
                px: x, py: y,
                hist: [], // recent positions — the trail, redrawn each frame
                fade: 1,    // 0..1 brightness multiplier (birth/death ramp)
                dying: false // true once the semicircle is done: dim out, then respawn
            };
        };
        var stars = cells.map(function(cellXY, idx) {
            return mkStar(cellXY, (idx / cells.length) * GATHER_MS);
        });
        var respawn = function(s) {
            var cellXY = cells[Math.floor(Math.random() * cells.length)];
            var ns = mkStar(cellXY, -1); // already visible
            s.c = ns.c; s.ang = ns.ang; s.rad = ns.rad; s.col = ns.col;
            s.omega = ns.omega; s.px = ns.px; s.py = ns.py;
            s.traveled = 0;
            s.hist = []; // no streak across the screen to the new spot
        };

        var t0 = performance.now();
        var sess = { canvas: canvas, raf: null };
        starry = sess;
        sky.classList.add('starry');

        var frame = function(now) {
            if (starry !== sess) return;
            // stop if the user switched to light mode mid-show
            if (document.documentElement.dataset.theme !== 'dark') { stopStarry(); return; }
            var t = now - t0;

            if (t < GATHER_MS) {
                // phase 1: gather — plain redraw, stars appear one by one, twinkle
                ctx.clearRect(0, 0, W, H);
                stars.forEach(function(s) {
                    if (s.appearAt > t) return;
                    var fadeIn = Math.min(1, (t - s.appearAt) / 900);
                    var tw = 0.55 + 0.45 * Math.sin(now * s.twF + s.tw);
                    ctx.beginPath();
                    ctx.arc(s.px, s.py, s.size, 0, Math.PI * 2);
                    ctx.fillStyle = 'rgba(' + s.col[0] + ',' + s.col[1] + ',' + s.col[2] + ',' + (fadeIn * tw * 0.9).toFixed(3) + ')';
                    ctx.fill();
                });
            } else {
                // phase 2: swirl — full redraw each frame; every star keeps a
                // short position history drawn as a fading blue arc, so old
                // traces ALWAYS vanish (destination-out leaves stuck residue)
                var ramp = Math.min(1, (t - GATHER_MS) / 8000);       // speed ramps up
                var speed = 0.15 + ramp * 1.35;                        // 0.15x -> 1.5x
                var dt = Math.min(50, now - (sess.last || now)); sess.last = now;

                ctx.clearRect(0, 0, W, H);
                ctx.lineCap = 'round';

                stars.forEach(function(s) {
                    // movement — keeps flowing even while dimming out
                    var dA = s.omega * speed * s.c.dir * dt / 1000 * Math.PI;
                    s.ang += dA;
                    s.traveled += Math.abs(dA);
                    var nx = s.c.x + Math.cos(s.ang) * s.rad;
                    var ny = s.c.y + Math.sin(s.ang) * s.rad;
                    s.px = nx; s.py = ny;
                    // trail = the last ~126° of arc (angle-based, not frame-based,
                    // so it stays a long brush stroke at any speed)
                    s.hist.push(nx, ny, s.traveled);
                    while (s.hist.length > 6 && (s.traveled - s.hist[2]) > 2.2) s.hist.splice(0, 3);
                    if (s.hist.length > 600) s.hist.splice(0, s.hist.length - 600);

                    if (s.dying) {
                        // semicircle done: dim out WHILE still flowing, then respawn
                        s.fade -= dt / 1300;
                        if (s.fade <= 0) {
                            respawn(s);
                            s.dying = false;
                            s.fade = 0; // ramps back in below
                        }
                    } else {
                        if (s.traveled >= Math.PI) s.dying = true;
                        if (s.fade < 1) s.fade = Math.min(1, s.fade + dt / 900); // newborn ramp-in
                    }

                    var tw = (0.6 + 0.4 * Math.sin(now * s.twF + s.tw)) * Math.max(0, s.fade);
                    var rgb = s.col[0] + ',' + s.col[1] + ',' + s.col[2];
                    var n = s.hist.length / 3;
                    for (var i = 1; i < n; i++) {
                        var f = i / n; // 0 at tail -> 1 at head
                        ctx.beginPath();
                        ctx.moveTo(s.hist[(i - 1) * 3], s.hist[(i - 1) * 3 + 1]);
                        ctx.lineTo(s.hist[i * 3], s.hist[i * 3 + 1]);
                        ctx.strokeStyle = 'rgba(' + rgb + ',' + (f * f * tw * 0.8).toFixed(3) + ')';
                        ctx.lineWidth = s.size * (0.35 + 0.65 * f);
                        ctx.stroke();
                    }
                    // bright head
                    if (tw > 0.01) {
                        ctx.beginPath();
                        ctx.arc(s.px, s.py, s.size * 0.9, 0, Math.PI * 2);
                        ctx.fillStyle = 'rgba(' + rgb + ',' + (tw * 0.95).toFixed(3) + ')';
                        ctx.fill();
                    }
                });
            }
            sess.raf = requestAnimationFrame(frame);
        };
        sess.raf = requestAnimationFrame(frame);

        clearTimeout(starryTimer);
        starryTimer = setTimeout(stopStarry, 50000);
    };

    var starryNight = function(auto) {
        if (!sky || reduceMotion) return;
        if (document.documentElement.dataset.theme !== 'dark') {
            showToast(isZh ? '🎨 星月夜只在黑夜出现' : '🎨 The Starry Night only shows at night');
            return;
        }
        if (starry) return; // already showing
        startStarry();
        showToast(auto ? (isZh ? '🎨 今晚的夜空是梵高画的（稀有彩蛋）' : '🎨 Van Gogh painted tonight\'s sky (rare!)')
                       : (isZh ? '🎨 星月夜' : '🎨 The Starry Night'));
    };

    // typed words: "starry" / "scorpio" (skipped while typing in inputs)
    var typeBuf = '';
    document.addEventListener('keydown', function(e) {
        if (e.key.length !== 1 || !/[a-z]/i.test(e.key)) return;
        var ae = document.activeElement;
        if (ae && /^(INPUT|TEXTAREA)$/.test(ae.tagName)) return;
        typeBuf = (typeBuf + e.key.toLowerCase()).slice(-8);
        if (typeBuf.endsWith('starry')) {
            typeBuf = '';
            starryNight(false);
        } else if (typeBuf.endsWith('scorpio')) {
            typeBuf = '';
            var c = document.querySelector('.constellation');
            if (c && !reduceMotion) {
                var cl = c.cloneNode(true); // re-insert to replay the draw-in animation
                cl.classList.add('con-show'); // hidden by default — summon it
                c.parentNode.replaceChild(cl, c);
            } else if (c) {
                c.classList.add('con-show');
            }
            showToast(isZh ? '♏ 天蝎座重新点亮' : '♏ Scorpius relit');
        } else if (typeBuf.endsWith('rainbow')) {
            typeBuf = '';
            showRainbow(false);
        }
    });

    // rare: ~4% of dark-mode visits get Van Gogh for free
    if (document.documentElement.dataset.theme === 'dark' && Math.random() < 0.04) {
        setTimeout(function() { starryNight(true); }, 2500);
    }

    // double rainbow — light-theme rare egg (~3% of day visits) / typed "rainbow"
    var rainbowTimer = null;
    var showRainbow = function(auto) {
        if (!sky) return;
        if (document.documentElement.dataset.theme !== 'light') {
            showToast(isZh ? '🌈 彩虹只在白天出现' : '🌈 Rainbows only show by day');
            return;
        }
        sky.classList.add('rainbow-on');
        clearTimeout(rainbowTimer);
        rainbowTimer = setTimeout(function() { sky.classList.remove('rainbow-on'); }, 15000);
        showToast(auto ? (isZh ? '🌈 双彩虹！（稀有彩蛋）' : '🌈 Double rainbow! (rare!)')
                       : (isZh ? '🌈 双彩虹' : '🌈 Double rainbow'));
    };
    if (document.documentElement.dataset.theme === 'light' && Math.random() < 0.03) {
        setTimeout(function() { showRainbow(true); }, 4000);
    }

    // logo ×5 clicks within 3s: disco mode
    var logoEl = document.querySelector('.logo');
    var logoClicks = [];
    if (logoEl) {
        logoEl.addEventListener('click', function() {
            var now = Date.now();
            logoClicks = logoClicks.filter(function(t) { return now - t < 3000; });
            logoClicks.push(now);
            if (logoClicks.length >= 5) {
                logoClicks = [];
                document.body.classList.add('disco');
                setTimeout(function() { document.body.classList.remove('disco'); }, 10000);
                showToast(isZh ? '🪩 迪斯科时间！' : '🪩 Disco time!');
            }
        });
    }

    // late-night visitor (00:00–05:00), once per session
    var hourNow = today.getHours();
    if (hourNow >= 0 && hourNow < 5 && !sessionStorage.getItem('night-owl-toasted')) {
        sessionStorage.setItem('night-owl-toasted', '1');
        setTimeout(function() {
            showToast(isZh ? '🌙 这么晚还没睡？早点休息' : '🌙 Up late? Get some rest');
        }, 4000);
    }

    // copy toast
    document.addEventListener('copy', function() {
        showToast(isZh ? '📋 已复制' : '📋 Copied', 1500);
    });

