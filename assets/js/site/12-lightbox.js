    /**
     * 9. Image Lightbox
     */
    var zoomables = document.querySelectorAll('.post-content img');
    if (zoomables.length) {
        var lb = document.createElement('div');
        lb.className = 'lightbox';
        lb.setAttribute('role', 'dialog');
        lb.setAttribute('aria-label', 'Image preview');
        lb.innerHTML = '<img alt=""><span class="lightbox-close" aria-hidden="true">×</span>';
        document.body.appendChild(lb);
        var lbImg = lb.querySelector('img');
        var closeLb = function() {
            lb.classList.remove('open');
            document.body.style.overflow = '';
        };
        zoomables.forEach(function(img) {
            img.classList.add('zoomable');
            img.addEventListener('click', function() {
                lbImg.src = img.currentSrc || img.src;
                lbImg.alt = img.alt || '';
                lb.classList.add('open');
                document.body.style.overflow = 'hidden';
            });
        });
        lb.addEventListener('click', closeLb);
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') closeLb();
        });
    }

