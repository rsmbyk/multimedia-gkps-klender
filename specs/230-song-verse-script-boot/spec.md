# Feature Specification: A song opened from the sidebar can edit its verses

**Slice**: `specs/230-song-verse-script-boot`
**Branch**: `fix/230-song-verse-script-boot`
**Created**: 2026-11-23
**Status**: Draft
**Input**: "when you open a song reading page from the sidebar, the Add Verse button does not work. you have to refresh the page for it to work"
**Demand**: `ITEM-245`
**Capability**: creates `reading/R55`

## User Scenarios & Testing

### US1 — The verse controls live after an in-page navigation (P1)

**Why this priority**: the public site is a search-first shell that swaps pages without a
reload. Opening a song by clicking its sidebar row therefore inserts the song's markup into
the live stage; the `Add verse` control is painted and looks active but does nothing. The only
way to edit that song's lyrics is to refresh the page, which throws away the operator's search
results, sidebar position and navigation history. Every verse control on the song page is
affected, not just Add verse: Edit is dead on the same path.

**Independent Test**: from `/` click Songs → the *Lagu* songbook → `HAL`-style song row
`/songs/1387/`, then click `Add verse`: `#editorModal` opens with `New verse` without a reload.
On unmodified `develop` the same three clicks leave the dialog closed.

**Acceptance scenarios**

1. **Given** the public shell at `/` **When** a song page is reached by sidebar clicks (no
   document reload) **Then** clicking `[data-add-verse]` opens `#editorModal` with the title
   `New verse`.
2. **Given** that same navigated song page **When** `[data-verse-edit]` is activated **Then**
   the dialog opens with `Edit verse 1` (the number of the chosen verse).
3. **Given** the same song reached by a direct load of its URL **When** either control is
   clicked **Then** the dialogs still open — this slice removes no direct-load behaviour.
4. **Given** the shell at `/` **When** no song has been opened **Then** the verse script is
   already present and executed, so the first in-page song arrival needs no second fetch that
   the swap would have to wait for.
5. **Given** a song page swapped in **When** its `Add verse` button is measured **Then** its box
   is byte-for-byte the old box: 111.765625×38 at x=900, y=681.34375 at 1440×900 on
   `/songs/1387/`. No markup, CSS, token or geometry changes.

### US2 — No duplicate binding on a direct song load (P1)

**Why this priority**: the current page loads `songs_verse.js` from a `<script src>` inside the
swapped `read_body` fragment. Simply adding a second include would double-bind the delegated
handlers on a hard load and double-fire the writes; the old include must go when the shell
takes ownership.

**Independent Test**: on `/songs/1387/` count live `script[src*=songs_verse]` nodes: exactly
`1`, and it resolves through `{% static %}` rather than a hard-coded `/static/` path.

**Acceptance scenarios**

1. **Given** a direct song load **When** the DOM is inspected **Then** exactly one
   `songs_verse.js` include exists, in the shell's script block.
2. **Given** the shell after a sidebar navigation **When** the DOM is inspected **Then** the
   same one include exists — the song fragment contributes none.
3. **Given** either path **When** Add verse is clicked **Then** one editor fetch happens and
   one dialog opens, never two.

### Edge Cases

- A hymn songbook's songs render no verse controls (`is_hymn_book`); this slice changes no
  permission rule and the script's delegated handlers stay inert there.
- An empty song's invitation button carries the same `data-add-verse` attribute; it is covered
  by the same handler and must work after navigation too.
- Other page-owning scripts (`obs_overlay.html`, `obs_dock.html`, `projector.html`) are loaded
  by standalone documents, not by a fragment of `reading.js`'s shell. `song.html` was the only
  script-bearing fragment and is the whole scope of this bug class.
- `songs_verse.js` binds on `document`, not on the nodes it manages, so one boot at shell load
  serves every later swap; it needs no re-binding on `shell:page`.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | `multimedia/web/templates/reading/base.html` SHALL load `web/songs_verse.js` through `{% static %}` in the shell's script block, once, alongside `reorder.js`. | `reading/R55` |
