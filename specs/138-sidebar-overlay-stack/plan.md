# Implementation Plan: on a small screen the sidebars are a drawer stack over the page

**Slice**: `specs/138-sidebar-overlay-stack` · **Branch**: `feat/138-sidebar-overlay-stack`
**Date**: 2026-10-27 · **Status**: Draft (gate 1 accepted the spec on 2026-10-27)
**bump**: `minor` — a behaviour the product did not have (a drawer shell on small screens); no stored
value, endpoint or model changes. One `CHANGELOG.md` line under `## [Unreleased]` → `### Changed`.

## Technical Context

| | |
| --- | --- |
| Language | Python 3.12, Django 4.0 templates |
| Front end | server-rendered templates, vanilla JS, hand-written CSS; no framework, no build step |
| Files | `static/styles/design/components.css`, `multimedia/web/templates/reading/base.html`, `static/web/reading.js`; a new `tests/e2e/test_drawer_shell.py` |
| Data | no migration, no payload change: the shell's own state attributes only |
| Tests | Playwright E2E through `StaticLiveServerTestCase`, the repository's user-visible acceptance layer |
| Constraints | the desktop layout above 1272px is untouched; no new icons, fonts or dependencies; the same panel, chapter and song-list markup |

## Constitution Check

`CONSTITUTION.md` does not exist and is never auto-created (SDD-01).

- Before Phase 0: n/a — no constitution.
- After Phase 1: n/a — no constitution.

## Phase 0 — Research

`research.md` records six decisions and exits at zero unknowns:

1. the overlay is a **media query**, not a script flag: `≤1272px` in CSS, mirrored once in JS;
2. the drawers are the **existing panels**, re-positioned: `--books-w`, `--ch-w-shown` and
   `--reserve-ch` go to 0, so the stage stops being pushed without a second layout;
3. stacking is **z-order plus one transform** — the rail above the drawers, the child above its
   parent — with no second animation to keep in step;
4. the phone's toolbar is **markup in `base.html`**, and the rail's foot is *positioned* into it,
   not moved in the DOM, so the controls keep their identity and their handlers;
5. the phone's menu is the **rail itself**, re-laid out: same buttons, their names shown, logo and
   foot hidden;
