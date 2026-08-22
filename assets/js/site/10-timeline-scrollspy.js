    /**
     * 7b. Timeline Axis Scroll-Spy (/daily/)
     */
    var axisLinks = document.querySelectorAll('.ta-day[href^="#post-"]');
    if (axisLinks.length && 'IntersectionObserver' in window) {
        var axisFor = {};
        var cards = [];
        axisLinks.forEach(function(a) {
            var id = decodeURIComponent(a.getAttribute('href').slice(1));
            var el = document.getElementById(id);
            if (el) { axisFor[id] = a; cards.push(el); }
        });
        var axisSpy = new IntersectionObserver(function(entries) {
            entries.forEach(function(en) {
                if (!en.isIntersecting) return;
                axisLinks.forEach(function(l) { l.classList.remove('active'); });
                var a = axisFor[en.target.id];
                if (a) a.classList.add('active');
            });
        }, { rootMargin: '-100px 0px -60% 0px' });
        cards.forEach(function(c) { axisSpy.observe(c); });
    }

