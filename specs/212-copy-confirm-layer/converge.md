# Convergence — spec 212

## Pass 1 — 2026-11-21

**Checked**: every row of `plan.md`'s traceability table, by the method that row declares. The two
new tests were written first and run against the unmodified stylesheet, then the block was added to
`components.css` and both were re-run.

### Evidence

**Red first** (T003–T005), against `components.css` before the change:

```
FAIL: test_the_copy_confirmation_covers_the_form
  AssertionError: 476.765625 != 241.25 within 0.1 delta (235.515625 difference)
  : the dialog must not grow when the confirmation opens
FAIL: test_the_copy_confirmation_card_matches_the_preview
  AssertionError: 436 != 448 within 0.5 delta (12 difference)
```

Both failed on the behaviour they name — the dialog's height and the card's width — not on an import,
a selector or a timeout (TDD-02).

**Green after** (T006–T007):

```
$ manage.py test tests.e2e.test_tatib_templates.TataIbadahTemplateE2ETests --noinput
Ran 29 tests in 39.264s
OK
```

29 tests in the class: the two new ones, the pre-existing `test_copy_as_template_asks_and_copies`
(FR-006, T010) and `test_a_fill_in_and_a_choice_settle_then_create` (the generate page's own
confirmation, T011). No other test in the class moved.

**Inspection — dark theme (T012, US2/AC3)**, in `preview/index.html` with the **Dark** toggle:

| | value |
| --- | --- |
| `data-theme` | `dark` |
| scrim | `rgba(0, 0, 0, 0.68)` — the dark `--backdrop` |
| card | `rgb(20, 19, 15)` — the dark `--canvas` |
| body ink | `rgb(245, 243, 238)` |
| card box | 448 × 176.3 — unchanged from the light theme |

No rule names a colour, so the dark theme needs nothing of its own: the tokens do the work.

**Inspection — narrow dialog (T013, Edge Cases)**, preview at a 380px viewport:

| | value |
| --- | --- |
| dialog | 337 wide at x 19 |
| layer | 337 wide at x 19 — the dialog's box |
| card | 305 wide at x 35, right edge 340 |
| card inside the layer | yes |
| page scroll width | 375 ≤ 380 — no horizontal scroll |

The card is `min(468px, 100%)` inside the layer's 16px padding, so it shrinks with the dialog and never
overflows it. At this width the dialog itself is capped by the user agent's own dialog rule, not by
`.editor`'s `min(30rem, 100vw - 32px)`; the card follows either way.

### Findings

| ID | Type | Where | Finding | Disposition |
| --- | --- | --- | --- | --- |
| C1 | — | — | none | — |

**Outcome**: converged on pass 1. No `missing`, `partial`, `contradicts` or `unrequested` gaps.

### Notes for the next reader

- `.editor__confirm-title` (the rule directly above the new block) styles a class no template emits. It
  predates this slice and is left alone: removing dead CSS is not this change's business.
- The scrim's `border-radius: 14px` duplicates `.editor`'s own radius by hand; `research.md` D003
  records why (`inherit` resolves against `.editor__body`) and why a `--radius-dialog` token is a
  separate decision.
