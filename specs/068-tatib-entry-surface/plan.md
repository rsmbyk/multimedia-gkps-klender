# Plan 068: Subtle surface for Tata Ibadah entries

- **Status:** Accepted
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-071
- **Bump:** patch

## Why

The owner wants the right-hand service editor's entry areas visible without making the page feel decorated. A live preview of `/tatib/142/` was iterated through border strength, fill strength, and padding. The selected result uses a faint fill and a slightly clearer 1px outline.

## Scope / edges

**In:** Tata Ibadah entry boxes with controls and section-break boxes in the new reading UI; light, dark, and system-selected theme appearances.

**Out:** Middle section list, sidebar, add rows, other reading types, legacy pages, and content or data changes.

## Approach

Style `.tatib__item--acts` and `.tatib__eos` in `static/styles/design/components.css`, with theme values in `static/styles/design/tokens.css` if shared variables keep the rules clearer. Use the exact fill and inset-outline values in the spec. Preserve the existing 9px corners and hover/focus/modal-origin fill. Set entry padding to 8px top/right/bottom and 12px left; retain controls at `top: 8px; right: 8px`. Match the preview's 56px minimum box height. Scope the rules to Tata Ibadah so other reading pages are unaffected.

## TDD

- Domain/app tests: N/A; visual CSS change.
- E2E: Targeted Tata Ibadah entry-control, hover, and section-break checks; inspect computed styles and layout in both themes and a narrow viewport.

## Risks

- Added vertical padding can increase row height and change where text wraps. Verify short and long entries, section breaks, and add-row gaps.
- A base fill must not override the existing stronger hover/focus/modal-origin fill.
