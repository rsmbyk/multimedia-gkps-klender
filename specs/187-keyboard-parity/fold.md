# Fold — spec 187 · one keyboard grammar for the dock and the projector

**Run**: 2026-11-05 · at Converged (2 passes, no accepted gap)
**Plan's bump declaration**: `minor` (1.26.4 → 1.27.0), applied at delivery as `C-SDD-VER` requires —
Fold carries no version.

## Capabilities touched

| Capability | Operations | Before → after |
| --- | --- | --- |
| `dock` | `R1` modified · `R3` modified · `R4` modified · `R5`…`R11` added | 4 → 11 requirements |
| `projector` | `R1` modified · `R9` modified · `R12` modified · `R13` added | 12 → 13 requirements |
| `display-state` | `R2` modified | 3 → 3 requirements |
| `overlay` | `R1` modified | 8 → 8 requirements |

No requirement was removed and none was renamed. `docs/GLOSSARY.md` gained one term, **Unit** (OBS
surfaces), which FR-012 and `dock.md`'s `R9` both lean on.

## What each operation carries

**dock**
- `R1` — a Go To now starts from the picker as well, with the same layer, lookup and keys, and a
  picker's go to stands alone (`service: null`, the runner holding the block, `Back` idles and returns
  to the picker). The runner's adoption of the browsed service is unchanged.
- `R3` — the live block also paints a go to that names no service (head `Go To`, no date line, the
  switch control usable), and the keys inside a go to are the projector's: verse, chapter, book, with
  a crossing fetching exactly the chapter it enters.
- `R4` — the band covers whichever view is showing; opened from the picker, its footer rides that view.
- `R5` — `Esc` returns to the picker on a 900 ms hold, cancelled by release, blur, the tab hiding or a
  layer opening; the tap still closes a layer.
- `R6` — the picker moves on `↑` / `↓` only.
- `R7` — `K`'s sheet: five groups on the runner and the picker's two leading on the picker, the
  projector's wording verbatim and in its order, a layer closed by `K`, `Esc`, the close control and
  the 8 px frame.
- `R8` — a fetch in flight refuses every key and pointer that would change what is on air, header
  `Loading…`.
- `R9` — `Home` / `End` act on the unit on show, by the projector's `unitBoundary`, `Shift` taking the
  bait or the entry's own ends, `Ctrl`/`⌘` the service's first or last entry.
- `R10` — the band keeps the keyboard in its field across a window that returns.
- `R11` — a refresh opens what is on air, not the picker.

**projector**
- `R1` — a go to that names no service is painted from its own payload, and `Back` leaves the page
  idle.
- `R9` — the sheet's frame follows its tallest column (686 px at 1080p, measured on the running page),
  never clips a row, and scrolls on the app's own scrollbar.
- `R12` — the sheet is grouped by subject in three columns (`Service` / `Song` / `Image and PDF` /
  `Audio and Video`, then `Passage` / `Library Detour`, then `Display` / `Find`), `Audio and Video`
  merged with one `Play/Pause`, `Passage` merging the verse and library rows, `Display` and `Find`
  each one group in the owner's order; one scrolling column below 1125 px; the topmost layer while
  open.
- `R13` — `⌘` and `Ctrl` are one modifier for the arrows and `Home`/`End`, and every other `⌘` chord
  is the browser's.

**display-state**
- `R2` — a go to may stand with `service: null`; `goTo`, `stepGoto`, `hide`, `resume` and `flip` act on
  it, `back` leaves the idle state, `show` ends it.

**overlay**
- `R1` — it paints a go to that names no service from the go to's own payload, and `Back` paints
  nothing.

## Spec at fault, resolved at Converge

The slice's only `contradicts` finding was C1 (`converge.md`): FR-012 required both "moves nothing on
an entry with none" and "the arithmetic SHALL be the projector's own `unitBoundary`", which cannot
both hold. The owner chose the projector's behaviour; `R9` above records the resolved rule.

## Not folded

Nothing. No accepted gap, no undeclared behaviour change.

## Before → after by the numbers

| | Before | After |
| --- | --- | --- |
| `dock` requirements | 4 | 11 |
| `projector` requirements | 12 | 13 |
| `display-state` requirements | 3 | 3 |
| `overlay` requirements | 8 | 8 |
| Glossary terms | — | +1 (`Unit`) |
