# Backlog

Kanban lives in [`board.md`](./board.md). Each card is an `ITEM-XXX`; details live in [`items/`](./items/). Copy [`items/_template.md`](./items/_template.md) for a new item.

Specs: [`../specs/_template/`](../specs/_template/). Process: [`../docs/PROCESS.md`](../docs/PROCESS.md). A spec may be written from **one or more** items.

## Columns

| Column | Meaning |
| --- | --- |
| Backlog | Captured — no complete spec pack yet. **Sorted by priority** (P0 first, then P1…; ties by ID). |
| Speccing | Spec pack in progress |
| Ready | Owner accepted the Draft — may implement |
| In progress | Execution started — feature/hotfix branch |
| In review | PR open |
| Done | Merged (`main` on GitHub Flow, `develop` on Git Flow until release) |

Files must match git: see [PROCESS.md — One PR is complete](../docs/PROCESS.md). Extra commits on the PR are fine. Do not merge and finish board/tasks/version in a second PR.

Other columns stay in **workflow order**, not priority order.

## Fields

| Field | Meaning |
| --- | --- |
| Type | `feat`, `fix`, `hotfix`, `chore`, `docs`, `refactor`, `test`, `idea` |
| Priority | `P0` highest … `P3` lowest |
| Effort | `S` / `M` / `L` |
| Bump | SemVer bump for this slice: `major` / `minor` / `patch` / `none`. Always set. If not `none`, this PR also writes `VERSION` and the changelog section. |

## Owner phrases

| Phrase | Effect |
| --- | --- |
| Capture ideas | Create `ITEM-XXX` on Backlog (keep that column sorted) |
| `spec ITEM-…` | Write spec pack; board → Speccing |
| Accept / OK on spec | Board → Ready |
| Implement the Accepted spec | In progress + branch |
| OK on PR | Same PR already has Done + version bump if needed; merge; tag in the same session |

Update `board.md` and the item file in **the same PR** as the work. Extra commits on that PR are fine.
