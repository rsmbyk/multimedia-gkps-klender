# Data model: a created Template opens on the stage

**Spec**: `specs/234-open-created-template/spec.md`

No persisted entity is added, removed or migrated. The slice reads values that already exist:

- **`TataIbadah.kind`** — `TataIbadahKind.SERVICE` (`0`) or `TEMPLATE` (`1`); the model already
  enforces "a template has no date" (`multimedia/tatib/models.py`).
- **`record_kind`** — `int(saved.kind)` in the `editor_save` JSON response
  (`multimedia/web/reading/views.py:212-214`); already delivered to the browser for Tata Ibadah
  saves.
- **`created`** — true only for a new record (no `pk` in the editor URL), so edits keep the
  list-refresh path.
- **Reading stage state** — `#read`, `#panelBody .book[aria-current="true"]` and the root's
  `data-nav` / `data-ch` attributes, swapped in place by `navigate(...)`.

No model, form, endpoint or migration changes.
