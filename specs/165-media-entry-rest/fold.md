# Fold: a media entry ends on a rest like every other entry

**Slice**: `specs/165-media-entry-rest` · **Date**: 2026-10-29 · **Capability**: `projector`

## Operations

| File | Operation | What |
| --- | --- | --- |
| `docs/spec/projector.md` | **added** | **R11 — A media entry ends on the built-in rest every other kind ends on**, with four scenarios (a picture ends on a rest; four pictures in a row; an entry whose file is gone; a service that ends on a picture). The header moves `last folded` to 2026-10-29 and prepends `165-media-entry-rest` to `slices`. |

## Counts

| | before | after |
| --- | --- | --- |
| requirements in `projector.md` | 10 (R1–R10) | 11 (R1–R11) |
| scenarios in `projector.md` | 35 | 39 |
| capability files touched | — | 1 (`projector`) |

`reading.md` and `media-library.md` are untouched: the change is what the projector builds, not what the
stage draws or the library stores. Spec 058's rule predates the capability tree (the file starts at spec
136) and is not folded anywhere, so R11 states the extension and cites 058 rather than duplicating it.

No behaviour change was left undeclared.
