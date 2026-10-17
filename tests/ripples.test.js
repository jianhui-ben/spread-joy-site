const test = require('node:test');
const assert = require('node:assert/strict');
const Ripples = require('../assets/ripples.js');
const { makeDoc } = require('./helpers/fakedom.js');

const { initRipples } = Ripples;
const START = Ripples.PLACEHOLDER_START_COUNT;
const ALL = ['sj-heart', 'sj-rings', 'sj-count'];
const FX = ALL.concat(['sj-fx']);

function fakeStorage(initial = {}) {
  const d = { ...initial };
  return { d, getItem: (k) => (k in d ? d[k] : null), setItem: (k, v) => { d[k] = String(v); } };
}

// --- the counter itself ---
test('formatCount adds thousands separators', () => {
  assert.equal(Ripples.formatCount(1284), '1,284');
  assert.equal(Ripples.formatCount(0), '0');
  assert.equal(Ripples.formatCount(1234567), '1,234,567');
});

test('placeholder start count is 1284', () => {
  assert.equal(START, 1284);
});

test('createCounter starts at the given value and each tap adds one', () => {
  const c = Ripples.createCounter(1284);
  assert.equal(c.value(), 1284);
  assert.equal(c.tap(), 1285);
  assert.equal(c.tap(), 1286);
  assert.equal(c.value(), 1286);
});

test('a counter with storage keeps a visitor\'s own taps between visits', () => {
  const s = fakeStorage();
  const first = Ripples.createCounter(1284, s);
  first.tap(); first.tap();
  const later = Ripples.createCounter(1284, s);
  assert.equal(later.value(), 1286);
  assert.equal(later.tap(), 1287);
});

test('counter ignores junk in storage and survives storage that throws', () => {
  assert.equal(Ripples.createCounter(100, fakeStorage({ 'sj-ripples': 'banana' })).value(), 100);
  assert.equal(Ripples.createCounter(100, fakeStorage({ 'sj-ripples': '-5' })).value(), 100);
  const broken = { getItem() { throw new Error('blocked'); }, setItem() { throw new Error('blocked'); } };
  const c = Ripples.createCounter(100, broken);
  assert.equal(c.value(), 100);
  assert.equal(c.tap(), 101);
});

// --- the heart ---
test('tapping the heart adds one ring and bumps the counter to 1,285', () => {
  const doc = makeDoc(ALL);
  initRipples(doc);
  doc.els['sj-heart'].fire('click');
  assert.equal(doc.els['sj-rings'].children.length, 1);
  assert.equal(doc.els['sj-count'].textContent, '1,285');
});

test('twenty rapid taps leave at most six rings and a correct count', () => {
  const doc = makeDoc(ALL);
  initRipples(doc);
  for (let i = 0; i < 20; i++) doc.els['sj-heart'].fire('click');
  assert.ok(doc.els['sj-rings'].children.length <= 6);
  assert.equal(doc.els['sj-count'].textContent, Ripples.formatCount(START + 20));
});

test('a ring removes itself when its animation ends', () => {
  const doc = makeDoc(ALL);
  initRipples(doc);
  doc.els['sj-heart'].fire('click');
  doc.els['sj-rings'].children[0].fire('animationend');
  assert.equal(doc.els['sj-rings'].children.length, 0);
});

test('with reduced motion no ring is created but the counter still counts', () => {
  const doc = makeDoc(ALL, { reduceMotion: true });
  initRipples(doc);
  doc.els['sj-heart'].fire('click');
  assert.equal(doc.els['sj-rings'].children.length, 0);
  assert.equal(doc.els['sj-count'].textContent, Ripples.formatCount(START + 1));
});

test('on load the counter shows the constant, whatever the markup said', () => {
  const doc = makeDoc(ALL);
  doc.els['sj-count'].textContent = '999';
  initRipples(doc);
  assert.equal(doc.els['sj-count'].textContent, Ripples.formatCount(START));
});

test('taps still work after the editor re-draws the heart block', () => {
  const doc = makeDoc(ALL);
  initRipples(doc);
  doc.rerender();
  doc.els['sj-heart'].fire('click');
  assert.equal(doc.els['sj-rings'].children.length, 1);
  assert.equal(doc.els['sj-count'].textContent, Ripples.formatCount(START + 1));
});

test('running the script a second time (block re-drawn) does not double count', () => {
  const doc = makeDoc(ALL);
  initRipples(doc);
  doc.rerender();
  initRipples(doc);
  doc.els['sj-heart'].fire('click');
  assert.equal(doc.els['sj-count'].textContent, Ripples.formatCount(START + 1));
});

