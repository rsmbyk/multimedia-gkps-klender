# Contracts: a media size reads in the unit that still shows its number

**Spec**: `specs/145-media-size-precision/spec.md`

## Interfaces exposed by this slice

none — the slice adds one page-local function, `window.gkpsFormatSize(bytes)`, and changes no HTTP
endpoint, payload or storage shape.

## Not exposed

The formatter is internal to the page bundle. A server-side formatter was considered and rejected
(`research.md` D004): two of the three surfaces are painted client-side from companion payloads.
