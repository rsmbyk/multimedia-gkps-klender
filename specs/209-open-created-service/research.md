# Research: a newly created service opens on the reading stage

**Spec**: `specs/209-open-created-service/spec.md`
**Unknowns remaining**: 0

## D001 — The save response tells the shell that a record was created

- **Decision**: `editor_save` (`multimedia/web/reading/views.py:173-185`) adds `created` (boolean) to
  its JSON answer for every editor save, and `record_kind` (the `TataIbadahKind` value) when the kind
  is `tatib`. The client opens a stage only when `kind == 'tatib'`, `created == true` and
  `record_kind == 0` (Normal service).
- **Rationale**: the success event at `static/web/editors.js:230-241` carries only `{ok, id, kind}`;
  the shell's listener at `static/web/reading.js:2033-2064` cannot tell a create from an edit. The
  server already knows (`pk is None` on the form) and owns the stored kind. The fields are additive,
  so the other `editor:saved` listeners (display, media-stage, generate) keep their current shape.
- **Alternatives considered**: infer a create from the form action URL or the dialog's opener id —
  both are DOM state that can be swapped by an in-page refresh, and they hide the record kind;
  add a dedicated create endpoint — unnecessary duplication of a working save path.
- **Provenance**: research (source read on base `989347f2`)

## D002 — Open with the shell's own in-place navigation

- **Decision**: in the `editor:saved` listener, a Normal create calls `navigate('/tatib/<id>/',
  {kind: 'service', forceServer: true})` and returns before the usual list-refresh branch. No
  `backgroundRefresh`, so `applyPage` lets the child pane follow the arriving page's `data-ch=open`;
  `kind: 'service'` is a `stageOnly` navigation, so the operator's `data-nav` choice survives.
- **Rationale**: `navigate()` (`static/web/reading.js:1459-1514`) already swaps lists, stage and
  child pane from one fetch while keeping shell state (`applyPage`, lines 1586-1594 and 1644-1668).
  This is exactly the state a row click produces, measured in the gate-1 reproduction:
  `/tatib/<id>/`, name filled, row current, `data-nav=open`, `data-ch=open`, in-page marker intact.
- **Alternatives considered**: `window.location.href` — a full reload, which the owner excluded;
  hand-copying the service markup — duplicates `applyPage` and drifts from the row-click path.
- **Provenance**: owner decision (in place) + research (navigation path)

## D003 — The seam is the existing sidebar-editor E2E module

- **Decision**: add focused browser tests to `tests/e2e/test_editor.py` using its
  `StaticLiveServerTestCase` harness and `override_settings(STATICFILES_STORAGE=...StaticFilesStorage)`.
  Update `test_add_empty_active_tatib`, whose `get_by_text('Ibadah Baru', exact=True)` would match
  both the row and the now-populated stage heading; click the `.book` row explicitly instead.
- **Rationale**: the behaviour crosses the save response, a custom event and the in-page navigator;
  no smaller seam observes all of them. The module already owns sidebar create/edit saves and runs
  locally with `DJANGO_DEVELOPMENT_MODE=true` (verified: one focused test ran green on this worktree).
- **Alternatives considered**: a unit test of the new response field alone — it would not prove the
  stage opens; a new E2E module — needless duplication of the harness and fixtures.
- **Provenance**: research

## D004 — Templates and edits keep their present behaviour

- **Decision**: only a create of `record_kind == 0` opens a stage. A Template create (kind 1), a
  service edit and every other record kind fall through to today's refresh branch unchanged.
- **Rationale**: a Template is undated and never projects; the owner's answer named the reading
  stage for a new *service*. Template-generate and copy-as-template already navigate to their
  created record (`generate.js:463`, `editors.js:509`), so they need no change.
- **Alternatives considered**: open any newly created Tata Ibadah — would pull a Template onto the
  stage and contradict `reading/R34`/`R36`.
- **Provenance**: owner decision + research

## D005 — Bump and board record

- **Decision**: `bump: patch` — `VERSION` 1.35.0 → 1.35.1 with one `## [Unreleased]` `### Fixed`
  line; planned card ITEM-222, created with the implementation PR in `Backlog` and closed in the
  repo's usual follow-up card PR.
- **Rationale**: a user-visible correction to an existing create flow, matching the neighbouring
  reading fixes (specs 199/201 each took a patch).
- **Alternatives considered**: `none` — the stage behaviour changes, so the user can see it;
  `minor` — no new capability is added.
- **Provenance**: research

## Open

<!-- empty when Phase 0 is finished; anything here blocks Phase 1 -->
