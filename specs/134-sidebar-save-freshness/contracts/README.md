# Contracts: Keep reading views current after sidebar edits

**Spec**: `specs/134-sidebar-save-freshness/spec.md`

## Interfaces exposed by this slice

none — the slice adds no external HTTP, API, persistence, or browser-extension interface. It reuses the existing same-origin reading routes and internal `editor:saved` browser event.

## Not exposed

No new public endpoint, request/response format, database contract, or cross-application event is introduced. The existing internal save event remains an implementation seam within the public reading shell.
