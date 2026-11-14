# Data Model: A text entry is written and edited in the media modal's large frame

**Spec**: `specs/133-text-modal-large-frame/spec.md`

## Entities

`n/a — the frame has no entity, no field and no stored value.`

The slice changes how one server-rendered fragment is drawn; nothing about a service entry is written
differently, and no migration is involved. What exists instead of a model is the two attributes the DOM
carries, recorded here because the plan and the tests both depend on them:

| Attribute | Written on | When | Read by |
| --- | --- | --- | --- |
| `data-editor-size="large"` | the entry form (`<form class="editor__form">`) | `kind == 'text'`, or `kind == 'media'` with no entry | `components.css` (`:has(...)`) |
| `data-editor-grow` | the Text field (`<div class="editor__field">`) | the text form, create and edit | `components.css` (`flex: 1` chain) |

**Relationships**: `none` — both attributes are presentational and are not persisted.

**Validation**: `none` beyond the template's own condition; a form without the marker draws the compact
frame, which is the correct behaviour for every other kind (FR-004).

**State transitions**: `compact → large` happens only by the server rendering a text or media-create
form; there is no runtime toggle, so a 400 re-render (which replaces the dialog body with a fresh
fragment) lands in the same state.

## Invariants

- A form that carries `data-editor-size="large"` is drawn 840×760 clamped to the window, and its fields
  are inset 26px — the same values the media create form uses (FR-001, FR-002).
- A form that does not carry it is drawn 480 wide with 22px content padding (FR-004).
- `data-editor-grow` only appears inside a large form, so the `flex: 1` chain never reaches the compact
  dialogs (FR-003, FR-004).

## Not modelled

- The dialog's position against the viewport (FR-007). It belongs to the dialog element, not to a form,
  and no attribute expresses it — the rule is `.editor { position: fixed }`.
- The breakpoint behaviour at 650px (FR-005): a media query, not state.
