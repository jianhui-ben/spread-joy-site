(function (root) {
  // Page-open effect on the landing page: a yellow heart-shaped cover shrinks away to reveal the page,
  // and a heart stays behind the headline. Added by a teammate on the Squarespace master. Its styles are
  // the style block at the top of this Code Block; like the heart counter, the block carries it on its own.
  var DURATION = 750;
  var DURATION_REDUCED = 150;

  // The landing page is "/" or "/home" on Squarespace, and "/index.html" in the local preview.
  function isHomePath(path) {
    var p = path.replace(/\/$/, '');
    return p === '' || p === '/home' || p === '/index.html';
  }

  function initHeartTransition(doc, win) {
    if (win.self !== win.top) return; // not inside the editor's preview frame

    var container = doc.querySelector('.sj-home');
    if (!container || container.querySelector('#heart-transition')) return;
    if (!isHomePath(win.location.pathname)) return;

    var duration = win.matchMedia('(prefers-reduced-motion: reduce)').matches ? DURATION_REDUCED : DURATION;

    var heart = doc.createElement('div');
    heart.id = 'heart-transition';
    heart.setAttribute('aria-hidden', 'true');
    container.insertBefore(heart, container.firstChild);

    // The staying heart sits in the middle of the headline and is as tall as the room between the top of
    // the section and the photo, so it never reaches down onto the photo. Measured, because the headline's
    // size depends on the screen; measured again when the window changes or the page has finished loading.
    function placeHeart() {
      var h1 = container.querySelector('.hero h1');
      if (!h1) return;
      var sub = container.querySelector('.hero .sub') || h1;
      var card = container.querySelector('.hero-card');
      var top = container.getBoundingClientRect().top;
      var from = h1.getBoundingClientRect().top - top;
      var to = sub.getBoundingClientRect().bottom - top;
      var middle = (from + to) / 2;
      var below = card ? card.getBoundingClientRect().top - top - middle : middle;
      var half = Math.max(0, Math.min(middle, below));
      heart.style.setProperty('--heart-y', Math.round(middle) + 'px');
      heart.style.setProperty('--heart-size', Math.round(half * 2) + 'px');
    }
    placeHeart();
    win.addEventListener('resize', placeHeart);
    win.addEventListener('load', placeHeart);

    // start fully covered with no animation, then let it shrink on the next painted frame
    heart.style.setProperty('--heart-duration', '0ms');
    heart.classList.add('visible', 'cover');
    win.requestAnimationFrame(function () {
      win.requestAnimationFrame(function () {
        heart.style.setProperty('--heart-duration', duration + 'ms');
        heart.classList.remove('cover');
        heart.classList.add('persistent');
      });
    });
  }

  var api = { initHeartTransition: initHeartTransition, isHomePath: isHomePath };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;

  if (typeof document !== 'undefined' && typeof window !== 'undefined') {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', function () { initHeartTransition(document, window); }, { once: true });
    } else {
      initHeartTransition(document, window);
    }
  }
})(typeof window !== 'undefined' ? window : globalThis);
