# Tasks 112: Temporary media handoff

- **Status:** In progress
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order. -->

## Checklist

- [x] Spec Accepted by the project owner, including its owner review points
- [x] Rebase the existing `feat/112-temporary-media-handoff` worktree onto current `develop` and resolve conflicts before implementation
- [x] Red — domain tests for cloud identity, verified upload/expiry, download authorization, and date eligibility
- [x] Provision private R2 Standard bucket and bucket-scoped Object Read & Write token; configure secret values in Vercel and local Django Compose without committing them (bucket smoke passed and the scoped eight-day production lifecycle rule was verified on 18 October 2026)
- [x] Green — server cloud metadata, narrowly scoped R2 presigned operations, expiry/cleanup command and schedule, lifecycle backstop, and relevant migrations/configuration
- [x] Add R2 health/configuration check and a temporary-object upload/GET/delete smoke test; confirm failed/missing configuration leaves local library usable (live bucket smoke passed on 18 October 2026)
- [x] Red — companion tests for durable jobs, cancellation, browser-close survival, restart failure, deduplication, protected deletion/cleanup, persistent bounded retry, and atomic hash-verified download
- [x] Green — companion transfer API/worker and named-volume persistence
- [x] Red — browser/E2E tests for library controls and untitled reference links, transfer modal/sidebar sessions, service status, light/dark and responsive behavior
- [x] Green — Media Library, sidebar, and Tata Ibadah UI from the approved preview
- [x] Verify local targeted Django/companion tests and the relevant single E2E classes; let full-suite/browser E2E run in push/CI
- [x] Document Cloudflare bucket/token setup, Vercel/Compose variables, seven-day cleanup and eight-day lifecycle backstop, cost limits, credential rotation, and operator workflow in `docs/local-media-companion.md`
- [x] Fill Traceability in `./spec.md`
- [x] Set `bump` on the ITEM and spec header
- [x] If bump is not `none`: `VERSION`, changelog `## [X.Y.Z]`, and `release_version` in **this PR**
- [x] Update ITEM + [`backlog/board.md`](../../backlog/board.md) in **this PR** (In review while open; Done before merge)
- [x] Conventional Commit + draft PR linking `./spec.md` (same PR; extra commits fine)

## Done when

- [ ] All acceptance scenarios in spec.md hold
- [ ] Tests named above are green
- [ ] Board, tasks, and version (if any) are complete in this PR
