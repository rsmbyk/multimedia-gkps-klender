# Feature Specification: the copy confirmation is a dialog of its own, and the copy is named there

**Slice**: `specs/215-copy-template-dialog`
**Branch**: `feat/215-copy-template-dialog`
**Created**: 2026-11-21
**Status**: Draft
**Input**: "use the C layout, but i want it to be a second dialog that draws on top of the edit tata ibadah dialog (not takeover). also i want you to add an input field to set the name for the created template (default to "TheCurrentTataIbadahName (Copy)". and when you click on the input field, it select the whole texts so that you can type the new name directly replacing it" — accepted against the preview at `specs/215-copy-template-dialog/preview/index.html`, 2026-11-21.

## User Scenarios & Testing

### US1 — The confirmation is a second dialog, not a card inside the first (P1)

**Why this priority**: spec 212 put the confirmation inside the edit dialog's own box, so it reads as the form being covered by a panel rather than as a question being asked. A second dialog is the shape the owner asked for: the Edit Tata Ibadah dialog stays open behind it, visible and dimmed, and the confirmation owns the window.

**Independent Test**: open a service's Edit modal, press **Copy as template**: a card appears centred on the window on a scrim that reaches every edge, and the Edit dialog is still visible behind it, dimmed but legible.

**Acceptance scenarios**

1. **Given** a Tata Ibadah's Edit modal is open **When** **Copy as template** is pressed **Then** the confirmation's layer covers the whole window — not the dialog's box — and its card is centred on the window.
2. **Given** the confirmation is up **When** the Edit dialog behind it is inspected **Then** it is still open, still in place and still legible as dimmed text, not erased.
3. **Given** the confirmation is up **When** the Edit dialog's own **Save** is clicked **Then** the click lands on the confirmation: the dialog underneath is inert.
4. **Given** the confirmation is up **When** it is measured at a second window size **Then** the layer still reaches every edge and the card is still centred on the window.

### US2 — The copy is named before it is made (P1)

**Why this priority**: today the copy silently keeps the source's name, so two records end up sharing one name and the person has to open the copy and rename it afterwards. Naming it at the moment of copying is the whole point of the second dialog.

**Independent Test**: from a service named `9 Agustus 2026`, press Copy as template: the field reads `9 Agustus 2026 (Copy)`; type a new name, accept, and the created template carries that name.

**Acceptance scenarios**

1. **Given** the confirmation opens **When** it renders **Then** its Name field holds the source's name followed by ` (Copy)`.
2. **Given** the Name field **When** it is clicked **Then** its whole value is selected, so typing replaces it in one go.
3. **Given** the Name field is selected **When** it is clicked a second time **Then** the click places a caret where it landed instead of selecting everything again.
4. **Given** a name is typed **When** **Copy as template** is pressed **Then** the created template carries exactly that name, and the source keeps its own.
5. **Given** the Name field is emptied **When** it holds only spaces **Then** **Copy as template** is disabled, and it re-enables as soon as a non-space character is typed.
6. **Given** a template's Edit modal **When** **Copy as template** is pressed **Then** the same dialog opens and the field is still editable — a template copies as a template, under a name of its own.

### US3 — The dialog says what is about to happen (P2)

**Why this priority**: the three facts are what makes the answer informed rather than a reflex; spec 167's wording had to be read twice, and the accepted preview rewrote it as three statements with the consequence first.

**Independent Test**: the dialog states the copy's entries, that the source does not change, and the three facts, in that order, above the two answers.

**Acceptance scenarios**

1. **Given** the confirmation is open **When** it is read top to bottom **Then** it names the copy ("a new template, same entries, same order"), states that the source does not change, offers the Name field, then lists the three facts, then the two answers.
2. **Given** the dialog is open **When** its answers are read **Then** **Cancel** discards everything and leaves the form as it was, and **Copy as template** performs the copy.

### Edge Cases

