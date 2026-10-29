# Implementation Plan: the first refresh authenticates its references write

**Spec**: `specs/150-references-token-order/spec.md`
**Branch**: `fix/150-references-token-order`
**Bump**: `patch` — 1.22.9 → 1.22.10
**Preview**: `n/a — no visible change; the readout is the live route, `preview/frame_sampler.py` in spec 148's folder`

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | JavaScript (ES5) in `static/web/media-library.js`; Playwright (Python) for the tests |
| Primary dependencies | none added |
| Storage | none; the token lives in the companion process (`local_media.py:601`) and in the page's closure |
| Testing | `tests/e2e/test_media_library.py` — the six spec-148 cases, a stricter companion stub, and one new case |
| Target platform | every browser the app supports |
| Project type | server-rendered Django app, vanilla JS, no build step |
| Performance goals | none; one assignment moves earlier, no request added or removed |
| Constraints | one draw per refresh (R24); head controls applied once, from the same response; no markup, CSS, endpoint, payload or copy change; the six spec-148 assertions keep their wording |
| Scale / scope | 2 lines in `refresh()`, the stub's token check, one new E2E case, one board card |

## Constitution Check

No `CONSTITUTION.md` exists (SDD-01: optional, never auto-created), so the check does not apply. The
constraint row above stands in its place.

Re-checked after Phase 1: pass — the design adds no file, no request and no state.

## Phase 0 — Research

See `research.md`. Four decisions, all measured or read: assign the token rather than move `setStatus`
(D001), make the stub refuse what the companion refuses (D002), pin the header in a case of its own
(D003), and take the live readout after the merge (D004). **Unknowns remaining: 0.**

## Phase 1 — Design

- `data-model.md` — the write token's lifetime and the three invariants this slice adds to spec 148's
  refresh model.
- `contracts/` — `none` (`contracts/none.md`): no interface changes.
- `quickstart.md` — the DB-isolated command, the new case, the module, and the post-merge live readout.

### The design

`static/web/media-library.js:153` — one statement, immediately after the two reads:

```js
next.status = results[0]; next.files = results[1].files || [];
if (next.status && next.status.write_token) token = next.status.write_token;   // ← this refresh's own write
```

Everything else stays: `write('/references', …)` at `:163` now carries the token, `next.uses` survives,
and the single `setStatus(next.status) … render()` at `:168` still makes the only visible update.

`tests/e2e/test_media_library.py` — `_sampled_library`'s `companion` gains the companion's own refusal:

```python
elif url.endswith('/references'):
    if route.request.headers.get('x-gkps-media-token') != 'test-token':
        return route.fulfill(status=403, content_type='application/json',
                             body=json.dumps({'error': 'Not authorized.'}),
                             headers={'Access-Control-Allow-Origin': self.live_server_url})
    payload = {'files': inventory}
```

**What is deliberately not done.** No `setStatus` moved earlier (D001), no retry on a 403, no change to
`write()`, `share()`, `media-handoff.js`, the templates, the CSS or the companion. The six spec-148 cases
keep their assertions unchanged — only the stub under them changes.

## Traceability

