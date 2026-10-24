# Convergence: Hymn songbooks above a single separator, the rest A–Z

**Spec**: `specs/128-songbook-hymn-separator/spec.md`
**Passes**: 2 of 3

## Pass 1 — 2026-10-24

| Gap | Type | Requirement | Evidence |
| --- | --- | --- | --- |
| The empty-group guard is written on the shared `.group.is-hidden + .group`, so a filtered Alkitab testament or Tata Ibadah month also loses its floating rule — outside the Kidung panel the spec names. | `unrequested` | FR-005 | `static/styles/design/components.css` — the rule added below `.group + .group`; the Kidung E2E test exercises it on `#panelBody` only. |
| The spec's US1/AC4 and the mini-rail values described a state the Kidung panel never reaches. | `contradicts` | US1/AC4 | `static/web/reading.js:1125` — `miniPanel()` is called only from the Alkitab branch and the idle collapse's Alkitab branch; `:1155` sends Kidung to `closed`. Artifact at fault, not code. |

**Outcome**: 2 findings.

- The `contradicts` finding was fixed at the artifact on the same date: US1/AC4, FR-003, SC-003 and `## UI/UX`
  lost the mini values, and the Clarifications session records why. No code change.
- The `unrequested` widening is kept and recorded, not undone: the guard answers the same bug class on a rule
  the panel shares with Alkitab and Tata Ibadah, and a hidden group's separator floating above an unrelated list
  is the defect FR-005 exists to remove. It is named in the closing report so the owner can veto it.

## Pass 2 — 2026-10-24

Re-ran the traceability rows against the code: every FR has its component and its test, the three views and the
two saved-render call sites share one builder on each side, and the existing reading assertions are unchanged.

**Outcome**: Converged — nothing remains.

## Accepted gaps

<!-- none -->

## Cap reached

<!-- not reached -->
