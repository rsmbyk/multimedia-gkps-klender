# Quickstart: a speaker's turn hangs under its words

**Spec**: `specs/211-overlay-turn-hang/spec.md`
**Design**: `data-model.md` · `contracts/README.md`

## Prerequisites

- Python 3.12 with the repo's venv at `~/Projects/multimedia-gkps-klender/.venv`.
- Playwright Chromium available in that venv (the existing overlay E2E suite uses it).
- No database service: `DJANGO_DEVELOPMENT_MODE=true` selects SQLite.

## Setup

```sh
cd ~/Projects/multimedia-gkps-klender-211
git status --short                      # branch: feat/211-overlay-turn-hang
```

## Run

```sh
DJANGO_DEVELOPMENT_MODE=true ~/Projects/multimedia-gkps-klender/.venv/bin/python manage.py test \
  tests.e2e.test_obs_overlay --noinput
```

The gate-1 static preview opens directly from disk (no server needed):

```sh
xdg-open specs/211-overlay-turn-hang/preview/index.html
```

It links the real `obs-overlay.css`; its readout measures the before/after words x live at
1280×720 and its third tab is the no-mark control. Note the review page overrides the sheet's
`html { overflow: hidden }` (an OBS browser-source rule) so the document can scroll.

## Verify

| Check | Command | Expected |
| --- | --- | --- |
| Overlay E2E | the `tests.e2e.test_obs_overlay` command above | all tests OK, including the new continuation scenarios |
| Wrap measurement | the same module's wrapped-continuation test | every glyph row of the continuation shares the words x within 1 px; no ink past the plate content edge |
| No-mark control | the preview's third tab | both frames identical; no indent added |
| Fold target | inspection of `docs/spec/overlay.md` R5 | one modified block with the continuation rule and its scenario |

## Not yet runnable

- No live compose server is started from this worktree at drafting time; the gate-1 measurement
  used the static preview with the project's real stylesheet, which is sufficient for this
  paint-only change (SDD-06). The E2E command above is the live verification.