| Requirement / scenario | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| FR-001 a refresh authenticates its own write | `static/web/media-library.js:157` | `test` → `tests/e2e/test_media_library.py::MediaLibraryE2ETests::test_the_first_refresh_writes_its_references_with_the_token` | the captured request's `X-GKPS-Media-Token` equals the token `/status` returned |
| FR-002 one draw still, with the references | `static/web/media-library.js:153-172` | `test` → `…::test_the_library_list_is_drawn_once_per_refresh`, `…::test_a_library_refresh_never_moves_a_row`, `…::test_clicking_share_online_never_moves_a_library_row`, `…::test_a_known_reference_never_shows_the_placeholder`, `…::test_a_failed_references_request_draws_the_placeholder_once`, `…::test_the_status_poll_leaves_the_list_where_it_is` | unchanged assertions, stricter stub |
| FR-003 the stub refuses a tokenless write | `tests/e2e/test_media_library.py:977` (`_sampled_library`) | `test` → the six spec-148 cases run red against the stub before the fix; `inspection` — the 403 branch carries the companion's own body (`local_media.py:515`) | US2 AC1/AC2 |
| FR-004 nothing else changes | `static/web/media-library.js` (diff), `media-handoff.js`, templates, CSS (untouched) | `inspection` — the diff is one statement plus the stub; `test` → `…::test_library_filter_sort_and_dialogs`, `…::test_connected_library_shows_file_and_status_details` re-run | SC-004 |
| US1 AC1 the first write carries the token | as FR-001 | `test` → `…::test_the_first_refresh_writes_its_references_with_the_token` | |
| US1 AC2 the first draw shows the references | `static/web/media-library.js:157` | `test` → the same case asserts no row shows `Service uses unavailable` for a file with references | |
| US1 AC3 later refreshes keep doing it | `static/web/media-library.js:153-172` | `test` → `…::test_a_library_refresh_never_moves_a_row` (two triggered refreshes) | |
| US2 AC1 no token, no write | `tests/e2e/test_media_library.py:977` | `test` → the red run of the six cases with the stricter stub | recorded in `analysis.md` |
| US2 AC2 with the token, 200 and the inventory | same | `test` → the six cases green | |
| Edge: `/status` fails | `static/web/media-library.js:166` (outer catch) | `inspection` — no token exists, one draw, the disconnected copy; unchanged by this slice | |
| Edge: the write fails with a valid token | `static/web/media-library.js:164` (`.catch`) | `inspection` — degrades once, as today; the next refresh recovers | |
| Edge: two tabs | `static/web/media-library.js:157` | `inspection` — the token is assigned per refresh inside each page's closure; no shared state | |
| Edge: a poll lands mid-refresh | `static/web/media-library.js:175` | `test` → `…::test_the_status_poll_leaves_the_list_where_it_is` | R24, FR-004 |
| SC-001 live: `worst jolt: 0px` and one authenticated write | the compose page after the merge | `manual` — `docker compose exec -T web python manage.py collectstatic --noinput && docker compose restart web`, then `specs/148-media-library-refresh-flicker/preview/frame_sampler.py`; expect exit 0 and `POST /v1/references` 200 | D004 |
| SC-002 the first write is answered 200 | `static/web/media-library.js:157` | `test` → the new case asserts the header; a 200 follows from the stub | |
| SC-003 the six cases are red before, green after | `tests/e2e/test_media_library.py` | `test` → the recorded red run and the green run | |
| SC-004 rows, order, text, cloud states, head controls, title unchanged | the diff + the module | `test` → the module's existing cases re-run; `inspection` — the diff touches one statement and the stub | |

**Verification split: 13 test · 3 inspection · 1 manual.**

## Plan exit gate

| Check | Result |
| --- | --- |
| Requirement coverage | FR-001…FR-004 each carry a row; every SC and every story scenario is mapped |
| Entity coverage | the write token's three fields and its lifetime are in `data-model.md`; nothing added |
| Interface coverage | `contracts/none.md` states `none` and why |
| Decision provenance | D001–D004 in `research.md`, each with its measurement or code read |
| Constitution conformance | no constitution exists (SDD-01); the constraint row is honoured |
| Zero unknowns | 0 |
| Verification declared | 15 `test` · 4 `inspection` · 1 `manual` |
| `quickstart.md` runnable | yes — the new case and the module run on this worktree; the live readout is the one `manual` row |

## Complexity Tracking

| Violation | Why needed | Simpler alternative rejected because |
| --- | --- | --- |
| — | — | — |

## Project Structure

### Documentation

```
specs/150-references-token-order/
  spec.md  plan.md  research.md  data-model.md  quickstart.md  tasks.md  analysis.md  converge.md  fold.md
  contracts/none.md  checklists/requirements.md
```

### Source

```
static/web/media-library.js                  one assignment in refresh() (:157)
tests/e2e/test_media_library.py              the stub's token check, one new case
docs/spec/reading.md                         R26 at Fold
backlog/items/ITEM-161-references-token-order.md   card
backlog/board.md                             the card's row
specs/README.md                              the spec's index row, at Accept
VERSION, CHANGELOG.md                        patch bump and one line, at delivery
```

### Structure Decision

No new module or file in the product; the fix lives in the function whose ordering caused it, and the
case lives in the module that already owns this surface.
