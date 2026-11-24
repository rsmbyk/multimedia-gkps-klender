# Live preview — spec 237

The change is applied in the slice worktree at
`/home/rsmbyk/Projects/multimedia-gkps-klender-237`. Start it if needed:

```
python ~/.hermes/cache/scratch/gkps237/run.py runserver 0.0.0.0:8776 --noreload
```

Open `/` first, click the **Tata Ibadah** rail, then open the service `111ojo`
(pk 151). Its contents list has one-line rows, a two-line song row, media, passage,
text and slot marks with the corner badge.

States to try:

- **Theme**: switch light/dark with the site control; the mark stays centred in both.
- **Hover / selected**: point at a row and click it; the mark keeps its centred seat.
- **Wrap**: resize the window to 1024px and 390px; the song row grows from 53px to
  74px and its mark stays centred.
- **Drag copy**: drag a row by its grip; the copy's mark follows its number.
- **Before control**: `probe.py` reverts only the mark's `align-self` inline on the
  live page to read the pre-change numbers; the served code keeps the fix.

Run the measurement harness (venv Python with Playwright, local Chrome):

```
~/Projects/multimedia-gkps-klender/.venv/bin/python \
  specs/237-sidebar-mark-centering/preview/probe.py
```

It prints the per-row before/after centre offsets at 1440px, 1024px and 390px, plus
the slot badge and number boxes.
