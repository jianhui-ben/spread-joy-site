const test = require('node:test');
const assert = require('node:assert/strict');
const Joy = require('../assets/joy.js');
const { initHome } = require('../assets/home.js');

// Minimal fake DOM: elements bubble clicks up to the document, like a browser.
function makeDoc(ids, { reduceMotion = false } = {}) {
  const docListeners = {};
  const root = { classList: { _s: new Set(), add(c) { this._s.add(c); }, remove(c) { this._s.delete(c); }, contains(c) { return this._s.has(c); } } };
  const doc = {
    els: {},
    documentElement: root,
    addEventListener(type, fn) { (docListeners[type] = docListeners[type] || []).push(fn); },
    dispatch(type, target) { (docListeners[type] || []).forEach((fn) => fn({ type, target })); },
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

const ALL = ['sj-heart', 'sj-rings', 'sj-count', 'sj-surprise', 'sj-idea'];

test('tapping the heart adds one ring and bumps the counter to 1,285', () => {
  const doc = makeDoc(ALL);
  initHome(doc, Joy);
  doc.els['sj-heart'].fire('click');
  assert.equal(doc.els['sj-rings'].children.length, 1);
  assert.equal(doc.els['sj-count'].textContent, '1,285');
});

test('twenty rapid taps leave at most six rings and a correct count', () => {
  const doc = makeDoc(ALL);
  initHome(doc, Joy);
  for (let i = 0; i < 20; i++) doc.els['sj-heart'].fire('click');
  assert.ok(doc.els['sj-rings'].children.length <= 6);
  assert.equal(doc.els['sj-count'].textContent, Joy.formatCount(Joy.PLACEHOLDER_START_COUNT + 20));
});

test('a ring removes itself when its animation ends', () => {
  const doc = makeDoc(ALL);
  initHome(doc, Joy);
  doc.els['sj-heart'].fire('click');
  const ring = doc.els['sj-rings'].children[0];
  ring.fire('animationend');
  assert.equal(doc.els['sj-rings'].children.length, 0);
});

test('with reduced motion no ring is created but the counter still counts', () => {
  const doc = makeDoc(ALL, { reduceMotion: true });
  initHome(doc, Joy);
  doc.els['sj-heart'].fire('click');
  assert.equal(doc.els['sj-rings'].children.length, 0);
  assert.equal(doc.els['sj-count'].textContent, Joy.formatCount(Joy.PLACEHOLDER_START_COUNT + 1));
});

test('surprise-me shows a different idea every click', () => {
  const doc = makeDoc(ALL);
  initHome(doc, Joy);
  let prev = '';
  for (let i = 0; i < 20; i++) {
    doc.els['sj-surprise'].fire('click');
    const idea = doc.els['sj-idea'].textContent;
    assert.ok(Joy.IDEAS.includes(idea));
    assert.notEqual(idea, prev);
    prev = idea;
  }
});

test('the page is marked as script-enabled so surprise-me and its idea line appear', () => {
  const doc = makeDoc(ALL);
  initHome(doc, Joy);
  assert.ok(doc.documentElement.classList.contains('sj-js'));
});

test('on load the counter shows the constant, whatever the markup said', () => {
  const doc = makeDoc(ALL);
  doc.els['sj-count'].textContent = '999';
  initHome(doc, Joy);
  assert.equal(doc.els['sj-count'].textContent, Joy.formatCount(Joy.PLACEHOLDER_START_COUNT));
});

test('taps still work after the editor re-draws the heart block', () => {
  const doc = makeDoc(ALL);
  initHome(doc, Joy);
  doc.rerender();
  doc.els['sj-heart'].fire('click');
  assert.equal(doc.els['sj-rings'].children.length, 1);
  assert.equal(doc.els['sj-count'].textContent, Joy.formatCount(Joy.PLACEHOLDER_START_COUNT + 1));
});

test('surprise-me still works after the editor re-draws its block', () => {
  const doc = makeDoc(ALL);
  initHome(doc, Joy);
  doc.rerender();
  doc.els['sj-surprise'].fire('click');
  assert.ok(Joy.IDEAS.includes(doc.els['sj-idea'].textContent));
});

test('a click on something inside the heart button counts as a tap', () => {
  const doc = makeDoc(ALL);
  initHome(doc, Joy);
  const img = doc.createElement();
  img.parentNode = doc.els['sj-heart'];
  doc.dispatch('click', img);
  assert.equal(doc.els['sj-count'].textContent, Joy.formatCount(Joy.PLACEHOLDER_START_COUNT + 1));
});

test('initHome does nothing and does not throw when expected elements are missing', () => {
  assert.doesNotThrow(() => initHome(makeDoc([]), Joy));
  assert.doesNotThrow(() => {
    const doc = makeDoc(['sj-heart']);
    initHome(doc, Joy);
    doc.els['sj-heart'].fire('click');
  });
  assert.doesNotThrow(() => {
    const doc = makeDoc(['sj-surprise']);
    initHome(doc, Joy);
    doc.els['sj-surprise'].fire('click');
  });
});
