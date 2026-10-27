# Research: a reading page's text wraps at its pane

**Slice**: `specs/137-reading-text-wrap` · **Date**: 2026-10-27
**Exit**: zero unknowns.

## D1 — `overflow-wrap: break-word`, not `anywhere`

**Decision.** The reading surfaces declare `overflow-wrap: break-word`.

**Rationale.** Both values break an unbreakable run at an arbitrary point when no normal break
opportunity fits the line, and neither inserts a hyphen. They differ in one thing: the soft wrap
opportunities `anywhere` introduces *do* count toward min-content intrinsic size, and `break-word`'s
do not (CSS Text Level 3; MDN). The reading title is a flex item in `.read__row`, beside the TB/SIM
toggle, with `flex-wrap: wrap`. If its min-content collapses to roughly one character, the flex line
stops wrapping and the toggle stays beside a title squeezed into the leftover width — a different
layout from today's. With `break-word`, min-content is unchanged, so the flex line wraps exactly as
it does now and the run breaks only because the line box is narrower than the word.

**Alternatives.** `anywhere` — changes the title's min-content and with it the header's layout at
narrow widths; rejected on measurement (`test_the_title_keeps_its_box_and_the_toggle_its_line` is
the guard). `word-break: break-word` / `word-break: break-all` — `break-all` breaks between any two
characters of normal prose too, which is wrong for lyrics; `word-break: break-word` is a deprecated
alias for this same behaviour. `hyphens: auto` — needs a dictionary for Simalungun and Indonesian and
inserts hyphens the design does not want. A server-side truncation — cannot know the pane's width,
and the report asks for wrapping, not a cut.

**Provenance.** MDN `overflow-wrap` (fetched 2026-10-27): *"`break-word` — the same as `anywhere`,
with normally unbreakable words allowed to be broken at arbitrary points … but soft wrap
opportunities introduced by the word break are NOT considered when calculating min-content intrinsic
sizes"*; CSS Text Module Level 3 §overflow-wrap-property, which MDN cites. Measured here: the title's
box is 400px at 1440×900 before and after, and the toggle keeps its line.

## D2 — Three roots, inherited, rather than a list of elements

**Decision.** One rule on `.read`, `.search-results` and `.preview`.

**Rationale.** `overflow-wrap` is an inherited property, so a declaration on a surface's root reaches
every text run in it. That is what makes "other kind of pages" true by construction: the Bible
chapter, the song page, the songbook page, the Tata Ibadah service and the media library all render
inside `.read`, and the search page and the Preview modal are the two reading surfaces that do not.
A list of element selectors (`.read__title`, `.read__sec`, `.v`, `.tatib__tx`, …) would be one
omission away from the bug coming back on a surface nobody listed — and the surfaces are named on
the *root*, which is the entity the spec's FR-009 names.

**Alternatives.** A selector list per element — rejected: fragile, and the next reading element
would silently default back to `normal`. `body { overflow-wrap: break-word }` — rejected as wider
than the spec: it would reach the editor modals, the rail and the dock, which are not reading
surfaces and whose text is not the owner's request.

**Provenance.** `static/styles/design/components.css` (`.read` is the reading article in
`multimedia/web/templates/reading/base.html:405`; `.search-results` at :401; the Preview dialog in
`_preview_modal.html:3`). Measured on the preview: every surfaced spill in the spec's inventory is
inside one of the three.

## D3 — The truncating surfaces are left alone

**Decision.** No change to `.book__n`, `.media-library__filename`, `.service-media__main strong`,
`.media-transfers__main strong` or `.songrow__t`.

**Rationale.** A wrap rule only takes effect where text is allowed to wrap; those elements set
`white-space: nowrap` (one line with `text-overflow: ellipsis`) or `-webkit-line-clamp` (three lines
with a trailing `…`, spec 135). They keep clipping, and the spec's FR-006 says so, because those are
index shapes: a service row carries a name and a date on one line, a media row carries a name and a
size.

**Alternatives.** Unclipping the sidebar rows so a long service name wraps there too — not the
report, and it would change the list's row heights, which spec 132's date buckets and the scroll
position depend on.

**Provenance.** `components.css:948` (`.book__n`), `:626` (`.media-library__filename`), `:1613`
(`.songrow__t`); the measured proof in `preview/probe_wrap.py`: `.book__n` still hides 281px inside a
293px row, one line, both before and after.

## D4 — No markup, view or model change

**Decision.** The slice touches `components.css` and adds one test module.

**Rationale.** Every page already sends the text it draws; the browser, not the server, decides where
a line breaks. Adding a class or an element would change nothing the CSS cannot reach and would put
a presentation detail in templates that mirror it (`tatib.html`, `bible.html`, `song.html`,
`_toc.html`, `search.html`) — five places to keep in step for no gain.

**Alternatives.** A template filter that pre-wraps the string — rejected: the same text is drawn at
four widths and in the Preview modal, so any fixed break is wrong somewhere.

**Provenance.** `specs/137-reading-text-wrap/spec.md` FR-008/FR-009; the served HTML of
`/tatib/149/`, which already carries the whole title in one span.

## D5 — Verification is geometry, not a screenshot

**Decision.** Each test measures the painted text with `Range.getClientRects()` against the box that
owns it, plus `document.scrollWidth` against `clientWidth`, at more than one viewport.

**Rationale.** "Overflow" is not a style — it is a relationship between a text run and its box, and
the same rule can leave one surface correct and another wrong. The measurement also distinguishes
overflow from deliberate clipping, which a screenshot cannot: the sidebar row *is* painted past its
box and *is* clipped by `overflow: hidden`, which is correct, while the title is painted past its box
and is not clipped, which is the bug. The E2E layer is the repository's user-visible acceptance
layer (`tests/e2e/`, Playwright through `StaticLiveServerTestCase`).

**Alternatives.** A CSS assertion alone (`expect(...).to_have_css('overflow-wrap', 'break-word')`) —
proves the declaration, not the outcome; kept only as an extra assertion in FR-009's test. A pixel
comparison — the repository already uses one (`tests/e2e/test_reading.py` scrollbar checks), but it
is brittle across fonts and platforms; geometry is the honest measure here.

**Provenance.** `tests/e2e/test_song_label_typography.py:82` (`scrollWidth <= clientWidth`),
`tests/e2e/test_reading.py` (the same pattern for panel rows); the probe already written in
`preview/probe_wrap.py`.

## Unknowns

None. Every question the plan needed answered — which value, which roots, what to leave alone,
whether markup changes, how to verify — is decided above with a source or a measurement.
