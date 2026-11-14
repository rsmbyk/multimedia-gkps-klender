# Spec: Distinct song label typography

- **ID:** 060
- **Status:** Accepted
- **Item:** ITEM-062
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** patch

## Intent

Make the song entries in the service-order sidebar shown in the owner's screenshot easier to scan by distinguishing hymn book and song number, song title, and lyric verse selection.

## Scope

### In scope

- First line: hymn book abbreviation and song number together as a compact semibold label (12px / 600), followed by the song title in regular primary text (14px / 400), separated by 8px.
- Second line: the existing lyric verse label and numbers, such as `Bait 1–7`, in smaller text (12px / 400), aligned with the first line's content. Use the muted theme color in light mode; use the primary text color in dark mode for readable contrast.
- Use the existing font and palette; preserve WCAG AA text contrast on normal, hovered, and selected rows in both themes. Typography must distinguish the parts without relying solely on color.
- Long titles wrap within the content column; lyric verse selection stays in a separate block below the complete title.
- Entries without a hymn book reference show the title without an empty label or extra gap.

### Out of scope

- Changes to wording, verse-range formatting, song data, ordering, filtering, projection output, or navigation behavior.
- Restyling Bible passages, text items, section breaks, row numbers, or drag handles.
- Adding dependencies or reconstructing the entire screenshot's sidebar if it is absent from this checkout.

## Domain rules

No domain rule changes. Render the three parts from structured fields if available; avoid inferring hymn book references by splitting arbitrary title text. Preserve existing safe text rendering.

## Acceptance scenarios

### Scenario: Song with a hymn book reference

- **Given** the entry `HAL 1 Jahowa Sihol Pujionku` with `Bait 1-7`,
- **When** the sidebar displays it,
- **Then** `HAL 1` has compact semibold styling, the title has regular primary styling, and `Bait 1-7` has smaller muted styling on the second line.

### Scenario: Song without a reference

- **Given** `Mars Sekolah GKPS` with `Bait 1`,
- **When** it is displayed,
- **Then** its title and lyric verse selection have the same corresponding styles without an empty reference label.

### Scenario: Narrow panel and selection

- **Given** long titles and both selected and unselected song entries,
- **When** the panel is approximately 404px wide as in the screenshot or narrower,
- **Then** text wraps without overlapping row numbers or drag handles, lyric verse selection stays below the title, and all parts remain readable.

### Scenario: Existing interactions

- **Given** styled song entries and other service items,
- **When** the operator filters, selects, or reorders entries,
- **Then** existing behavior and non-song styling are preserved.

## Traceability

- Domain/app tests: not required unless implementation introduces a data-formatting rule.
- E2E: `tests/e2e/test_song_label_typography.py` — Django StaticLiveServerTestCase and Playwright verify hierarchy, wrapping, theme contrast, filtering, and link behavior.
- Implementation: `multimedia/web/reading/views.py`, `multimedia/web/templates/reading/_toc.html`, and `static/styles/design/components.css`.
