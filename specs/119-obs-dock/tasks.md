# Tasks 119: OBS dock — one state for the dock, the projector, and the overlay

- **Status:** In review
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order. -->

## Checklist

- [x] Spec Accepted by the project owner.
- [x] Branch from the current base (`feat/obs-dock`).
- [x] Red — routes and template contexts (`multimedia/web/test_obs_dock.py`): `/projector`
      renders with and without `?service`; `/obs/dock` lists services; `/obs/source/overlay`
      renders an empty listen-only shell; the old `/obs/service/*`, `/lookup/`, and
      `/detour/` routes are gone.
- [x] Green — move the projector route to `/projector` (+ `lookup/`, `detour/`), update
      every reverse/link (corner service list, Go To, project button `projector_url`,
      service worker and offline shell paths).
- [x] Red — display-state contract (E2E): `show`/`hide`/`release`/`flip` and catch-up with
      all surfaces closed; multiple tabs agree.
- [x] Green — extend `static/web/display.js` (state shape + verbs, no reaper, no
      step-aside), convert the projector to adopt services in place, and add the overlay
      reader.
- [x] Red — dock behaviour E2E (`tests/e2e/test_obs_dock.py`): picker → runner, browse vs
      run, entry/step/keyboard moves, hide, catch-up, `?service` adoption. TB/SIM flip and
      song baits are not in the browser test: the local database carries no service with a
      two-edition passage or a song, and CI fixtures do not build one yet (see Open).
- [x] Green — build `/obs/dock` from the approved mockup: header (logo, reload,
      appearance), picker, runner, pinned row + NEXT band, transport, keyboard/focus
      policy, theme morph.
- [x] Red — overlay E2E (`tests/e2e/test_obs_overlay.py`): caption content and typography,
      hide empties, zero focusable elements, bundled Source Sans 3. Media blanking is not
      exercised there (same fixture gap as TB/SIM).
- [x] Green — build `/obs/source/overlay` as a state-driven caption renderer.
- [x] Red — projector adoption E2E (in `tests/e2e/test_obs_dock.py`): `?service` adoption
      and mid-run adoption without navigation. Fonts and balance are pinned by
      `test_obs_dock.BundledTypefacesTest` plus the live measurements in the spec.
- [x] Green — projector adoption + `text-wrap: balance` + the font stack swap.
- [x] Bundle the display faces with CMG Sans Bold and Source Sans 3 plus their licence
      texts under `static/assets/fonts/` (beside `gkps.png`); add the `@font-face` rules in
      `fonts.css`; verify both load without machine installs.
- [x] Update the service page button: opens `/projector?service=<id>`, Stop project
      becomes a release.
- [x] Run targeted Django tests and focused browser E2E classes locally (87 unit tests,
      6 browser scenarios); the full suite and browser matrix run in CI after push.
- [x] Fill Traceability in `spec.md` with final paths.
- [x] In the same implementation PR, move ITEM-119 to review, bump VERSION once (minor →
      1.20.0), add the changelog, and fill `release_version`. **Done** waits for the merge.
- [x] Conventional Commit and draft PR to develop linking this spec.
- [ ] Verify exact-head CI before merge.
- [ ] Move ITEM-119 and the board to Done after the merge.

## Open

- TB/SIM flip, song bait grouping and chips, and media blanking on the overlay have code
  paths and unit coverage but no browser test yet: they need fixtures with a two-edition
  passage, a song with baits, and a media entry. A follow-up slice should add them.

## Done when

- [x] All acceptance scenarios in `spec.md` hold that the local fixtures can exercise.
- [x] Tests named above are green.
- [x] Board, tasks, and version are complete in this PR.
