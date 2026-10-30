# Converge: a Tata Ibadah is a service or a template

**Spec**: `specs/167-tata-ibadah-templates/spec.md`
**Run**: 2026-10-30, after Implement

## What was checked

Every FR and SC in `plan.md`'s traceability table against the built tree, and every scenario in the spec
against a test that exercises it. Three passes: requirement coverage, the state a record is in rather than
the transition that produced it, and the seams with the neighbouring slices.

## Findings and their disposition

| # | Finding | Disposition |
| --- | --- | --- |
| C1 | The slot pair's hairline and dashed border existed in the preview's stylesheet only; the shipped add bars drew six plain buttons. | **fixed** — `.entry__add-sep`, `.entry__add-btn--slot` and `.entry__empty-btn--slot` are in `generate.css`; the E2E case reads the six labels in order. |
| C2 | A slot's form was first opened by hand-rolled `fetch` + `innerHTML`; the editor's own loader never ran, so its Save stayed disabled and the phone's busy state never cleared. | **fixed** — the form is opened through `window.gkpsEntry.openSlotForm`, which reuses `load()`; the slot marker lives on the form (`data-slot-entry`), and the POST goes to `entry/validate/`. |
| C3 | A slot resolution fired `editor:saved`, which made the reading shell re-read the page and replace the generate modal under the operator. | **fixed** — `reading.js` ignores a saved event carrying `slotEntry`; nothing on the page changed, so there is nothing to refresh. |
| C4 | `TataIbadahForm` set the type on the instance only in `save()`, so the model's own rule ran against the default before it. | **fixed** — `clean()` writes `instance.kind` before `_post_clean`. |
| C5 | Two existing tests encoded the pre-slice rules: a date-less service was expected to project, and clearing a Normal's date was expected to save. | **fixed** — the video case dates its service; the editor case now asserts the refusal and the kept date. Both are the slice's own rule. |
| C6 | The choice's chooser stays open after a pick, covering the footer. | **fixed** — a pick closes the chooser (the row is what changed). |
| C7 | A choice's `Add option` cannot be reached on a template that has options but no rows visible in the pane… | **not reproducible** — the control renders on the choice's row and the E2E adds an option through it. Closed. |

## The three passes

- **First (spec coverage)**: 24/24 FR, 6/6 SC, 38/38 scenarios, 5/5 stories.
- **Second (state, not transition)**: a row written outside the editor — the API, a fixture, a migration —
  still satisfies INV-1 because the pairing is a database constraint as well as a form rule; a template
  copied from a template keeps its slots because the copy walks `parent`; a slot resolved twice keeps only
  the last resolution, which is what the row shows.
- **Third (seams)**: media retention and the manifest are untouched and pinned by two tests; the dock and
  the projector read the type; the reorder endpoint keeps a choice with its options.

## Evidence

- `manage.py test multimedia.web multimedia.api.tatib tests.e2e.test_tatib_templates` — **399 tests, OK**.
- The probe still exits 0 with `console_errors: []` for the preview the spec's numbers come from.
