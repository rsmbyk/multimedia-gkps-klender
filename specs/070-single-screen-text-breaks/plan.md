# Plan 070: Manual breaks for Single-screen Text entries

- **Status:** Accepted
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Visual preview:** [./preview.html](./preview.html)
- **Item:** ITEM-073
- **Bump:** minor

## Why

A Single-screen Text entry currently puts its entire body on one projector screen, fitting the font and shortening the end if it cannot fit. An editor sometimes needs selected lines or paragraphs to appear on separate screens without changing the written text or replacing the entry.

## Scope / edges

**In:** Reuse the accepted Text-entry break controls from Spec 069 in the preview modal for Single-screen Text entries; keep one screen as their default; save a custom arrangement for each entry; apply it to the projector and live display.

**Out:** Changing ordinary Text's two-line default; song, Scripture, legacy, and section-break entries; editing words in Preview; changing the Single-screen entry label or adding projection typography controls.

## Approach

Make Preview available for every Single-screen Text entry. In default mode show its written lines without any divider and put `Default · 1 screen` beside `Screen breaks` in the footer. Blank lines remain paragraph spacing on that screen. The same hover, focus, Add break, Remove break, custom mode, and Reset breaks controls as Spec 069 appear in Preview. The first added break divides the content into exactly two fitted screens; later clicks toggle only their chosen boundary. A break may separate paragraphs, while blank lines alone never create a screen break for this entry kind.

Store optional boundaries in the existing `ServiceEntry.screen_breaks` field. `null` keeps the kind-specific default: pairs for ordinary Text, one screen for Single-screen Text. For a custom arrangement, split the Single-screen body at saved boundaries, keep every nonempty line once, and retain its title and speaker cues on each resulting screen. Fit each resulting screen with the existing Single-screen rules. Editing the line/blank-line pattern invalidates saved boundaries and returns to one-screen default with the existing reset notice. Only an authorized editor can change breaks.

The accepted Spec 069 modal is the visual and interaction reference. The linked Draft preview shows the Single-screen default and the first custom break before product code changes. The owner asked to implement this accepted slice on the existing Spec 069 feature branch and PR #323.

## TDD

- Domain/app tests: Kind-specific defaults, legal boundaries across paragraphs, custom grouping, blank-line behavior, stale edits, save/reset permissions, and voice continuity.
- E2E: Modal default, first-break two-screen split, toggle/reset, keyboard access, and live projector update.

## Risks

- The kind remains named Single-screen after a deliberate custom split. The footer makes the override visible without renaming existing entries.
- A very large custom group can still need the current Single-screen fitting and overflow safeguard. Verify that smaller groups expose lines that were previously shortened.
