# Implementation Plan: the preview's verse tabs get their own row

**Spec**: `specs/153-preview-tabs-row/spec.md`
**Branch**: `fix/153-preview-tabs-row`
**Bump**: `patch` — 1.22.10 → 1.22.11 (the level is declared here; the number is stamped against
`develop` in the pre-merge commit, after the sibling slices in flight)
**Preview**: `static preview at specs/153-preview-tabs-row/preview/preview.html`

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | ES5 in `static/web/preview.js`; CSS in `static/styles/design/components.css`; a Django template for the dialog's skeleton; Playwright (Python) for the acceptance tests |
| Primary dependencies | none added |
| Storage | none — the dialog is built from the pane's payload on every open |
| Testing | `tests/e2e/test_entry_preview.py`: seven new cases, two existing cases' locators moved, the rest unchanged |
| Target platform | every browser the app supports; `:has()` is already used by the product |
| Project type | server-rendered Django app, vanilla JS, no build step |
| Performance goals | none; one re-parented node and one focus call |
| Constraints | no payload, endpoint, copy or ARIA-contract change; every preview without verse tabs pixel-identical; the three moved locators keep their assertions |
| Scale / scope | one template div, ~10 CSS lines, ~20 JS lines, seven E2E cases, one board card |

## Constitution Check

No `CONSTITUTION.md` exists (SDD-01: optional, never auto-created), so the check does not apply. The
constraint row above stands in its place.

Re-checked after Phase 1: pass — no new file, no new state, no new dependency.

## Phase 0 — Research

See `research.md`. Five decisions, each measured in the preview or read in the code it names: the focus
target is the scroller (D001), the rule falls below the tab band (D002), `:has()` carries it (D003), the
keyboard loop stops at body ↔ selected tab (D004), and the tests move three locators plus four claims
(D005). **Unknowns remaining: 0.**

## Phase 1 — Design

- `data-model.md` — the dialog's DOM and the three invariants this slice creates.
- `contracts/` — `none` (`contracts/none.md`): no interface changes.
- `quickstart.md` — the DB-isolated command, the module, the preview probe, and the live check.

### The design

**Template** — `multimedia/web/templates/reading/_preview_modal.html`: the tab host leaves the head and
follows it.

```html
  <div class="preview__head" data-preview-head hidden>
    <span class="preview__title" id="previewTitle"></span>
  </div>
  <div class="preview__versetabs" data-preview-tabs-host hidden></div>
  <div class="preview__body" id="previewContent" tabindex="0"></div>
```

**CSS** — `static/styles/design/components.css`, the preview block at `:2076`:

```css
.preview__versetabs {
  display: flex; margin: 0; width: 100%; padding: 0 22px 14px;
  border-bottom: 1px solid var(--divider); background: var(--canvas);
}
.preview__head:has(+ .preview__versetabs:not([hidden])) { border-bottom: 0; }
.preview__versetabs .preview__tabs { margin: 0; }          /* was .preview__head .preview__tabs */
@media (max-width: 560px) {
  .preview__head { padding: 12px 16px; }                   /* flex-wrap drops with the tabs */
  .preview__versetabs { padding: 0 16px 12px; }
}
```

- `margin: 0` on the band is load-bearing: as a column-flex item, the old `margin-left: auto` would shrink
  it to `max-content` and push it to the dialog's right edge (measured in the preview before the fix).
- The `[hidden]` rule already in the file outranks the band's `display: flex`, so an entry with no tabs
  draws nothing.

**Script** — `static/web/preview.js`:

1. `liftIdentity()` (`:324`): `head.hidden = !identity; tabsHost.hidden = !tabs;` — the two independent.
2. The open handler (`:509`): `content.focus({ preventScroll: true })` after the dialog is shown, so the
   scroller takes the dialog's first focus however the tabs are arranged.
3. The dialog's keydown handler (`:571`): the two-step loop, before the confirm layer's own Tab handling —
   `Tab` on the body focuses the selected tab, `Shift+Tab` on it returns to the body; guarded by a visible
   tab band and `footer.hidden`, so no other preview's order changes.

