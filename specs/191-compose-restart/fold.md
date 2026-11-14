# Fold: Stack Restart Policy

**Capability**: `docs/spec/local-stack.md`
**Folded at**: 2026-11-14

## Delta

| Type | Requirement | Change |
| --- | --- | --- |
| `added` | `local-stack/R3` | The stack returns when the daemon restarts — every always-on service (`web`, `db`) declares `unless-stopped` beside media's existing policy, and a deliberate stop stays stopped. |

## Drift guard

- **Files changed in this capability**: `docker-compose.yml`, `tests/test_docker_compose.py`
- **Declared no behaviour change**: no — the behaviour change is exactly the `added` delta above
  (R3); no other capability behaviour was touched.
