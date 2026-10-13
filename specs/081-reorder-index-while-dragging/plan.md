# Plan 081: Renumber the drag copy while a row is being reordered

- **Status:** Accepted
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-084
- **Bump:** patch

## Why

`renumber()` in `static/web/reorder.js` keeps the sidebar's numbers in step with the order on every
placement step, but it only reaches the rows inside `#chList`:

```js
function renumber() {
  var l = list();
  if (!l) return;
  var number = 0;
  [].slice.call(l.children).forEach(function (item) { … cell.textContent = String(number); … });
}
```

The row being dragged paints no number of its own — `#chList li.is-dragging > * { visibility: hidden }`
hides it — so the number the operator actually reads while dragging is the one on the drag copy
(`.reorder__ghost`), and that copy was stamped once from `drag.row.innerHTML` in `makeGhost()` and
never touched again. The grabbed entry therefore keeps showing the index it had when it was picked up,
while every row around it counts up correctly.

## Scope / edges

**In:**

- `static/web/reorder.js`: the number on the drag copy during pointer dragging.
- The number's value, its geometry (centered per spec 064), and the moment it changes.

**Out:**

- The keyboard arrow move (there is no drag copy), the cover of the ghost, its width/height/opacity
  and shadow, the persist payload, and the pane on the right.
- Numbers anywhere but the Tata Ibadah contents list.

## Approach

Make `renumber()` the single source of the number everywhere it is painted: after it walks the list,
hand the dragged row's current number to the drag copy. Keep `renumber()` synchronous and cheap — it
already runs on every placement step, so the copy updates in the same frame as the rows that parted.

## TDD

- Domain/app tests: N/A — client-side presentation only.
- E2E (Playwright): `tests/e2e/test_reorder.py` and `tests/e2e/test_toc_number_centering.py`
  (`test_drag_copy_keeps_the_number_centered` already owns the copy's number geometry).

## Risks

- The ghost is built from `drag.row.innerHTML` with its links and grips stripped, so the copy has no
  `data-num` and no `[data-move-grip]`; the fix must address the cell directly and tolerate a break
  row, which has no number cell at all.
- `renumber()` runs during the cancel path too; a cancel removes the copy before renumbering, so the
  guard has to survive a missing or detached ghost.
