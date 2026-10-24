# Preview: The sidebars say which nothing they show

**Spec**: `specs/129-sidebar-empty-states/spec.md`

**No mockup.** The request came with three screenshots of the defect and named the target state (centred,
under a glyph, typed empty versus miss), so there is no design fork to explore — the branch itself is the
preview, and the probe below is what measured it.

## The running branch

`quickstart.md` serves it on `0.0.0.0:8801`. Four states, all reachable from the reading shell:

| State | Route | Block |
| --- | --- | --- |
| empty sections | `/tatib/<a service with no entries>/` | list glyph · `No sections yet.` |
| empty songs | `/songs/book/<a songbook with no songs>/` | music glyph · `No songs yet.` |
| miss in the sections list | the same route with sections, filter `zzz` | magnifier-with-cross · `No matching sections.` |
| miss in the first column | `/bible/`, `/tatib/`, `/songs/`, filter `zzz` | magnifier-with-cross · `No matching <list>.` |

## The probe

`preview/probe_empty_states.py` opens each state in headless Chromium at 1440×900, prints the state, the
title, the hint, which glyph is displayed, and the block's ink offset from its pane's centre in CSS pixels.
Measured on the branch:

```
tatib <empty>  empty   "No sections yet."   glyph=empty   38px  dv=0.0  dh=0.0
tatib <filled> filter  "No matching sections."  glyph=filter  38px  dv=0.0  dh=0.0
tatib <filled> filter  "No matching Tata Ibadah."  glyph=filter  38px  dv=0.0  dh=0.0
songs <empty>  empty   "No songs yet."      glyph=empty   38px  dv=0.0  dh=0.0
songbook 1     filter  "No matching songs." glyph=filter  38px  dv=0.0  dh=0.0
collapsed panel        block display: none
```

The same script writes the screenshots this slice's review used; they are not committed (binary), the
numbers above are.
