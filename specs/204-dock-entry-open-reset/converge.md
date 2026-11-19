# Convergence: opening a service starts its entry blocks shut

**Spec**: `specs/204-dock-entry-open-reset/spec.md` (Accepted, gates 1 and 2, 2026-11-19)
**Plan**: `specs/204-dock-entry-open-reset/plan.md`
**Base**: `ab46f384` (`origin/develop`); the branch was cut at `85319b73` and fast-forwarded.

## Phase 1: Convergence

**Checked**: every row of the plan's traceability table, by the method it declares — 30 `test`
rows run, 1 `inspection` row inspected. The code was read against the table, not against the task
checkboxes.

### The change as it stands

`static/web/obs-dock.js` `openService()` — six added lines, one of them a statement:

```js
entryOverrides.clear();
```

Nothing else in the product changed: `git diff --stat` reports `static/web/obs-dock.js | 6 ++++++`
and the board row. No stylesheet, template, model, storage key or endpoint.

### Row-by-row evidence

| Row | Method | Evidence | Outcome |
| --- | --- | --- | --- |
| FR-001 | test | `test_an_open_starts_every_block_shut_in_another_service` — red on the base (`[3] != []`), green on the slice | converged |
| FR-002 | test | `test_the_live_entrys_block_stays_open_when_its_service_is_opened` — red on the base (`[3] != []`), green; live row `aria-current="true"`, chevron count 0, height > 0 | converged |
| FR-003 click | test | the FR-001 test drives a picker click | converged |
| FR-003 `Enter` | test | `test_the_keyboard_open_resets_like_a_click` — red on the base (`[3] != []`), green; preview `measurements-enter.json`: drafted `[]`, today `[3]` | converged |
| FR-003 on-load | test | `test_the_on_load_open_keeps_only_the_live_block` — green on the base and the slice (a reload already forgets page memory, so this row is a pin, not a red-first row); after reload `live=[3]`, `open=[3]`, `nonLive=[]` | converged |
| FR-003 not a re-read | test | `test_a_reread_keeps_a_hand_opened_block_open` — green on both; a real saved change (ORM edit in its own thread) plus an `update` posted from a second tab forces a rebuild, and `[3, 8]` stay open with `scrollTop` unchanged. Preview: `rebuilds=13`, open blocks `[0, 6, 9]` before and after | converged |
| FR-004 | test | spec 198's `test_open_blocks_survive_crossings_and_forget_on_reload`, re-run **unedited**, green | converged |
| FR-005 no write | test | `test_an_open_writes_no_display_state_and_broadcasts_nothing` — raw bytes identical across two opens, 0 channel messages; preview: 10 opens, all byte-identical, 0 messages | converged |
| FR-005 no motion | test | `test_an_open_paints_no_morph_in_the_new_list` — 0 `.is-morph` frames and `scrollTop` 0 across a 600 ms rAF sample; red on the base only at its final open assertion (`[1, 3] != []`) | converged |
| FR-006 page memory | test | the reload half of spec 198's pin, green | converged |
| FR-006 no new storage | inspection | `git diff -U0 \| grep '^+'` for `localStorage`, `sessionStorage`, `document.cookie`, `fetch(`, `/api/`, `BroadcastChannel`, `postMessage` → **no match**; the only added statement is the `Map.clear()` | converged |
| SC-001…SC-003 | test | the three US1 open tests; preview `today` paints `[3]`, `[3]`, `[1, 3]` where `drafted` paints `[]` | converged |
| SC-004 | test | the live-entry test; preview `drafted: back on the on-air service` → `open=[3] live=[3]` | converged |
| SC-005 | test | the re-read test and spec 198's crossing pin, one per event | converged |
| SC-006 | test | the no-write and no-morph tests; `measurements-open-write.json` | converged |
| SC-007 | test | the seven-module lane: **89 tests, 87 pass, 2 fail** — both proven identical on the base with the slice's change stashed (`1832 != 1873` in each), and already carded as `ITEM-215` on `develop`'s Backlog | converged with a base-identical red, carded |
| US1/AC1…AC6 | test | the six US1 tests (AC6 has one per path) | converged |
| US2/AC1…AC3 | test | spec 198's pin (crossing, reload) and the re-read test | converged |
| US3/AC1…AC3 | test | the no-morph and no-write tests, plus spec 200's `test_opening_the_service_on_air_enters_following` re-run unedited | converged |
| Edge: empty service | test | `test_an_empty_service_opens_without_a_block_or_an_error` — 0 rows, no page error | converged |

### The red-first record (T002)

Run against the base with the product file untouched: **11 tests, 7 failures, 0 errors**, every
failure the leak itself — `[3] != []` (five tests) and `[1, 3] != []` (two). Four tests were green
on the base and are pins, not red-first rows: the re-read, the no-write, the on-load resume and the
empty-service edge. Two harness defects were found and fixed before the red record was taken (a
missing `)` in one `page.evaluate`, and an ORM read inside Playwright's event loop, moved to
`setUp`); neither touched the product.

### The base-identical reds

| Test | Assertion on the slice | Assertion on the base (change stashed) | Card |
| --- | --- | --- | --- |
| `test_obs_dock_follow.py::test_other_state_notices_never_centre` | `1832 != 1873` | `1832 != 1873` | `ITEM-215` (Backlog on `develop`) |
| `test_obs_dock_follow.py::test_scrolling_and_expanding_another_entry_end_following` | `1832 != 1873` | `1832 != 1873` | `ITEM-215` |

Both are exact-`scrollTop` assertions that a scroll clamp defeats by ~one row; the behaviour under
test is correct and the card already owns the repair. This slice neither caused nor masks them.

### Preview parity (T017)

`diff static/web/obs-dock.js preview/assets/obs-dock.js` → one line, the preview's gate around the
same clear (`if (window.__openReset !== false) entryOverrides.clear();`). Both stylesheets are
byte-identical to the product's. Re-run on the implemented code: 64 states × 4 contexts (normal,
reduced-motion, narrow, light) with **0 page errors** on both `http://` and `file://`; 10 opens
byte-identical with 0 messages and 0 morph frames; the `Enter` path drafted `[]` / today `[3]`;
the re-read now forces a real rebuild (`rebuilds=13`) and keeps the hand-opened blocks.

### Findings

| ID | Type | Finding | Disposition |
| --- | --- | --- | --- |
| C1 | — | The plan declared 10 new tests; the module carries 11 (the empty-service edge case was added at Implement). | Mechanical: the plan gained its row and the split is now 30 test · 1 inspection · 0 manual; tasks carry T019. No requirement changed. |
| C2 | — | The preview's re-read button originally re-served an unchanged payload, which the dock's own shortcut skips without rebuilding — the state was vacuous. | Fixed in the preview only: the shim serves a revision marker so the rebuild is real, documented in `preview/README.md`. The product is untouched. |
| C3 | — | Two dock-follow tests are red. | Proven identical on the base under the same command; `ITEM-215` already cards them. Not this slice's work. |

**Outcome: Converged.** Zero `missing`, `partial`, `contradicts` or `unrequested` findings against
the traceability table; one pass, no cap reached. The two reds are base-identical and carded, so
they are not gaps in this slice's behaviour.

## History

- **2026-11-19** — pass 1: 30 test rows run (13 targeted green; the 89-test lane 87/89 with two
  base-identical reds proven by a stashed run), 1 inspection row clean, preview parity confirmed.
  Converged; C1 and C2 fixed mechanically, C3 carded elsewhere.
