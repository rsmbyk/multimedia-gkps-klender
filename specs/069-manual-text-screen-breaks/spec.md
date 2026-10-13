# Spec 069: Manual screen breaks for multiline Text entries

- **ID:** 069
- **Status:** Accepted
- **Item:** ITEM-072
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** minor

## Intent

Let the editor of an ordinary Tata Ibadah Text entry choose projector-screen breaks directly in the entry's preview modal.

## Scope

### In scope

- One row per written line in the existing preview modal, with hoverable gaps, clickable break dividers, and a mode indicator.
- Preview access for ordinary Text entries even when the reading pane does not clamp their text.
- A saved custom arrangement for one Text entry, shared by the projector page and live display refresh.
- A Reset breaks action in the modal footer that returns to automatic two-line grouping.

### Out of scope

- Song, Scripture, legacy, and single-screen Text entries.
- Changing text content to encode breaks, or changing the meaning of blank lines.
- New projection typography or layout controls.

## Domain rules

- A written line is a newline-delimited line in a Text entry. A blank line remains a mandatory boundary; it is not projected as text. Custom groups cannot cross one.
- **Default mode:** the existing two-line grouping is shown and used until a divider is changed. The modal names this mode explicitly.
- **Custom mode:** adding or removing a break changes the entry to custom mode. The modal names this mode explicitly, and the custom break positions are saved for this entry without opening its Create/Edit form.
- Default-mode breaks use a delicate, low-contrast line. Once the mode is custom, present existing breaks with the regular divider contrast.
- A break shows one uninterrupted line at rest, with no reserved space for a label. Hovering or focusing it changes the line's shade and reveals a centered “Remove break” label over the line; leaving it returns to the uninterrupted line. An empty gap reveals a dotted “Add break” line and label on hover or focus.
- Each eligible gap has a keyboard-focusable target as well as a hover target. Hover or focus reveals a prospective divider without changing the saved split. Clicking or activating a gap without a break adds one; clicking or activating a visible break removes it.
- On the first added custom break, that chosen gap becomes the anchor. In its blank-line-separated block, set the other breaks every two nonempty lines in both directions from that anchor. Other blocks retain their default two-line positions. Later toggles change only the chosen gap. Removing an existing default break as the first action removes that break and leaves the other default breaks in place.
- Each nonempty line appears exactly once, in its written order. Within a block between blank lines, a custom screen may contain one or more consecutive lines. A break can occur only between written lines.
- The modal's dividers and mode update immediately after each toggle. The Draft includes an interactive browser preview of that proposed interaction.
- A custom arrangement belongs to its Text entry only. Editing another entry does not change it.
- The entry's title continues to head each of its screens, and voice cues are resolved over the whole body before grouping so they carry across screens.
- A later text edit that changes the sequence of line and blank-line positions clears the saved custom arrangement and uses default mode; the next preview explains the reset. A wording-only edit that preserves that sequence keeps the breaks.
- Viewing the modal does not require edit permission. Only an authorized editor sees or can use the split controls. Other preview kinds remain read-only.
- The current trailing blank screen and next/previous navigation remain in place.

## Acceptance scenarios

### Scenario: First custom break sets a two-line cadence

- **Given** a Text entry with six nonempty lines in default mode
- **When** the editor hovers the gap after line one and clicks the prospective divider
- **Then** the mode becomes custom and breaks appear after lines one, three, and five
- **And** the projector shows screens containing lines 1, 2–3, 4–5, and 6
- **And** the saved text is unchanged.

### Scenario: Show a specific line alone

- **Given** a Text entry with four nonempty lines
- **When** the editor clicks the gaps before and after line two in the preview modal
- **Then** line two appears on its own screen and every line appears once in order.

### Scenario: Remove a displayed break

- **Given** a Text entry showing a break after line two
- **When** the editor clicks that divider
- **Then** that break disappears, the mode is custom, and the adjoining groups become one projector screen
- **And** other existing breaks stay where they were.

### Scenario: Divider feedback

- **Given** a Text entry in default mode
- **Then** its automatic breaks are delicate lines without visible labels
- **When** the editor hovers or focuses one
- **Then** that line changes shade and shows “Remove break” at its center
- **And** after the first change, remaining breaks use the normal divider contrast of custom mode.

### Scenario: Keep blank-line pauses

- **Given** a Text entry with a blank line between two blocks of text
- **When** the editor changes screen breaks in either block
- **Then** no projector screen contains lines from both blocks.

### Scenario: Existing entries retain their layout

- **Given** a Text entry without custom breaks
- **When** it is projected
- **Then** its nonempty lines appear in pairs, with a blank line ending the current screen, as before.

### Scenario: Reset an arrangement

- **Given** a Text entry with saved custom breaks
- **When** the editor presses Reset breaks in the preview modal footer
- **Then** the override is removed and the preview and projector use the default pairing.

### Scenario: Avoid stale breaks after editing text

- **Given** a Text entry with saved custom breaks
- **When** the editor saves text with a different line/blank-line pattern
- **Then** the old split is cleared and the entry returns to default mode
- **And** the preview modal explains why the split was reset.

### Scenario: Preserve speaker cues and live display

- **Given** a Text entry with speaker cues that continue across a screen break and an open projector
- **When** the editor changes a divider in the preview modal
- **Then** the projector refreshes to the saved screen sequence and the cue remains assigned to the correct lines.

### Scenario: Preview access and edit permissions

- **Given** a short Text entry whose text is fully visible in the reading pane
- **Then** it still offers a Preview action so its screen breaks can be configured
- **And** a viewer without edit permission can read the preview but cannot change the split.

## Traceability

- Domain/app tests: `multimedia/tatib/tests.py` (boundary validation), `multimedia/web/tests.py` (save/reset, stale requests, projector grouping, editor permissions), and `multimedia/web/test_speaker_voices.py` (speaker markup).
- E2E: `tests/e2e/test_text_screen_breaks.py` (modal, first-break cadence, reset, and live projector refresh); `tests/e2e/test_entry_preview.py` (existing preview kinds).
- Implementation: `multimedia/tatib/models.py`, `multimedia/tatib/screen_breaks.py`, `multimedia/web/reading/entries.py`, `multimedia/web/reading/views.py`, `multimedia/web/templates/reading/tatib.html`, `multimedia/web/templates/reading/_preview_modal.html`, `static/web/preview.js`, and `static/styles/design/components.css`.
