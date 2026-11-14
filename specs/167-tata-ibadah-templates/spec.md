# Feature Specification: a Tata Ibadah is a service or a template

**Slice**: `specs/167-tata-ibadah-templates`
**Branch**: `feat/167-tata-ibadah-templates`
**Created**: 2026-10-30
**Status**: Accepted (owner, gate 1, 2026-10-30)
**Input**: the owner's request — *"i want to change how template tata ibadah works. today, it is recognized as tata ibadah without dates. i want it to behave more like a template or skeleton"* — with the switcher in the New Tata Ibadah modal, fill-in and choice entries, a copy-as-template action in the Edit modal, and a two-step generate flow that ends in the normal Tata Ibadah form.

## What the page does today

A template is not a type; it is a Tata Ibadah whose date happens to be empty. The panel list is chosen by
that emptiness (`multimedia/web/reading/views.py:843`), the panel's mode follows it (`:1914`), and the
editor's own help text instructs the operator to create one by leaving the date out
(`multimedia/web/reading/editors.py:60–62`):

> Leave empty for a recurring template (shown under Templates).

Nothing forbids a date-less service and nothing marks a dated one, so the Edit modal can turn a shipped
service into a template by clearing its date: the model's field is `blank=True, null=True`
(`multimedia/tatib/models.py:10`) and the form only exposes `name` and `date` (`editors.py:52–63`).
The picker's `Clear date` button (`_editor_form.html:20`) is the whole mechanism. On a new record the
picker preselects the nearest Sunday and writes it into the hidden value at init
(`static/web/date-picker.js:72–74`, `:259`), so the empty case is always a deliberate clearing.

Every Tata Ibadah projects. Both controls render on every service page
(`multimedia/web/templates/reading/tatib.html:10–34`), `service_projector` adopts whatever
`?service=<pk>` names (`views.py:1334–1338`), and `_projector_data` turns whatever rows exist into screens
(`:1214`). An unresolved skeleton would therefore project whatever half-order it holds.

Entries are four writable kinds — text, passage, song, media (`multimedia/web/reading/entries.py:18–26`);
the retired section break still renders, and legacy `TataIbadahItem` text rows still render beside them.
The Edit modal offers nothing but name and date: there is no copy of any kind.

## User Scenarios & Testing

### US1 — A Tata Ibadah is created as a Normal service or a Template (P1)

**Why this priority**: the type decides everything else — whether a date is demanded, whether projection is
offered, and whether the generate flow exists at all. It must be chosen where the record is born, because
the owner's rule is that it never changes afterwards.

**Independent Test**: from the Tata Ibadah panel, create one Normal and one Template from the New Tata
Ibadah modal; the Normal lands in the dated list with its date, the Template lands under Templates with no
date, and neither can change its type afterwards.

**Acceptance scenarios**

1. **Given** the New Tata Ibadah modal is opened, **When** it renders, **Then** it carries a two-option
   switcher at the top — **Normal** (selected) and **Template** — in the shape the New text and New passage
   modals already use.
2. **Given** Normal is selected, **When** the operator saves with the default date, **Then** a normal Tata
   Ibadah is created with that date and appears in the dated list.
3. **Given** Normal is selected, **When** the date field renders, **Then** it offers no control that
   empties it — the app's `Clear date` button is gone — so every Normal save carries a date.
4. **Given** Template is selected, **When** the modal renders, **Then** the date field and its picker are
   absent, and the save creates a template with no date.
5. **Given** either type is being edited, **When** the Edit modal opens, **Then** it carries no switcher; its
   title names the type (`Edit Tata Ibadah` or `Edit template`) and the date is editable only for the normal
   one.
6. **Given** a normal service's date is cleared in the Edit modal, **When** Save is pressed, **Then** the
   save is refused: the type does not change through an edit.
7. **Given** the migration has run, **When** the panel opens, **Then** every previously date-less Tata Ibadah
   is a template under Templates and every dated one is a normal service in the dated list.

### US2 — A template carries fill-in and choice entries (P1)

**Why this priority**: a skeleton is only useful if the parts that vary every week have a shape the generate
step can fill. This story is the vocabulary the generate flow speaks.

**Independent Test**: on a template, add one fill-in of kind song and one choice of kind song with two
options; all three survive a reload, draw as their own rows, and neither can be added to a normal Tata Ibadah.

**Acceptance scenarios**

