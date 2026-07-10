# Specs

Living specifications for this project. Process: [`docs/SDD.md`](../docs/SDD.md).

| Path | Purpose |
|------|---------|
| [`constitution.md`](constitution.md) | Project-wide guardrails (points at `docs/`) |
| [`_templates/`](_templates/) | Starter `spec.md` / `plan.md` / `tasks.md` |
| `<area>/<feature>/` | One folder per capability or change |

## Starting a new change

1. Copy `_templates/` into `specs/<area>/<short-feature-name>/`.
2. Fill `spec.md` → get human OK → `plan.md` → OK → `tasks.md` → OK.
3. Implement tasks with TDD; keep the spec updated if intent shifts.

`<area>` should align with changelog labels when possible (`songs`, `bible`,
`api`, `web`, `deploy`, `docs`, …).
