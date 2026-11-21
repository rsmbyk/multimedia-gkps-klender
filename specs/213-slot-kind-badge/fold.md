# Fold 213: a slot states the kind it resolves to

**Date**: 2026-11-21 · **Capabilities touched**: `reading`

| Capability | Operation | Requirement | Before | After |
| --- | --- | --- | --- | --- |
| `reading` | modified | R35 — A template carries fill-ins and choices | the requirement ended at "such a choice cannot be settled at generation" | + one paragraph stating the kind badge, its geometry, its four glyphs, the no-replace / `aria-hidden` / no-height / fill-state clauses, the unreadable-kind rule, and two new scenarios |

**Counts**: requirements 37 → 37 (one modified, none added, none removed) · scenarios in R35 2 → 4.

**Header**: `last folded` already read `2026-11-21`; `slices` now leads with `213-slot-kind-badge`.

## What was deliberately not folded

- **The two accepted gaps in `converge.md`** — there are none to exclude: F7 is a wording note inside a
  requirement that was folded, and F12 is a comment fixed in the same pass.
- **`docs/spec/reading.md` R35's existing sentence** "its mark in the gutter" (about a choice's
  option rows) was left exactly as it stands. It describes option rows, not the slot's own mark, and
  the option rows still carry no mark — a mismatch noted in the card's Notes and explicitly out of
  scope here. Folding a change to it would claim work this slice did not do.