1. **Given** a template's page, **When** an add row renders, **Then** it offers `+ Text`, `+ Song`,
   `+ Passage`, `+ Media`, then `+ Fill-in` and `+ Choice` past a hairline; on a normal Tata Ibadah
   only the four kind buttons are offered.
2. **Given** `+ Fill-in` is chosen, **When** its modal opens, **Then** it asks for a title/note and one kind
   (Passage, Song, Text, Media); saving draws a row naming the kind and the title.
3. **Given** `+ Choice` is chosen, **When** its modal opens, **Then** it asks for a title and one kind;
   saving draws the choice row with an `Add option` control.
4. **Given** a choice row, **When** `Add option` is chosen, **Then** the chosen kind's normal New modal
   opens, and the saved entry appears as an indented child row under the choice, in its own order.
5. **Given** a choice of kind song, **When** an option is added, **Then** the option is a song entry of that
   choice; an option of another kind cannot be attached to it.
6. **Given** a choice with no options, **When** the template page draws it, **Then** the row says it has no
   options yet — the template is allowed to be unfinished, but the choice cannot be settled at generation.
7. **Given** a request that writes a fill-in or a choice onto a normal Tata Ibadah, **When** it reaches the
   server, **Then** it is refused, whatever surface sent it.

### US3 — A template creates a dated service in two steps (P1)

**Why this priority**: this is the point of the whole feature — the weekly order assembled from the
skeleton without rebuilding it, with the skeleton left intact for the next week.

**Independent Test**: on a template holding two fixed entries, one fill-in and one choice with two options,
press **Use template**, settle both, press **Next**, confirm **Create**: a normal Tata Ibadah appears with
the fixed entries and the two resolutions in the template's order, and the template is unchanged.

**Acceptance scenarios**

1. **Given** a template's page, **When** the read actions render, **Then** **Use template** takes the place
   the Project button takes on a normal service, and no projector-window control is offered.
2. **Given** **Use template** is pressed, **When** the generate modal opens, **Then** it shows the template's
   order view-only: ordinary entries are muted and inert, and only fill-ins and choices carry controls.
3. **Given** a fill-in row, **When** **Set** is pressed, **Then** that kind's New modal opens over the
   generate modal, and the chosen content is reflected in the row on save and can be changed before
   **Next**.
4. **Given** a choice row, **When** **Choose** is pressed, **Then** a chooser lists the choice's options with
   their content and opens the existing Preview for any one of them; picking one reflects it in the row and
   can be changed before **Next**.
5. **Given** a chooser open over the generate modal, **When** it is dismissed — `Cancel`, Escape, or a click on
   its backdrop — **Then** only the chooser closes: the modal is still open, every settled slot is as it was,
   and focus returns to the row's control.
6. **Given** at least one fill-in or choice is unsettled, **When** the modal renders, **Then** **Next** is
   disabled and the modal states how many are left.
7. **Given** every slot is settled, **When** **Next** is pressed, **Then** the modal moves to step 2: the
   normal Tata Ibadah form, with the name prefilled from the template and the date picker preselecting the
   nearest Sunday.
8. **Given** step 2, **When** **Create** is pressed, **Then** a confirmation names the service and its date,
   and confirms into the new service's page.
9. **Given** the confirmation is accepted, **When** the service is created, **Then** its entries follow the
   template's order: each ordinary entry is copied as an entry, each fill-in is replaced by its resolver,
   and each choice by its chosen option.
10. **Given** the generate modal is cancelled or abandoned at any step, **When** the operator returns to the
   page, **Then** no service was created and the template is byte-identical.

### US4 — Any Tata Ibadah can be copied as a template (P2)

**Why this priority**: last week's order is the best skeleton for next week's, but the flow is usable
without the copy — templates can be built empty. It follows the type and the entries, and it is the only
way a normal service becomes a template, since an edit never changes the type.

**Independent Test**: from a normal service's Edit modal, press **Copy as template**, confirm: a template
appears under Templates with the same name and the same entries in the same order, no date, and the original
service is unchanged.

**Acceptance scenarios**

1. **Given** a Tata Ibadah's Edit modal, **When** it renders, **Then** it carries a **Copy as template**
   button beside Save/Cancel, for a normal service and for a template alike.
2. **Given** the button is pressed, **When** the confirmation opens, **Then** it names the consequence: the
   copy has no date, can never become a normal Tata Ibadah, and a template can be copied again as another
   template.