**Tests** — `tests/e2e/test_entry_preview.py`:

- `test_a_song_preview_tabs_between_its_verses` and `test_a_song_preview_verse_tabs_keep_equal_circles_and_scroll`
  reach the tabs through `.preview__versetabs .preview__tab` instead of `.preview__head .preview__tab`;
  every assertion they carry stays.
- New, seven cases: the long title's width; the tab row under the header; one rule under the tabs; the
  passage's unchanged box and rule; the pointer-open focus; the keyboard-open focus; the Tab loop.

**What is deliberately not done.** No focus trap for the whole dialog (D004), no change to `wireTabs`, the
payload, the screen-break footer, or any other preview kind's styling. No `tabindex` is added to the
`<dialog>`.

## Traceability

| Requirement / scenario | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| FR-001 the tab row is a sibling of the title band | `reading/_preview_modal.html`; `preview.js:324` | `test` → `tests/e2e/test_entry_preview.py::EntryPreviewE2ETests::test_a_song_preview_puts_its_verse_tabs_under_the_header` | asserts `head.contains(tabsHost)` is false and the tab host is the head's next sibling |
| FR-002 the title takes the header's full content width | `components.css` (`.preview__title` unchanged; the row no longer holds the tabs) | `test` → `…::test_a_song_preview_gives_its_long_title_the_header_width` | title box = head width − 44px, ellipsized from a longer string |
| FR-003 one rule, below the tabs; today's rule without tabs | `components.css` (`:has(+)`); `.preview__versetabs` | `test` → `…::test_a_song_preview_draws_one_header_rule_below_the_tabs`, `…::test_a_passage_preview_keeps_its_header_box_and_rule` | computed `border-bottom-width` on both bands |
| FR-004 the body takes the dialog's first focus | `preview.js:509` | `test` → `…::test_a_song_preview_opens_with_the_body_focused`, `…::test_a_song_preview_opened_by_keyboard_focuses_the_body` | `document.activeElement.id === 'previewContent'`; no `.preview__tab` focus-visible |
| FR-005 a preview without tabs is unchanged | `reading/_preview_modal.html`; `components.css` | `test` → `…::test_a_passage_preview_keeps_its_header_box_and_rule`, plus the module's existing passage/text/image cases | 704×52 header and body at 52px at 1440 |
| FR-006 the tab row keeps its circles, gap and scroll | `components.css` (`.preview__tabs`, `.preview__tab` untouched) | `test` → `…::test_a_song_preview_verse_tabs_keep_equal_circles_and_scroll` | 12 tabs at 390px: 30×30, 50%, scrollWidth > clientWidth |
| FR-007 the two-step keyboard loop | `preview.js:571` | `test` → `…::test_tab_from_the_body_reaches_the_selected_verse_tab` | body → Tab → selected tab → Shift+Tab → body |
| US1 AC1 the long title is not squeezed | as FR-002 | `test` → the title-width case | 569.6 → 660px at a 704px dialog |
| US1 AC2 the tab row is not a child and starts at 52px | as FR-001 | `test` → the under-the-header case | tab row top = dialog top + 52 |
| US1 AC3 a short title keeps the same row | `components.css` | `inspection` — the band's padding does not depend on the title | the preview's `After` column with a title that fits |
| US2 AC1 one rule below the tabs | as FR-003 | `test` → the rule case | head 0px, band 1px |
| US2 AC2 14px and 22px gaps | `components.css` | `test` → the rule case measures the tab row's bottom to the band's rule and the rule to the first line | 14px band padding + 1px rule; body's 22px |
| US2 AC3 no empty band without tabs | `reading/_preview_modal.html` + `:has` | `test` → the passage case | band `hidden`, head keeps its rule |
| US3 AC1 pointer open focuses the body | as FR-004 | `test` → the pointer case | no ring in this Chromium; the assertion is the focus target |
| US3 AC2 keyboard open focuses the body, ring on the body | as FR-004 | `test` → the keyboard case | `:focus-visible` true on the body, false on every tab |
| US3 AC3 a passage still focuses the body | `preview.js:509` | `test` → the module's existing passage case (`…::test_a_passage_preview_shows_its_reference_and_full_text`) | unchanged behaviour |
| US3 AC4 Tab reaches the selected tab | as FR-007 | `test` → the Tab-loop case | |
| Edge: twelve tabs at 358px | `components.css` | `test` → the 12-tab case at 390px | unchanged rules |
| Edge: an untitled text hides both bands | `preview.js:324` | `test` → `…::test_an_untitled_text_preview_has_no_header` | head hidden, band hidden |
| Edge: a song with one verse | `tatib.html` payload | `inspection` — the payload emits no `.preview__tabs`; the band stays hidden | no tabs, 52px head |
| Edge: dark theme | `components.css` tokens | `inspection` — the preview's `Dark` toggle; `--divider` `#3A362F`, numbers unchanged | |
| Edge: re-opened while open | `preview.js:509` | `inspection` — the focus call runs on every open, `preventScroll` keeps the body's position | |
| SC-001 title 569.6 → 660px | the preview page | `manual` — `specs/153-preview-tabs-row/preview/probe.py`, and the worktree page | numbers recorded in the spec |
| SC-002 tab row 14 → 52px, first tab 22px | the preview page | `manual` — `probe.py` | |
| SC-003 focus on the body, by pointer and keyboard | the worktree page | `test` → the two focus cases | |
| SC-004 a passage unchanged | the module | `test` → the passage case | 704×52 / 52px |
| SC-005 first lyric line 22px under the rule | `components.css` | `test` → the rule case | |
| SC-006 Tab: body → selected tab → body | `preview.js:571` | `test` → the Tab-loop case | |

