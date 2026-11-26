# Static preview — spec 243

## Current: v14 (placeholder aligned to stage padding)

`index.html` keeps v13's three layout-matched placeholders but applies the
real `.stage` padding to the placeholder box: `var(--stage-pad-top)` and
`clamp(24px, 5vw, 64px)` horizontally, with 18px at ≤720px. Measured at 1440px,
the placeholder `.read` and its header now start at x=520, y=218 — exactly the
same as the real `.read`, instead of the stage corner at x=456, y=178. Layout
anatomy, dim-only lock, bars and v1–v13 references are unchanged.
`build14.py` / `probe14.py` build and measure; `grid-v14.png` is the contact
sheet. Chat-frame verifier PASS (1,173 rules, zero external resources).

## Earlier: v13 (layout-matched placeholders)

`index.html` replaces the generic placeholder with three skeletons built from
the real stage markup: Bible uses `read__head` / `read__title` / `read__lang` /
`read__ed` / `read__sec` / `p.v` with `v__n` verse numbers; song uses the same
anatomy with `HAL n` eyebrow, song title and three-line verse bars; Tata Ibadah
uses `read__eyebrow`, `entry__start` add buttons and `tatib__item` / `read__sec`
/ `read__sub` rows. Known sidebar data seeds the title, number and eyebrow.
Measured: bible 5 verse rows, song 3 verse rows, service 3 entry rows, all with
real `read__head` and `read__body`. v1–v12 remain in the reference row.
`build13.py` / `probe13.py` build and measure; `grid-v13.png` is the contact
sheet. Chat-frame verifier PASS (1,172 rules, zero external resources).

## Earlier: v12 (leaf stand-ins moved out of the sidebar)

`index.html` keeps v11's top-edge bars and dim-only lock. The song / verse /
service stand-in rows that used to sit above the chapter list are now in a
labelled **Clicked leaf** row in the preview toolbar, so the second-level
sidebar starts cleanly with its own header and numbers. Their selectors and
dim-only state are unchanged. `build12.py` / `probe12.py` build and measure;
`grid-v12.png` is the contact sheet. Chat-frame verifier PASS (1,166 rules,
zero external resources).

## Earlier: v11 (bars at the very top edge)

`index.html` keeps R4 but moves the first- and second-level bars from the top
of their scroll bodies to the very top edge of the `.panel` / `.chapters`
asides. Measured bar-to-parent top offset is 0px for all three bars. The
reading page bar was already at 0px. Dim-only lock, write classification,
cancellation rules and v1–v10 references are unchanged. `build11.py` /
`probe11.py` build and measure; `grid-v11.png` is the contact sheet.
Chat-frame verifier PASS (1,161 rules, zero external resources).

## Earlier: v10 (bars follow the updated section)

`index.html` now draws a 3px bar at the top of the section a fetch will update:
rail click → first- and second-level bars; chapter/songbook click → second-level
bar; song/verse/service click → reading-page bar (unchanged). The reading page
keeps its old content on list-only clicks. Dim-only lock and all cancellation
rules remain. v1–v9 stay as thumbnails/links. `build10.py` / `probe10.py` build
and measure; `grid-v10.png` is the contact sheet. Chat-frame verifier PASS
(1,161 rules, zero external resources). R4 in `rules-v5-draft.md` records the
rule.

## Earlier: v9 (dim-only lock)

`index.html` now uses **dim only** for the clicked item: the rail icon stays
visible at 0.45 opacity, sidebar rows dim to 0.58, and there is no spinner,
label, edge fill or ring. The stage rules are unchanged — list-only clicks keep
the reading page as displayed; song, verse/passage and service clicks disable
it, show the bar above it and seed the placeholder. v1–v8 remain as thumbnails
and links in the **Previous** row. `build9.py` / `probe9.py` build and measure;
`grid-v9.png` is the contact sheet. Chat-frame verifier PASS (1,157 rules, zero
external resources). The decision is recorded in `rules-v5-draft.md`.

## Earlier: v8 (spinner alternatives)

`index.html` is rewired to the confirmed rule: **rail, chapter-number list and
songbook are list-only** — the item locks but the stage keeps whatever it shows.
Only **song, verse/passage and service** write to the reading page and get the
disabled stage, bar above it and sidebar-seeded placeholder. The cancellation
scenarios now use those classes too. The three row variants and v1–v6 reference
thumbnails remain. `build7.py` / `probe7.py` build and measure; `grid-v7.png` is
the contact sheet. Chat-frame verifier PASS (1,144 rules, zero external
resources). `rules-v5-draft.md` records the correction and confirmation.

