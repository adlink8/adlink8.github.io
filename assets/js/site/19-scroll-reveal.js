    /**
     * 5. Scroll-Reveal Animations
     * Fades/slides entries into view with a subtle stagger
     */
    var revealTargets = document.querySelectorAll(
        '.post-entry, .archive-entry, .terms-tags li, .first-entry.home-info'
    );
    if (reduceMotion || !('IntersectionObserver' in window)) {
        return;
    }
    var observer = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting) {
                var el = entry.target;
                el.classList.add('revealed');
                observer.unobserve(el);
                // Clear the entrance stagger so later hover transitions stay snappy
                setTimeout(function() { el.style.transitionDelay = '0ms'; }, 800);
            }
        });
    }, { threshold: 0.08, rootMargin: '0px 0px -40px 0px' });

    revealTargets.forEach(function(el, i) {
        el.classList.add('reveal');
        el.style.transitionDelay = Math.min(i * 70, 350) + 'ms';
        observer.observe(el);
    });
