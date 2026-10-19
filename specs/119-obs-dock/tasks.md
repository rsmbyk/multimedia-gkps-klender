# Tasks 119: OBS dock — one state for the dock, the projector, and the overlay

- **Status:** Draft
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order. -->

## Checklist

- [ ] Spec Accepted by the project owner.
- [ ] Branch from the current base (`feat/obs-dock`).
- [ ] Red — routes and template contexts (`multimedia/web/test_reading.py`):
      `/projector` renders with and without `?service`; `/obs/dock` lists services;
      `/obs/source/overlay` renders an empty listen-only shell; the old
      `/obs/service/*`, `/lookup/`, and `/detour/` routes are gone.
- [ ] Green — move the projector route to `/projector` (+ `lookup/`, `detour/`), update
      every reverse/link (corner service list, Go To, project button `projector_url`,
      service worker and offline shell paths).
- [ ] Red — display-state contract (JS-level via E2E): `show`/`hide`/`release`/`flip`
      and catch-up with all surfaces closed; multiple tabs agree.
- [ ] Green — extend `static/web/display.js` (state shape + verbs, no reaper, no
      step-aside), convert the projector to adopt services in place, and add the
      overlay reader.
- [ ] Red — dock behaviour E2E (`tests/e2e/test_obs_dock.py`): picker → runner, browse vs
      run, entry/step/bait/keyboard moves, sticky current + NEXT band, TB/SIM, hide,
      release from the service page, appearance cycle + persistence.
- [ ] Green — build `/obs/dock` from the approved mockup: header (logo, reload,
      appearance), picker, runner, transport, keyboard/focus policy, theme morph.
- [ ] Red — overlay E2E (`tests/e2e/test_obs_overlay.py`): caption content and typography,
      blank on hide/release/media, zero focusable elements, bundled Source Sans 3.
- [ ] Green — build `/obs/source/overlay` as a state-driven caption renderer.
- [ ] Red — projector E2E (`tests/e2e/test_projector_follows.py`): `?service` adoption,
      mid-run adoption without navigation, balanced wrapped rows, bundled CMG Sans, and
      unchanged media behaviour.
- [ ] Green — projector adoption + `text-wrap: balance` + the font stack swap.
- [ ] Bundle `static/fonts/` with CMG Sans Bold and Source Sans 3 plus both license
      texts; add the `@font-face` rules; verify the faces load without machine installs.
- [ ] Update the service page button: opens `/projector?service=<id>`, Stop project
      becomes a release.
- [ ] Run targeted Django tests and one focused browser E2E class locally; full suite and
      browser matrix run in CI after push.
- [ ] Fill Traceability in `spec.md` with final paths.
- [ ] In the same implementation PR, move ITEM-119 and board through review to Done,
      bump VERSION once (minor), add changelog, and fill `release_version`.
- [ ] Conventional Commit and draft PR to develop linking this spec.
- [ ] Verify exact-head CI before merge.

## Done when

- [ ] All acceptance scenarios in `spec.md` hold.
- [ ] Tests named above are green.
- [ ] Board, tasks, and version (if any) are complete in this PR.