3. **Given** the confirmation is accepted, **When** the copy is created, **Then** it keeps the name and every
   entry in order, as ordinary entries that stay editable; no entry is converted to a fill-in or a choice.
4. **Given** the source is a template, **When** it is copied, **Then** the copy keeps its fill-ins, choices
   and their options as well.
5. **Given** the copy exists, **When** it was made from the Edit modal, **Then** the app lands on the new
   template with the panel on Templates, ready for fill-ins and choices to be added.
6. **Given** the confirmation is cancelled, **When** the modal closes, **Then** nothing was created.

### US5 — A template never reaches a screen (P2)

**Why this priority**: an unresolved skeleton projected into a service is worse than not projecting at all.
The guard has to hold at every entry point, not only on the page that hides the button.

**Independent Test**: a template's page offers no projector control; `/projector?service=<template>` shows
the empty display; the OBS dock's service list does not offer the template.

**Acceptance scenarios**

1. **Given** a template's page, **When** it renders, **Then** neither the projector-window control nor the
   Project control is present, and **Use template** holds their place.
2. **Given** a normal service's page, **When** it renders, **Then** both projector controls are exactly as
   they are today.
3. **Given** `/projector?service=<template id>`, **When** the page loads, **Then** it shows the empty display
   it shows with no service, never the template's order.
4. **Given** the OBS dock lists services, **When** the list is read, **Then** templates are absent.

### Edge Cases

- **When** a template holds no fill-in and no choice, **Then** **Use template** still works: step 1 shows the
  muted order with **Next** already enabled, and **Create** makes a straight copy.
- **When** a choice has no options, **Then** it cannot be settled: its row reads `No options yet`, its
  control is **disabled** and labelled **`No options`**, **Next** stays disabled, and the template page
  marks the choice until an option is added.
- **When** a fill-in's New modal is cancelled, **Then** the slot stays unsettled and its previous resolution,
  if any, is kept.
- **When** a resolved song is deleted before **Create**, **Then** the create is refused, names the entry, and
  the row returns to unsettled rather than creating a broken service.
- **When** a chosen option is deleted from the template while the generate modal is open, **Then** the same
  refusal applies at **Create**.
- **When** the template holds legacy `TataIbadahItem` text rows or a retired section-break entry, **Then**
  they are ordinary entries: muted in step 1 and copied in order.
- **When** a normal service's date is cleared, **Then** the refusal is the same on create and on edit, and
  no path turns a normal service into a template except **Copy as template**.
- **When** two templates share a name, **Then** both are listed; names were never unique and this slice does
  not make them so.
- **When** a template's Media files dialog is opened, **Then** it works as it does on a service: the list is
  preparation information, not projection.
- **When** a fill-in of kind media is settled, **Then** the chosen file is the operator's own local copy, and
  the service entry references its identity exactly as a media entry added directly does.
- **When** a file is referenced only by templates, **Then** it is a use — never auto-deleted, however long it
  sits — but it is **not** in the download manifest: the manifest is built from active services dated today
  or later, so the bytes arrive only once a dated service uses that file.
- **When** a file used by a template is removed by hand from the library, **Then** the removal is allowed as
  for any file no service due today or later holds; the template keeps its reference, and the file is fetched
  again when a dated service needs it.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | A Tata Ibadah SHALL carry a type — Normal or Template — chosen when it is created and never changed afterwards. | `new: reading` → R34 |
