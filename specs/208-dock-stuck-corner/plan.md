# Plan: the live entry header's corners follow its pin state

**Spec**: `specs/208-dock-stuck-corner/spec.md` · **Bump**: `minor` — two new dock capabilities
(`dock/R17`, `dock/R18`); declared at Plan and shown at gate 2.

## Technical context

- Python 3.12, Django 4.0; the dock is server-rendered templates with vanilla JS and a design
  stylesheet served by WhiteNoise. No new dependency, no migration, no endpoint, no template change.
- The corner face is a CSS class (`.is-stuck`); the bottom pin is a `cloneNode(true)` of the live
  `.entryrow` held in a list-level sticky slot. No framework, no build step.
- E2E: Playwright (Python) through Django's `StaticLiveServerTestCase`, in
  `tests/e2e/test_dock_stuck_corner.py`, run against the throwaway `gkps208` database via
  `specs/208-dock-stuck-corner/preview/run-tests.sh`.

## Constitution check

No `CONSTITUTION.md` in the repo (SDD-01); nothing to check.

## Decisions

Recorded in [research.md](./research.md): an unguarded `updateStuck()` leaves the band's own
motion guard intact (D001); pinned means top at the edge with the block still below (D002); the
bottom pin is a faithful list-level clone, not the header node or a caption strip (D003); the Next
band is list-level and always visible, with the list filling the scrollport so it pins when nothing
scrolls (D004); the clone clips when the header's bottom reaches the band's top, not a row early
(D005); clicking the pin is the centre control's act (D006).

## Change surface

| File | Change |
| --- | --- |
| `static/web/obs-dock.js` | `updateStuck()` on every geometry path; `updateLiveBand()` with band-top trigger and measured inset; always-shown Next band; pin click act |
| `static/styles/design/obs-dock.css` | `.is-stuck` flat-top rule; `.nextband-slot` / `.liveband-slot` list-level slots; list fills scrollport, body loses bottom padding |
| `tests/e2e/test_dock_stuck_corner.py` | 12 E2E pins: top corner state and tracking, faithful bottom clone, no-doubling, band trigger, per-frame, click act, reduced motion, always-visible band |
| `specs/208-dock-stuck-corner/preview/` | live preview, probe and run-tests harness |
| `docs/spec/dock.md` | `dock/R17` and `dock/R18` added at Fold |
| `CHANGELOG.md`, `VERSION` | release bookkeeping, at Fold |

## Traceability

| Requirement | Component | Verified by |
| --- | --- | --- |
| FR-001 | `obs-dock.js` `updateStuck()` · `obs-dock.css` `.is-stuck` | test — `test_a_pinned_header_wears_a_flat_top_after_advancing` |
| FR-002 | `updateStuck()` on scroll/sync/glide/morph/toggle/resize | test — `test_the_corners_track_the_pin_line_during_a_glide` + `preview/probe.py` |
| FR-003 | live-header selector in `updateStuck()` | test — `test_only_the_live_header_wears_the_stuck_state` |
| FR-004, FR-011 | `updateBand()`, `.nextband-slot` | test — `test_the_next_band_is_always_visible_even_when_the_list_fits` |
| FR-005 | reduced-motion path | test — `test_the_flat_top_lands_instantly_under_reduced_motion` |
| FR-006 | unchanged sticky top geometry, R14 wash, `.offstrip` | inspection — diff of `obs-dock.js` / `obs-dock.css` against base |
| FR-007 | `updateLiveBand()` trigger and clone | test — `test_the_bottom_pin_starts_as_soon_as_the_header_goes_off` |
| FR-008 | per-frame tracking | test — `test_the_bottom_pin_tracks_the_header_visibility_per_frame` |
| FR-009 | measured inset above the band | test — `test_the_bottom_pin_is_the_header_pinned_when_fully_off` |
| FR-010 | slot click handler | test — `test_clicking_the_bottom_pin_performs_the_ruled_act` |
| SC-012 | band-top boundary, no added height | test — `test_the_bottom_pin_starts_as_soon_as_the_header_goes_off` |
| SC-013 | flush band in a fitting viewport | test — `test_the_next_band_is_always_visible_even_when_the_list_fits` |

Verification split: **12 test · 3 inspection · 1 manual** (manual: the owner's live review on
`http://127.0.0.1:8767/obs/dock`).
