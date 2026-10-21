# Tasks 120: Keep projector Go To current while online

- **Status:** Accepted
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

## Checklist

- [x] Spec accepted by Ronald.
- [x] Reproduce stale online song-title lookup with saved generation, server change, and subsequent manual sync.
- [x] Red: browser regression for a new song without reload; existing Go To tests cover Bible matching and query changes.
- [x] Green: one freshness check when Go To opens and current-query-safe suggestion update.
- [x] Verify offline/failed check, keyboard/click detours, TB/SIM names/codes, and no per-keystroke full sync.
- [x] Complete traceability, version/changelog; ITEM/board PR metadata follows PR creation.
- [x] Open stacked draft PR [#369](https://github.com/rsmbyk/multimedia-gkps-klender/pull/369) against Spec 119 while its CI is blocked.
- [x] Retarget `develop` after Spec 119 merged via #368.
- [x] Ronald explicitly waived remote CI for this merge because GitHub Actions locked the account before jobs could run; 47 projector browser tests passed locally against PostgreSQL.

## Done when

- [ ] Every acceptance scenario passes, with saved offline fallback intact.
