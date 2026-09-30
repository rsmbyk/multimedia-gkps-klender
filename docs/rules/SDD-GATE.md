# SDD permission gate (non-negotiable)

This project uses Spec-Driven Development. This overrides “just do it” instincts. This repository and every project spawned from it share the same loop.

## Required loop

1. **Plan** (manual notes or any AI agent plan mode) — what / why / scope
2. **Draft** — `specs/NNN-slug/{plan,spec,tasks}.md` **before** code
3. **STOP** — wait for the project owner’s explicit OK / Accept on that Draft
4. **Then** implement (TDD for domain/app), branch, PR linking the spec

Plan **stops at Draft specs**. Do not treat plan approval as permission to implement. If you are unsure whether the owner Accepted or OKed a Draft, **ask again** — do not treat ambiguous “proceed”, plan-UI accept, or “OK” on a different artifact as implement permission.

## One concern per spec

- Do not mix unrelated features or fixes in one numbered spec
- Spec **000** is reserved for scaffolding and is **one spec**
- A spec may be written from **one or more** ITEMs

## Do NOT

- Implement, add deps, or scaffold until a Draft is **Accepted** (or the owner explicitly OKs that Draft)
- Treat “proceed”, “do it”, or “fix X” as coding permission unless the owner already Accepted that Draft
- Treat “proceed to draft” as permission to implement — write Drafts only
- Retrofit specs after coding except to recover from a gate miss the owner already acknowledged

## Exceptions

Ops / docs-only / hotfix one-liners may skip a numbered spec, but still get a short plan and OK when more than trivial. **CSS and copy still get a numbered spec.**

## When the owner says proceed

- **Accept / OK on a Draft** → implement that spec only
- **Draft specs** → write Draft markdown only; do not code
- **New change** → start at Plan/Draft, do not code yet
- If unsure whether a change needs a spec → **ask**, do not code
- If unsure whether Accept/OK applies to this Draft → **ask again**, do not code

## Recovery

If you already coded without a spec: stop, Draft the missing spec, wait for Accept, then continue. Say so plainly.