| FR-002 | `multimedia/web/templates/reading/song.html` SHALL NOT carry a `<script src>` for `songs_verse.js`; the fragment contributes markup only. | `reading/R55` |
| FR-003 | After an in-page navigation from the shell to a song page, `[data-add-verse]` SHALL open `#editorModal` with `New verse` without a reload. | `reading/R55` |
| FR-004 | After the same navigation, `[data-verse-edit]` SHALL open the dialog with the verse's number, and the drag/delete handlers bound by the same file SHALL behave as on a direct load. | `reading/R55` |
| FR-005 | A direct song load SHALL keep exactly one `songs_verse.js` include and the same behaviour. | `reading/R55` |
| FR-006 | The verse button's markup, box, write endpoints and permission guards SHALL be unchanged; no CSS, image or script body is edited. | `reading/R55` |
| FR-007 | `reading/R55` SHALL state the rule that a script owning controls on a swapped-in page is booted by the shell, not by the swapped fragment. | `reading/R55` |

### Key Entities

None. The change is one script include moved between two templates; no model, endpoint or
context value is touched.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | Add verse works after sidebar navigation. | Playwright from `/` → Songs → book 18 → `/songs/1387/`: dialog `open=false` before, `open=true` after, title `New verse`. |
| SC-002 | Edit verse works on the same path. | Same probe: `Edit verse 1` after, closed before. |
| SC-003 | The script boots at shell load. | `script[src*=songs_verse]` count at `/`: `0` before, `1` after; count on the navigated page: `1` in both, but unexecuted before. |
| SC-004 | Direct load is unchanged and not doubled. | `direct_load_dialog_open=true` in both; one script node in the after tree. |
| SC-005 | The button does not move. | Playwright box before and after: 111.765625×38 at x=900, y=681.34375 (Δ0.00px). |
| SC-006 | No new console/page errors. | `page_errors=[]` on both paths in both trees. |

## UI/UX

`live preview at http://127.0.0.1:8771/` — this slice's own worktree, served with
`manage.py runserver 0.0.0.0:8771 --noreload` from `multimedia/web/templates/`. The change is
which document boots a script, not what the page paints, so a static page could not show it;
the comparison server at `http://127.0.0.1:63404/` runs unmodified `develop`. Harness:
`specs/230-song-verse-script-boot/preview/probe.py` (Playwright, both URLs as arguments),
launcher `preview/serve.sh`.

- **Before (measured, live, 1440×900)**: home has `0` `songs_verse.js` script tags; after the
  three sidebar clicks the navigated song page has `1` tag imported into the stage but never
  executed. Add verse leaves `#editorModal` closed after 3s; Edit leaves it closed; the box is
  111.765625×38 at x=900, y=681.34375. A direct load of `/songs/1387/` opens the dialog.
- **After (measured, live, 1440×900)**: home has `1` tag and it is executed at boot (resource
  completes at 220–223ms across two runs). After the same three clicks the page still has `1` tag. Add verse opens
  `New verse`; Edit opens `Edit verse 1`; the box is unchanged to 0.00px. Direct load still
  opens the dialog, and there are no page errors on either path.
- **States**: hover, focus, active and disabled styles of `.verse-add__btn` and `.v__edit` are
  the product's existing CSS, untouched; the empty-song invitation and hymn read-only paths are
  unchanged.
- **Colour / typography / motion**: unchanged — no token, font, transition or animation is
  added or removed.
- **Responsive**: no breakpoint changes; no measured element moves at any width because no
  markup or CSS is edited.

## Assumptions

- The shell should own the script even on pages that paint no verse controls: its handlers are
  delegated on `document` and inert until a song arrives, and every other reading script is
  already loaded the same way. Loading it on first paint avoids a fetch during the swap.
- The old include must be removed, not kept as a fallback: a direct song load would otherwise
  execute the file twice and bind two delegated click handlers.
- The script is loaded through `{% static %}` like its neighbours; the old hard-coded
  `/static/web/songs_verse.js` path is not carried over to the shell.
- No owner question was needed: the report names one broken control, the failure is a single
  script that never executes, and the only design choice (which document boots it) follows the
  shell's existing convention.

## Clarifications

### Session 2026-11-23

- No questions were raised. The one design choice — which document boots the script — follows
  the shell's existing convention and is recorded under Assumptions. Zero open items; zero
  `[NEEDS CLARIFICATION]` markers remain.
