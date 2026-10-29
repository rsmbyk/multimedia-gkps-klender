# Implementation Plan: a passage and a song carry their own kind mark

**Slice**: `specs/144-passage-song-icons` · **Branch**: `feat/144-passage-song-icons` · **Bump**: `patch` (1.22.8 → 1.22.9)
**Spec**: [`spec.md`](./spec.md) · **Research**: [`research.md`](./research.md)
**Data model**: [`data-model.md`](./data-model.md) — none, no migration
**Contract**: [`contracts/stage-markup.md`](./contracts/stage-markup.md)
**Quickstart**: [`quickstart.md`](./quickstart.md)

## Technical context

| | |
| --- | --- |
| Language / runtime | Python 3.12, Django 4.0 templates; no JavaScript added |
| Surface | `multimedia/web/templates/reading/tatib.html` (stage row), `static/styles/design/components.css` |
| Data | none — `kind` already reaches the template (see `data-model.md`) |
| Verification | Playwright (Python) E2E, new module `tests/e2e/test_stage_kind_marks.py` |
| Scale / performance | one extra inline SVG per marked row; the fixture service draws 5 |
| Constraints | specs 055/140/143 fix the row geometry; spec 137 requires titles to wrap rather than overflow |

## Constitution Check

`CONSTITUTION.md` does not exist in this repository and SDD-01 forbids creating it implicitly, so there
is nothing to check against. **No violations, no Complexity Tracking table.**

The repo-level rules that do bind this slice:

- **TDD** — the E2E is written first and must fail for the right reason (the mark is absent) before the
  template change lands.
- **One slice, one branch** — `feat/144-passage-song-icons`, this worktree only; `develop` untouched.
- **No behaviour change beyond the spec** — FR-008 keeps the sidebar and the dock out.

## Phase 0 exit

`research.md` answers D1–D8 with provenance; **zero unknowns**. No research question needed the owner —
the one open question at gate 1 (which mark) was answered there and is recorded in `spec.md`'s
Clarifications.

## Phase 1 exit

- `data-model.md` — states none, with the keys the mark reads.
- `contracts/stage-markup.md` — the DOM, the geometry and the test hooks; no external interface to
  declare.
- `quickstart.md` — server, test and preview commands, all runnable today.

## Design

**Template** (`tatib.html:143`) — one element, added inside the heading:

```django
{% if item.kind == 'scripture' or item.kind == 'song' %}<span class="entry__kind-icon" aria-hidden="true" data-kind-icon="{{ item.kind }}">{% if item.kind == 'scripture' %}<svg …open book…></svg>{% else %}<svg …flagged note…></svg>{% endif %}</span>{% endif %}
```

and one class on the section, beside the existing `tatib__item--media`:

```django
{% if item.kind == 'scripture' or item.kind == 'song' %} tatib__item--{{ item.kind }}{% endif %}
```