- **When** the source's name is long enough that `<name> (Copy)` would exceed the 64 characters the field allows **Then** the default is cut to fit: the source's name is trimmed to 57 characters and ` (Copy)` appended, so the field always starts inside the limit.
- **When** the confirmation is open and the scrim is clicked **Then** it dismisses exactly as Cancel does — the confirmation closes and the edit dialog is left as it was.
- **When** the name typed is one another Tata Ibadah already carries **Then** the copy is still made: names were never unique (spec 167) and this slice does not make them so.
- **When** the copy fails **Then** the dialog stays open with the name as typed, and the failure is announced as it is today.
- **When** Escape is pressed with the confirmation open **Then** the confirmation closes and the Edit dialog does not — one Escape, one layer.
- **When** the confirmation closes by any path **Then** the Edit dialog's height and scroll position are unchanged.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | The Copy as template confirmation SHALL be a dialog of its own: a layer that covers the whole window, with its card centred on the window rather than on the edit dialog. | `reading` R47 (modified) |
| FR-002 | The edit dialog SHALL stay open and legible behind that layer, dimmed by a scrim light enough to leave it readable, and SHALL be inert while the confirmation is up. | `reading` R47 (modified) |
| FR-003 | The confirmation SHALL carry a Name field for the record it creates, holding the source's name followed by ` (Copy)` — with the source's name trimmed to 57 characters first, so the default never exceeds the 64 the field allows. | `reading` R37 (modified) |
| FR-004 | Clicking the Name field SHALL select its whole value, and a subsequent click SHALL place a caret rather than select again. | `reading` R37 (modified) |
| FR-005 | The copy SHALL be created under the name the field holds at accept time, and the source SHALL keep its own name. | `reading` R37 (modified) |
| FR-006 | **Copy as template** SHALL be disabled while the field is empty or holds only spaces. | `reading` R37 (modified) |
| FR-007 | The field SHALL accept at most the 64 characters the record's name holds, and the copy endpoint SHALL refuse a name that is empty after trimming or longer than 64 characters. | `reading` R37 (modified) |
| FR-008 | The dialog SHALL keep the three facts and the two answers spec 167's confirmation carried, with the copy's entries and the source's safety stated above the field. | `reading` R47 (modified) |
| FR-009 | The confirmation's Cancel SHALL close it and leave the edit dialog exactly as it was, and Escape SHALL do the same without closing the edit dialog. | `reading` R47 (modified) |
| FR-010 | The card SHALL keep spec 212's card: `min(448px, 100%)`, 22px padding, a 14px radius, the canvas fill, the hairline and the dialog shadow, with the answers right-aligned 8px apart on its right edge. | `reading` R47 (modified) |
| FR-011 | A click on the confirmation's scrim SHALL dismiss it as Cancel does, and a click inside the card SHALL not. | `reading` R47 (modified) |

### Key Entities

- **TataIbadah** — unchanged in shape. `name` (64 characters) is now written from the confirmation rather than copied from the source; `kind` is `template` for every copy; `date` stays empty. No field, no constraint and no migration changes.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | The confirmation is a layer of the window, not of the dialog | the layer's rect equals the viewport's, and its computed `position` is `fixed` |
| SC-002 | The card is centred on the window | its centre is within 1px of the viewport's centre, in both dialog sizes |
| SC-003 | The edit dialog survives behind it | its title's text is unchanged and its rendered text colour differs from the scrim's fill — it is dimmed, not erased |
| SC-004 | Opening and closing the confirmation never moves the edit dialog | its height is equal before and after, to the tenth of a pixel |
| SC-005 | The default name is the source's name plus ` (Copy)` | the field's value equals that string |
| SC-006 | One click selects the whole name | `selectionStart` is 0 and `selectionEnd` is the value's length |
| SC-007 | The copy takes the typed name | the created record's `name` equals what the field held, and the source's is unchanged |
| SC-008 | An empty name cannot be accepted | the accept button is `disabled` for an empty or spaces-only field, and enabled otherwise |
| SC-009 | The default name always fits the field | for a 64-character source name the field holds 64 characters ending in ` (Copy)` |
| SC-010 | The scrim dismisses | a click at the layer's own edge closes the confirmation, and a click on the card's heading does not |

## UI/UX

