# Data model: an empty reading stage after deleting the open record

**Spec**: `specs/221-empty-reading-stage/spec.md`

None. The empty stage is a render state carried by a query flag on an existing parent-list URL. No
model, field, migration, serializer, API payload or stored preference is added or changed. The shell's
`data-read` / `data-home` attributes and the existing `#readName` / `#readBody` nodes carry it in the
DOM; the deleted record itself is untouched by this slice beyond the delete flow it already has.
