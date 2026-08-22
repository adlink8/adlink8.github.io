    /**
     * 4. Reading Progress Bar (rAF-throttled)
     */
    var progBar = document.getElementById('scroll-progress');
    if (progBar) {
        var ticking = false;
        var updateProgress = function() {
            var winScroll = document.documentElement.scrollTop || document.body.scrollTop;
            var height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
            var scrolled = height > 0 ? (winScroll / height) * 100 : 0;
            progBar.style.width = scrolled + '%';
            ticking = false;
        };
        window.addEventListener('scroll', function() {
            if (!ticking) {
                window.requestAnimationFrame(updateProgress);
                ticking = true;
            }
        }, { passive: true });
        updateProgress();
    }

