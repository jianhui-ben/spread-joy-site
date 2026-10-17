const test = require('node:test');
const assert = require('node:assert/strict');
const Joy = require('../assets/joy.js');

test('formatCount adds thousands separators', () => {
  assert.equal(Joy.formatCount(1284), '1,284');
  assert.equal(Joy.formatCount(0), '0');
  assert.equal(Joy.formatCount(1234567), '1,234,567');
});

test('placeholder start count is 1284', () => {
  assert.equal(Joy.PLACEHOLDER_START_COUNT, 1284);
});

test('createCounter starts at the given value and each tap adds one', () => {
  const c = Joy.createCounter(1284);
  assert.equal(c.value(), 1284);
  assert.equal(c.tap(), 1285);
  assert.equal(c.tap(), 1286);
  assert.equal(c.tap(), 1287);
  assert.equal(c.value(), 1287);
});

test('the brainstorm list is intact, including the glad-you-are-here idea', () => {
  assert.equal(Joy.IDEAS.length, 16);
  assert.ok(Joy.IDEAS.includes('Tell someone, "I\'m so glad you\'re here."'));
});

test('shuffler never repeats an idea back to back', () => {
  const s = Joy.createShuffler(Joy.IDEAS);
  let prev = null;
  for (let i = 0; i < Joy.IDEAS.length * 3; i++) {
    const next = s.next();
    assert.notEqual(next, prev);
    prev = next;
  }
});

test('shuffler visits every idea before any repeats', () => {
  const s = Joy.createShuffler(Joy.IDEAS);
  const seen = new Set();
  for (let i = 0; i < Joy.IDEAS.length; i++) seen.add(s.next());
  assert.equal(seen.size, Joy.IDEAS.length);
});

test('a one-item shuffler keeps returning that item', () => {
  const s = Joy.createShuffler(['only']);
  assert.equal(s.next(), 'only');
  assert.equal(s.next(), 'only');
});
