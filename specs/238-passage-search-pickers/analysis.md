# Analysis: passage search comboboxes

**Spec**: `specs/238-passage-search-pickers/spec.md`
**Plan**: `specs/238-passage-search-pickers/plan.md`

## Verdict

Pass. The slice is contained in one Django fragment, one vanilla-JS file and one stylesheet, with
no persisted, contractual or runtime change beyond the picker behaviour.

## Complexity gate

- **CRITICAL**: none. The change adds no new dependency, endpoint, interface or entity.
- **Complexity**: acceptable and minimal — one new internal helper (`wireSearchCombo`) and one
  CSS rule.

## Coverage gate

- **FR coverage**: all eight FRs have a traceability row and an inspection or test driver.
- **US coverage**: US1–US4 each have independent tests written red and green by plan task.
- **SC coverage**: SC-001 through SC-004 each have a driver recorded in the plan table.
- **Edge cases**: covered by inspection on the disabled/no-verse/last-verse rules.

## Convergence findings

1. Two defects found and fixed during live verification: (a) keyboard `.is-active` was left on a
   hidden option after filtering (now cleared on refresh); (b) Escape in a native search input
   clears the value, which would have emptied a chosen label while the hidden select held it
   (now `preventDefault()`d in the new combos only).
2. One assumption corrected during live verification: focus-select-all is confirmed working
   (6 of 6 characters selected), and it had not been exercised with a non-empty label before
   this slice's probe.

## Open findings

- None blocking. The legacy selector migration (`tests/e2e/test_entry_pickers.py`) and the
  version/board delivery records remain to be executed at Implement/Delivery.