| FR-002 | A Normal Tata Ibadah SHALL carry a date; a Template SHALL NOT. The pairing SHALL be enforced at the model and at every writing endpoint. | `new: reading` → R34 |
| FR-003 | The New Tata Ibadah modal SHALL carry a Normal/Template switcher at its top, Normal preselected; the date field SHALL be present and asked for Normal — with no control that empties it, the app's `Clear date` button dropped — and absent for Template. | `new: reading` → R34 |
| FR-004 | The Edit modal SHALL NOT carry the switcher; it SHALL name the type, SHALL allow the date only on a Normal one, and SHALL refuse a save that clears it. | `new: reading` → R34 |
| FR-005 | The panel SHALL choose its two lists by the type: dated services by date, templates under Templates. | `new: reading` → R34 |
| FR-006 | Existing rows SHALL be typed by their date at migration: date present → Normal, date empty → Template; no entry is converted. | `new: reading` → R34 |
| FR-007 | A template's add rows SHALL offer `+ Fill-in` and `+ Choice` after the four kind buttons; a normal Tata Ibadah SHALL NOT offer either. | `new: reading` → R35 |
| FR-008 | A fill-in SHALL carry a title/note and one kind — passage, song, text or media — and no content of its own. | `new: reading` → R35 |
| FR-009 | A choice SHALL carry a title, one kind, and an ordered list of options, each a complete entry of that kind added from the choice's own row as an indented child row. | `new: reading` → R35 |
| FR-010 | A fill-in or choice SHALL NOT be creatable on a Normal Tata Ibadah: every writing endpoint SHALL refuse it. | `new: reading` → R35 |
| FR-011 | A template's page SHALL replace the projector controls with **Use template**, keeping the Media files dialog where it exists today. | `new: reading` → R34 |
| FR-012 | A Template SHALL never be projectable: the projector route SHALL answer with the empty display and the OBS dock's list SHALL omit templates. | `new: reading` → R34 |
| FR-013 | **Use template** SHALL open a generate modal that shows the template's order view-only, ordinary entries muted and inert, fill-ins and choices active. | `new: reading` → R36 |
| FR-014 | A fill-in SHALL be settled by **Set**, which opens that kind's New modal; the chosen content SHALL be reflected in the row and SHALL be changeable before **Next**. | `new: reading` → R36 |
| FR-015 | A choice SHALL be settled by **Choose**, which opens a chooser listing its options, each previewable through the existing Preview; the chosen option SHALL be reflected in the row and SHALL be changeable. A choice with no options SHALL carry a disabled control labelled **No options** and a row value of **No options yet**. | `new: reading` → R36 |
| FR-016 | **Next** SHALL be disabled while any fill-in or choice is unsettled, and the modal SHALL state how many are left. | `new: reading` → R36 |
| FR-017 | **Next** SHALL move to step 2: the normal Tata Ibadah form, name prefilled from the template and the date picker preselecting the nearest Sunday. | `new: reading` → R36 |
| FR-018 | **Create** SHALL ask for confirmation and SHALL create the service atomically: ordinary entries copied in order, each fill-in replaced by its resolution and each choice by its chosen option. | `new: reading` → R36 |
| FR-019 | Generation SHALL leave the template unchanged, and abandoning the modal before **Create** SHALL store nothing. | `new: reading` → R36 |
| FR-020 | The Edit modal SHALL offer **Copy as template** for either type, opening a confirmation that names the consequence. | `new: reading` → R37 |
| FR-021 | A copy SHALL keep the name and every entry in order as ordinary editable entries; a template source SHALL also bring its fill-ins, choices and options. A copy SHALL have no date and SHALL be a template. | `new: reading` → R37 |
| FR-022 | After a copy, the app SHALL open the new template with the panel on Templates. | `new: reading` → R37 |
| FR-023 | A template's media SHALL count as a use for retention: a file referenced by any active Tata Ibadah — dated or template, entry or option — SHALL never be auto-deleted, whatever its age. | `new: reading` → R38 |
| FR-024 | A template's media SHALL NOT be auto-downloaded: only files referenced by an active dated Tata Ibadah due today or later SHALL enter the download manifest. A reference held only by templates SHALL wait for a dated service that uses it. | `new: reading` → R38 |

### Key Entities

- **Tata Ibadah (service order)** — gains a type: Normal or Template. A Normal carries a date; a Template
  never does; the pairing is the model's invariant. The type is set at creation and never changes.
- **Fill-in entry** — a template-only entry: a title/note, one kind (passage, song, text, media), no content.
  It occupies one position in the order and is resolved at generation.
- **Choice entry** — a template-only entry: a title, one kind, and an ordered list of options. Each option is
  a complete entry of that kind, owned by the choice and drawn as its child. One option is chosen at
  generation.
- **Resolution** — what one slot holds during generation: the chosen entry's own fields, held only in the
  dialog, never stored on the template, and dropped when the dialog is abandoned.
- **Copy** — a new template made from any Tata Ibadah: same name, same order, no date; a template source also
  brings its fill-ins, choices and options.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | No Normal Tata Ibadah exists without a date and no Template exists with one, after creating and editing both types. | the panel's lists and a direct count of rows whose date is empty against their type |
