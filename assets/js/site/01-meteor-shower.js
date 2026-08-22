    /**
     * Meteor Shower (generated)
     * Dozens of meteors with randomized orbits; CSS keyframes do the falling.
     * Hidden by CSS in light mode.
     */
    var sky = document.querySelector('.sky');
    if (sky && !reduceMotion) {
        var isMobile = window.matchMedia('(max-width: 768px)').matches;
        var COUNT = isMobile ? 18 : 36;
        for (var i = 0; i < COUNT; i++) {
            var m = document.createElement('div');
            m.className = 'meteor';
            m.style.top = (Math.random() * 45 - 5) + '%';
            m.style.left = (25 + Math.random() * 85) + '%';
            m.style.width = (50 + Math.random() * 120) + 'px';
            var dur = 5 + Math.random() * 11;
            m.style.animationDuration = dur + 's';
            m.style.animationDelay = (Math.random() * dur * 2) + 's';
            sky.appendChild(m);
        }
    }

