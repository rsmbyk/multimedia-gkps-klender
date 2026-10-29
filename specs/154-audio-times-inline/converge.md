# Converge: an audio preview reads its times as `current / total`

**Spec**: `specs/154-audio-times-inline/spec.md` · **Date**: 2026-10-29

## Pass 1

Every row of `plan.md`'s traceability table was re-assessed by the method it declares, whatever its task
checkbox says (SDD-22). What was checked, and with what evidence:

**Test rows (8).** `manage.py test tests.e2e.test_audio_display --noinput --keepdb` on the branch: 6 cases,
5 pass, and `test_preview_times_read_current_over_total_beside_the_bar` is one of the five — the text
matches `^\d+:\d\d\s*/\s*\d+:\d\d$` and the helper's five geometry assertions hold before and after `Space`
+ `fill('1')`. The sixth case, `test_untitled_preview_and_projector_idle_display_off`, fails — and fails
identically on unmodified `develop` (re-run at `24a6d6d2`, `AssertionError: Locator expected to have
attribute 'false'` on the projector's `data-showing`), which is ITEM-140, a card already on the board. It
is not this slice's.

**Inspection rows (5).** `git diff` on the branch touches two product lines —
`multimedia/web/templates/reading/tatib.html:56` and `static/styles/design/components.css:2134`. Neither
`multimedia/web/templates/reading/projector.html` nor `static/styles/design/projector.css` appears in it,
so the projector's line keeps its font size, colour, margin and alignment (US2-S2), and reading the two
times lines side by side shows the same order and the same `/` (US2-S1). `static/web/media-audio.js` also
does not appear, so `clock()` is untouched and never wraps minutes (E2). The before/after probe table in
spec §UI/UX lists every other box — dialog 620×125, player 568×69, seek 504×14 at y 445.5, line at y 466.5
— with the same values on both sides (FR-004, SC-004).

**Manual rows (5).** Measured on the live preview (`http://localhost:8814/tatib/144/`, entry `e1`), not
recalled: idle `0:00 / 5:02` with the pair at x 941.9→1004 and the bar's right edge at 1004 (SC-001,
SC-002); playing `0:01 / 5:02` with the pair's box unmoved; ended `5:02 / 5:02`; dark — `var(--head-ink)`
= rgb(156, 154, 145); 420×820 — dialog 382px at x 19, bar x 103→381, pair x 318.9→381, 232px clear of the
play button (E1, E4, E5).

**Findings: none.** No `missing`, `partial`, `contradicts` or `unrequested` gap was found: the two product
lines are the whole behaviour change, and each row's declared method confirms its statement. The four LOW
findings in `analysis.md` stand as accepted, not as gaps.

**Outcome**: converged on pass 1. Passes used: 1 of 3.
