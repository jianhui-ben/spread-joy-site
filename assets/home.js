(function (root) {
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

    var shuffler = joy.createShuffler(joy.IDEAS);

    function clearDone() {
      var note = doc.getElementById('sj-done');
      if (!note) return;
      note.hidden = true;
      note.textContent = '';
    }

    function surprise() {
      var idea = doc.getElementById('sj-idea');
      if (idea) idea.textContent = shuffler.next();
      clearDone();
    }

    // "I did it!" from the brainstorm. Nothing is stored; the line only confirms this tap.
    function didIt() {
      var note = doc.getElementById('sj-done');
      if (!note) return;
      note.hidden = false;
      note.textContent = 'You just put more kindness into the world.';
    }

    doc.addEventListener('click', function (e) {
      if (closestWithId(e.target, 'sj-surprise')) surprise();
      else if (closestWithId(e.target, 'sj-did-it')) didIt();
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
