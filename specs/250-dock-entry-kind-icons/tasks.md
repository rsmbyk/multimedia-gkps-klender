# Tasks: entry-kind icons in the OBS dock

- [x] Read the dock's header/chevron writers and the product's existing kind glyphs.
- [x] TDD: write the kind/placement and live-row E2E cases; run them red against unmodified code.
- [x] Add the four kind marks to `obs-dock.js` and append them before each chevron; leave breaks bare.
- [x] Seat `.entryicon` in `obs-dock.css`; move the trailing auto margin off the chevron; use live ink on the live row.
- [x] Run the new module and the targeted chevron/wrap/pin cases.
- [x] Measure the live page at 420×800, dark, 1× and record the numbers in `spec.md` §UI/UX.
- [x] Fold `dock/R20` into `docs/spec/dock.md` after acceptance.
- [x] Raise ITEM-266, bump `VERSION` to 1.37.6, write the changelog line and commit delivery.
