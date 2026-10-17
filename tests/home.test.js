const test = require('node:test');
const assert = require('node:assert/strict');
const Joy = require('../assets/joy.js');
const { initHome } = require('../assets/home.js');
const { makeDoc } = require('./helpers/fakedom.js');

const ALL = ['sj-surprise', 'sj-idea'];

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

test('I did it confirms the tap and the next idea clears that line', () => {
  const doc = makeDoc(ALL.concat(['sj-did-it', 'sj-done']));
  initHome(doc, Joy);
  doc.els['sj-did-it'].fire('click');
  assert.equal(doc.els['sj-done'].hidden, false);
  assert.match(doc.els['sj-done'].textContent, /kindness into the world/);
  doc.els['sj-surprise'].fire('click');
  assert.equal(doc.els['sj-done'].hidden, true);
  assert.equal(doc.els['sj-done'].textContent, '');
});

test('surprise-me still works after the editor re-draws its block', () => {
  const doc = makeDoc(ALL);
  initHome(doc, Joy);
  doc.rerender();
  doc.els['sj-surprise'].fire('click');
  assert.ok(Joy.IDEAS.includes(doc.els['sj-idea'].textContent));
});

test('initHome does nothing and does not throw when expected elements are missing', () => {
  assert.doesNotThrow(() => initHome(makeDoc([]), Joy));
  assert.doesNotThrow(() => {
    const doc = makeDoc(['sj-surprise']);
    initHome(doc, Joy);
    doc.els['sj-surprise'].fire('click');
  });
});

test('the heart and its counter are not home.js business any more (ripples.js owns them)', () => {
  const doc = makeDoc(['sj-heart', 'sj-count']);
  doc.els['sj-count'].textContent = '1,284';
  initHome(doc, Joy);
  doc.els['sj-heart'].fire('click');
  assert.equal(doc.els['sj-count'].textContent, '1,284');
});
