# Process

What this project uses:

| Area | Choice |
| --- | --- |
| Specification | Specification-driven development with Spec Kit |
| Tests | Test-driven development; Playwright (Python) E2E |
| Board | In-repo Kanban board |
| Git | Git Flow |
| Commits | Conventional Commits |
| Versioning | SemVer; `VERSION`, `CHANGELOG.md`, annotated `vX.Y.Z` tags |

## Repo conventions

- **Docs-only changes** may skip the numbered spec with a short plan and owner approval.

## Templates

- SDD artifacts: `specs/_templates/`
- Board cards: `backlog/items/_template.md`
- Pull requests: `.github/pull_request_template.md`
- ADRs: `docs/adr/_template.md`

## Where the work lives

- Specs: `specs/NNN-slug/`
- Board: `backlog/board.md`, cards in `backlog/items/`
- Release record: `CHANGELOG.md` + `VERSION`
- Decisions: `docs/adr/`
