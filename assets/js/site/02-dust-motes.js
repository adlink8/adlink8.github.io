    /**
     * Dust Motes (generated)
     * Daylight's counterpart to meteors: tiny glowing specks drifting
     * slowly upward. Hidden by CSS in dark mode.
     */
    if (sky && !reduceMotion) {
        var MOTES = isMobile ? 8 : 16;
        for (var mi = 0; mi < MOTES; mi++) {
            var mo = document.createElement('div');
            mo.className = 'mote';
            var msz = 2 + Math.random() * 4;
            mo.style.width = msz + 'px';
            mo.style.height = msz + 'px';
            mo.style.left = (15 + Math.random() * 80) + '%';
            mo.style.top = (25 + Math.random() * 70) + '%';
            mo.style.setProperty('--mo', (0.4 + Math.random() * 0.45).toFixed(2));
            var mdur = 16 + Math.random() * 20;
            mo.style.animationDuration = mdur + 's';
            mo.style.animationDelay = (Math.random() * mdur) + 's';
            sky.appendChild(mo);
        }
    }

