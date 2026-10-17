(function (root) {
  var MAX_RINGS = 6;
  var MAX_FLOATS = 12;
  var CONFETTI_EVERY = 10;
  var CONFETTI_BITS = 14;

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

    var taps = 0;

    // a heart that floats up from the button, and a burst of confetti on every tenth tap
    function playful(fx) {
      taps += 1;
      var heart = doc.createElement('span');
      heart.classList.add('float');
      heart.textContent = '\u2665';
      heart.style.setProperty('--x', Math.round((Math.random() - 0.5) * 120) + 'px');
      heart.addEventListener('animationend', function () { heart.remove(); });
      fx.appendChild(heart);
      // children is a live HTMLCollection in browsers (no filter/shift), so copy it into an array first
      var floats = Array.prototype.filter.call(fx.children, function (c) { return c.classList.contains('float'); });
      while (floats.length > MAX_FLOATS) fx.removeChild(floats.shift());

      if (taps % CONFETTI_EVERY === 0) {
        for (var i = 0; i < CONFETTI_BITS; i++) {
          var bit = doc.createElement('i');
          bit.classList.add('bit');
          var angle = (i / CONFETTI_BITS) * Math.PI * 2;
          var dist = 70 + Math.random() * 60;
          bit.style.setProperty('--dx', Math.round(Math.cos(angle) * dist) + 'px');
          bit.style.setProperty('--dy', Math.round(Math.sin(angle) * dist - 40) + 'px');
          bit.style.setProperty('--c', i % 3 === 0 ? '#fdcd17' : i % 3 === 1 ? '#ffffff' : '#231f20');
          bit.addEventListener('animationend', function (b) { return function () { b.remove(); }; }(bit));
          fx.appendChild(bit);
        }
      }
    }

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

      var fx = doc.getElementById('sj-fx');
      if (fx) playful(fx);
      number.classList.add('bump');
      setTimeout(function () { number.classList.remove('bump'); }, 250);

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
