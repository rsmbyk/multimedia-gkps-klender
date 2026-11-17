# Data model: The dock's bucket head owns the strip above its label

**Spec**: `specs/197-dock-bucket-head-pin/spec.md`

**No entities.** The slice changes where a sticky box starts inside the picker's scroll body and how much air
sits above a bucket's label. No model, migration, fixture, template or script is touched; nothing is stored or
fetched, and the existing `TataIbadah` / `ServiceEntry` rows the page reads are unchanged.

The only "shape" involved is the box model below, and it lives in the stylesheet:

| Box | Before | After |
| --- | --- | --- |
| `.dock__body#pickBody` | `padding: 4px 8px 10px` | `padding: 0 8px 10px` |
| `h3.group__head` | `padding: 10px 6px 7px` | `padding: 14px 6px 7px` |
| `#pickBody section + section` | — | `padding-top: 12px` |