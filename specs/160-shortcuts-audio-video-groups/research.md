# Research: Audio and video name their play/pause key

**Spec**: `specs/160-shortcuts-audio-video-groups/spec.md`

Six decisions. All of them were settled by reading the code or measuring the sheet; none needed the
owner beyond the two answers gate 1 already carries.

## D001 — The change is markup in one template

**Decision**: edit `multimedia/web/templates/reading/projector_controls.html` only: delete one
`<p class="row">` from the `Display` group and append two `<section class="group">` blocks to the
second `.stack`.

**Rationale**: the sheet is static markup — `projector.js` never touches its rows, it only toggles
`body.projector.keys-open` (`static/web/projector.js:750-772`), and the Space behaviour lives in the
key handler at `static/web/projector.js:1254-1260`, which reads the media hosts, not the sheet. A
group is `h3` + `.row` paragraphs; the CSS that draws them (`.group h3`, `.row`, `.k.sp`) is already
there for every other group.

**Alternatives**: building the rows in script from a data table (rejected — the sheet has no other
dynamic part, and it would put copy in JavaScript); a new component or CSS class (rejected — the two
groups want exactly what `Song` and `Library Detour` already get).

**Provenance**: read of the template (lines 51-123) and of `projector.js:1249-1260`; the sheet's
rules at `static/styles/design/projector.css:459-560`.

## D002 — Two groups, each one row

**Decision**: `Audio` and `Video` are two `.group` sections, each holding only a `Play/Pause` row.

**Rationale**: the owner's own words — "move it to their own groups of 'Audio' and 'Video'". The
sheet already has a one-row group (`Library Detour`), so a group is not required to hold several
rows.

**Alternatives**: one `Media` group with two rows (rejected — not the words asked for); keeping the
combined row in `Display` (rejected — that is the thing being moved).

**Provenance**: owner answer at gate 1, 2026-10-29.

## D003 — The middle column, after `Library Detour`

**Decision**: append the two groups to the second `.stack`, after `Library Detour`.

**Rationale**: the sheet's height is its tallest column's natural height, and the middle column is
the shortest. Measured on the preview (`preview/preview.html`, Chromium, dpr 1):

| placement | sheet at 1920×1080 | sheet at 1280×720 (limit 688px) |
| --- | --- | --- |
| today | 676.1 × 1123.4 | 676.1 × 1123.4 |
| middle column, after `Library Detour` | 676.1 × 1094.4 | 676.1 × 1094.4 |
| third column, beside `Display` | 775.0 × 1094.4 | 688.0 tall, `scrollHeight` 753 — it scrolls |

The same two placements were measured on the running develop page before the preview existed
(676.5 × 1124 today; 775 beside `Display`; 676.5 in the middle column), so the preview and the
product agree.

**Alternatives**: beside `Display`, where the row's subject is nearest (rejected — it makes the
sheet 775px and leaves an operator on a 1280×720 canvas scrolling to reach `Fullscreen`); the top of
the middle column (rejected — it would separate `Library passage` from `Library Detour`, which are
one walkthrough); a fourth group in the first column (rejected — that column is the tallest, so any
addition there grows the sheet).

**Provenance**: `preview/measure.py` output, 2026-10-29; the live page measured before the preview.

## D004 — The label and the chord

**Decision**: each row reads `Play/Pause` and carries the sheet's existing Space cap
(`.k.sp.glyph`, `␣`, `title`/`aria-label` "Space").

**Rationale**: the group heading is the context, so the label names the action only — which is what
the removed row called it (`Audio/Video Play/Pause` → `Play/Pause`). The chord is copied verbatim so
the cap's 84 × 28px, its border, radius and shadow are the ones every other Space row uses.

**Alternatives**: `Play or Pause` or `Play/Pause (media)` (rejected — the sheet's rows never repeat
their heading, and `Show or Hide Words` shows the house style for a two-verb row is `or`, but a
toggle of one kind reads plainer as `Play/Pause`, the wording the sheet already shipped).

**Provenance**: the removed row in the template; the Space row in `Display`.

## D005 — Verified by a template test, not a new browser case

**Decision**: add one case to `multimedia/web/tests.py::ServiceProjectorTests` that reads the
rendered `/projector` HTML and asserts the sheet's groups and rows; update the one incidental
assertion in `multimedia/web/test_media.py:278`. No new E2E case.

**Rationale**: the change is markup, and the rendered response carries the sheet verbatim, so a
Django test is the same evidence a browser would give for the *content*. Behaviour (Space toggling
audio, video, words) is already covered by `tests/e2e/test_audio_display.py`,
`tests/e2e/test_video_display.py` and `tests/e2e/test_projector.py:420-462`; this slice does not
touch the handler, and those cases stay the guard.

**Alternatives**: extend `tests/e2e/test_projector.py::test_f_and_k_toggle_fullscreen_and_shortcut_sheet`
to read the sheet in the browser (deferred — the suite is heavy, carries known-red cases on develop
(ITEM-137, 139, 140, 141, 144, 153, 156, 159) and the owner's standing rule is that heavy suites run
at the push step); no test at all (rejected — SC-001 would be unverifiable).

**Provenance**: `multimedia/web/tests.py:2554` (`ServiceProjectorTests`), `test_media.py:278`,
`tests/e2e/test_audio_display.py:128-138`.

## D006 — Folding into `projector/R3`

**Decision**: Fold adds `R3` to `docs/spec/projector.md`; no new capability file.

**Rationale**: the file already owns the projector page (`R1` its Go To index, `R2` its own-response
rendering). The shortcuts sheet is the same page's durable behaviour, and a capability file holding
one requirement about a modal would be a file per surface rather than per behaviour area.

**Alternatives**: a `projector-shortcuts` capability (rejected — same page, same file's subject).

**Provenance**: `docs/spec/projector.md` (header and R1-R2), SDD-03's "one file per durable behaviour
area".

**Unknowns remaining: 0.**
