# Data model — spec 241

**Spec**: `specs/241-tatib-reorder-kept/spec.md`

No schema change. The slice reads and writes only data that already exists.

| Entity / field | Role in this slice |
| --- | --- |
| `ServiceEntry.pk` | identity of a movable sidebar row and its stage section (`data-entry-pk`) |
| `ServiceEntry.order_number` | the shared slot the reorder endpoint rewrites; options follow their choice |
| `TataIbadahItem.order_number` | legacy slots; those rows have `data-old-item-pk` and are deliberately outside `readNodes()` |
| `Song.sort_title`, `Song.modified` | rendered as `data-t` / `data-m` on real song rows; absent on contents rows |
| `nodes` (client cache) | pk → `[section, optional .entry__add]`, rebuilt at each `applyPaneOrder()` call |
| `drag` (client state) | the in-flight gesture; cleared before the pane is rewritten |

Invariants: every live entry appears once in `#chList`; every `ServiceEntry` has one
`section[data-entry-pk]` in `#readBody` (a break draws a divider instead); the order posted is
a permutation of the live entries' existing slots.
