# Data Model: a small image or PDF page fills the stage

**Spec**: `specs/158-projector-media-fit/spec.md`

Nothing is stored: the fit and the pan are page state, like the showing screen (spec 119). The model
below is the state the projector keeps while a media screen is up, and the invariants the code must
hold. No Django model, no migration, no request body.

## Entities

### Media screen (existing, unchanged shape)

| Field | Type | Constraints | From |
| --- | --- | --- | --- |
| `[data-media-image]` / `[data-media-pdf]` / `[data-media-slides]` | host element | exactly one per media `.screen`; its `getBoundingClientRect()` is the stage the fit measures | FR-001, FR-002 |
| own size | `{w, h}` | image: `naturalWidth`/`naturalHeight` from the decoded blob; PDF: the page viewport at scale 1 | FR-001, FR-002 |

### Fit state (new, page-local)

| Field | Type | Constraints | From |
| --- | --- | --- | --- |
| `fitState` | `'fit' \| 'width' \| 'height'` | starts `'fit'`; set by `T`; reset when the active media host changes | FR-003, FR-004, FR-005 |
| `painted` | `{w, h}` px | `floor(own × scale)`; written to the element's inline width/height | FR-001, FR-002 |
| `overflow` | `{x, y}` px | `max(0, (painted − stage) / 2)` per axis | FR-009, FR-010 |
| `pan` | `{x, y}` px | `−overflow ≤ pan ≤ overflow`; `{0, 0}` on a fit or host change | FR-010 |

**Relationships**: one fit state belongs to the one media screen that is showing; leaving it (another
entry, a detour, the display off) drops it.
**Validation**: a fit is only computed when the media's bytes loaded and its own size is known; a
missing file keeps the missing icon and never enters this model.
**State transitions**: `fit → width → height → width …` by `T`; any state → `fit` when the host changes.

## Invariants

- The painted media never leaves a gap: `|pan.x| ≤ overflow.x` and `|pan.y| ≤ overflow.y` (FR-010).
- With `overflow` zero on both axes the element carries no transform and no `grab` cursor (FR-012).
- The scale is one of three values only — `min(byWidth, byHeight)`, `byWidth`, `byHeight` — so no state
  can stretch an image: the aspect ratio is the source's, always (FR-001).
- A press that pans never navigates, and a press that navigates never pans (FR-011).
- Nothing in this model is written to storage, the URL, the display channel or the server (spec
  assumption 7).

## Not modelled

- The corner cue: it keeps showing the filename and the page count, and gains no fit indicator
  (assumption 5).
- Per-page fit inside one document: one fit state covers the whole document, as the spec says, even
  though pages may differ in size.
- The reader's Preview dialog: it keeps its own sizing and its own clamp (assumption 4).
