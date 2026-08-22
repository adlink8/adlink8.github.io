    /**
     * 1. Heart-Pop Interaction
     * Triggers a heart animation when clicking the profile avatar only
     */
    if (!reduceMotion) {
        document.addEventListener('click', function(e) {
            var avatar = e.target.closest('.home-info p:first-child img, .sidebar-avatar');
            if (!avatar) return;
            var heart = document.createElement('div');
            heart.textContent = '❤️';
            heart.className = 'heart-pop';
            heart.style.left = e.clientX + 'px';
            heart.style.top = e.clientY + 'px';
            document.body.appendChild(heart);
            setTimeout(function() { heart.remove(); }, 1000);
        });
    }

