// Dependency-free event/DOM contract test for both course components.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');

for (const file of ['assets/lesson.js',
  'machine-learning/deep-learning/language-modeling-from-scratch/assets/lesson.js']) {
  let click;
  vm.runInNewContext(fs.readFileSync(path.join(__dirname, '..', file), 'utf8'), {
    document: { addEventListener: (name, handler) => { assert.equal(name, 'click'); click = handler; } }
  });
  function quiz() {
    const feedback = { textContent: '' };
    const attrs = { 'data-answer': 'B', 'data-correct-feedback': 'Correct',
      'data-incorrect-feedback': 'Try again' };
    const q = { getAttribute: key => attrs[key], querySelector: () => feedback,
      querySelectorAll: () => choices };
    const choices = ['A', 'B', 'C'].map(value => {
      const classes = new Set();
      return { classes, disabled: false, closest: () => q,
        getAttribute: () => value,
        classList: { toggle: (key, enabled) => enabled ? classes.add(key) : classes.delete(key) } };
    });
    return { choices, feedback };
  }
  const one = quiz(), two = quiz();
  const choose = button => click({ target: { closest: () => button } });
  choose(one.choices[0]);
  assert.equal(one.feedback.textContent, 'Try again');
  assert(one.choices.every(c => !c.disabled && !c.classes.has('is-correct')));
  assert(one.choices[0].classes.has('is-incorrect'));
  choose(one.choices[0]); // repeated wrong click stays retryable
  choose(one.choices[2]);
  assert(!one.choices[0].classes.has('is-incorrect'));
  assert(one.choices[2].classes.has('is-incorrect'));
  assert.equal(two.feedback.textContent, '');
  assert(two.choices.every(c => !c.disabled));
  choose(one.choices[1]); // wrong -> correct
  assert.equal(one.feedback.textContent, 'Correct');
  assert(one.choices.every(c => c.disabled && !c.classes.has('is-incorrect')));
  assert(one.choices[1].classes.has('is-correct'));
  choose(one.choices[0]); // ignore even a synthetic click after completion
  assert.equal(one.feedback.textContent, 'Correct');
  choose(two.choices[1]); // another question remains independent
  assert.equal(two.feedback.textContent, 'Correct');
  click({ target: { closest: () => null } });
  console.log(`PASS ${file}: wrong/repeat/retry/correct/disabled/independent quiz flows`);
}
