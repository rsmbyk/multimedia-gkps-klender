# Contracts: none

**Slice**: `specs/142-entry-surface`

This slice exposes no interface. It removes two declarations from a rule and two custom properties
from a palette:

- no endpoint, request or response changes;
- no template variable or payload key is added — the entries render from the same context as before;
- no stored value changes: nothing is written, and nothing is read that was not read already;
- the two custom properties it deletes are read by nothing after the change, checked by
  `git grep -- '--tatib-entry-'` over the repository.

The nearest thing to a contract is the one this slice leans on: `.tatib__item--acts` and
`.tatib__eos` are the classes the stage template emits, and `.read__body` is the container. The
slice consumes them and adds nothing.

Stated explicitly rather than left absent, per SDD-12.
