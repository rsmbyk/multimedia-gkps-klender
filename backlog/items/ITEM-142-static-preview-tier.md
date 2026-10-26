---
id: ITEM-142
status: in review
title: 'Count a static page built from the real components as a preview'
type: chore
priority: P2
effort: S
created: 2026-10-26
updated: 2026-10-26
spec:
branch: docs/process-static-preview
pr:
issue: https://github.com/rsmbyk/multimedia-gkps-klender/issues/395
closed_at:
closed_reason:
bump: none
release_version:
---

# ITEM-142: Count a static page built from the real components as a preview

## Summary

The grammar's preview rule required a live preview served from the project, with a `MOCKUP` page
only as a labelled fallback. The owner amends it: a preview does not need a duplicate server — one
or more HTML pages assembled from the project's real components are a preview in their own right.
This card carries that amendment into `docs/PROCESS.md` and the preview template at vintage
2026-10-26.

## Notes

- **Grammar source:** `SDD-06` and the gate-1 materials of `SDD-09`; the SDD parent's 2026-10-26
  history entry retracts the 2026-10-20 clause *"it must run, served from the project"* and the
  2026-10-22 `MOCKUP` tier, both left visible in the record.
- **Rule now:** one tier, two shapes — **live** (served from the project) and **static** (pages
  assembled from the real templates, class names, stylesheets, tokens and assets, opened directly,
  no server of its own and never a duplicate of the project's dev server).
- **Bound stated with it:** a static page cannot show what fetches — server-rendered context, the
  API, uploaded media — so a slice that changes one of those is previewed live.
- **Unchanged:** every `## UI/UX` state reachable by hand; the real materials only, since an
  approximation is a different design; screenshots, static images and recordings are still not
  previews.
- **Template:** `specs/_templates/preview/README.md` records the shape and how to open it, replacing
  the mandatory route and serving command.
- **Regeneration:** `emit_process.py`; the page diff is the vintage stamp, `SDD-06` and `SDD-09`
  only, with the five `repo:` blocks byte-identical.
- No `VERSION` change and no changelog line: documentation only, `bump: none`.

## Acceptance sketch

- `verify_process.py`: 77/77 rule IDs, verbatim text, vintage 2026-10-26, balanced `repo:` markers,
  `AGENTS.md` clean, templates matching the grammar — exit 0.
- `docs/PROCESS.md` diff touches the version stamp and the two SDD rules, and nothing else.
- `specs/_templates/preview/README.md` byte-identical to the template block in the grammar.
- ADR 0006 names the same vintage as the page.

## Links

- Spec: —
- Related items: ITEM-135 (the page was last regenerated at vintage 2026-10-25)
