# Plan 062: System theme as the default appearance mode

- **Status:** Accepted
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-065
- **Bump:** minor

## Why

Readers should get an appearance suited to their device by default while retaining explicit Light and Dark choices.

## Scope / edges

**In:** Public reading pages, a three-choice theme control, existing local preference storage, and live system color-scheme detection.

**Out:** Editor and OBS surfaces, account-level preferences, server persistence.

The current `develop` branch already has Light and Dark palettes and a two-state switcher. The accepted Draft was first written against an older detached checkout; this plan uses the existing switcher and palettes. The Draft ID and ITEM ID were advanced to the next available consecutive numbers (062 and 065).

## Approach

Define the preference as `system | light | dark` in the existing `gkps-theme` key. With no valid saved preference, use `system`. Resolve the active palette from `prefers-color-scheme` only while the preference is `system`. Apply the palette before visible page content renders. Replace the two-state button with three labeled choices in the shared reading rail, retaining `#themeBtn` for the Dark choice and existing test hooks.

## TDD

- Domain/app tests: none; this is browser presentation behavior.
- E2E: Playwright tests for first visit, explicit override, persistence, and a live system theme change.

## Risks

- Applying the palette after render could flash the wrong colors. Initialize it early.
- Existing tests assume `#themeBtn` chooses Dark. Preserve that hook.
- Browser storage may be unavailable. Fall back to System without breaking the page.
