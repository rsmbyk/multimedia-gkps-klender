## What changed

Every service entry header in the OBS dock's runner now shows a small icon of its kind immediately to the left of its expand chevron. The four marks are the product's own contents-row glyphs: an open book for a passage, a flagged note for a song, a framed play mark for media, and three rules for text. A section break stays a bare hairline with neither mark nor chevron.

The mark is decorative (`aria-hidden`, no pointer) and carries the trailing margin, so the chevron keeps its place and both stay centred on the whole row even when the header wraps to four lines. The live header keeps its mark in live ink after the chevron hides, and the pinned clones inherit it from the copied header. No endpoint, schema, template or dependency changes.

## Verification

- Split: 2 test · 2 inspection · 0 manual, plus the deferred browser matrix at push.
- `tests.e2e.test_dock_entry_kind_icons`: red before the writer, green after — the four-kind placement matrix, break rows, and the live row's retained mark.
- Targeted regressions: spec 198's chevron matrix, spec 203's header wrap and spec 208's stuck header — green.
- Live probe at 420×800, dark, 1×: mark 361–377px, chevron 387–402px, 10px gap, 0px off the row centre. Wrapped rows: 3-line media 76.7px, 2-line song + Bait 77px, 4-line media 96.3px; the long song's title column loses 26px with no new wrap.
- Dock/browser matrix run at push: see the push report for the module counts and any machine-local reds.

## Records

- Board: ITEM-267.
- Spec: `specs/250-dock-entry-kind-icons/spec.md` (Accepted).
- Fold: `docs/spec/dock.md`, new `dock/R20` with three scenarios.
- Version: 1.37.7; changelog line under `## [Unreleased] → Added`.
