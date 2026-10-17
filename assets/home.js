(function (root) {
  var MAX_RINGS = 6;

  function reducedMotion(doc) {
    var view = doc.defaultView;
    return !!(view && view.matchMedia && view.matchMedia('(prefers-reduced-motion: reduce)').matches);
  }

  function initRipple(doc, joy) {
    var heart = doc.getElementById('sj-heart');
    var rings = doc.getElementById('sj-rings');
    var count = doc.getElementById('sj-count');
    if (!heart || !rings || !count) return;

    var counter = joy.createCounter(joy.PLACEHOLDER_START_COUNT);
    var calm = reducedMotion(doc);

    heart.addEventListener('click', function () {
      count.textContent = joy.formatCount(counter.tap());

      if (calm) {
        heart.classList.add('pulse');
        setTimeout(function () { heart.classList.remove('pulse'); }, 300);
        return;
      }

      var ring = doc.createElement('span');
      ring.classList.add('ring');
      ring.addEventListener('animationend', function () { ring.remove(); });
      rings.appendChild(ring);
      while (rings.children.length > MAX_RINGS) rings.removeChild(rings.children[0]);
    });
  }

  function initSurprise(doc, joy) {
    var button = doc.getElementById('sj-surprise');
    var idea = doc.getElementById('sj-idea');
    if (!button || !idea) return;

    var shuffler = joy.createShuffler(joy.IDEAS);
    button.removeAttribute('hidden');
    button.addEventListener('click', function () {
      idea.textContent = shuffler.next();
    });
  }

  function initHome(doc, joy) {
    initRipple(doc, joy);
    initSurprise(doc, joy);
  }

  if (typeof module !== 'undefined' && module.exports) module.exports = { initHome: initHome };

  if (typeof document !== 'undefined' && root.Joy) {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', function () { initHome(document, root.Joy); });
    } else {
      initHome(document, root.Joy);
    }
  }
})(typeof window !== 'undefined' ? window : globalThis);
