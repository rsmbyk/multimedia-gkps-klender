# Convergence: the Media Library list holds still while it refreshes

**Spec**: `specs/148-media-library-refresh-flicker/spec.md`
**Passes**: 1 of 3

## Pass 1 — 2026-10-28

Checked every row of `plan.md`'s traceability table against the code and the runs, by the method each
row declares.

| Gap | Type | Requirement | Evidence |
| --- | --- | --- | --- |
| The live sampler readout of the fixed page is not available before the merge: the compose `web` service bind-mounts the `develop` checkout, so `localhost:63404` serves the unfixed JavaScript, and a worktree `runserver` cannot reach the companion — `multimedia/local_media.py:447` admits only the origins in `GKPS_MEDIA_ALLOWED_ORIGINS`, which names the compose origin alone. | `partial` | FR-002 | Measured while running T012: `http://127.0.0.1:8765/media-library/` renders `Local library unavailable on this computer.` and Chromium logs `blocked by CORS policy` on `/v1/files` and `/v1/status`. The requirement's live evidence is the E2E frame sampling on a running Django server instead; both cases are green. |
| SC-003's instrument is not the `MutationObserver` T005 planned, and not the `replaceChildren` wrapper the first run used either: a draw is counted as a frame whose list differs from the frame before. The observer fires one record per removed and per added node, so a single draw read as 6–8 (`6 != 1`, one run); the wrapper double-counted the 2s poll's identical rebuild (`2 != 1` on two consecutive runs of the fixed page). The poll's rebuild is kept by FR-004, so the count must exclude it. | `partial` | SC-003 | Red run with the change counter: `2 not less than or equal to 1` on the unfixed page, 0 on the fixed one. The two guards (a failed references read, the poll) are green on the shipped page by design and were reworded to guard form (`≤ 1` change, no row moved), because the degraded list and the poll draw one picture either way. |

No `missing`, `contradicts` or `unrequested` gap was found: the diff touches `refresh()` in
`static/web/media-library.js` and the six cases in `tests/e2e/test_media_library.py`, and every
requirement row resolves to a green measurement or a recorded inspection.

**Outcome**: 2 findings recorded, one appended as a task (`T019`, the post-merge live readout), one
reconciled in `tasks.md` (`T005`'s method). No code change was required by either.

## Pass 2 — 2026-10-28

**Outcome**: Converged — nothing remains. The two pass-1 findings are a verification surface that is
unavailable until the branch is on the compose stack, and a probe method that was already reconciled;
neither is a gap between the code and a requirement.

## Accepted gaps

<!-- none: both pass-1 findings were recorded and dispositioned inside the slice -->

## Cap reached

<!-- not reached: pass 2 converged -->

## Pass 2 note — 2026-10-28, after the merge from `develop`

Merging `origin/develop` (`954dee75`, carrying 145 and 147) resolved four shared-document conflicts and
two identifiers moved:

- **The card**: `develop` had taken `ITEM-156` for the media-entry spacing E2E — the same failure this
  slice found and carded. That duplicate card was dropped, this slice's card renumbered
  `ITEM-158` (now `ITEM-183`), and its anchor issue (#423) renamed to match, keeping its number.
- **The bump**: `develop` reached `1.22.7` (145, 146, 147), so this slice's patch lands as `1.22.8`.
- **The capability number moved**: `develop` had already folded `R20`–`R23` (145, 146 and 147), so this
  slice's requirement is `R24`, not the `R22` it was drafted as. It is a new number, never a reuse.
- **The test module** kept both sides' cases: the transfer-icon cases from 147, then this slice's six.
