    /**
     * 0. Theme Toggle
     * The theme's own handler lives in its footer partial, which this file
     * overrides — so we re-implement it here (same localStorage keys).
     */
    var themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            var html = document.querySelector('html');
            if (html.dataset.theme === 'dark') {
                html.dataset.theme = 'light';
                localStorage.setItem('pref-theme', 'light');
            } else {
                html.dataset.theme = 'dark';
                localStorage.setItem('pref-theme', 'dark');
            }
        });
    }

