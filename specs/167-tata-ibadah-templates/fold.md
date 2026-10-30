# Fold: a Tata Ibadah is a service or a template

**Spec**: `specs/167-tata-ibadah-templates/spec.md`
**Capability delta**: `docs/spec/reading.md` R34–R38
**Bump**: `minor` — 1.23.2 → 1.24.0, stamped against `develop` in the pre-merge commit.

## What the capability now says

- **R34** — every Tata Ibadah carries a type chosen at creation; the type and the date cannot disagree; the
  panel lists by type; existing rows keep the type they behaved as.
- **R35** — a template carries fill-ins and choices; options are child entries; a service refuses both.
- **R36** — a template generates a dated service in two steps; **Next** gates on the settled count; the
  create is one transaction and leaves the template untouched.
- **R37** — any Tata Ibadah copies as a template, converting nothing.
- **R38** — a template never projects, and its media is kept as a use but never auto-downloaded.

## The seams

- **Media**: `media_references` and `media_manifest` are unchanged; two tests pin the two directions.
- **Projector and dock**: the projector answers the empty display for a template's id; the dock filters on
  the type.
- **Reorder**: a choice moves with its options, so the running order cannot orphan them.
- **API**: `kind` is read-only; a create with no date is still a template.

## Recorded for the release

- `VERSION` and the `## [Unreleased]` line are written in the pre-merge commit, not here (C-SDD-VER).
- The card is closed after the merge, in its own board pull request (the repo's convention).
