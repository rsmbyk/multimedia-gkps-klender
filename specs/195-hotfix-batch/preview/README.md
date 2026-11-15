# Preview — spec 195

## Static

`index.html`, opened over `file://` (or `::preview{file=specs/195-hotfix-batch/preview/index.html}` in the desktop chat).

States it demonstrates:

- **US1** — a Today row at rest (badge as accepted) and hovered (badge hidden, date hidden, edit/delete revealed). The badge stays in the row's accessible label.
- **US2** — the Edit Tata Ibadah modal's header: title left, Copy as template right (34px tall), hairline rule under the row. Numbers ported from spec 167's accepted preview.
- **US5** — two overlay caption fixtures: one lyric that already fits (unchanged size), one that wraps (fit shrinks the type to two visual lines, floor 11px). The fit loop on the page is the planned mechanism; the caption CSS is the real sheet's block.

## Live (US3, US4, US6 — fetches and server rendering)

Serve the slice worktree, then click through:

```
cd ~/Projects/multimedia-gkps-klender-195
~/Projects/multimedia-gkps-klender/.venv/bin/python manage.py migrate --noinput
~/Projects/multimedia-gkps-klender/.venv/bin/python manage.py runserver 0.0.0.0:8765 --noreload
```

- **US3** — sidebar → click a template row (stage swap) → "+ New Tata Ibadah from template" → Next → click **Date**. The calendar must open. Then reload the template page by URL (deep link) and repeat — must open the same way.
- **US4** — sidebar → open a service → add a song entry → pick a song, check verses, **Save**. The entry saves; the stage names the verse numbers. Refuse-path: empty the checklist and save — the refusal still names it. Reopen the entry for edit — the server-rendered checklist shows the same rows as the fresh picker, summary in numbers.
- **US6** — put the service on air (Project), open `/obs/source/overlay` beside it, edit one of its entries in the service stage, save. The overlay repaints the changed words; the dock (`/obs/source/dock`) follows.
