const test = require('node:test');
const assert = require('node:assert/strict');
const Joy = require('../assets/joy.js');
const { initHome } = require('../assets/home.js');

// Minimal fake DOM: just enough for initHome.
function makeEl(id) {
  const listeners = {};
  const el = {
    id,
    textContent: '',
    hidden: false,
    children: [],
    classList: { _s: new Set(), add(c) { this._s.add(c); }, remove(c) { this._s.delete(c); }, contains(c) { return this._s.has(c); } },
    attrs: {},
    addEventListener(type, fn) { (listeners[type] = listeners[type] || []).push(fn); },
    fire(type) { (listeners[type] || []).forEach((fn) => fn({ type })); },
    appendChild(child) { child.parent = el; el.children.push(child); return child; },
    removeChild(child) { el.children = el.children.filter((c) => c !== child); },
    removeAttribute(name) { if (name === 'hidden') el.hidden = false; delete el.attrs[name]; },
    setAttribute(name, v) { el.attrs[name] = v; },
    remove() { if (el.parent) el.parent.removeChild(el); },
  };
  return el;
}

function makeDoc(ids, { reduceMotion = false } = {}) {
  const els = {};
  ids.forEach((id) => { els[id] = makeEl(id); });
  els['sj-surprise'] && (els['sj-surprise'].hidden = true);
  return {
    els,
    getElementById: (id) => els[id] || null,
    createElement: () => makeEl(''),
    defaultView: { matchMedia: () => ({ matches: reduceMotion }) },
  };
}

const ALL = ['sj-heart', 'sj-rings', 'sj-count', 'sj-surprise', 'sj-idea'];

test('tapping the heart adds one ring and bumps the counter to 1,285', () => {
  const doc = makeDoc(ALL);
  doc.els['sj-count'].textContent = '1,284';
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

test('surprise-me is revealed and shows a different idea every click', () => {
  const doc = makeDoc(ALL);
  initHome(doc, Joy);
  assert.equal(doc.els['sj-surprise'].hidden, false);
  let prev = '';
  for (let i = 0; i < 20; i++) {
    doc.els['sj-surprise'].fire('click');
    const idea = doc.els['sj-idea'].textContent;
    assert.ok(Joy.IDEAS.includes(idea));
    assert.notEqual(idea, prev);
    prev = idea;
  }
});

test('initHome does nothing and does not throw when expected elements are missing', () => {
  assert.doesNotThrow(() => initHome(makeDoc([]), Joy));
  assert.doesNotThrow(() => initHome(makeDoc(['sj-heart']), Joy));
  assert.doesNotThrow(() => initHome(makeDoc(['sj-surprise']), Joy));
});

test('on load the counter shows the constant, whatever the markup said', () => {
  const doc = makeDoc(ALL);
  doc.els['sj-count'].textContent = '999';
  initHome(doc, Joy);
  assert.equal(doc.els['sj-count'].textContent, Joy.formatCount(Joy.PLACEHOLDER_START_COUNT));
});

test('the idea line is revealed along with the surprise button', () => {
  const doc = makeDoc(ALL);
  doc.els['sj-idea'].hidden = true;
  initHome(doc, Joy);
  assert.equal(doc.els['sj-idea'].hidden, false);
});
