# Data Model: Media Library filter-pill hover

**Spec**: `specs/239-media-filter-pill-hover/spec.md`

## Entities

No persisted entity is added, removed or changed. The slice touches one CSS rule;
no model, migration, form, serialiser, endpoint or template is involved.

## Existing boxes and tokens the rule relies on

| Box / token | Current rule | Role in this slice |
| --- | --- | --- |
| `.media-library__chips` | `display: flex; align-items: center; gap: 7px; flex-wrap: wrap` | the `role="group"` filter row |
| `.media-library__chips button` | `padding: 7px 11px; border: 1px solid var(--divider); border-radius: 999px; background: transparent; color: var(--ink); font-size: 12px` | the five type pills and the Unused pill; base state |
| `.media-library__chips button[aria-pressed="true"]` | `background: var(--active-bg); color: var(--active-ink); border-color: var(--active-bg)` | selected state; untouched |
| `.media-library__chips > span` | `color: var(--head-ink)` | the centred dot; not a button, untouched |
| `--focus` | `#1C5C3C` light / `#7C9CF0` dark | hover border token |
| `--icon-hover-bg` | `rgba(31,31,29,.08)` light / `rgba(255,255,255,.09)` dark | hover fill token |

**Relationships**: the row contains five `[data-media-type]` buttons, a separator span
and `#mediaUnusedFilter`. `static/web/media-library.js:154` toggles `aria-pressed` on
click and never writes style. **Validation**: none. **State transitions**: rest → hover
→ rest on pointer movement; hover is ignored while `aria-pressed="true"`.

## Invariants

- Only border-color and background change for unpressed pills (FR-001, FR-003).
- A pressed pill keeps its accent fill, text and border under the pointer (FR-002).
- Box geometry stays 63.36 × 30 px at 1440 px in all three states (SC-003).
- No surface outside the filter row's unpressed buttons changes (FR-004).

## Not modelled

- No new CSS custom property, state flag or data attribute.
- No hover media query: the rule is a plain selector so the same-origin stylesheet
  can be asserted and the state driven in a browser probe.
