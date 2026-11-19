# Research: A long word wraps in the dock runner

**Spec**: `specs/203-dock-long-word-wrap/spec.md`
**Unknowns remaining**: 0

## D001 — Which boxes overflow, and which already wrap

- **Decision**: the slice reaches the runner's three text surfaces — `.serviceline` (the service title),
  `.entryrow__t` (every entry header shape) and `.screenerow` (a screen row inside an open block). Nothing
  else changes.
- **Rationale**: measured on the owner's own service 149 at 456×1087, dark, 1×: title spill 328px, URL entry
  header 178px, URL screen row 97px, `#runBody` scroll − client 135px. The same service's 137-character
  hyphenated filename spills 0 — hyphens are break opportunities, so only the unbroken run overflows. The
  sibling surfaces measured clean on the same service at the same width: `/tatib/149/` (`.read__title`
  computes `break-word`, `.read__sec` and `.tatib__tx` compute `anywhere`), `/projector?service=149` and
  `/obs/source/overlay` (zero spill, zero document overflow). The dock's own picker already wraps
  (`.servicerow__n { overflow-wrap: anywhere }`, spec 119).
- **Alternatives considered**: (a) only the two surfaces the request names — leaves the screen row's 97px
  and half the body's scrollbar, so the reported symptom survives; (b) one inherited rule on `.dock` — would
  reach the transport chips and the find band for no gain, and spec 137 recorded that a blanket `anywhere`
  can collapse a min-content size and move a control; (c) extending the slice to the reading page — measured
  unnecessary, `reading/R13` already holds it.
- **Provenance**: research — `preview/shots/before/measure.json` and the sibling-surface probe, both against
  the running worktree server.

## D002 — `anywhere`, not `break-word`

- **Decision**: `overflow-wrap: anywhere` on all three.
- **Rationale**: it is the dock's own convention (`.servicerow__n`). Spec 137 chose `break-word` for the
  reading page because `anywhere` collapses the min-content size, which stopped the header's flex line from
  wrapping and moved the language toggle beside a squeezed title. That trap needs a flex item whose automatic
  minimum size is still in play; every box here is either a block inside `.dock__runtitles`
  (`min-width: 0; flex: 1`) or a flex item carrying `min-width: 0` itself, so the minimum is already overridden.
  Verified rather than argued: with the rule and with its value restored to `normal`, the number column reads
  33.6px at left 18 in both, and every visible chevron reads 10px off its row's right edge and 0px off its
  centre in both.
- **Alternatives considered**: `break-word` — works here too, but would be the second convention in one file
  for no measured gain; `word-break: break-all` — breaks every word at every character, including ones that
  fit, which is not what the request asks for.
- **Provenance**: research (spec 137's recorded reason, `tests/e2e/test_text_wrap.py::test_the_title_keeps_its_box_and_the_toggle_its_line`),
  plus the before/after geometry read from the running page.

## D003 — No line clamp

- **Decision**: a wrapped header grows to as many lines as the run needs; no clamp, no ellipsis.
- **Rationale**: the same list already draws a hyphenated filename over 3–4 lines and the owner reads it that
  way today. An unbroken run gets the same treatment rather than a new cut. The request asks for wrapping.
- **Alternatives considered**: a 3-line clamp like the reading contents row (`reading/R12`) — would hide the
  tail of a filename the operator needs to tell two files apart, and would be a new behaviour rather than the
  fix asked for.
- **Provenance**: research (the owner's screenshot shows the four-line filename as the accepted state).

## D004 — The labels that declare their own cut

- **Decision**: `.nextband__label` and `.offstrip__label` keep `white-space: nowrap` + `text-overflow: ellipsis`;
  the slice adds no rule to either and pins that they stay one line.
- **Rationale**: `overflow-wrap` inherits into them but cannot wrap a `nowrap` line, so the mechanism is safe
  by construction. Both are transport geometry (spec 119), not text the operator reads in full.
- **Alternatives considered**: excluding them with `overflow-wrap: normal` — redundant, and a second
  declaration to keep in step; letting them wrap — would grow the sticky band and the off-strip.
- **Provenance**: research (the stylesheet's own declarations), pinned by
  `test_a_truncating_label_still_truncates`.

## D005 — Where the test lives, and three fixture facts that cost a red run

- **Decision**: a new module, `tests/e2e/test_dock_text_wrap.py`, on the same
  `StaticLiveServerTestCase` + Playwright harness the dock's other suites use, with spec 137's range-rect
  spill measurement and its read-the-page-twice technique.
- **Rationale**: the repo keeps per-slice E2E modules; `test_obs_dock.py` is spec 119's display-state suite
  and `test_text_wrap.py` is the reading page's. Three facts about the dock's own rendering decided the
  fixtures, each found by a failing run rather than by reading:
  1. A **hymn** song's dock label is its number alone (`BE 581`) — `views.py` builds `label` from
     `song.book_number` for a hymn book — so a long song title reaches the header only through an
     **ordinary** songbook.
  2. A song entry's screens come from `ServiceEntry.verses` (a list of verse PKs); with it empty the entry
     has no screens, no block and no chevron, so projecting it does nothing.
  3. The **NEXT band** is hidden while the live entry's own end is in view
     (`obs-dock.js`: `nextBand.hidden = liveEntry.bottom <= box.bottom + 6`), so proving its cut needs a
     live block tall enough to run past the scrollport — a song with twelve verses.
  A tall block's first screen row can also sit under the pinned live header, where a pointer hit-test never
  lands; the projection is dispatched as `test_obs_dock_follow.py` dispatches it.
- **Alternatives considered**: extending `test_text_wrap.py` with a dock class — its fixtures and its subject
  are the reading routes; a computed-style assertion alone — `overflow-wrap: anywhere` says nothing about
  where the painted text lands, which is the whole defect.
- **Provenance**: research (repo layout, `docs/PROCESS.md`'s TDD repo block) plus three failing runs.

## D006 — The bump

- **Decision**: `bump: patch`.
- **Rationale**: a visible fix to a shipped surface; no new capability, no breaking change (VER-10).
- **Alternatives considered**: `minor` — nothing new is offered; `none` — the change is user-visible and
  belongs in the changelog (VER-05).
- **Provenance**: research.

## D007 — The sequence this slice actually ran in

- **Decision**: record the deviation rather than backdate the artifacts. The CSS and the test landed
  **during Preview, before gate 1**, on the owner's correction "your preview still does not wrap": the live
  preview had been showing the shipped state with the candidate rule injected only inside the probe, which
  is not the change he asked to see.
- **Rationale**: SDD-06 wants the preview to be the screen *with the change*, and the owner judges a visual
  change on the running page. Making the preview real meant writing the declaration. TDD's red-first was
  kept inside that: the test was written and run **before** the declaration (4 failures, all the overflow
  assertions — 464px title, 314px header, 243px screen row, 2021px body), then the declaration landed, then
  the suite went green. What was skipped is the gate order, not the evidence.
- **Alternatives considered**: keeping the preview injected and asking the owner to read probe output — the
  correction he already made; reverting the CSS to re-run the stages in order — would remove the fix from
  the page he is reviewing and re-create the complaint.
- **Provenance**: owner correction (2026-11-19), and the two logged runs
  (`gkps203-red2.log` 4 failures → `gkps203-green3.log` 10 pass).

## Open

None.
