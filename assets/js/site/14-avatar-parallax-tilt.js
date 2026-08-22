    /**
     * 11. Avatar Parallax + Card Tilt (desktop pointers only)
     */
    var finePointer = window.matchMedia('(pointer: fine)').matches;
    if (finePointer && !reduceMotion) {
        var avatar = document.querySelector('.first-entry.home-info p:first-child img');
        var homeCard = document.querySelector('.first-entry.home-info');
        if (avatar && homeCard) {
            homeCard.addEventListener('mousemove', function(e) {
                var r = homeCard.getBoundingClientRect();
                var dx = (e.clientX - r.left - r.width / 2) / r.width;
                var dy = (e.clientY - r.top - r.height / 2) / r.height;
                avatar.style.transform = 'translate(' + (dx * 8) + 'px, ' + (dy * 8) + 'px) scale(1.03)';
            });
            homeCard.addEventListener('mouseleave', function() {
                avatar.style.transform = '';
            });
        }

        document.querySelectorAll('.post-entry, .featured-card, .project-card, .stat-card')
            .forEach(function(card) {
                card.addEventListener('mousemove', function(e) {
                    var r = card.getBoundingClientRect();
                    var rx = ((e.clientY - r.top) / r.height - 0.5) * -2.5;
                    var ry = ((e.clientX - r.left) / r.width - 0.5) * 2.5;
                    card.style.transform = 'perspective(900px) rotateX(' + rx + 'deg) rotateY(' + ry + 'deg) translateY(-4px)';
                });
                card.addEventListener('mouseleave', function() {
                    card.style.transform = '';
                });
            });
    }

