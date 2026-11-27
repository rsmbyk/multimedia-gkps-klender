# Quickstart: Verse modal header draws one rule

**Spec**: `specs/226-verse-modal-header-rule/spec.md`

## Prerequisites

- Repository venv with the project requirements and Playwright Chromium installed.
- The compose stack running its `web` and `db` services on this machine.

## Setup

```sh
# Nothing to install: both test paths use the checkout's own venv.
```

## Run

```sh
/home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python manage.py test   tests.e2e.test_verse_modal_header --keepdb
/home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python   specs/226-verse-modal-header-rule/preview/probe.py --inject-fix
```

## Verify

| Check | Command | Expected |
| --- | --- | --- |
| Both dialogs paint one rule | targeted E2E above | one ruled descendant in `.editor__head`, title border `0px` |
| Spacing matches the other editors | targeted E2E above | 21px top gap, 16–17px title-to-rule gap, x=289 inset |
| Narrow dialog | targeted E2E above | head rule width `100vw - 32px` |
| Live read-back | probe with `--inject-fix` | `report.json` and both dialog screenshots under `preview/shots/` |

## Not yet runnable

- A deployed build: the preview uses the local compose service; a Vercel deployment is separate
  evidence and is not part of this slice's local verification.
