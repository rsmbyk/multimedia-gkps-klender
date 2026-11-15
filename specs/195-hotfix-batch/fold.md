# Fold — spec 195 (2026-11-15)

Run at Converged. Typed deltas into `docs/spec/<capability>.md`; idempotent.

## Capabilities touched

| Capability | File | Operations | Before → after |
| --- | --- | --- | --- |
| `reading` | `docs/spec/reading.md` | **modified** R9 (badge hides for the row's action reveal, +1 scenario) · **modified** R36 (the dialog's date picker binds whichever way the dialog arrived, +1 scenario) · **modified** R37 (Copy as template stands in the header right, 34px, +1 scenario) · **added** R43 (the verse checklist speaks verse IDs and names numbers, 3 scenarios) | requirements 42 → 43; scenarios +6 |
| `overlay` | `docs/spec/overlay.md` | **modified** R2 (two-line cap: fit shrinks `font-size`, floor 11px; +3 scenarios) · **modified** R1 (service-data cache invalidation: `update` message + 10 s visible-only re-read; +2 scenarios) | scenarios +5 |
| `dock` | `docs/spec/dock.md` | **added** R13 (a saved change re-reads the open service: message drop + 10 s visible-only re-read, in place; 2 scenarios) | requirements 12 → 13; scenarios +2 |

## Not folded

- nothing — every behaviour change the slice shipped is folded; no accepted gaps.

## Counts

- requirements added: 2 (`reading/R43`, `dock/R13`)
- requirements modified: 5 (`reading/R9`, `reading/R36`, `reading/R37`, `overlay/R1`, `overlay/R2`)
- requirements removed / renamed: 0
- `last folded` moved to 2026-11-15 and `195-hotfix-batch` prepended in all three files.