| SC-002 | A template offers no projection control and `/projector?service=<template>` renders no screens. | the template page's read actions and the projector page's payload for its id |
| SC-003 | **Next** is disabled while at least one slot is unsettled and enabled at zero, on a template holding several of each. | the button's `disabled` state read at each settling step |
| SC-004 | Generating leaves the template's entry count and every entry's fields unchanged. | a read of the template before and after a generation |
| SC-005 | Every service that existed before the slice keeps its list: dated ones in the dated list, undated ones under Templates. | the panel's two lists over the pre-slice fixture |
| SC-006 | The generated service's entries follow the template's order with each slot replaced in place. | the new service's ordered entries against the template's |

## Preview

`static preview at specs/167-tata-ibadah-templates/preview/index.html` — built from the reading page's
own markup, tokens and stylesheets, with every surface in one page: the New Tata Ibadah modal and its
switcher, a template's page with its slots and **Use template**, the generate modal's two steps with
their confirmations, and an **entry-kinds** sheet that draws all four kinds as a fixed entry, a fill-in
and a choice. Every state is reachable by hand: Normal and Template, a settled and an unsettled
slot, a disabled **Next**, both confirmations, light and dark, 1440 through 420 wide.

## UI/UX

Measured on the preview in Chromium at 1440×900 unless stated; the preview draws the stage at a **760px**
column, its width at that window.

**Layout and position**

- **Template page** — the eyebrow reads `TEMPLATE` at the stage's own 16.5px/600/.12em; the read actions
  hold `Media files` (quiet, 34px) and **Use template** in the Project button's place and treatment
  (solid `--active-bg`, 34px). No projector control is rendered.
- **A fill-in row** — the stage's row rhythm: 56px minimum height, an inset 1px dashed edge at
  `color-mix(--divider 55%, --focus)` with a 9px radius, the kind mark at x = 24 (20px), the kind label
  at x = 56, then the title and the state line. **A choice row** is the same box with its options in an
  indented list: a 1px `--divider` guide line at 24px, option rows 42px high with a 16px kind icon, the
  reference at 14px serif/600 and the verse line at 12px, and `+ Add option` under them.
- **Add bars** — six buttons: the four kinds, a 1px 16px split, then `+ Fill-in` and `+ Choice` in
  `--focus` ink and a focus-tinted dash.
- **New Tata Ibadah** — a 480px modal; the switcher is the screen-mode component at **308×42** (thumb
  150×34, sliding with `--ease`), centred, with **no help line under it**. The date field is 38px and
  carries **no `Clear date` control** — the app's button is dropped, so a Normal can never lose its
  date. **Save** is 66.6×38.
- **Edit Tata Ibadah** — the same 480px modal without a switcher; `Copy as template` sits **in the
  modal's header, right of the title**, 137.8×34, with no note under it — the confirmation carries the
  consequence.
- **Generate** — the large editor frame, **840×760 at (300, 70)** on a 1440 window: a step line
  (18px circles, 10.8px/600/.09em labels), then the **21px title and the 13px `From template · <name>`**
  stacked on one left edge — the app frame's 26px title indent removed, its rule between them — the
  header **150.7px** tall, then a scrolling row list
  (12px vertical padding per row, hairline dividers — the preview's twenty-three-row order is
  **1685px** inside a **540px** body), and a footer holding the status left and the actions right
  (69px). Every
  kind is in the order: text, song, passage and media as fixed rows and as fill-ins, and a text, a
  song and a passage choice, each opening its own option chooser — **a modal card like the editor's**,
  canvas fill on a 12px radius, the dialog shadow, and the same 1px `--divider` hairline drawn as a
  `0 0 0 1px` ring rather than a border, so the card's width is untouched (measured 560×261.3 for the
  passage chooser, unchanged by the ring). **A fixed row uses the page's entry styles at
  the row's scale** — 640 sans/14px left heading, 14px serif body, 11.5px sans meta, a
  16px kind mark (18px media chip) in a 24px gutter — at 52% opacity and inert; **a slot row is the
  template page's slot row** — 600 sans/11.5px uppercase kind, 620 serif/17px title, sans/12.5px
  value — with the Set/Choose/Change control beside it. A choice with no options draws that control disabled at 55%
  opacity, labelled **`No options`**, over a row value of **`No options yet`**; it can never settle, so
  **Next** stays disabled for as long as it is in the order. A slot may have no title — `ServiceEntry.title`
  is optional — so it drops the title line: the kind line is the name and the value sits 7px under it,
  never a placeholder. Every row's words start on the same 24px
  column; a slot leaves the gutter empty. A muted row is deliberately a step below the slot's title,
  so the operator's work stays the largest thing in the list. A settled song carries its verses
  inline after a middle dot, in the muted text colour — `KJ 152 — Ada Kuasa · Bait 1, 2, 3` — and a
  title-less text shows its opening line, because `ServiceEntry.title` is optional and the stage
  renders a body-only entry with no heading (`tatib.html`).
