(function (root) {
  var MAX_RINGS = 6;

  function reducedMotion(doc) {
    var view = doc.defaultView;
    return !!(view && view.matchMedia && view.matchMedia('(prefers-reduced-motion: reduce)').matches);
  }

  function closestWithId(node, id) {
    while (node) {
      if (node.id === id) return node;
      node = node.parentNode;
    }
    return null;
  }

  // Clicks are handled on the whole document, and elements are looked up at click time,
  // because Squarespace's editor can re-draw a Code Block's HTML after this script has run.
  function initHome(doc, joy) {
    var html = doc.documentElement;
    if (html && html.classList.contains('sj-js')) return; // already running
    if (html) html.classList.add('sj-js'); // reveals the elements marked sj-needs-js

    var counter = joy.createCounter(joy.PLACEHOLDER_START_COUNT);
    var shuffler = joy.createShuffler(joy.IDEAS);
    var calm = reducedMotion(doc);

    var count = doc.getElementById('sj-count');
    if (count) count.textContent = joy.formatCount(counter.value());

    function tap() {
      var heart = doc.getElementById('sj-heart');
      var rings = doc.getElementById('sj-rings');
      var number = doc.getElementById('sj-count');
      if (!heart || !rings || !number) return;

      number.textContent = joy.formatCount(counter.tap());

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
    }

    function surprise() {
      var idea = doc.getElementById('sj-idea');
      if (idea) idea.textContent = shuffler.next();
    }

    doc.addEventListener('click', function (e) {
      if (closestWithId(e.target, 'sj-heart')) tap();
      else if (closestWithId(e.target, 'sj-surprise')) surprise();
    });
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
