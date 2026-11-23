# Research: a created Template opens on the stage

**Spec**: `specs/234-open-created-template/spec.md`
**Unknowns remaining**: 0

## D001 — The destination URL for a created Template

- **Decision**: `/tatib/<id>/?mode=template`.
- **Rationale**: the copy-as-template flow already lands there (`reading/views.py:1023`), and the
  live probe measured the sidebar list in template mode with `#tatibMode` pressed on arrival.
- **Alternatives considered**: bare `/tatib/<id>/` — `TatibView` derives the mode from the record's
  kind, so it would show the same stage, but the URL would not say which list the operator is in;
  rejected in favour of the explicit form used by the neighbouring flow. Staying on the list was
  the current behaviour and is the defect.
- **Provenance**: owner decision (accepted gate-1 question) + research of the existing copy flow.

## D002 — Where the behaviour changes

- **Decision**: extend the existing `editor:saved` create branch in `static/web/reading.js` to
  accept `record_kind === 1` and choose the URL from that value.
- **Rationale**: that handler already owns the in-place open for a dated create, including the
  no-reload navigation and quiet focus restore; a template should take the same path. The server's
  `record_kind` field already distinguishes the two kinds (`reading/views.py:212-214`).
- **Alternatives considered**: a server redirect after create (would reload and break the
  shell's in-place contract); a second event or new endpoint (duplicates the same branch); a CSS
  or template change (cannot affect navigation).
- **Provenance**: research — code path traced from `editor_save` to the `editor:saved` listener.

## D003 — Verification seam

- **Decision**: add and rewrite E2E cases in `tests/e2e/test_editor.py`, class `EditorE2ETests`,
  beside the spec 209 create cases.
- **Rationale**: the same class already drives the real sidebar create dialog, reads
  `#readName`, `aria-current`, `data-nav`, `data-ch`, the in-page marker and `timeOrigin`, and
  holds the superseded template assertion. One module keeps the red/green evidence together.
- **Alternatives considered**: a new E2E module (splits one behaviour across two files); a unit
  test of the URL expression (tests structure, not the observable destination); manual clicks only
  (not repeatable at the push step).
- **Provenance**: research — existing test layout and the repository's TDD/E2E convention.

## D004 — Version level

- **Decision**: `bump: patch`.
- **Rationale**: this corrects an existing create behaviour without adding a capability or
  breaking one; `VERSION` at the base is `1.36.19`. The number is stamped at the pre-merge
  delivery commit and re-checked then.
- **Alternatives considered**: `none` — a user-visible change is notable, so the changelog needs a
  line; `minor` — no new capability is introduced.
- **Provenance**: research — SemVer mapping in `docs/PROCESS.md` VER-10.

## Open

None.