- **New fill-in / New choice** — the small 480px frame, **333.5px** and **351.5px** tall: a title (or a
  title/note, both optional, with `Optional — leave empty to show the kind alone` as the placeholder),
  a four-chip kind picker (Text, Song, Passage, Media; Text preselected, the selected chip filled with
  the active token), a help line — the fill-in's content is chosen at generation; a choice's options
  are added on its row afterwards — and `Add fill-in` / `Add choice` beside `Cancel`.
- **Confirmations** — a 468px card (448 inside the 480px edit modal) over a `--backdrop` layer: 22px
  padding, an 18px title, 13.5px message, the two answers equal in height.
- **Choose** — a 560px card, each option a 10px-radius row with `Preview` and a solid **Choose**.
  The card's heading is the slot's own title, or the kind's name when the slot is title-less — it
  never resurrects a title the row does not have. A passage option states its reference only — the
  verses are already in it, and the edition is not shown — so its row is a single line; a text option
  is its title, with the prayer behind `Preview`, and a title-less text is its body's opening line,
  muted and cut to one line with an ellipsis.
- **The entry-kinds sheet** is a review surface, not a product screen: it draws the four kinds as a
  fixed entry, a fill-in and a choice with two options each, so every row variant is on one page. The
  rows are the stage's own: a text entry carries no kind mark, a passage or a song its 20px mark, media
  its 42px chip; a choice's options carry no per-option mark, because the choice names the kind once.
  **The two slot marks are one pair**: a 20px dashed rounded square whose inner glyph states the
  behaviour — a plus for a fill-in, a radio for a choice — at the kind marks' stroke weight. **Dashed
  means still to be filled or added** (the two slot marks, `+ Add option`, the add bar); everything that
  is already content — a fixed entry's kind mark, the media chip, the chooser's rows — is solid.
- **The media-and-title matrix lives in the generate modal itself**: the order carries all five media
  families as fill-ins, each as a titled row and an untitled one — `Family · Title` when the entry has
  a title, `Family · filename` when it does not, the filename drawn in the quiet ink — a titled and an
  untitled media choice (the titled
  chooser lists the five families and mixes one filename-only option, the untitled one lists the five
  filenames), and an untitled text choice beside the titled one. Nothing invents a name: a title-less
  slot shows its kind line and value only, and a title-less option shows its filename or opening line,
  both in the quiet ink.

**Colour and typography** — every value comes from `tokens.css`; the slice adds no hex. Ordinary entries
inside the generate modal are drawn at **opacity .52** and take no pointer; the slots keep full ink, their
kind label tinted toward `--focus`. Dark mode renders the same shapes on `--canvas #14130F`.

**States**

- The switcher: Normal/Template with `aria-pressed` and the thumb's position; the date field present and
  absent.
- A fill-in/choice row: at rest the dashed edge is quiet; under the pointer or keyboard focus it
  strengthens toward `--focus`.
- A slot in the generate modal: **unsettled** = `Not set` + a solid `Set`/`Choose`; **settled** = the
  chosen value in ink + a quiet `Change`.
- **Next**: `disabled` at ≥1 unsettled (the app's disabled treatment, `--divider` fill and `--head-ink`
  label), with the count in the status line; enabled at zero.
- Step 1 on step 2 of the modal: its circle carries a check, filled like the current step's. The badges
  are 18px circles with a 1px border, their marks **optically centred against the rendered pixels**, not
  the line box: the list's `.09em` tracking is cancelled on the badge (it alone pushed a lone digit .47px
  left), the check is drawn as a 10px SVG path rather than typed (a `✓` glyph's bearings leave it .69px
  right and .31px high; a symmetric path is exact), and the digit correction lives behind
  `@media (min-resolution: 1.5dppx)` — at 1dppx the glyph snaps to whole device pixels and already lands
  centred, so nudging it there moves it a full pixel off. Measured `1` / `2` / check: **0.00 / 0.00** at
  1dppx; −0.25 dy, ±0.5 dx at 2dppx; −0.12..−0.19 dy, ±0.31 dx at 8dppx.
