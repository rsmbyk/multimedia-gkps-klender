# Data model: a media entry ends on a rest like every other entry

**Spec**: `specs/165-media-entry-rest/spec.md` · **Base**: `develop` `59182b12`

No stored data changes: no model, no migration, no field. The slice changes only the list of projection
screens `_projector_data` builds at request time.

## The screen object

A projector screen is a plain dict with a fixed core and one optional payload:

| key | rest (measured, service 149 screen 1) | media screen (screen 2) |
| --- | --- | --- |
| `blank` | `true` | `false` |
| `header` | `""` | `""` |
| `lines` | `[]` | `[]` |
| `entry_index` | `0` | `1` |
| family payload | absent | `image_sha256` = the identity's sha |

The family payload key is the only thing that differs between the five media screens:

| family (`MediaFamily`) | key |
| --- | --- |
| `image` | `image_sha256` |
| `audio` | `audio_sha256` |
| `video` | `video_sha256` |
| `pdf` | `pdf_sha256` |
| `slides` | `slides_sha256` |

A rest carries **no** `bait`, `bait_rest`, `split`, `split_total`, `translation` or payload key — the same
four keys the built-in blank has today.

## The entry range

`_projector_data` returns `{'screens': [...], 'entries': [...]}`. Each entry is
`{'type', 'label', 'untitled', 'start', 'end', 'baits', 'translation'}`; the dock's step list
(`buildStops`) and the projector's entry stepping (`moveEntry`, `unitBoundary`) read `start`/`end`.

| entry | today | after |
| --- | --- | --- |
| text / legacy / passage / song | unchanged | unchanged |
| section break | `start == end`, one blank | `start == end`, one blank |
| media with a file | `start == end`, the payload screen | `start`, `start + 1` — payload screen, then rest |
| media with no file | `start == end`, one blank | `start == end`, one blank (no second) |

## Before / after on real services

**Service 149** — 1 legacy text + 4 image entries:

| | today | after |
| --- | --- | --- |
| screens | 6 | 10 |
| entry ranges | `(0,1) (2,2) (3,3) (4,4) (5,5)` | `(0,1) (2,3) (4,5) (6,7) (8,9)` |
| blank screens | `1` | `1, 3, 5, 7, 9` |
| last screen | the fourth image | a rest |

**Service 146** — 1 passage + 1 slides entry: screens 3 → 4; ranges `(0,1) (2,2)` → `(0,1) (2,3)`.

**Service 144** — 16 entries, measured ranges today:

| entry | its screens today | after |
| --- | --- | --- |
| 1 passage `Kisah Para Rasul 1:1` | `0–1` | `0–1` |
| 2 video | `2–2` | `2–3` |
| 3 image `images.jpeg` | `3–3` | `4–5` |
| 4 song | `4–18` | `6–20` |
| 5 PDF `Receipt-2773-9204.png` | `19–19` | `21–22` |
| 6 text `VOTUM, INTROITUS, DOA` | `20–84` | `23–87` |
| 7 audio `Sujud & Terima Kasih` | `85–85` | `88–89` |
| 8–10 songs `HAL 7`, `HAL 1`, `HAL 7` | `86–112`, `113–133`, `134–160` | `90–116`, `117–137`, `138–164` |
| 11–16 section breaks | `161–166` | `165–170` |
| **total screens** | **167** | **171** |

Every non-media entry keeps its own screens and its own rests, shifted by the four media rests; each
media entry gains exactly one. The six trailing breaks keep one screen each.
