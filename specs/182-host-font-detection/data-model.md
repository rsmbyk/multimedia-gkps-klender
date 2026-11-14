# Data Model — the computer's own fonts reach the converter

No database entity is added or changed. The entities below are filesystem facts: two directories, the
mounts that carry them into the `media` container, and the order that decides which one wins.

## Host font source

| Field | Value |
| --- | --- |
| Path | platform directory — `C:/Windows/Fonts`, `%LOCALAPPDATA%\Microsoft\Windows\Fonts`, `/System/Library/Fonts`, `/Library/Fonts`, `~/Library/Fonts`, `/usr/share/fonts`, `~/.local/share/fonts`, `~/.local/share/gkps-fonts` |
| Mounted at | `/usr/share/fonts/host/<n>`, read-only, `<n>` assigned in discovery order |
| Identity | the path itself; the same path yields the same mount |
| Lifecycle | discovered by the launcher at every start; absent when plain `docker compose up` is used; a directory that does not exist is skipped, never created |
| Owner | the operating system, or the person who installed the font |

## Operator font directory

| Field | Value |
| --- | --- |
| Path | `GKPS_FONTS_DIR`, defaulting to `.fonts/` inside the checkout |
| Mounted at | `/usr/share/fonts/operator`, read-only |
| Identity | the resolved absolute path |
| Lifecycle | created empty by Docker when missing (unchanged behaviour); re-scanned when the companion starts; may hold a face the computer does not have |
| Owner | the operator — a file placed here is a deliberate choice |

## Precedence

1. **Operator directory** — wins a same-family clash, because placing a file there is deliberate
   (owner decision, 2026-11-01).
2. **Host font source** — wins over the image's substitutes, because it is the face the machine is
   licensed for.
3. **Image substitutes** — used only when the family is absent from both, which is the state the image
   is built and verified in.

The order is expressed once, in `docker/slides-fonts.conf`, as the order of its explicit `<dir>`
entries; `binding="weak"` is what lets an installed family outrank its alias.

## Derived facts

- **Font inventory** — `fc-list` inside the container; already part of the renderer identity
  (`multimedia/local_media.py`), so a source that appears or disappears changes the derivative's key.
- **Generated override** — `${TMPDIR:-/tmp}/gkps-host-fonts.yaml`, rewritten at every launcher run;
  never committed, never read by the application.
