// Minimal fake DOM: elements bubble clicks up to the document, like a browser.
function makeDoc(ids, { reduceMotion = false } = {}) {
  const docListeners = {};
  const root = { classList: { _s: new Set(), add(c) { this._s.add(c); }, remove(c) { this._s.delete(c); }, contains(c) { return this._s.has(c); } } };
  const doc = {
    els: {},
    documentElement: root,
    addEventListener(type, fn) { (docListeners[type] = docListeners[type] || []).push(fn); },
    dispatch(type, target, extra) { (docListeners[type] || []).forEach((fn) => fn(Object.assign({ type, target }, extra))); },
    getElementById(id) { return doc.els[id] || null; },
    createElement() { return makeEl('', doc); },
    defaultView: { matchMedia: () => ({ matches: reduceMotion }) },
    build() { ids.forEach((id) => { doc.els[id] = makeEl(id, doc, docListeners); }); },
    // Squarespace re-draws a block's HTML: same ids, brand new elements, no listeners.
    rerender() { ids.forEach((id) => { doc.els[id] = makeEl(id, doc, docListeners); }); },
  };
  doc.build();
  return doc;
}

function makeEl(id, doc, docListeners) {
  const listeners = {};
  const el = {
    id,
    textContent: '',
    style: { setProperty(k, v) { this[k] = v; } },
    children: [],
    classList: { _s: new Set(), add(c) { this._s.add(c); }, remove(c) { this._s.delete(c); }, contains(c) { return this._s.has(c); } },
    parentNode: null,
    addEventListener(type, fn) { (listeners[type] = listeners[type] || []).push(fn); },
    fire(type) {
      const event = { type, target: el };
      (listeners[type] || []).forEach((fn) => fn(event));
      if (docListeners) (docListeners[type] || []).forEach((fn) => fn(event));
    },
    appendChild(child) { child.parentNode = el; el.children.push(child); return child; },
    removeChild(child) { el.children = el.children.filter((c) => c !== child); },
    remove() { if (el.parentNode) el.parentNode.removeChild(el); },
  };
  return el;
}

module.exports = { makeDoc, makeEl };
