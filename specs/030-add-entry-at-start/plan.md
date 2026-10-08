# Plan 030: Add a service entry at the beginning

- **Status:** Draft
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-032
- **Bump:** minor

## Why

The pane offers an add bar **after** each row, and `entry_save()` only knows how to insert after a
marker (`e<id>` / `l<id>`) or append when there is none (`next_order_number()`). There is no way to
insert an entry at the very **start** of the running order — the first item can only be arrived at by
reordering afterwards. Add a start affordance and the insertion logic behind it.

## Scope / edges

**In:**

- A leading add bar above the first row, mirroring the per-item bar (every kind), carrying
  `after=start`.
- `entry_save()` recognizes `after=start` and inserts at order 1, shifting every existing
  `ServiceEntry` and legacy `TataIbadahItem` up by one so the shared order stays contiguous from 1.
- The editor form carries `after=start` through GET and the 400 re-render (the existing `after`
  plumbing), so a validation error does not lose the insertion point.

**Out:**

- The per-row "after" insertion — unchanged.
- Reorder, the shared-order rules, and the legacy API.
- The empty state, which already appends at order 1.

## Approach

- `multimedia/web/templates/reading/tatib.html` — render one add bar before the `{% for item in
  items %}` loop (guarded by `editor_enabled`, only when there are items) with
  `data-entry-after="start"` and the same `data-entry-open` buttons as the per-item bar.
- `static/web/entries.js` — no change needed: the opener's `[data-entry-after]` value flows into
  `newUrl()` and the fetched form.
- `multimedia/web/reading/views.py` — in `entry_save()`'s new-entry branch, after
  `_compact_service_order()`, when `after == 'start'`: shift `order_number + 1` for every row of
  both models in the service, then set `form.instance.order_number = 1`. Keep the existing
  `e<id>` / `l<id>` / append cases as they are.
- `_entry_form.html` already renders `<input type="hidden" name="after" value="{{ after }}">` for a
  new entry with an `after`; `entry_form()` and the 400 branch in `entry_save()` already pass it
  through. Confirm `start` survives both.

## TDD

- Domain/app tests: `multimedia/web/tests.py` — posting a new entry with `after=start` gives it
  `order_number=1`, shifts the rest, and leaves the shared order contiguous across entries and
  legacy rows; a validation error re-renders with `after=start` still present.
- E2E: `tests/e2e/test_reorder.py` or a small addition — the leading bar adds an entry at the top
  and the pane and projector both show it first.

## Risks

- **Order corruption.** The shift must touch both tables in one transaction, after
  `_compact_service_order()`, or a mixed entry/legacy service can end up with a duplicate order 1.
- **A missing sentinel.** If `after=start` is not carried through the 400 re-render, a corrected
  form would append instead of starting.
