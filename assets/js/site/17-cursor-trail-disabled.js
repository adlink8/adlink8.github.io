    /**
     * 14. Cursor Trail — DISABLED (too gamey for a portfolio default).
     * CSS section 34 is kept dormant; re-enable by uncommenting this block.
     */
    /*
    if (finePointer && !reduceMotion) {
        var lastTrail = 0;
        var liveDots = 0;
        document.addEventListener('mousemove', function(e) {
            var now = performance.now();
            if (now - lastTrail < 26 || liveDots > 48) return;
            lastTrail = now;
            liveDots++;
            var d = document.createElement('div');
            d.className = 'cursor-dot';
            var size = 7 + Math.random() * 9;
            d.style.width = size + 'px';
            d.style.height = size + 'px';
            d.style.left = (e.clientX + (Math.random() - 0.5) * 12) + 'px';
            d.style.top = (e.clientY + (Math.random() - 0.5) * 12) + 'px';
            document.body.appendChild(d);
            setTimeout(function() { d.remove(); liveDots--; }, 1200);
        }, { passive: true });
    }
    */

