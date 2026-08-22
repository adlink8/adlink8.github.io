    /**
     * 7. TOC Scroll-Spy
     * Highlights the current section in the table of contents
     */
    var tocLinks = document.querySelectorAll('.toc a[href^="#"]');
    if (tocLinks.length && 'IntersectionObserver' in window) {
        var linkFor = {};
        var heads = [];
        tocLinks.forEach(function(a) {
            var id = decodeURIComponent(a.getAttribute('href').slice(1));
            var h = document.getElementById(id);
            if (h) { linkFor[id] = a; heads.push(h); }
        });
        var spy = new IntersectionObserver(function(entries) {
            entries.forEach(function(en) {
                if (!en.isIntersecting) return;
                tocLinks.forEach(function(l) { l.classList.remove('active-toc'); });
                var a = linkFor[en.target.id];
                if (a) a.classList.add('active-toc');
            });
        }, { rootMargin: '-90px 0px -70% 0px' });
        heads.forEach(function(h) { spy.observe(h); });
    }

