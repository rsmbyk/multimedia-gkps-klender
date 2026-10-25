# Fold — A text entry's form is the media modal's large frame

**Slice**: `specs/133-text-modal-large-frame/`
**Folded**: 2026-10-25
**Capability touched**: `reading` (`docs/spec/reading.md`)

## Operations

| Operation | Requirement | What was written |
| --- | --- | --- |
| `added` | `R10` | A text entry's form is the media modal's large frame — the 840×760 box clamped to the window, the shared chrome (no content padding, a `20px 26px` title band at 21px over a 1px divider, 26px gutters with 14px between fields, an undivided action row at `14px 26px 20px`), the Text field taking the leftover height, the marker that decides the frame (`data-editor-size="large"` on text create/edit and media create, absent everywhere else), the 18px gutters and `16px 18px` title band below 650px, the dialog placed against the window rather than the document, and the text form's behaviour declared unchanged — with five scenarios |

## Counts

- `reading`: 9 requirements → **10** (`R1`–`R10`); `R10` is new, nothing renamed, nothing removed.
- Slices recorded on the capability: 7 → 8.
- `last folded`: unchanged at 2026-10-25 (the previous fold and this one share the date).

## Not folded — accepted gaps

None. Every requirement converged, and the rows that fell to `inspection` were checked by the probe's
printed values rather than deferred: `converge.md` records the numbers each one returned.

## Refactor check

Mostly a refactor with one behaviour change, and the behaviour change is the slice: the large frame's six
rules stopped keying on the media form's script hook and now key on what the form *is*, which draws two
new forms large; and the dialog's placement moved from document coordinates to the window. No stored
behaviour, no endpoint and no copy changed, so nothing outside `R10` moves.
