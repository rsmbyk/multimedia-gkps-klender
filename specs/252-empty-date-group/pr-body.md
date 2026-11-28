Deleting the last row of a grouped sidebar left its heading painted. The shared delete path now retires
the section when no rows remain and hides it when a filter has hidden every survivor; template mode no
longer emits an empty `Templates` group. Service date buckets, templates and songbook groups follow the
same rule; the other grouped surfaces were surveyed and left untouched.

Four E2E pins go red on unmodified develop and green here; 13 neighbouring E2E and 69 targeted unit
tests are green. Live control/preview probes at ports 8776/8777 confirm the frozen UI/UX counts.

Refs #648
Card `ITEM-269` — In review
Spec `252` — Accepted; Converged and Folded into `reading/R64`.
