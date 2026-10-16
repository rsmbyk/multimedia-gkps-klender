# Plan 099: Keep the selected Bible Version across menu switches

- **Status:** Accepted
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-099
- **Bump:** patch

## Why

The reader reports that the TB/SIM choice is forgotten when the reading stage is on another section and they return to Bible through the sidebar. Current `develop` keeps a transient `selectedEdition` in the reading shell and reapplies it after stage swaps; Spec 092 covers chapter navigation and refresh reset, but does not explicitly test this menu round trip. This slice makes that path an acceptance case and corrects the shell only if the regression test reproduces the reported loss. The accepted cases pass against current `develop`, so no runtime correction is needed; this slice adds regression coverage for the menu paths.

## Scope / edges

**In:**

- Carrying a deliberate TB/SIM choice through in-page switches among Bible, Kidung, and Tata Ibadah menus, then applying it to the next Bible chapter opened from the Bible sidebar.
- Online and saved-copy reading shells, chapter navigation, browser Back/Forward within the same tab, and the existing fallback when a chapter has no verses for the selected Version.
- Keeping the choice local to the currently loaded tab. A full page load or a separate new tab starts from the route's usual initial edition (TB by default).

**Out:**

- Persisting the choice across refreshes, separate tabs, browser sessions, cookies, storage, or server-side settings.
- Translation controls in passage editors, Tata Ibadah entries, or projector sources.
- Changing the initial TB default, explicit `?ed=` deep-link behavior, or no-JavaScript navigation.

## Approach

Keep the last deliberate Bible Version choice as transient state owned by the live reading shell. Reapply it when a Bible verse page is installed after a menu or section switch, including when the page uses saved library data. Start a fresh choice from the route's existing initial edition on a full document load. If a selected Version is unavailable for the arriving chapter, preserve the existing display fallback without erasing the tab's preference for a later chapter that supports it.

## TDD

- Domain/app tests: N/A; the choice is browser-side reading state.
- E2E: Extend `tests/e2e/test_reading.py` for menu round trips, Back/Forward, reload, and a separate tab. Extend `tests/e2e/test_offline_library.py` for the saved-copy menu round trip.

## Risks

- Replacing the reading stage while another menu is active must not discard the tab's choice, and applying it must update both the visible verse text and Bible sidebar labels.
- A refresh must discard an in-memory choice while existing explicit `?ed=sim` deep links and no-JavaScript behavior continue to work.
- A chapter without SIM must keep its current fallback behavior without overwriting the remembered SIM preference.
