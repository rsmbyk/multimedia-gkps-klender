---
id: ITEM-279
status: backlog
title: 'A release deploys code whose migrations never ran'
type: fix
priority: P1
effort: M
created: 2026-11-29
updated: 2026-11-29
spec:
branch:
pr:
issue:
closed_at:
closed_reason:
bump:
release_version:
---

# ITEM-279: A release deploys code whose migrations never ran

## Summary

Both Cloud Run triggers run their migrations through a job whose image is set once, when the job is
created. Every build pushes and deploys `${COMMIT_SHA}`, but the job kept an old tag, so `migrate` ran
against code that did not know the new migrations, printed `No migrations to apply.`, exited 0 and the
build reported SUCCESS. Staging then served the spec 254 columns that nobody had created and answered
500 on every page reading a versioned table; production carried the same defect, one migration away
from the same outage.

## Notes

- The chain, measured on 2026-11-28: build `4f0b38d4` succeeded at 17:43Z and deployed `2aeadbbd`
  (spec 254); the step before it, staging migrate execution `l5gp7` at 17:45Z, logged
  `No migrations to apply.` because the job's image was `staging:setuptools`, a manual tag from
  2026-11-27, not `staging:2aeadbbd…`. Production's job was likewise pinned to `production:initial`.
- Symptom: `/songs/`, `/tatib/`, `/tatib/<id>/` and `/api/songs/books/` answered 500 with
  `ProgrammingError: column songs_book.version does not exist` / `column tatib_serviceentry.version
  does not exist`; `/`, `/bible/`, `/search` and `/projector` stayed 200, so the site looked reachable.
  Missing: `songs.0017_book_version_song_version_verse_version`,
  `tatib.0015_serviceentry_version_tataibadah_version_and_more`.
- Remediation applied 2026-11-28 in GCP, not in the repo: each job was pointed at the deployed
  revision and executed (both migrations applied; all routes 200 again), and both triggers gained a
  step that runs `gcloud run jobs update <job> --image=<env>:${COMMIT_SHA}` before
  `gcloud run jobs execute`. Verified by running each trigger: staging build `0627741b`, production
  build `c45b59b7`, each updating its job's image and deploying cleanly.
- Still open, and why this is a card: the trigger definitions live only in the GCP project. Nothing in
  the repo diffs them, so the next edit there is invisible to review, and there is no test that fails
  when a deploy ships ahead of its migrations.
- Editing gotcha for whoever works this: on these 2nd-gen triggers `--inline-config` and a raw
  `PATCH …/triggers/<id>?updateMask=build` both answer a bare `INVALID_ARGUMENT`; `--trigger-config`
  with the full `BuildTrigger` resource (name, `repositoryEventConfig`, `serviceAccount`, `build`) is
  what updates them.

## Acceptance sketch

- A commit that adds a migration reaches a service only after that migration has run against the image
  being deployed.
- A migrate step that cannot apply the pending migrations fails the build instead of deploying.
- The pipeline definition is reviewable in the repo, or the reason it stays outside is recorded where
  the deploy is described.

## Links

- Spec: —
- Related items: [ITEM-268](ITEM-268-cloudrun-csrf-origin.md) (the previous Cloud Run incident),
  [ITEM-271](ITEM-271-entity-versioning.md) (spec 254, whose migrations were never applied).