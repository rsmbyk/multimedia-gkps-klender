# Research: Verse modal header draws one rule

**Spec**: `specs/226-verse-modal-header-rule/spec.md`
**Unknowns remaining**: 0

## D001 — Where the second line comes from

- **Decision**: remove `border-bottom` from the large-editor `.editor__title` rule; keep the
  header's own border as the only rule.
- **Rationale**: at `static/styles/design/components.css:541` the selector
  `.editor:has([data-editor-size="large"]) .editor__title` has specificity (0,3,0) and beats
  `.editor__head .editor__title` at `:689` (0,2,0). Spec 195 added the head reset but not a
  matching large-dialog override, so the title still paints the border spec 189 gave it.
- **Alternatives considered**: raising the head reset's specificity with `!important` was rejected
  because it hides the bad selector and keeps the 20px bottom padding; deleting the whole title
  rule was rejected because it would also drop the 21px type the dialog keeps.
- **Provenance**: research — computed styles on the live route at `4ad9e6ff`.

## D002 — The target spacing

- **Decision**: move the title's 20px bottom padding to the large head as
  `padding: 20px 26px 14px`, leaving the title with `padding: 0`.
- **Rationale**: the owner asked for the gaps to be "just like the other modals's". The non-verse
  `New song` editor measures 16px from title text to divider; the candidate measures 16.5px with
  the 21px title's line box. The 26px side inset and 21px top inset stay, so the title keeps its
  alignment with the `Lyric` label.
- **Alternatives considered**: dropping only the bottom padding leaves a 17.5px gap; tightening
  the head to 8px leaves 11.5px. Both were offered and the owner chose the other editors' rhythm.
- **Provenance**: owner decision — measured reference at `4ad9e6ff`.

## D003 — What stays unchanged

- **Decision**: keep the head's 16px bottom margin and the large first field's 14px top margin.
- **Rationale**: they produce the 30px divider-to-label gap in the large dialog; the owner's
  request named the title-to-border gaps only.
- **Alternatives considered**: matching the other editors' 16px divider-to-label gap would remove
  the large form's 14px field margin and move the textarea up, a scope the report did not ask for.
- **Provenance**: research — computed boxes on both dialogs.

## D004 — Verification shape

- **Decision**: a new Playwright E2E file measures both dialogs and the narrow viewport; the live
  probe stays beside the spec as gate material.
- **Rationale**: the requirement is a painted state, and the repo's acceptance tests for visible
  behaviour are Playwright through `StaticLiveServerTestCase`.
- **Alternatives considered**: a CSS-text assertion alone would pass while the title still painted
  a second rule through a different selector.
- **Provenance**: research — repo convention in `docs/PROCESS.md`.

## Open

<!-- empty when Phase 0 is finished -->