**Verification split: 22 test · 4 inspection · 2 manual.**

## Plan exit gate

| Check | Result |
| --- | --- |
| Requirement coverage | FR-001…FR-007 each carry a row; every SC and every story scenario is mapped |
| Entity coverage | the dialog's DOM and its three invariants are in `data-model.md`; no entity added |
| Interface coverage | `contracts/none.md` states `none` and why |
| Decision provenance | D001–D005 in `research.md`, each with its measurement or code read |
| Constitution conformance | no constitution exists (SDD-01); the constraint row is honoured |
| Zero unknowns | 0 |
| Verification declared | 22 `test` · 4 `inspection` · 2 `manual` |
| `quickstart.md` runnable | yes — the module runs on this worktree against a throwaway database; the two `manual` rows are the preview probe (static, runnable now) and the post-merge live page |

## Complexity Tracking

| Violation | Why needed | Simpler alternative rejected because |
| --- | --- | --- |
| — | — | — |

## Project Structure

### Documentation

```
specs/153-preview-tabs-row/
  spec.md  plan.md  research.md  data-model.md  quickstart.md  tasks.md  analysis.md  converge.md  fold.md
  contracts/none.md  checklists/requirements.md
  preview/{preview.html,build_preview.py,probe.py,README.md,assets/}
```

### Source

```
multimedia/web/templates/reading/_preview_modal.html   the tab host leaves the head
static/styles/design/components.css                    the tab band, the :has() rule, the mobile padding
static/web/preview.js                                  liftIdentity, the focus call, the Tab loop
tests/e2e/test_entry_preview.py                        two locators moved, six cases added
docs/spec/reading.md                                   R27 at Fold
backlog/items/ITEM-162-preview-tabs-row.md             card
backlog/board.md                                       the card's row
specs/README.md                                         the spec's index row, at Accept
VERSION, CHANGELOG.md                                  patch bump and one line, at delivery
```

### Structure Decision

No new file in the product: the dialog's skeleton already owns both bands, the stylesheet already owns the
preview block, and the module that lifts the identity is the module that opens the dialog.
