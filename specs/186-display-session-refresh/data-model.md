# Data Model: a surface re-reads the session it is showing

**Spec**: `specs/186-display-session-refresh/spec.md`

`n/a` — the stored shape is untouched. The slice adds no entity, no field and no document: it makes
existing readers read the same object again at three moments. `display-state/R3` (Fold) records the
rule, not a shape.

The state it re-reads is the one `docs/spec/display-state.md` R1 and R2 already pin:
`{service, screen, on, translation, at, session, goto}`.
