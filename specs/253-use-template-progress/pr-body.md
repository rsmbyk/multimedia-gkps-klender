## What

The Use template modal now keeps its work per template in the browser session. Settled slots, the
step, the name and the date are written to `sessionStorage` under `gkps:generate:<templateId>` on
every change, restored when that template is reopened, and cleared once a service is created. A close
with saved work — Cancel, the backdrop or Escape — first confirms that the progress is saved and can
be resumed later, with Stay and Leave; a clean modal still closes silently. Slot ids that no longer
exist in the template are dropped on restore.

## Why

`specs/253-use-template-progress/spec.md`; card `ITEM-270`. Closing the modal used to discard several
slot resolutions with no warning, so an accidental dismissal meant starting over.

## Evidence

- **Verification**: 22 test · 0 inspection · 0 manual
- **Convergence**: Converged in 1 pass · accepted gaps: none
- **Folded**: `docs/spec/reading.md` — R65 added (R64 was already taken by spec 252)
- **Board**: `ITEM-270` → In review
- **Refs** #650

The new module `tests/e2e/test_use_template_progress` passes 15/15, and the existing
`tests.e2e.test_tatib_templates` passes 38/38 after its superseded "reopening starts from nothing"
pin was rewritten to the restored behaviour — 53/53 together, zero console errors. The preview probe
passes 10/10. A full-suite run was started but the environment killed it mid-run; the touched flow's
regression scope is green.

## Risk

Client-only: no model, migration, endpoint or template write. A browser that refuses storage still
opens and works, just without a resume. Reverting the squash commit restores the old discard-on-close
behaviour with no data migration.