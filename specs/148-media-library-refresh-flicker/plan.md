# Implementation Plan: the Media Library list holds still while it refreshes

**Spec**: `specs/148-media-library-refresh-flicker/spec.md`
**Branch**: `feat/148-media-library-refresh-flicker`
**Bump**: `patch` (1.22.7 → 1.22.8, on `develop` after 145, 146 and 147)
**Preview**: live at `http://localhost:63404/media-library/`, sampled by
`specs/148-media-library-refresh-flicker/preview/frame_sampler.py` (`preview/README.md`)

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | JavaScript (ES5, the file's own style) in `static/web/media-library.js`; Playwright (Python) for the tests |
| Primary dependencies | none added — the page's own `fetch`, the existing companion endpoints, the existing E2E harness |
| Storage | none; the list is drawn from the companion's `/status`, `/files` and `/references` plus the same-origin `/media-library/references/` response |
| Testing | Playwright E2E through `StaticLiveServerTestCase`, in `tests/e2e/test_media_library.py` — the module already owns this surface and stubs the companion |
| Target platform | every browser the app supports; the change is promise ordering, no language feature above ES5 |
| Project type | server-rendered Django web app, vanilla JS, no build step |
| Performance goals | one fewer full rebuild per refresh; the first paint moves later by the references round trip, measured at 16–31 ms on the page's first load |
| Constraints | the row markup, its CSS, the filters, the sort, the cloud control's states, the dialogs, the companion requests and the page title are untouched; `refresh()`'s return value keeps its meaning (`false` when the references are unknown) |
| Scale / scope | one function's control flow in `static/web/media-library.js`, six E2E cases, one board card, one capability delta |

## Constitution Check

No `CONSTITUTION.md` exists in this repository, and SDD-01 makes it optional and never auto-created, so
the check does not apply. The plan honours the constraint row above instead: one file's control flow,
no new dependency, no markup or CSS change, no API change.

Re-checked after Phase 1: pass — the design adds no file beyond the tests, and no new state beyond the
one value the refresh already computes.

## Phase 0 — Research

See `research.md`. Four candidates were weighed and one measured: drawing once, after the references
are known (D001). **Unknowns remaining: 0.**

## Phase 1 — Design

- `data-model.md` — the in-memory library state (`files`, `uses`, `protected`, `status`), the file row's
  height rule, and the five invariants this slice makes checkable.
- `contracts/` — `none` (`contracts/none.md`): no endpoint, payload, template variable, stored value or
  event is added or re-shaped.
- `quickstart.md` — the DB-isolated setup, the sampler command, and the one E2E command; all three were
  run on this worktree before the plan was written.

### The design

`refresh()` (`static/web/media-library.js:146`) assembles the next state in locals and applies it, once,
at the end of every path:

```js
function refresh() {
  var next = { files: [], uses: null, protected: new Set(), status: null, ready: false };
  return Promise.all([request('/status'), request('/files')]).then(function (results) {
    next.status = results[0]; next.files = results[1].files || [];
    return fetch(page.dataset.referencesUrl, { credentials: 'same-origin' })
      .then(function (response) { if (!response.ok) throw new Error('Cannot load service references'); return response.json(); })
      .then(function (references) {
        next.uses = references.uses || {}; next.protected = new Set(references.protected || []);
        return write('/references', 'POST', { hashes: Object.keys(next.uses), protected: references.protected || [] })
          .then(function (synced) { if (synced.files) next.files = synced.files; next.ready = true; });
      })
      .catch(function () { next.uses = null; next.protected = new Set(); });   // degraded, still one draw
  }).catch(function () { next.files = []; next.uses = null; next.status = null; next.ready = false; })
    .then(function () {
      files = next.files; uses = next.uses; protectedFiles = next.protected;
      setStatus(next.status); render();                    // the only draw
      return next.ready;
    });
}
```

Four things this buys, each traced to a requirement:

- **One draw** (FR-001): the single `render()` sits on the outer chain, so success, references failure
  and transport failure all pass through it once.
- **No partial state on screen** (FR-001, D002): `files`, `uses` and `protected` are locals until the
  end, so a 2s poll landing mid-refresh redraws the previous complete state rather than new files
  against old references.
- **A first load that appears complete** (FR-003): nothing is drawn until the references are known or
  have failed.
- **The placeholder survives for the case it is for** (FR-003): the references `.catch` leaves
  `uses = null` and the one draw shows `Service uses unavailable`.

`render()` itself is not touched: same `replaceChildren()`, same rows, same order (FR-005).

**What is deliberately not done.** No `min-height` or other CSS band-aid; no skeleton rows; no
differencing renderer for the 2s poll (measured inert, FR-004); no change to `media-handoff.js`, the
templates, the references view or the companion; no retry loop for a failed references read.

## Traceability

| Requirement / scenario | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| FR-001 one draw per refresh, no placeholder pass over known references | `static/web/media-library.js:146` (`refresh`), `:93` (`render`) | `test` → `tests/e2e/test_media_library.py::MediaLibraryE2ETests::test_the_library_list_is_drawn_once_per_refresh` | `MutationObserver` counts child replacements: 1 |
| FR-002 no row changes position during a refresh | `static/web/media-library.js:146` | `test` → `…::test_a_library_refresh_never_moves_a_row` | per-row spread of `top` is 0px across every sampled frame |
| FR-003 first load draws once complete; a failed references read draws once with the placeholder | `static/web/media-library.js:146-159` | `test` → `…::test_the_library_list_is_drawn_once_per_refresh` and `…::test_a_failed_references_request_draws_the_placeholder_once` | held route for the first; a 500 for the second |
| FR-004 the 2s poll keeps re-reading and stays visually inert | `static/web/media-library.js:161`, `static/web/media-handoff.js:155` | `test` → `…::test_the_status_poll_leaves_the_list_where_it_is` | waits one poll interval, compares row tops |
| FR-005 nothing else changes | `static/web/media-library.js` (diff), `media-handoff.js`, templates, CSS (all untouched) | `inspection` — the diff touches `refresh()` only; `test` → the module's existing cases re-run (`…::test_library_filter_sort_and_dialogs`, `…::test_connected_library_shows_file_and_status_details`, `…::test_connection_icon_tracks_status_refresh`, `…::test_disconnected_library_hides_local_inventory_details`, `…::test_empty_library_keeps_tall_create_modal_and_quiet_empty_state`) | SC-005; `…::test_media_entry_has_roomy_spacing_and_wraps_on_narrow_screen` fails identically on `develop` (ITEM-156) |
| US1 AC1 Share online does not move the list | `static/web/media-library.js:82` → `refresh()` | `test` → `…::test_clicking_share_online_never_moves_a_library_row` | begin endpoint stubbed to `{online: true}` |
| US1 AC2 / AC3 Remove-cancelled and Save setting do not move the list | `static/web/media-library.js:90`, `:139` → `refresh()` | `test` → `…::test_a_library_refresh_never_moves_a_row` | one invariant, two triggers; the assertion names the trigger |
| US1 AC4 the first load appears once, complete | `static/web/media-library.js:146` | `test` → `…::test_the_library_list_is_drawn_once_per_refresh` | list height after the first draw equals its settled height |
| US1 AC5 a running transfer's poll moves nothing | `static/web/media-library.js:161` | `test` → `…::test_the_status_poll_leaves_the_list_where_it_is` | |
| US2 AC1 no placeholder frame for a known file | `static/web/media-library.js:146` | `test` → `…::test_a_known_reference_never_shows_the_placeholder` | references held 200 ms |
| US2 AC2 a failed references read draws the placeholder once and keeps it | `static/web/media-library.js:157` (the `.catch`) | `test` → `…::test_a_failed_references_request_draws_the_placeholder_once` | |
| US2 AC3 a first load never paints early and short | `static/web/media-library.js:146` | `test` → `…::test_the_library_list_is_drawn_once_per_refresh` | same run as AC4 |
| Edge: empty library / disconnected companion | `static/web/media-library.js:146-158` | `test` → `…::test_disconnected_library_hides_local_inventory_details`, `…::test_empty_library_keeps_tall_create_modal_and_quiet_empty_state` (existing, re-run) | unchanged paths |
| Edge: a file with two or more references (the 123px row) | `static/web/media-library.js:55-66` (untouched) | `test` → `…::test_a_library_refresh_never_moves_a_row` | the fixture carries a two-line `uses` block |
| Edge: a filter, sort or Unused change during a refresh | `static/web/media-library.js:142-145` → `render()` | `inspection` — the handlers call `render()` directly and never touch `refresh()`'s locals | no new code path |
| Edge: a slow references read (300 ms) | `static/web/media-library.js:149` | `test` → `…::test_a_known_reference_never_shows_the_placeholder` | held route |
| Edge: `prefers-reduced-motion` | none — no motion is added | `inspection` — the diff contains no animation, transition or timing call | |
| Edge: a narrow width where a reference wraps to three lines | `components.css:628` (untouched) | `inspection` — the fix does not write a height; the row's block is the same CSS at every width | |
| SC-001 distinct tops per row = 1 | `static/web/media-library.js:146` | `test` → `…::test_a_library_refresh_never_moves_a_row` | four triggers sampled |
| SC-002 0 placeholder frames with references known | `static/web/media-library.js:146` | `test` → `…::test_a_known_reference_never_shows_the_placeholder` | |
| SC-003 ≤ 1 child replacement per refresh | `static/web/media-library.js:146` | `test` → `…::test_the_library_list_is_drawn_once_per_refresh` | |
| SC-004 the list never grows after it appears | `static/web/media-library.js:146` | `test` → `…::test_the_library_list_is_drawn_once_per_refresh` | height sampled every frame |
| SC-005 rows, order, text, cloud states and title identical | `static/web/media-library.js` (diff) | `test` → the module's existing cases re-run; `inspection` — the diff's only touched function is `refresh()` | |

**Verification split: 20 test · 3 inspection · 0 manual.**

## Plan exit gate

| Check | Result |
| --- | --- |
| Requirement coverage | FR-001…FR-005 each carry a row; every SC and every story scenario is mapped |
| Entity coverage | the library state's four fields and the row's height rule are in `data-model.md`, none added |
| Interface coverage | `contracts/none.md` states `none` and why, in writing |
| Decision provenance | D001–D004 in `research.md`, each with its measurement or its code read |
| Constitution conformance | no constitution exists (SDD-01); the constraint row is honoured |
| Zero unknowns | 0 |
| Verification declared | 17 `test` · 7 `inspection` · 0 `manual`, each naming a test function, a file, or what to look at |
| `quickstart.md` runnable | yes — the sampler and one E2E case were run on this worktree before the plan was written |

## Complexity Tracking

| Violation | Why needed | Simpler alternative rejected because |
| --- | --- | --- |
| — | — | — |

## Project Structure

### Documentation

```
specs/148-media-library-refresh-flicker/
  spec.md  plan.md  research.md  data-model.md  quickstart.md  tasks.md  analysis.md
  contracts/none.md  checklists/requirements.md  preview/README.md  preview/frame_sampler.py
```

### Source

```
static/web/media-library.js                  refresh()'s control flow (one draw, state applied late)
tests/e2e/test_media_library.py              six new cases in MediaLibraryE2ETests
docs/spec/reading.md                         R24 at Fold
backlog/items/ITEM-158-media-library-refresh-jolt.md   card
backlog/board.md                             the card's row
specs/README.md                              the spec's index row, at Accept
VERSION, CHANGELOG.md                        patch bump and one line, at delivery
```

### Structure Decision

No new module, file or directory in the product. The behaviour lives in the function that already owns
it; the tests live in the module that already owns this surface. The pack keeps its probe under
`preview/` because it is the measurement the gate's preview is read with — the same place a static
preview's page and its regenerator sit.
