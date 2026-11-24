# Live preview — spec 240

The fix is applied to the served CSS in the slice worktree at
`/home/rsmbyk/Projects/multimedia-gkps-klender-240`. Start the server if needed:

```
python3 ~/.hermes/cache/scratch/gkps240/run.py runserver 0.0.0.0:8790 --noreload
```

Open `/` first, click the **Tata Ibadah** rail, then open the service
`hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh` (pk 149). It has a modern text row and media rows.

States to try:

- **New text**: `+ Text` on the add row — title inset 26px/21px with a divider.
- **Edit text**: the pencil on the text row (pk 21) — same band on the Edit form.
- **New media**: `+ Media` — same band on the large media Create form; the 190ms
  entrance animation ends before measuring.
- **Edit media**: a media row's pencil — compact dialog, title unchanged.
- **Narrow**: resize to 390×844 — band becomes `16px 18px`, divider retained.
- **Theme**: switch light/dark — the rule uses `var(--divider)` in both.
- **Verse**: open a song's Add verse — spec 226's single header rule is unchanged.
- **Before control**: `probe.py` injects a browser-local override to read the broken
  numbers; the served code keeps the fix.

Run the measurement harness (venv Python with Playwright, local Chromium):

```
~/Projects/multimedia-gkps-klender/.venv/bin/python \
  specs/240-entry-modal-title/preview/probe.py
```

The media library itself is served by a companion pinned to the compose origin, so
this slice's port may show `media library unavailable` behind the dialog; the title
band and form controls are rendered by this server and are unaffected.
