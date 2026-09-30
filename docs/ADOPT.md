# Adopt and sync

**Greenfield** (new repo from the GitHub template): follow [`KICKOFF.md`](./KICKOFF.md) only.

**Existing** repo that wants this process, or a spawn/adopter that should catch up to a newer vexbook release: follow **this file**. Humans and AIs both follow it in order. Do not invent a second path.

vexbook is not a runtime dependency. Do not add it as a package or submodule. There is **no automatic sync** — the project owner triggers adopt or sync.

## Process file set

Copy these from a **chosen vexbook tag / release / commit** (owner names the source). Overwrite process docs; do **not** wipe product docs.

| Path | Notes |
| --- | --- |
| `docs/PROCESS.md` | Locked way of working |
| `docs/KICKOFF.md` | Greenfield start (kept so future agents know the spawn path) |
| `docs/ADOPT.md` | This file |
| `docs/rules/SDD-GATE.md` | Canonical SDD gate |
| `backlog/items/_template.md` | Reusable ITEM stub |
| `specs/_template/` | Reusable plan/spec/tasks stubs |
| `docs/adr/_template.md` | Reusable ADR stub |
| `.github/PULL_REQUEST_TEMPLATE.md` | If present in the source |
| `AGENTS.md` | Align **process / kickoff / adopt** sections with vexbook; **keep** (or create) the product-specific section |

**Do not copy** into an existing product:

- vexbook `templates/` (one-time spawn stubs only)
- vexbook backlog / specs history, `VERSION`, or `CHANGELOG.md` history
- vexbook’s multi-ADR chain as a replacement for the product’s ADRs

Ensure the ITEM board (`backlog/board.md`) and reusable `_template`s exist after the copy. Do not invent product ADRs just to fill gaps.

## First-time adopt

Owner asks to adopt. Owner names the vexbook source (e.g. `v0.4.0`). Then:

1. Copy the **process file set** from that source into the target repo.
2. Write **one** adoption ADR at the **next free** number (from [`docs/adr/_template.md`](./adr/_template.md)):
   - **Decision:** adopt vexbook process at the named source.
   - **Consequences:** [`PROCESS.md`](./PROCESS.md), [`KICKOFF.md`](./KICKOFF.md), and [`rules/SDD-GATE.md`](./rules/SDD-GATE.md) are binding; link those paths.
   - Do **not** renumber existing ADRs. Do **not** force spawn-style ADR **0001** (process) / **0002** (product). Greenfield numbering applies only under KICKOFF.
3. Leave `PRODUCT.md` / `ARCHITECTURE.md` as the product already has them. If stack, git model, or architecture were never decided, **point the owner** at those gaps (same questions as KICKOFF) — do not invent answers or fake a renumbered ADR 0002.
4. Refresh local vendor project rules so they reference **every** must-apply shared doc listed in PROCESS (same bootstrap as AGENTS).
5. First behavior change after adopt still goes through SDD: Draft → owner Accept → implement ([PROCESS.md](./PROCESS.md)).

## Sync / keep-up

Owner asks to sync (chat, ITEM, or explicit OK). Agents **never** sync unprompted. Owner names the vexbook source.

1. Re-copy the **process file set** from that source (same table as above).
2. Do **not** renumber ADRs. Prefer a short note on the existing adoption ADR (source tag + date). Add a new thin ADR at the next number only if the owner wants a distinct decision record (“synced to vexbook `vX.Y.Z`”).
3. Leave product ADRs, application code, the child’s `VERSION` / changelog, and board history alone unless the owner’s sync ITEM explicitly includes a product change.
4. After sync, vendor local rules still must reference every must-apply shared doc from PROCESS.

## Afterward

Continue with [PROCESS.md](./PROCESS.md). New greenfield children of this product (if any) still use KICKOFF when spawning from a template — not this file.
