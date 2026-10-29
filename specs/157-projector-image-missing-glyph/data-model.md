# Data Model: the projector's image placeholder waits for the image to fail

**Spec**: `specs/157-projector-image-missing-glyph/spec.md`

Nothing stored changes and nothing is stored here at all. What this slice models is one element's
visibility across three states, in one screen at a time.

## Entities

### Image screen

| Field | Type | Constraints | From |
| --- | --- | --- | --- |
| `data-media-image` | attribute, sha256 | exactly 64 lowercase hex, rendered by the server from `screen.image_sha256` | FR-001, FR-002 |
| `.screen__image` | `<img>` | no `src` and `hidden` until the bytes arrive; one per screen | FR-001 |
| `.screen__image-missing` | `<svg>` | `hidden` unless a load has failed; `display: none` while hidden; 80×80, `aria-hidden` | FR-001, FR-004 |
| `.is-active` | class on `section.screen` | exactly one screen at a time; the placeholder is only read on this one | FR-002, FR-003 |

**Relationships**: one service screen → at most one image box → one picture and one placeholder. The
box is the only element that holds both, and the two never paint together.
**Validation**: a screen whose bytes did not arrive keeps its `<img>` without `src`; a screen whose bytes
did keeps its placeholder carrying `hidden` (FR-001, FR-002).
**State transitions**: `pending → loaded` (the fetch resolves and the object URL is set) · `pending →
failed` (the fetch rejects, the response is not `ok`, the bytes are not an image, or the player errors) ·
`failed → pending` (the screen stops being active; FR-003). `loaded → pending` happens with the screen's
own clear, not with this slice's change.

### Placeholder

| Field | Type | Constraints | From |
| --- | --- | --- | --- |
| `hidden` attribute | presence | the only switch; the property of the same name does not exist on an SVG element | FR-004 |
| box | 80×80 px | takes no space while hidden (`display: none`), so the picture's own box is what the row centres | FR-001 |
| drawing | 60×65 px inside the box | `viewBox 0 0 48 48`: the frame is inset 7/48 horizontally and 5/48 vertically | FR-006 |

## Invariants

- **Picture and placeholder are never painted together.** One of the two states holds, or neither
  (FR-001, FR-002).
- **An active image screen with a loaded picture is centred on the stage's middle.** The placeholder is
  out of the flow, so nothing of it contributes to the row's width (FR-001, SC-001).
- **Every placeholder in `projector.html` is hidden by default and toggled by its attribute.** Image,
  audio, video, PDF and slides — one mechanism, five places (FR-004).

## Not modelled

- **The object URL's lifetime** — `imageUrl` is revoked in `clearImageScreen`, unchanged; the model only
  says the picture is hidden once the screen is left.
- **The fetch itself** — `window.GKPSMediaImage.load` (`static/web/media-image.js`) is untouched: the same
  request, the same abort signal, the same MIME sniffing.
- **The bytes and their identity** — a sha256 in the companion (`multimedia/local_media.py`); nothing about
  storage, upload or the media library's own model changes.
