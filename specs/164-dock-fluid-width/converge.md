# Converge: the dock fills whatever panel it is given

**Spec**: `specs/164-dock-fluid-width/spec.md` · **Plan**: `specs/164-dock-fluid-width/plan.md`

## Pass 1 — 2026-10-29

**What was checked**: every row of `plan.md`'s traceability table, by the method it declares. The
`test` rows were run, not assumed: `tests.e2e.test_obs_dock` + `multimedia.web.test_obs_dock`, 18
tests, green. The `inspection` rows were read in the files they name. The `manual` rows were read off
`probe/probe.py` against the live page.

**The code against the table**

| Row | Checked | Result |
| --- | --- | --- |
| FR-001 `.dock` full width and height, no cap, no centring | `obs-dock.css:29–39` | `width: 100%; height: 100%; margin: 0` — `max-width` gone, one `margin` declaration |
| FR-002 no horizontal overflow | the fill case | `overflow == 0` at 320/420/560/720/900/1440/1920/2560 |
| FR-003 one column at every width | `#pickBody` | no layout rule of any kind; the body keeps block flow |
| FR-004 a row spans the body's content width | the one-column case + the sheet | row = `clientWidth − 8 − 8`; the name is `flex: 1`, the date the row's last item |
| FR-005 the head keeps sticking | the one-column case | `position: sticky` at 560/900/1440/1920 |
| FR-006 nothing else moves | `git diff` | 5 insertions (one comment), 2 deletions (`max-width`, `margin: 0 auto`) — no other rule in the sheet changes |
| SC-001…SC-004 | the two cases | green; the numbers are the spec's table |
| SC-005 red on 1.23.1 | the stashed-stylesheet run | `AssertionError: 80 != 0 within 0.5 delta (80 difference) : panel starts at 80 at 720px` and `AssertionError: 544 != 884 within 1 delta (340 difference) : row spans 544 of 900px` — the width reason, not an import error |
| US3 AC1/AC2 (320, 420, 560 unchanged) | `probe/probe.py` | 320 → panel 320, row 304; 420 → panel 420, row 404; 560 → panel 560, row 544 — the spec's 1.23.1 column, unchanged |

**Findings**: `missing` 0 · `partial` 0 · `contradicts` 0 · `unrequested` 0.

**Outcome**: converged on the first pass. Nothing was changed inside the pass; no row rests on a
checkbox.

## History

- **2026-10-29 — pass 1.** 19 rows checked by their declared method; 0 findings; converged.
