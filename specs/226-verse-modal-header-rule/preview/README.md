# Preview: verse modal header draws one rule

**Shape**: live preview. The slice's only visible effect is a double draw, so the material for
gate 1 is the measured defect on the app's own route and its removal — not a new look to approve.

- Before: `http://127.0.0.1:63404/songs/1820/` — press `Add verse`, then the pencil on verse 1.
- After (candidate, before the product file changes): the same route with the CSS injected by the
  probe below (header padding moved, title padding and border removed). After implementation, reload the route: the product file itself carries the change.

## States

| State | How to reach | What is read |
| --- | --- | --- |
| New verse | `Add verse` at the foot of a song's verses | title/head border widths and boxes |
| Edit verse n | the pencil on any verse row | the same read-back |
| Loading skeleton | the form fetch in flight | not painted by the large rule; unchanged, inspected in code |
| Non-verse editor | any sidebar editor | unchanged header, one rule |
| Light / dark | the app's theme switch | same geometry, `--divider` follows the theme |
| Narrow viewport | 390×844 browser width | the remaining rule follows the dialog width |

## Harness

```sh
../.venv/bin/python specs/226-verse-modal-header-rule/preview/probe.py
../.venv/bin/python specs/226-verse-modal-header-rule/preview/probe.py --inject-fix
```

`--url` points the probe at any running build; `--width` / `--height` set the viewport. Each run
writes `preview/report.json` and screenshots of both dialogs into `preview/shots/` (both gitignored).
The probe reads the shipped DOM with `getComputedStyle` after the fetched form has settled; it does
not click Save or write data.

The probe exercises the live fetch and the product's own `openEditor` path. It does not exercise a
deployment or a stale static manifest: a worktree server needs its own `collectstatic` before its
static files match its code.