## Earlier: v6 (list-only fetches leave the page alone)

`index.html` now adds explicit **Rail list only** and **Sidebar list only**
scenarios: the clicked rail/sidebar item locks, but `aria-busy` is absent from
the stage, the bar and placeholder stay hidden, and the reading content keeps
whatever it was displaying. Stage-changing scenarios still disable the page and
seed the placeholder from sidebar data; cancellation scenarios and the three
row variants are unchanged. `rules-v5-draft.md` carries the refined R2 text.
`build6.py` / `probe6.py` build and measure it, `grid-v6.png` is the contact
sheet. Chat-frame verifier PASS (1,140 rules, zero external resources).

## Earlier: v5 (owner rules)

`index.html` is now the v5 preview: the clicked rail/sidebar item locks (rail
icon swaps to a spinner; three sidebar-row variants A/B/C are selectable), a
stage-changing fetch disables the reading page, shows a bar above it and a
placeholder prefilled from the sidebar, and six scenarios demonstrate both
cancellation rules. The three earlier approaches remain as thumbnails/links in
the page's **Previous** row. Rules are drafted in `rules-v5-draft.md`;
`build5.py` / `probe5.py` build and measure it, `grid-v5.png` is the contact
sheet. Chat-frame verifier PASS (1,140 rules, zero external resources).

## Earlier: v4 (optimistic selection)

`index.html` is a self-contained page built from the real `/bible/1/1/` shell:
the body markup comes from `source.html` (fetched from the local dev server),
and `tokens.css`, `components.css` and `generate.css` are the project's own
stylesheets inlined by `build4.py`. No external subresources; it opens directly
in a browser or in the chat frame.

**Static comparison, not shipped code.** The three earlier approaches are kept
on the page itself as a reference strip with thumbnails that link to their
full files, and as separate files:

- `index-v1.html` — four signs: top bar, row spinner, stage overlay, toast.
- `index-v2.html` — global bar + solid/dashed source marks + queued click.
- `index-v3.html` — quiet strip / skeleton / placeholder child rows.
- `index.html` (this file) — approach D below.
- `loading-patterns-research.md` — the cited reasoning behind the change.

## Approach D — the click itself is the feedback

No bar, spinner, skeleton, dim or disabled control. The existing `aria-current`
selection moves to the target **at 0 ms**, so the operator sees the click land.
The old reading body stays on screen until the fetched page is ready.

- **Prefetched hit (fast):** title follows at 200 ms. No loading text at all.
  This is the path a hover/focus prefetch should make dominant; the preview
  models it with the **Prefetched hit** button.
- **Slow miss:** at 300 ms a quiet `Opening…` appears inside the existing
  title band (a dot plus label in `--head-ink`), not a new overlay. The title
  and body follow at 2.4 s.
- **Failure (not simulated here):** revert the optimistic selection and use
  the existing failure toast.
- Accessibility: the `role="status"` live region announces `Opening <name>`
  at click time and `<name> opened` at settlement; no focus move.

The toolbar offers three click sources — rail tile, first-level row and
second-level row — and clicking the real rail/rows in the shell also works.

## Why this is a different approach

The first three rounds all added a *loading artifact* somewhere in the UI. This
one tries to remove the wait from the common path instead: prefetch on
hover/focus, move the selection optimistically, and use only one line of text
in an existing band when a miss is slow. It follows GitHub's "stream structure
before content" and the local-first/optimistic approach recorded in the
research note; it does not depend on a new indicator being liked.

## Verify

`probe4.py` measured six combinations at 1440×900. At 80 ms the target alone
carried `aria-current` (one item per list); the title was still the old one and
`Opening…` was hidden. At 440 ms the slow path showed `Opening…` and the fast
path had already settled to the new title. After 2.4 s every path had the new
title and no notice. `verify-chat-preview-frame.py --width 900` passed: 888
elements, 1 stylesheet / 1,114 rules, 1 script, zero external subresources.

Rebuild: `python3 preview/build4.py`, then
`~/Projects/multimedia-gkps-klender/.venv/bin/python preview/probe4.py`.
`grid-v4.png` is the 3×2 contact sheet. App code, spec and board remain
untouched.
