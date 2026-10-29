# Feature Specification: the first refresh authenticates its references write

**Slice**: `specs/150-references-token-order`
**Branch**: `fix/150-references-token-order`
**Created**: 2026-10-28
**Status**: Accepted (owner, gate 1 and gate 2, 2026-10-28)
**Input**: spec 148's post-merge verification (task T019): the live `/media-library/` still jolts, with `POST /v1/references` 403 on the first refresh

## What the page does today

Spec 148's `refresh()` (`static/web/media-library.js:153`) assembles the next state in locals and applies
it once:

```js
var next = { files: [], uses: null, protected: new Set(), status: null, ready: false };
return Promise.all([request('/status'), request('/files')]).then(function (results) {
  next.status = results[0]; next.files = results[1].files || [];        // the status is kept, not applied
  return fetch(page.dataset.referencesUrl, …)
    .then(…)                       // ← write('/references', …) uses `token`, which setStatus still owns
    .catch(function () { next.uses = null; … });
}).catch(…).then(function () {
  files = next.files; uses = next.uses; protectedFiles = next.protected;
  setStatus(next.status); render();                                     // ← the token arrives here, too late
  return next.ready;
});
```

`write()` (`:21`) sends `X-GKPS-Media-Token: token`, and `token` is assigned only inside `setStatus`
(`:37`). So the **first** refresh after a page load fires its `POST /v1/references` with an empty
token, and the companion refuses it — `multimedia/local_media.py:514` → `403 {'error': 'Not
authorized.'}`. The references `.catch` then treats the read as failed, `next.uses` stays `null`, and
that refresh's one draw paints `Service uses unavailable` on every row.

Measured on the compose page serving the merged code (VERSION 1.22.8, `/media-library/`, 1920×1100,
every frame sampled):

| | first draw | second draw (190ms later) |
| --- | --- | --- |
| rows showing `Service uses unavailable` | **8 of 8** | 1 of 8 (the file that is genuinely unused) |
| `#mediaFileList` height | **800 px** | 868 px |
| row 2 / 3 / 4 / 5 top | 355 / 452 / 549 / 646 | 377 / 478 / 601 / 702 |

So the row jolt spec 148 removed is still there — 22 / 26 / 52 / 56 px — produced across two refreshes
instead of two passes inside one. The network shows it directly: `POST /v1/references` **403**, then
**200** once a later refresh has a token.

**Why the suite did not see it.** The E2E module's companion stub (`tests/e2e/test_media_library.py`,
`_sampled_library`'s `companion`) answers `/references` with `{'files': inventory}` and 200 for every
request. It never reads `X-GKPS-Media-Token`, so a tokenless write is indistinguishable from an
authenticated one — six green cases against a page that fails on the real companion.

## User Scenarios & Testing

### US1 — The first refresh draws the list once, with its references (P1)

**Why this priority**: it is the shipped requirement (R24) failing in the product while its tests pass,
and it is a race every page load loses — the operator sees a placeholder list for a beat and a 68px jump
on the first action.

**Independent Test**: with the real companion behind the page, open `/media-library/` after a server
restart and sample every frame: one draw, with the references, no row moving.

**Acceptance scenarios**

1. **Given** a page that has just been opened and a companion that demands its write token, **When** the
   page's first refresh runs, **Then** its references write carries that refresh's token and the list is
   drawn once with its references.
2. **Given** the same page, **When** the first draw lands, **Then** the rows that carry references show
   them, and `Service uses unavailable` appears only for a file that has none.
3. **Given** any later refresh, **When** it writes its references, **Then** it still carries the token and
   still draws once.

### US2 — The suite cannot pass this again by accident (P2)

**Why this priority**: the green suite is what let this ship. A stub that accepts everything is the
opposite of a test.

**Independent Test**: run the six spec-148 cases against a stub that answers a tokenless references write
with 403; they must fail before the fix and pass after it.

**Acceptance scenarios**

1. **Given** the E2E stub, **When** a page writes `/references` with no `X-GKPS-Media-Token`, **Then** the
   stub answers 403 with the companion's own body.
2. **Given** a page that sends the token, **When** it writes `/references`, **Then** the stub answers 200
   with the inventory, and the six spec-148 cases stay green.

### Edge Cases

- **When** `/status` itself fails, **Then** the refresh degrades as it does today: no token exists, one
  draw, the disconnected copy — no change.
- **When** the references write fails with a valid token (a companion restart mid-refresh), **Then** the
  page degrades once, as today, and the next refresh recovers.
- **When** the page is opened twice in two tabs, **Then** each tab's first refresh writes with the token
  from its own `/status` response.
- **When** a poll lands between the token's arrival and the draw, **Then** nothing about it changes: the
  poll still redraws the last complete state (R24, FR-004).

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | A refresh SHALL authenticate its own references write: the token from that refresh's `/status` response SHALL be in place before the write is sent. | `new: reading` → R25 |
| FR-002 | The refresh SHALL still draw the list at most once, with its references — the behaviour R24 states — and the head controls SHALL still be applied from the same response. | `reading/R24` |
| FR-003 | The E2E companion stub SHALL refuse a references write that carries no valid `X-GKPS-Media-Token` with the companion's own 403 body. | `new: reading` → R25 |
| FR-004 | Nothing else changes: no markup, CSS, endpoint, payload, row geometry or copy; the six spec-148 cases keep their assertions. | `reading/R24` |

### Key Entities

- **Refresh** — unchanged: one `/status` + `/files` read, one references read and write, one draw.
- **Write token** — the `write_token` string in the `/status` payload (`multimedia/local_media.py:587`),
  sent as `X-GKPS-Media-Token` and compared at `:514`. Not stored; it lives as long as the companion.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | On the live page after a restart, the first draw carries the references: 0 rows showing `Service uses unavailable` beyond the files that have none, and no row's top changes. | `preview/frame_sampler.py`: `worst jolt: 0px` |
| SC-002 | `POST /v1/references` is answered 200 on the page's first refresh. | the sampler's network log, or the browser's own log on the live route |
| SC-003 | With the stub refusing a tokenless write, the six spec-148 cases are red before the fix and green after it. | `manage.py test tests.e2e.test_media_library` |
| SC-004 | Rows, order, text, cloud states, head controls and title after a refresh are identical to 1.22.8's. | the existing module cases re-run unchanged |

## UI/UX

`n/a — no look changes; the slice removes the placeholder first draw that R24 already forbids.` The
transient it fixes is the one R24 measured, and the live route is where it is read:
`preview/frame_sampler.py` against `http://localhost:63404/media-library/`.

## Assumptions

- **The token is assigned before the write, and the visible state is still applied once.** The fix
  assigns `token` from the `/status` response at the top of the refresh and leaves `setStatus` and
  `render()` where they are; that keeps one draw and puts authentication where the write needs it.
- **The head controls' copy is not split into two updates.** Only the token moves earlier; nothing else
  about `setStatus` changes, so a reader sees no half-applied status.
- **The stub mirrors the companion, including its body.** It refuses with `403 {'error': 'Not
  authorized.'}`, the reply at `local_media.py:515`, so a future failure reads the same in both places.
- **No other surface changes.** No markup, CSS, endpoint, payload or copy; the fix is two lines of
  ordering plus the stub's check.
- **The capability number is R25.** `R24` is this page's one-draw requirement from spec 148; this is the
  authentication half of it, stated separately because it can fail alone.

## Clarifications

### Session 2026-10-28

- No open items: the defect was reproduced on the running page before Specify (two draws 190ms apart,
  `POST /v1/references` 403 then 200), and the stub's blind spot was read in the test module. Zero open
  markers remain.