`static preview at specs/215-copy-template-dialog/preview/index.html` — the dialog markup the server actually sends (`#editorContent`'s innerHTML, read off a service and a template), the product's own `tokens.css` and `components.css` (copied by `build.py`, never retyped), and `preview.css` for the harness alone. The page's own bar switches state (`Edit modal` ⇄ `Copy as template`), dialog size (service 480 × 312.5 ⇄ template 480 × 241.3), and theme. Its stage stands in for the window: `contain: layout` makes the stage the layer's containing block, so the page can show a window-wide layer without covering its own controls.

Measured at device scale 1 (`probe.py`, both themes, both dialog sizes), and confirmed in the product by the E2E lane at 1440 × 900:

- **Layout / position**: the layer is `position: fixed; inset: 0` — in the product **1440 × 900 at (0, 0)**, so its box is the window's, with 24px padding and no radius; in the preview it is the stage's box (958 × 518 inside the stage's 1px border). The card is **448 × 341.7**, centred on the window — at 1440 × 900 it sits at (496, 279.1), its centre (720, 450) exactly the viewport's — and the edit dialog keeps its own place behind it (**480 × 312.5 at (480, 293.8)** for a service, **480 × 241.3 at (480, 329.4)** for a template — both centred, so the shorter dialog starts lower).
- **Size / spacing**: card padding **22px 22px 20px**, radius **14px**, hairline `--divider` + `--shadow-dialog`. Inside, on a 404px content column: heading **404 × 22.5**, lead **404 × 41.8**, label **404 × 16.3**, Name field **404 × 38**, facts **404 × 84.1** as three 19.4px rows, answers **404 × 38** — **Cancel 81.6 × 38** and **Copy as template 150 × 38**, the pair ending 22px inside the card's right edge, 8px apart.
- **Colour / typography**: scrim **rgba(0, 0, 0, .26)** in dark and **rgba(20, 20, 18, .26)** in light — light on purpose, because the dialog's own `::backdrop` already sits under it. Card `--canvas` (**rgb(20, 19, 15)** dark, **rgb(247, 245, 241)** light). Heading **650 18px/22.5**; lead **13.5px/20.925** in `--ink`; facts **12.5px/19.375** in `--head-ink` with their bold lead-ins in `--ink` at 600. The Name field is the editor's own field: label **12.5px/560** in `--head-ink`, input **500 14px/18.9** on `--rail-bg` (**rgb(35, 32, 25)** dark, **rgb(237, 234, 227)** light) with a `--divider` border, and the editor's own focus ring on focus.
- **States**: closed — `hidden` keeps the layer `display: none`; open — as measured, focus on **Copy as template**; the Name field unfocused shows the default value with no selection; clicked — the whole value selected (`[0, 21]` of 21 characters) and the field's focus ring up; empty — accept `disabled`; a second click — a caret, no selection. Hover and focus on the answers come from `.editor__save` / `.editor__cancel` as they already ship.
- **Motion**: none. The layer appears at once, as spec 212's does; the slice adds no animation.
- **Responsive**: the card is `min(448px, 100%)` inside the layer's 24px padding, so at a 480px window it is 432px wide and never overflows; the layer always equals the viewport.

The state this replaces, for comparison: the layer is `position: absolute; inset: 0` **inside the dialog**, so it is 480 × 241.3 at the dialog's own box and its scrim squares off nothing but the dialog; the card is the same 448px wide but only **176.3** tall, holding one paragraph instead of a lead, a field and three facts, and there is no way to name the copy at all.

What the card covers, stated plainly: it is taller than either dialog, so the edit dialog's own text never shows through — it reads as a dimmed silhouette around the card. That is what the accepted preview shows, and R47 was worded to match it at Converge rather than claim a legibility the surface does not have.

## Assumptions

- **No new capability is created.** The slice modifies two existing requirements rather than adding an `R48`: R47 already governs this confirmation and R37 already governs what a copy is, and duplicating either would leave the capability file with two statements of one behaviour.
- **The confirmation is a layer in the same document, not a second `<dialog>` element.** A nested native `<dialog>` inside a modal dialog cannot take focus or paint above its ancestor's top layer reliably; the layer keeps the product's existing `[data-copy-confirm]` hook, so `editors.js`, `_copy_confirm.html` and the tests keep addressing the same node.
- **The scrim is light because the stack is real.** The edit dialog's own `::backdrop` is already a full-strength `--backdrop`; a second one at the same strength erases the dialog completely, which defeats the point of leaving it open. The measured value is `.26` in both themes.
- **The Name field is the editor's own field**, `.editor__field` + `input[type="text"]` from `components.css`, rather than a new control: it already carries the 38px height, the `--rail-bg` fill, the radius and the focus ring the rest of the dialog uses.
- **The card keeps spec 212's card but not its two derived numbers.** It is 448px wide, 22px padding, `--canvas`, the hairline and the dialog shadow as 212 measured them; its radius moves 12 → 14px so it matches the dialog it now stands over rather than a card inside it, and its width is stated directly as `min(448px, 100%)` because the layer no longer has a 16px-padded inner box to cap `min(468px, 100%)`. 212's *"the layer is the dialog's box"* is what this slice replaces.
- **This slice supersedes spec 167's FR-021 — *"a copy SHALL keep the name"*.** A copy now takes the name typed in the confirmation, defaulting to the source's plus ` (Copy)`. Nothing else about FR-021 changes: the copy still carries no date, is still a template, and still brings the source's entries in order.
- **A 57-character base plus ` (Copy)` is the fit rule**, not a mid-word ellipsis: a trimmed name keeps its beginning, which is what distinguishes one Tata Ibadah from another in the sidebar, and the suffix is what says this is a copy.
- **The dialog opens with focus on Copy as template, not on the field.** The field is an option, not the point; putting the caret in it on open would make every copy a rename.
- **`(Copy)` is interface chrome**, so it is English like the rest of the chrome; the domain noun and the source's own name stay as they are.
- **The copy's entries are unchanged.** This slice renames the copy; it does not touch what the copy contains, and spec 167's rule that a copy converts nothing still holds.
- **The generate flow's own confirmation is untouched**, as spec 212 decided for it.

## Clarifications

### Session 2026-11-21

- Q: A name is capped at 64 characters and the default is `<source name> (Copy)` — what happens when the source's name is 58–64 characters? → A: **cut the source name so the default fits** — 57 characters plus ` (Copy)`. A default that starts over-long would hand the person a field they cannot submit without editing.
- Q: Should a click outside the card dismiss the confirmation? → A: **yes, as Cancel does.** The accepted preview already behaves that way, and a second dialog whose only exits are a button and Escape is stricter than the product's own dialogs.

- Zero open items: both markers are answered above and written into FR-003, FR-011, SC-009 and SC-010.
