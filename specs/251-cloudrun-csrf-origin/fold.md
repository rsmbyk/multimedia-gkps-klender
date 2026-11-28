# Fold: Cloud Run writes pass CSRF

**Capability**: `docs/spec/deployment.md`
**Folded at**: 2026-11-28

## Delta

| Type | Requirement | Change |
| --- | --- | --- |
| `added` | `R1` | `deployment` created with the requirement that a forwarded HTTPS request is secure, so same-origin writes pass CSRF; without the header the WSGI scheme stands. |

## Drift guard

- **Files changed in this capability**: `docs/spec/deployment.md` (new file).
- **Declared no behaviour change**: no — writes behind the TLS-terminating proxy now reach their
  views instead of being rejected before them. No endpoint, model, template or static asset changed.
