    /**
     * 15. Heatmap Day Tooltip — instant hover readout of one day's activity.
     * Delegated so it covers home + /stats/ grids without per-page wiring.
     */
    var aiTip = null;
    function aiTipHide() { if (aiTip) aiTip.classList.remove('on'); }
    function aiTipPlace(e) {
        var x = Math.min(e.clientX + 12, window.innerWidth - aiTip.offsetWidth - 8);
        var y = e.clientY - aiTip.offsetHeight - 10;
        if (y < 8) y = e.clientY + 18;
        aiTip.style.left = x + 'px';
        aiTip.style.top = y + 'px';
    }
    document.addEventListener('mouseover', function(e) {
        var cell = e.target.closest ? e.target.closest('.heatmap-cell[data-date]') : null;
        if (!cell) { aiTipHide(); return; }
        if (!aiTip) {
            aiTip = document.createElement('div');
            aiTip.className = 'ai-day-tip';
            aiTip.setAttribute('aria-hidden', 'true');
            document.body.appendChild(aiTip);
        }
        aiTip.textContent = isZh
            ? cell.dataset.date + ' · ' + (cell.dataset.messages || 0) + ' 条消息 · ' + (cell.dataset.sessions || 0) + ' 场会话'
            : cell.dataset.date + ' · ' + (cell.dataset.messages || 0) + ' messages · '
                + (cell.dataset.sessions || 0) + ' session' + (cell.dataset.sessions === '1' ? '' : 's');
        aiTip.classList.add('on');
        aiTipPlace(e);
    }, { passive: true });
    document.addEventListener('mouseout', function(e) {
        if (e.target.closest && e.target.closest('.heatmap-cell[data-date]')) aiTipHide();
    }, { passive: true });

