# Backlog and tracker

In-repo, docs-native backlog and status tracker. No GitHub Projects / Linear
required. Specs remain the source of *intent* for in-scope product work; the
backlog is the source of *what we might do next*.

## Layout

```text
backlog/
  README.md           # status board (tracker) + index
  _templates/
    item.md           # copy for new items
  items/
    BL-NNN-slug.md    # one file per backlog item
```

Process detail lives here; the living board lives in
[`backlog/README.md`](../backlog/README.md).

## Roles

| Piece | Job |
|-------|-----|
| **Backlog item** (`BL-*`) | Prioritized idea or work not yet finished |
| **Tracker** (`backlog/README.md`) | Status board of active and recently done work |
| **Specs** (`specs/`) | Agreed intent (`APP`, `OBS-SONGS-AC3`, …) |

Typical flow:

```text
Backlog item → (optional) Spec → Plan → Tasks → PR → Done
```

Tiny chores and docs-only work may skip a full `specs/` tree — same rules as
[`SDD.md`](SDD.md) “When to use SDD”.

## Item IDs

| Kind | Pattern | Example |
|------|---------|---------|
| Backlog item | `BL-<nnn>` | `BL-001` |
| Spec cross-ref | Spec IDs | `OBS-SONGS-AC12` |
| PR / issue | GitHub | `#245`, full URL |

- Numbers are **global and stable**. Do not reuse a `BL-*` number after
  `dropped` or `done`.
- Next free number: see “Next ID” in [`backlog/README.md`](../backlog/README.md).
- Filename: `items/BL-NNN-short-slug.md` (slug is for humans; ID is canonical).

## Statuses

| Status | Meaning |
|--------|---------|
| `idea` | Captured; not ready to pull |
| `ready` | Clear enough to start (or to write a spec) |
| `specified` | Spec folder exists / agreed; implementation not started |
| `in-progress` | Active branch / work underway |
| `in-review` | PR open |
| `done` | Merged / shipped intent met |
| `dropped` | Won’t do; keep the file for history |

Update the **item file** and the **board** in `backlog/README.md` when status
changes.

## Priority and size

| Priority | Meaning |
|----------|---------|
| `P0` | Do next / blocking |
| `P1` | Important soon |
| `P2` | Normal |
| `P3` | Nice to have |

| Size | Rough effort |
|------|----------------|
| `S` | Hours / one small PR |
| `M` | About a day or a focused PR |
| `L` | Multi-PR or cross-cutting |

Area labels should match changelog labels when possible (`songs`, `bible`,
`api`, `web`, `deploy`, `docs`, `test`, …). See [`VERSIONING.md`](VERSIONING.md).

## Creating an item

1. Copy [`backlog/_templates/item.md`](../backlog/_templates/item.md) to
   `backlog/items/BL-NNN-slug.md` using the next free `BL-*` number.
2. Fill fields; link related Spec IDs if any.
3. Add a row to the matching status table in `backlog/README.md`.
4. Bump “Next ID” in that README.

## Relationship to other docs

| Doc | Role vs backlog |
|-----|-----------------|
| [`SDD.md`](SDD.md) | Intent for in-scope work once pulled from backlog |
| [`TDD.md`](TDD.md) | How implementation tasks are proven |
| [`GIT_FLOW.md`](GIT_FLOW.md) | Branches and PRs for `in-progress` / `in-review` |
| [`specs/README.md`](../specs/README.md) | Spec ID registry |

## Agent expectations

- Prefer linking work to a `BL-*` item when the change is planned product or
  non-trivial chore work.
- When status changes, update both the item and the tracker board.
- Do not invent large process toolchains; keep this Markdown-native.
