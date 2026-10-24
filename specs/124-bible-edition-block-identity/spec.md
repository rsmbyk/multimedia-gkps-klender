# Feature Specification: Keep a chapter's verse text when the reading page updates in place

**Slice**: `specs/124-bible-edition-block-identity`
**Branch**: `fix/124-bible-edition-block-identity`
**Created**: 2026-10-24
**Status**: Accepted (owner, gate 1, 2026-10-24)
**Input**: "when you open a passage whose name is the same for both translations, the verse text is gone. only after you refresh on the same page the text appear" (sent with a screenshot of `/bible/8/1/` showing `Rut 1`, TB selected, and no verse text)

## User Scenarios & Testing

### US1 — Read a chapter whose two translations share a book name (P1)

**Why this priority**: through the normal sidebar path these chapters show no text at all, and only a
reload recovers them; the translation switch stops responding as well, so the reader is stuck on an
empty page.

**Independent Test**: open any chapter of another book, then open Rut 1 through the sidebar; Rut's
verses appear on the stage without a reload.

**Acceptance scenarios**

1. **Given** the stage is showing a Bible chapter, **When** the reader opens a chapter of a book whose TB and SIM names are identical through the sidebar, **Then** that chapter's verse text is visible and matches a direct load of the same page.
2. **Given** such a chapter is on the stage, **When** the reader opens another chapter of the same book, **Then** the new chapter's verse text is visible without a reload.
3. **Given** such a chapter is on the stage, **When** the reader selects SIM and then TB, **Then** each translation's own text appears in turn.

### US2 — Nothing else changes (P2)

**Why this priority**: the fault sits in how an in-place update reconciles the page, a path every
reading page and the saved library share, so the fix must not disturb what already works.

**Independent Test**: browse a book whose two names differ and reload a same-name chapter; both look
and behave as they do today.

**Acceptance scenarios**

1. **Given** a book whose TB and SIM names differ, **When** the reader browses its chapters, **Then** the text and the translation switch behave as before.
2. **Given** any chapter of a book whose names match, **When** the reader loads or reloads its URL directly, **Then** the page renders exactly as it does today.
3. **Given** a saved copy of such a chapter, **When** the reader opens it through the sidebar while online, **Then** the settled view shows the verse text.

### Edge Cases

- **When** only one translation has text for the chapter **Then** that translation is shown and the other is not offered.
- **When** SIM is the selected translation before an in-place move **Then** the new chapter keeps SIM visible.
- **When** the two translations name the book differently **Then** behaviour is unchanged.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | An in-place chapter opening leaves one mounted block per translation that has text, with the translation a direct load of that page would show visible and the other hidden. | `new: reading-navigation` |
| FR-002 | Moving between chapters of a book whose two translations share a name keeps the verse text visible and keeps the selected translation. | `new: reading-navigation` |
| FR-003 | After any in-place move, the translation switch still reaches every mounted translation. | `new: reading-navigation` |
| FR-004 | Direct loads, reloads, books whose names differ, and the saved-library reading view are unchanged. | `new: reading-navigation` |

### Key Entities

- **Edition block** — the reading stage's per-translation container for one chapter: that translation's
  verses and section headings, shown when its translation is selected and hidden otherwise. A chapter
  has at most two, one per translation that has text.
- **Book translation** — a book's name and abbreviation in one version. It supplies an edition block's
  label, and two versions may supply the same label.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | A same-name chapter opened through the sidebar shows its verse text without a reload | home → Alkitab → Rut → chapter 1 on the running site: the stage's visible text is non-empty and matches a direct load of `/bible/8/1/` |
| SC-002 | Moving between that book's chapters keeps the text and the selected translation | click the next chapter: the stage shows the new chapter's text, and SIM stays selected when it was selected before the move |
| SC-003 | Books whose names differ, direct loads, and the saved library are unaffected | the existing edition-navigation and saved-parity browser tests pass unchanged |

## UI/UX

`n/a — nothing visible changes: a direct load already renders these chapters correctly, so layout, type, colour, spacing, states and motion stay as they are.`

## Assumptions

- Every in-place move that updates the reading stage is in scope, not only the first opening after a
  full load — the reported symptom follows a page that is already open.
- Every book whose two translations share a name is affected, not only Rut — the sidebar shows the same
  pair for Ezra, Nehemia and others.
- The saved-library reading view shares the stage markup, so it is covered by the same behaviour and
  needs no separate design.

## Clarifications

### Session 2026-10-24

- No open question: the request names the trigger (a book whose two translations share a name) and the observable (no verse text until a reload), and the reproduction confirms both.
- Q: how does the fault appear on the running site? → A: a direct load of `/bible/8/1/` shows Rut 1 in TB with its verses; opening chapter 2 from the chapter sidebar leaves the stage empty until that URL is reloaded. A book with distinct names (Kejadian / 1 Musa) browsed the same way keeps its text.