6. the state machine gains one attribute (`data-rail`) and one rule (the phone never offers a
   service's contents), and Escape and the scroll lock join the existing key/`overflow` handling.

## Phase 1 — Design artifacts

- `data-model.md` — the shell's state: which attribute holds which level, and what each may be.
- `contracts/shell-state.md` — the agreement between `reading.js` and `components.css`: the four
  state attributes, who writes them, and what each one promises the stylesheet.
- `quickstart.md` — the commands that run the slice's checks.

## Design

### Stylesheet (`static/styles/design/components.css`)

At `≤1272px`:

```css
:root { --books-w: 0px; --ch-w-shown: 0px; --reserve-ch: 0px; }
.rail { z-index: 50; }                    /* above the drawers, so they slide out from under it */
.panel, .chapters {
  position: fixed; top: 0; bottom: 0; left: var(--rail-w);
  width: var(--panel-w); max-width: none;
  transform: translateX(-100%);            /* at rest, behind the rail */
}
[data-nav="open"] .panel, [data-ch="open"] .chapters { transform: none; }
[data-ch="open"] .chapters { z-index: 41; } /* covers its parent exactly */
```

At `≤720px` the same drawers take `left: 0; width: 100vw; top: var(--topbar-h)`, the toolbar is
shown, `.rail` becomes a full-width drawer (`top: var(--topbar-h)`), `.rail__logo` is hidden,
`.rail__foot` is positioned into the toolbar's right end, `.read__project-btn[data-project-open]`
is hidden, a row's `.book` becomes a two-line grid with `padding-right` clear of the edit control,
and `.row-edit` joins the existing touch exemption. The song list's `max-width: 26rem` and the
`[data-ch-mode="song"]` left pin need `!important`-free overrides by selector order.

### Template (`base.html`)

```html
<header class="topbar" aria-label="Site">
  <button id="drawerControl" class="topbar__control" type="button" data-state="menu">…</button>
  <a class="topbar__logo" href="{% url 'web-index' %}"><img …></a>
  <span class="topbar__title"></span>
  <span class="topbar__spacer"></span>
</header>
<div class="drawer-backdrop" id="drawerBackdrop" hidden></div>
```

The toolbar is in the document at every width and hidden by CSS above 720px, so the control's
handlers bind once. The rail keeps its markup; nothing moves in the DOM.

### Script (`static/web/reading.js`)

- `openRail()`, `openLevel1()`, `openLevel2()`, `closeAll()`, and `restoreLast()` keyed per section;
  `openLevel2()` refuses when the phone width meets a Tata Ibadah section.
- The control's click: open the menu when nothing is open, close everything otherwise; its glyph
  follows `anyOpen()`.
- Escape closes the stack; `document.documentElement` gets `data-drawer-open`, and the stylesheet
  locks the stage's scroll while it is set.
- A section chosen from the menu opens level 1 *over* the menu (the menu stays open underneath); a
  drawer's own back control returns one level.
- Navigating from a phone's list closes the stack after the swap.

## Traceability

| ID | Requirement / scenario | Component | Verified by |
| --- | --- | --- | --- |
| FR-001 | a drawer never changes the stage's width at ≤1272px | `components.css` overlay block | `test` — `tests/e2e/test_drawer_shell.py::test_the_stage_keeps_its_width_when_a_drawer_opens` |
| FR-002 | the second level covers its parent exactly | `[data-ch="open"] .chapters` | `test` — `test_the_second_level_covers_its_parent` |
| FR-003 | a drawer slides out from under the rail | rail z-index + resting transform | `test` — `test_a_drawer_rests_behind_the_rail` |
| FR-004 | one section's stack at a time | `reading.js` section switch | `test` — `test_only_one_sections_stack_is_open` |
| FR-005 | the backdrop closes the whole stack | `.drawer-backdrop` + `closeAll()` | `test` — `test_the_backdrop_closes_the_stack` |
| FR-006 | the rail reopens the last level | `restoreLast()` per section | `test` — `test_the_rail_reopens_the_last_level` |
| FR-007 | the phone toolbar: control, logo, theme | `base.html` `.topbar` | `test` — `test_the_phone_shows_the_toolbar_and_no_strip` |
| FR-008 | the control has two glyphs, menu and close | `syncState()` | `test` — `test_the_control_opens_and_closes_the_stack` |
| FR-009 | the control never steps back a level | same | `test` — `test_the_control_opens_and_closes_the_stack` |
| FR-010 | the phone's menu is the main menu, with names | `.rail` re-laid out | `test` — `test_the_menu_lists_the_sections_with_their_names` |
| FR-011 | the foot moves into the toolbar | `.rail__foot` positioned | `test` — `test_the_phone_shows_the_toolbar_and_no_strip` |
| FR-012 | phone drawers are the full window width | `≤720px` block | `test` — `test_the_phone_drawers_span_the_window` |
| FR-013 | the stage is unchanged by opening and closing | no layout writes | `test` — `test_the_stage_keeps_its_width_when_a_drawer_opens` |
| FR-014 | above 1272px nothing changes | the media query only | `test` — `test_the_columns_layout_is_unchanged_above_the_breakpoint` |
| FR-015 | the drawers' own back controls work at every width | `panelCollapse`, `chCollapse` | `test` — `test_each_drawers_own_back_control_steps_one_level` |
| FR-016 | a selected menu row's name takes its icon's ink | `.proto-label` → `.rail__name` | `test` — `test_a_selected_menu_row_paints_its_name_in_the_icon_ink` |
| FR-017 | the Project control is not drawn on a phone | `.read__project-btn` | `test` — `test_the_project_control_is_hidden_on_a_phone` |
| FR-018 | a service offers no contents drawer on a phone | `openLevel2()` guard | `test` — `test_a_service_offers_no_contents_drawer_on_a_phone` |
| FR-019 | a section's list slides over the menu, which stays | drawer z-order, rail kept open | `test` — `test_a_sections_list_opens_over_the_menu` |
| FR-020 | a service row on a phone opens the page and closes the stack | navigation + `closeAll()` | `test` — `test_a_service_row_on_a_phone_opens_the_page` |
| FR-021 | a row's edit control shows without hover on touch | touch media query | `test` — `test_a_rows_edit_control_shows_without_hover` |
| FR-022 | one icon size in the toolbar | `.topbar` icon rule | `test` — `test_the_toolbar_icons_share_one_size` |
| FR-023 | a phone's row stacks name over date, clear of the control | `.book` grid | `test` — `test_a_phone_row_is_two_lines` |
| SC-001 | the stage's width is identical before and after | as FR-001 | `test` — same |
| SC-002 | the two drawers' left edges and widths are equal | as FR-002 | `test` — same |
| SC-003 | the rail paints above the drawers | as FR-003 | `test` — same |
| SC-004 | one section at a time | as FR-004 | `test` — same |
| SC-005 | the backdrop closes everything | as FR-005 | `test` — same |
| SC-006 | the last level is restored | as FR-006 | `test` — same |
| SC-007 | one toolbar and no strip | as FR-007 | `test` — same |
| SC-008 | the control's two glyph states | as FR-008 | `test` — same |
| SC-009 | the menu is the main menu only | as FR-010 | `test` — same |
| SC-010 | the foot is in the toolbar | as FR-011 | `test` — same |
| US1.1–US1.4 | the drawer over the page, and the columns above | as FR-001, FR-014 | `test` — the two |
| US2.1–US2.2 | one stack; the parent survives its child closing | as FR-004, FR-015 | `test` — both |
| US3.1–US3.4 | backdrop, restore, Escape | as FR-005, FR-006 | `test` — those three, plus `test_escape_closes_the_stack` |
| US4.1–US4.6 | the toolbar, the menu, the control, the logo inert | as FR-007–FR-012 | `test` — the phone tests |
| US5.1–US5.2 | the page untouched, no scroll behind | `data-drawer-open` lock | `test` — `test_the_page_behind_a_drawer_does_not_scroll` |
| Edge: resizing across the breakpoint | media query + resize handler | `test` — `test_resizing_across_the_breakpoint_leaves_a_fitting_state` |
| Edge: the search landing | the shell without a stage page | `inspection` — the toolbar and drawers on `/` in the preview |
| Edge: navigating in place keeps the stack | `navigate()` untouched | `test` — `test_a_navigation_keeps_the_open_stack` |
| Edge: an empty second level | its own empty state | `inspection` — the empty songbook panel in the preview |
| Edge: a modal above toolbar and drawers | modal z-index | `inspection` — `.editor`/`.preview` sit at 70/80, above both |

**Verification split: 40 test · 3 inspection · 0 manual.** Untested is allowed; unverifiable is not.

## Risks

- **The page's own `[data-ch-mode="song"]` rules** pin the song list's left edge and `max-width`
  below 1272px; the overlay block must win by selector order and, where it cannot, by a more
  specific selector — the prototype needed one to get there.
- **The scroll lock** is the first time this shell stops the document scrolling; a lock that outlives
  a closed drawer would freeze the page, so it is cleared in `closeAll()` and on a resize above the
  breakpoint.
- **The control's glyph swap** re-renders an SVG path; a focus or hover state lost across it would be
  visible, so the swap only touches `innerHTML` of the `svg` and never the button.
- **Inline navigation on a phone** must close the stack *after* the swap, or the operator lands on a
  page with a drawer still over it.
