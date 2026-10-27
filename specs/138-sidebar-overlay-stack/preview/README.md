# Preview: the sidebar drawer stack

**Spec**: `specs/138-sidebar-overlay-stack/spec.md`
**Shape**: a live prototype at `specs/138-sidebar-overlay-stack/preview/prototype-tatib.html`
(and `prototype-songs.html`)

Open either file in a browser. It is the project's own page — shell, rail, panels, stage, type,
tokens and stylesheets — with the page's scripts removed and `proto.css` + `proto.js` added. The
prototype adds the drawer behaviour and a small control panel of its own; **nothing else on screen
is the proposal**.

Every number below is measured by `probe_prototype.py`:

| Width | Mode | Stage closed → level 1 → level 2 |
| --- | --- | --- |
| 1440 | columns | 1360 → **944** → **528** (today's push, untouched) |
| 1024 | overlay | 944 → 944 → 944 |
| 768 (your screenshot) | overlay | 688 → 688 → 688 |
| 425 (your screenshot) | overlay + toolbar | 425 → 425 → 425 |

At 1024 and 768 the first drawer is 416/368px wide at the rail's edge and the second covers it
exactly — same left edge, same width — while the stage never moves. A drawer at rest sits behind the
rail and slides out from under it. The backdrop dimmed the page and closed the stack on a click; the
rail reopened **both** levels because the last level open was the second one.

## The controls

The **⚙ prototype** chip at the bottom right opens the panel:

| Control | What it changes |
| --- | --- |
| **Overlay at** | where the drawers take over from the columns: 1272 / 1024 / 720 |
| **Toolbar at** | where the phone shell starts: 720 / 560 / 425 |
| **Level 1 / Level 2 / Close** | drive the stack without hunting for the right row |
| readout | `width · mode · levels` |

Resize the window with the panel open and the readout tells you which side of the threshold you are
on. Flipping **Overlay at** re-classifies the same window immediately, so the three candidate
breakpoints can be compared without resizing.

## What to look at

| State | How to reach it | What to look for |
| --- | --- | --- |
| Today's layout, untouched | 1440 wide | the columns still push: opening level 1 narrows the stage |
| The reported 768px screen | 768 wide, **Overlay at ≤1272** | the stage stays 688px; the drawer floats over it |
| A stack | 768, **Level 2** | the second drawer covering the first exactly, its shadow the only separation |
| Closing | click the dimmed page | both levels close, the stage is unchanged |
| The rail restores | click the rail's Tata Ibadah icon after closing | both levels return, together |
| The phone toolbar | 425 wide | the control, then the logo, at the left; transfer and theme at the right |
| The rail as a drawer | 425, the control | the five sections, icon **and name**, one per row; no logo, no footer |
| A section over the menu | 425, menu open, then a section | the list slides in **over** the menu, which stays underneath; the control stays a close glyph; the list's own back returns to the menu.
| A service on a phone | 425, a Tata Ibadah service | no contents drawer is offered, the Project control is not drawn, and tapping a service row closes the drawer onto the page |
| A phone's rows | 425, the section list | every row is two lines — name over date — with its pencil always on and no text under it |
| The phone's drawers | 425, **Level 1** then **Level 2** | the window's full width, the second covering the first; the control reads `back` |

## Rebuild and measure

```sh
export DATABASE_URL="postgres://multimedia:***@127.0.0.1:59075/multimedia"
PY=/home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python
$PY manage.py collectstatic --noinput
$PY manage.py runserver 0.0.0.0:8772 --noreload
$PY specs/138-sidebar-overlay-stack/preview/build_prototype.py    # the two prototype pages
$PY specs/138-sidebar-overlay-stack/preview/probe_prototype.py    # the numbers above + screenshots
```

## What this preview cannot show

The page's own scripts are removed, so in-page navigation, the filter, the row edits and the
projector do not run here; the prototype's rows open level 2 instead of following their links. The
proposal is layout and dismissal — every behaviour it adds is driven by `proto.js`, which the real
implementation replaces with the shell's own state machine.
