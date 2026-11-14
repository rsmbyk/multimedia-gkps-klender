# Fold: 190-sidebar-delete

**Date**: 2026-11-14
**Capabilities touched**: `reading` — `reading/R41` added (sidebar delete controls, confirmed delete, guards, on-stage navigation).

| Operation | ID | Detail |
| --- | --- | --- |
| added | reading/R41 | Delete controls beside edit on non-hymn songbook/song and Tata Ibadah service/template rows; confirmed delete in the shared modal with kind noun; GET confirm + POST delete endpoints (soft-delete for songs/songbooks, active-flag for services/templates); dated row hides its date during the reveal; on-stage delete returns to the parent list with history replaced |
| modified | — | none (R40 and earlier untouched) |
| removed | — | none |

**Before**: 40 requirements (R1–R40)
**After**: 41 requirements (R1–R41)

**Not folded — accepted gaps**: none.
**Behaviour change**: new user-visible capability, per spec (not a refactor).
**Header**: `last folded` → 2026-11-14, slices prepended `190-sidebar-delete`.

SDD-23 idempotent typed delta applied; no undeclared behaviour change.