- A chooser is dismissed by `Cancel`, by Escape, or by a click on its backdrop, and each closes the chooser
  **alone**: the generate modal keeps its open state, its scroll and every settled slot, and focus returns to
  the row's Set/Choose/Change control. The same holds for the kind's New modal and the Preview opened from a
  slot: dismissing any of them returns to the generate modal untouched. Escape reaches the modal only when
  none of them is open.
- Both confirmations are dismissible (`Cancel` / `Back`), and neither is the default focus.
- Hover, focus-visible and reduced-motion follow the existing component rules; no new motion is added.

**Responsive**

- 1440 and 900: the generate frame is **840×760**; its footer is **69px** at both.
- 420: the native dialog caps it at **382×760** at (19, 50); the footer wraps to **102.5px**.
- The add bar fits one **455.2×35.6** row down to a ~471px pane. At a 388px pane it wraps to
  **324×75.2**, and there it becomes a plate (`--canvas`, 1px `--divider`, 10px radius, `--shadow`) so
  the wrapped bar does not let words read through its buttons. The cost, stated: at a phone-width pane
  the plate covers ~55px more of the seam than the four-button bar, and on a coarse pointer — where the
  bar is always shown — it sits over the entry's edge until the operator scrolls it away. Template
  editing is a desktop act; this is its narrow fallback.

## Assumptions

- **A1 — "Fill-in" is the UI word for the owner's "empty".** "Empty" already names the empty-service state on
  the same pane (`.entry__empty`), and the entry's act at generation is filling it. The owner named the
  concept "empty"; the label is vetoable at gate 1.
- **A2 — "Use template" replaces the Project button, and the flow is titled "New Tata Ibadah" and "Create".**
  "Generate" names the machine's act; the operator prepares a service, and what is created is an ordinary
  Tata Ibadah. The word stays as the concept's internal name. Vetoable at gate 1.
- **A3 — The switcher reads "Normal" and "Template", Normal preselected.** "Normal" is the owner's own word
  for the non-template kind.
- **A4 — A copy keeps its source's name.** Two Tata Ibadah of one name have always been allowed, and the copy
  is renamed from its own Edit modal if the operator wants otherwise.
- **A5 — A copy lands on the new template, panel on Templates.** The next act after copying is adding
  fill-ins and choices, which is done on the template's page.
- **A6 — A template keeps its Media files dialog.** The list is preparation information, not projection.
- **A7 — Resolutions live only in the dialog.** Nothing is stored until **Create**; abandoning loses them,
  which is the same contract the other editor modals have with an unsaved form.
- **A8 — A template with no slots generates a straight copy** of its order.
- **A9 — Search keeps today's scope.** Templates are active service orders, and the search index reads them
  as it does today; this slice changes no search behaviour.
- **A10 — The model API keeps reading every Tata Ibadah.** A create that names no date produces a template
  (the same rule as the editor), and an update never changes the type. No new API surface is added.
- **A11 — Existing undated services become templates with their entries unchanged.** A fixed entry is not a
  fill-in; the owner's rule is that the skeleton's slots are added by hand.
- **A12 — Capability numbers R34–R38 are claimed against `origin/develop` on 2026-10-30** and re-read before
  Fold; `reading/R33` is the latest on that base. R38 covers the media rule a template changes: kept as a
  use, never auto-downloaded.

## Clarifications

### Session 2026-10-30

- Q: How are fill-ins and choices added to a template? → A: two new add-row buttons, `+ Fill-in` and
  `+ Choice`, each asking for the title and the kind. *(owner, 2026-10-30)*
- Q: How are a choice's options added and where do they live? → A: from the choice's own row, an `Add option`
  control opens that kind's normal New modal, and each option is an indented child row under the choice.
  *(owner, 2026-10-30)*
- Q: Where do the generated service's name and date come from? → A: the generate modal is a sequence: first
  the slots are settled, its button is **Next**; the second step is the normal Tata Ibadah form. *(owner,
  2026-10-30)*
- Q: Does copying a service as a template convert its entries? → A: No. Copying changes nothing about the
  entries — they stay ordinary and editable — and the fill-ins and choices are added by hand afterwards.
  *(owner, 2026-10-30)*
- Q: What does the media library do with a file only a template references? → A: It counts as used, so it is
  never auto-deleted; but it is not auto-downloaded, because the download manifest is built from services
  dated today or later. The bytes arrive when a dated service uses the file. *(owner, 2026-10-30)*

No open markers remain.
