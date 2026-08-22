    /**
     * 6. Code Block Language Labels
     * Replaces the decorative "zsh — 80x24" tag with the real language name
     */
    document.querySelectorAll('.post-content pre').forEach(function(pre) {
        if (pre.closest('.linenodiv')) return; // skip line-number gutter
        var host = pre.closest('.highlight') || pre;
        if (host.querySelector('.code-lang')) return; // one label per block
        var code = pre.querySelector('code');
        if (!code) return;
        var lang = code.getAttribute('data-lang')
            || (code.className.match(/language-(\w+)/) || [])[1]
            || 'text';
        host.classList.add('has-lang');
        var tag = document.createElement('span');
        tag.className = 'code-lang';
        tag.textContent = lang;
        host.appendChild(tag);
    });

