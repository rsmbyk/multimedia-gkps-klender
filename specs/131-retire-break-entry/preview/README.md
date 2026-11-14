# Preview — the Break control removed

**Spec**: `specs/131-retire-break-entry/spec.md`

The preview is the running page, not a redraw: `probe_break_controls.py` opens the served branch, reveals an
add row and the empty service's action row, photographs them, removes the Break control from the live DOM, and
photographs the same element again. Same markup, same stylesheet, one button fewer.

| Frame | Surface | Before | After |
| --- | --- | --- | --- |
| `add-row-before.png` / `add-row-after.png` | the add row under a service's first item, 1440×900 | five buttons, 400px block | four buttons, same left edge, right edge 75px left |
| `empty-before.png` / `empty-after.png` | the empty service's action row (spec 130's tiles), 1440×900 | five 52px tiles, 300px | four 52px tiles, 238px, same centre |
| `add-row-after-shipped.png` | the add row after the slice landed | — | the same four buttons, measured on the finished branch |
| `empty-before-shipped.png` | the empty action row after the slice landed | — | four 52px tiles, 238px wide, centred |

Measured geometry is in the spec's `## UI/UX`; the probe reprints it on every run:

```bash
cd ../multimedia-gkps-klender-131
DATABASE_URL=… ../multimedia-gkps-klender/.venv/bin/python manage.py runserver 0.0.0.0:8803 --noreload
../multimedia-gkps-klender/.venv/bin/python specs/131-retire-break-entry/preview/probe_break_controls.py            # the removal preview
../multimedia-gkps-klender/.venv/bin/python specs/131-retire-break-entry/preview/probe_break_controls.py --shipped  # the shipped surfaces
```

On the finished branch there is no Break control to remove, so `--shipped`'s "before" and "after" readings are
one and the same; the shipped frames record what the branch actually serves. Their measured reading: the add
row's four buttons 84 / 64 / 58 / 71px wide, 28px tall, 6px apart in a 400px block; the empty row 238px of
four 52px tiles at 10px gaps, centred (x 1057, centre 1176).

The empty-row frames were retaken after spec 130's tiles landed: the branch is based on `3a360d06`, where the
tile row is the empty state's layout. The probe widens the row's grid from five tracks to four with the same
removal, so the frame shows the slice's own result rather than an uncentred leftover slot.
