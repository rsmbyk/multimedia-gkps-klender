# Kickoff

**Greenfield only** — new project from the GitHub template. Humans and AIs both follow it in order. Do not add extra steps. Do not skip steps. Same answers must produce the same stubs and gates.

**Existing** repo, or owner-triggered keep-up when behind: use [ADOPT.md](./ADOPT.md), not this file.

Spawn the project with GitHub **Use this template** (private template). That copy has the same process tree as vexbook’s default branch. Then:

1. **Replace template identity.** This repo’s README and `specs/000-vexbook-scaffold/` describe *vexbook*. Replace them with this product’s README and Spec **000** (still one scaffold spec). Keep PROCESS, this file, [`ADOPT.md`](./ADOPT.md), [`docs/rules/SDD-GATE.md`](./rules/SDD-GATE.md), reusable stubs (`backlog/items/_template.md`, `specs/_template/`, `docs/adr/_template.md`), and the PR template. Reset [`VERSION`](../VERSION) to `0.0.0`.
2. **Apply one-time stubs, then remove `templates/`.** Copy [`templates/changelog.md`](../templates/changelog.md) over [`CHANGELOG.md`](../CHANGELOG.md) so the new product does not inherit vexbook’s version history (Keep a Changelog header, empty `[Unreleased]`, no version sections, no vexbook compare URLs). Write squashed process ADR [`docs/adr/0001-process.md`](./adr/0001-process.md) from [`templates/adr-spawn-process.md`](../templates/adr-spawn-process.md) — do **not** keep copying vexbook’s ADR 0001–N history as separate files. Then **delete the entire `templates/` directory** from this spawn. (Vexbook itself keeps `templates/` for future GitHub template copies.)
3. **Fill** [`PRODUCT.md`](./PRODUCT.md) — problem, who, locked decisions, non-goals, parked.
4. **Ask the owner** (do not assume):
   - GitHub Flow or Git Flow? (see [PROCESS.md](./PROCESS.md))
   - Stack and language?
5. **Propose architecture.** Tell the owner. Write **ADR 0002** (stack, hosting, architecture, CI, and related kickoff product decisions) from [`docs/adr/_template.md`](./adr/_template.md) and fill [`ARCHITECTURE.md`](./ARCHITECTURE.md). Record git model there (or in ADR 0002). Record versioning as SemVer (locked by vexbook). Paths and tool names go here, not in vexbook. If the stack mirrors `VERSION` into a language manifest, write that path here. Later product ADRs continue 0003+.
6. **`ITEM-000` → Spec 000.** One spec for the **whole scaffold**, including CI once the stack exists. Draft `{plan,spec,tasks}.md`. Put the item on the board (P0–P3; Backlog sorted by priority). First version is usually this scaffold PR (`0.0.0` + minor → `0.1.0` in that same PR; tag at merge).
7. **STOP.** Wait for the owner’s Accept / OK on that Draft. If Accept is unclear, ask again.
8. **Then implement** Spec 000 (TDD, branch per the chosen git model, draft PR linking the spec). Scaffold may land on `main` once if GitHub Flow was chosen.

After scaffold, every later change follows [PROCESS.md](./PROCESS.md): Draft specs → Accept → implement. Vexbook itself uses that same loop; it is not a special case.

vexbook is not a runtime dependency. Do not add it as a package or submodule.
