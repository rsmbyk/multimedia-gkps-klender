# Data Model: Retired Addresses

**Slice**: `specs/194-legacy-route-retirement` · **Phase 1** · **Written**: 2026-11-14

**None.** The slice changes which addresses answer and where they send the request. There is no
entity, no model, no migration and no stored mapping: the retirement is a Python tuple read at
import time, and `/obs/blank` is a document with no state.

Deliberately not invented (SDD-23: Fold cannot invent intent): the capability tree gains
`docs/spec/routing.md` at Fold, which is bookkeeping against the approved behaviour, not a data
shape. A database-backed redirect table (`django.contrib.redirects`) was considered and rejected in
research D001 — nine static addresses do not earn a migration and an admin surface.
