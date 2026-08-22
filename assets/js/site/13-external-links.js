    /**
     * 10. External Link Markers (open in new tab, add ↗)
     */
    document.querySelectorAll('.post-content a[href^="http"]').forEach(function(a) {
        if (a.hostname === location.hostname) return;
        if (/(^|\.)(adlink8\.github\.io|shuoyan\.me)$/.test(a.hostname)) return;
        a.classList.add('ext-link');
        a.target = '_blank';
        a.rel = 'noopener noreferrer';
    });

