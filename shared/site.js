/* Plots – Shared Site JavaScript */

(function() {
    'use strict';

    // Inject navigation bar if not already present
    function injectNavBar() {
        if (document.querySelector('.nav-bar')) return;

        const isSubpage = window.location.pathname.includes('/plots/') &&
                          !window.location.pathname.endsWith('/plots/') &&
                          !window.location.pathname.endsWith('/plots/index.html');

        if (!isSubpage) return;

        const nav = document.createElement('div');
        nav.className = 'nav-bar';
        nav.innerHTML = '<a href="../">&larr; Back to Plots</a>';

        document.body.insertBefore(nav, document.body.firstChild);
    }

    // Initialize on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', injectNavBar);
    } else {
        injectNavBar();
    }
})();