test('a click on something inside the heart button counts as a tap', () => {
  const doc = makeDoc(ALL);
  initRipples(doc);
  const img = doc.createElement();
  img.parentNode = doc.els['sj-heart'];
  doc.dispatch('click', img);
  assert.equal(doc.els['sj-count'].textContent, Ripples.formatCount(START + 1));
});

test('the heart tap is claimed so no other script on the page counts it again', () => {
  const doc = makeDoc(ALL);
  initRipples(doc);
  let stopped = false;
  doc.dispatch('click', doc.els['sj-heart'], { stopPropagation() { stopped = true; } });
  assert.ok(stopped);
});

test('does nothing and does not throw when expected elements are missing', () => {
  assert.doesNotThrow(() => initRipples(makeDoc([])));
  assert.doesNotThrow(() => {
    const doc = makeDoc(['sj-heart']);
    initRipples(doc);
    doc.els['sj-heart'].fire('click');
  });
});

test('the counter remembers this visitor\'s taps after a reload', () => {
  const storage = fakeStorage();
  const doc = makeDoc(ALL);
  initRipples(doc, storage);
  doc.els['sj-heart'].fire('click');
  doc.els['sj-heart'].fire('click');
  const again = makeDoc(ALL);
  initRipples(again, storage);
  assert.equal(again.els['sj-count'].textContent, Ripples.formatCount(START + 2));
});

// --- floating hearts and confetti (live in an optional #sj-fx container over the photo) ---
// A browser's element.children is an HTMLCollection: indexable and iterable, but with no .filter/.map/.shift
function asHtmlCollection(el) {
  let list = [];
  Object.defineProperty(el, 'children', {
    get() { const c = list.slice(); c.filter = undefined; c.map = undefined; c.forEach = undefined; return c; },
    set(v) { list = v; },
  });
  el.children = [];
  el.appendChild = (child) => { child.parentNode = el; list.push(child); return child; };
  el.removeChild = (child) => { list = list.filter((c) => c !== child); };
}

const kinds = (el, cls) => el.children.filter((c) => c.classList.contains(cls));

test('each tap floats one heart up from the button, and it removes itself when it finishes', () => {
  const doc = makeDoc(FX);
  initRipples(doc);
  doc.els['sj-heart'].fire('click');
  const floats = kinds(doc.els['sj-fx'], 'float');
  assert.equal(floats.length, 1);
  floats[0].fire('animationend');
  assert.equal(kinds(doc.els['sj-fx'], 'float').length, 0);
});

test('rapid taps never leave more than twelve floating hearts', () => {
  const doc = makeDoc(FX);
  initRipples(doc);
  for (let i = 0; i < 9; i++) doc.els['sj-heart'].fire('click');
  assert.ok(kinds(doc.els['sj-fx'], 'float').length <= 12);
});

test('confetti bursts only on every tenth tap', () => {
  const doc = makeDoc(FX);
  initRipples(doc);
  for (let i = 0; i < 9; i++) doc.els['sj-heart'].fire('click');
  assert.equal(kinds(doc.els['sj-fx'], 'bit').length, 0, 'none before the tenth tap');
  doc.els['sj-heart'].fire('click');
  assert.ok(kinds(doc.els['sj-fx'], 'bit').length >= 10, 'burst on the tenth tap');
});

test('with reduced motion there are no floating hearts or confetti', () => {
  const doc = makeDoc(FX, { reduceMotion: true });
  initRipples(doc);
  for (let i = 0; i < 10; i++) doc.els['sj-heart'].fire('click');
  assert.equal(doc.els['sj-fx'].children.length, 0);
});

test('taps work when the page has no #sj-fx container', () => {
  const doc = makeDoc(ALL);
  initRipples(doc);
  assert.doesNotThrow(() => doc.els['sj-heart'].fire('click'));
});

test('works when children is a browser HTMLCollection (no array methods): hearts, confetti and rings all still appear', () => {
  const doc = makeDoc(FX);
  asHtmlCollection(doc.els['sj-fx']);
  asHtmlCollection(doc.els['sj-rings']);
  initRipples(doc);
  for (let i = 0; i < 10; i++) assert.doesNotThrow(() => doc.els['sj-heart'].fire('click'));
  const all = Array.prototype.slice.call(doc.els['sj-fx'].children);
  assert.ok(all.some((c) => c.classList.contains('bit')), 'confetti on the tenth tap');
  assert.ok(Array.prototype.slice.call(doc.els['sj-rings'].children).length >= 1, 'ring still added');
});
