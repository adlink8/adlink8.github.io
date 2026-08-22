    /**
     * 8. Stats Count-Up
     */
    var statNums = document.querySelectorAll('.stat-num');
    if (statNums.length && !reduceMotion && 'IntersectionObserver' in window) {
        var countUp = function(el) {
            var target = parseInt(el.textContent.replace(/\D/g, ''), 10) || 0;
            var duration = 900, t0 = null;
            var step = function(ts) {
                if (!t0) t0 = ts;
                var p = Math.min((ts - t0) / duration, 1);
                var eased = 1 - Math.pow(1 - p, 3);
                el.textContent = Math.round(target * eased);
                if (p < 1) requestAnimationFrame(step);
            };
            requestAnimationFrame(step);
        };
        var cObs = new IntersectionObserver(function(entries) {
            entries.forEach(function(en) {
                if (en.isIntersecting) { countUp(en.target); cObs.unobserve(en.target); }
            });
        }, { threshold: 0.5 });
        statNums.forEach(function(n) { cObs.observe(n); });
    }

