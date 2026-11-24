# Preview — spec 238 passage search comboboxes

**Live preview** at `http://127.0.0.1:8792/tatib/151/`. From `/`, open the Tata Ibadah rail and
the service `111ojo` (id 151); the start bar's `+ Passage` opens the modal. If the server is
down, run from the slice worktree:

```
python specs/238-passage-search-pickers/preview/run.py runserver 0.0.0.0:8792 --noreload
```

`run.py` reads the database URL from the compose web container, so no credentials are written
to disk.

## States to drive by hand

| State | How to reach it | What to look for |
| --- | --- | --- |
| Rest | Open `+ Passage` | Book is a search field; Chapter, From verse and To verse are the original button popovers with chevrons; the numeric buttons are disabled until the preceding list is loaded |
| Book focus | Click the Book field | Full 66-book list in two Testament groups; text selected so typing replaces it |
| Book filter | Type `mat` | Imamat + Matius only; empty hint when nothing matches |
| Book active | ArrowDown / ArrowUp | One option tinted at a time |
| Book chosen | Enter or click | Field shows the book name in the active translation; menu closes; Chapter enables and shows `1` |
| Chapter filter | Click the Chapter button, type `1` in the filter inside the popover | Chapters 1, 10–19, 21… filtered by number substring |
| Verse cascade | Choose chapter 10 | Verses for that chapter load; From verse enables and its label shows `1` |
| From verse filter | Click From verse, type `1` in its popover filter | Matching verse numbers; choosing one refreshes To verse |
| Translation | Toggle TB/SIM | Book labels, group headings and the chosen book's translation-aware id change; cascade reloads |
| Dismissal | Escape, or click outside | Only the menu closes; the dialog and all field values stay |
| To verse filter | Choose a start verse, click To verse, type `1` in its popover filter | Later verse numbers containing 1; choosing one sets `verse_end` |
| One menu | Focus Book, then open Chapter, then To verse | Only the newest menu is visible; the previous one closes |
| Tab commit | Type in Book or any popover filter, press Tab | The highlighted (or first visible) match is chosen and focus lands on the next field |
| Edit | Open an existing passage entry | Stored book/chapter/verse show in the fields and hidden selects |
| Dark theme | Toggle the app theme | Same chrome, theme tokens |

To verse keeps its button picker and "No ending verse"
state and hover note; only the in-menu filter was added.

## Probes

- `probe.py` — exercises focus/filter/keyboard/choose/Escape/outside-click and prints the
  field geometry, hidden select values and active-option counts.
- `parity.py` — measures the passage fields and menus against `#entry-song-search` in the
  song modal at 1440×900.
- `run.py` — manage.py wrapper for the live server and shell.

Run either probe with the venv Python:
`/home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python specs/238-passage-search-pickers/preview/probe.py`.
