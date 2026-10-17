// Local preview only. Squarespace uses its own forms; this does not send or store anything.
(function () {
  document.addEventListener('submit', function (e) {
    var form = e.target;
    if (!form || !form.getAttribute || form.getAttribute('data-preview-form') === null) return;
    e.preventDefault();
    var note = form.querySelector('[data-preview-note]');
    if (!note) return;
    note.hidden = false;
    note.textContent = note.getAttribute('data-preview-note');
  });
})();
