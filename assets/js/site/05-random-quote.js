    /**
     * 2. Random Quote Generator
     * Injects a random technical quote into the footer
     */
    var quotes = [
        '“Slow is smooth, smooth is fast.”'
    ];
    var quoteEl = document.getElementById('quote-container');
    if (quoteEl) {
        quoteEl.textContent = quotes[Math.floor(Math.random() * quotes.length)];
    }

