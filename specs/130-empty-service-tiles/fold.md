# Fold — 130-empty-service-tiles

**Target**: `docs/spec/reading.md`, requirement `R6`.

Written: R6 as the behaviour the three renderers share (centred block, five square icon-only tiles, three and
two below 300px of column, the label kept as the name and the tooltip, the two non-server renderers included,
items present untouched). Header updated: `last folded: 2026-10-25`, `slices` gains `130-empty-service-tiles`.

No undeclared behaviour change was found while folding: what the code does and what R6 says are the same
thing, including the two width regimes and the scoped margin rules.

Idempotent: re-running the fold would produce the same R6 paragraph; nothing else in `reading.md` was edited.
