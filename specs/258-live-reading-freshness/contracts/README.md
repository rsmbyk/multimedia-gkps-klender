# Contracts: live reading freshness

**Spec**: `specs/258-live-reading-freshness/spec.md`

## Interfaces exposed by this slice

| Interface | Kind | Defined in | Consumed by |
| --- | --- | --- | --- |
| `GET /freshness/page/` | JSON endpoint | `contracts/http.md` | service and song pages |
| `GET /freshness/songbooks/` | JSON endpoint | `contracts/http.md` | songbooks sidebar |
| `GET /freshness/songs/` | JSON endpoint | `contracts/http.md` | songs sidebar |
| `GET /freshness/services/` | JSON endpoint | `contracts/http.md` | services sidebar |

## Not exposed

No write endpoint changes and no DRF serializer changes. List fragments remain the existing server-rendered HTML consumed by the shell's reconcile path.