**Stylesheet** (`components.css`, beside the media chip's rules at 2008–2033):

```css
.tatib__item--scripture, .tatib__item--song { padding-left: 64px; }   /* the media row's column */
.entry__kind-icon {
  position: absolute; left: 24px; top: 50%; transform: translateY(-50%);
  width: 20px; height: 20px; display: grid; place-items: center; color: var(--head-ink);
}
.entry__kind-icon svg { width: 100%; height: 100%; fill: none; stroke: currentColor;
  stroke-width: 1.8; stroke-linecap: round; stroke-linejoin: round; }
```

`left: 24px` is the chip's centre line minus half the glyph: `13 + 42/2 − 20/2`.

**Nothing else.** No script, no view, no model, no serializer, no migration, no new asset.

## Traceability

| Row | Requirement / scenario | Component | Verified by |
| --- | --- | --- | --- |
| FR-001 | a passage row paints a passage mark | `tatib.html` mark + `--scripture` class | test — `test_a_passage_row_carries_the_passage_mark` |
| FR-002 | a song row paints a different song mark | same, `--song` | test — `test_a_song_row_carries_the_song_mark` |
| FR-003 | distinguishable from the media chip by size + one more property | `.entry__kind-icon` vs `.entry__media-icon` | test — `test_the_mark_is_not_a_media_chip` |
| FR-004 | a text entry is not marked | the template's kind test | test — `test_a_text_row_carries_no_mark` |
| FR-005 | no height added of its own; declared wraps only | `.tatib__item--acts` padding + absolute mark | test — `test_a_passage_row_keeps_its_56px_box` |
| FR-006 | `aria-hidden`, no text, no focus stop | the mark element | test — `test_the_mark_is_decorative` |
| FR-007 | legible on the hover fill, both themes | `--head-ink` | test — `test_the_mark_holds_contrast_in_both_themes` |
| FR-008 | sidebar and dock unmarked | `_tatib_panel.html`, `obs-dock.js` | test — `test_the_sidebar_and_dock_keep_their_own_rows` |
| SC-001 | passage and song rows marked, text and break not | stage markup | test — `test_only_passage_and_song_rows_are_marked` |
| SC-002 | the marks differ from the chip in size, fill and colour | computed styles | test — `test_the_mark_is_not_a_media_chip` |
| SC-003 | nothing moves | every `.tatib__item`'s top + scroll height | test — `test_no_other_block_moves` |
| SC-004 | row boxes: passage 56px, media 80px | computed boxes | test — `test_a_passage_row_keeps_its_56px_box` |
| SC-005 | accessible name unchanged | `aria-hidden`, no text | test — `test_the_mark_is_decorative` |
| US1.1 | passage glyph is drawn | stage | test — `test_a_passage_row_carries_the_passage_mark` |
| US1.2 | song glyph differs from the passage's | `data-kind-icon` + path data | test — `test_a_song_row_carries_the_song_mark` |
| US1.3 | the two are told apart without reading | whole stage | manual — open `/tatib/144/`, look at the first two blocks |
| US2.1 | the chip reads heavier than the mark | whole stage | manual — same page, compare the chip's weight |
| US2.2 | song mark vs audio chip differ by more than outline | computed styles | test — `test_the_mark_is_not_a_media_chip` |
| US3.1 | a passage row's box stays 56px, first line centred | box + `padding-top` | test — `test_a_passage_row_keeps_its_56px_box` |
| US3.2 | a song row grows only by its declared wrap | box heights of the four songs | test — `test_the_declared_wraps_at_the_400px_pane` |
| US3.3 | mark legible on hover | computed colour on the hover fill | test — `test_the_mark_holds_contrast_in_both_themes` |
| US3.4 | nothing animates | no `transition` on the mark | inspection — `components.css`, the mark's rule block |

**Verification split: 19 test · 1 inspection · 2 manual** — 22 rows, one method each.

## Risks and their owners

| risk | mitigation |
| --- | --- |
| the mark takes the section's `:first-child` seat and gives the heading its 30px margin back | research D1 — the mark is the heading's child; the E2E's 56px assertion fails loudly if it regresses |
| a song title wraps where it did not, and an unrelated test measures its height | the spec declares the wrap set and the E2E pins the four fixture songs; `test_text_wrap` only asserts no horizontal overflow |
| a future rule keyed on `> :last-child` targets the mark | the mark is inside the heading, so the section's last child is still the controls |
| the glyph reads as a media chip at a glance | `manual` US1.3 / US2.1 at gate 2's live page, plus the measured size and colour difference |

## Exit gate

- [x] Requirement coverage — every FR-001…008 has a row above
- [x] Entity coverage — `data-model.md` states none, with the keys read
- [x] Interface coverage — `contracts/stage-markup.md` (no external interface, stated)
- [x] Decision provenance — `research.md` D1–D8 each name a source
- [x] Constitution conformance — no `CONSTITUTION.md`, recorded
- [x] Zero unknowns — no marker in `spec.md`
- [x] Verification declared — 19 test · 1 inspection · 2 manual
- [x] `quickstart.md` runnable — its server and test commands were run for this slice's preview
