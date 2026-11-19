# Fold: a clicked service keeps its date

**Capability**: `docs/spec/reading.md`
**Folded at**: 2026-11-19

## Delta

| Type | Requirement | Change |
| --- | --- | --- |
| `modified` | `R41` | The reveal that hides a dated service row's date is now the row's hover or its own edit/delete control's `:focus-visible`, not generic `focus`; clicking the row's link is named as a state that keeps the date. The "revealing the delete control" scenario gains the clicked-then-pointer-away case. |
| `modified` | `R9` | The Today badge follows that same reveal; focusing the row's link alone does not hide it. The badge scenario gains the clicked-then-pointer-away case. |

No requirement was added, removed or renamed. `R41` and `R9` keep their IDs and their existing behaviour — the change only says which focus counts as an action reveal, matching what the controls already did.

## Drift guard

- **Files changed in this capability**: `docs/spec/reading.md` (header, `R9`, `R41`); `static/styles/design/components.css` (the reveal rule those two blocks describe); `tests/e2e/test_sidebar_date_reveal.py` (their verification).
- **Declared no behaviour change**: no — the reported click state changes from date hidden to date painted.
