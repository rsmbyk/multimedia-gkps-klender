# Quickstart: An empty song names itself in the Verses section

Contracts: [`contracts/none.md`](./contracts/none.md). Data model: [`data-model.md`](./data-model.md).
Preview: [`preview/index.html`](./preview/index.html) (open directly; regenerate with
`python3 specs/235-empty-song-verse-summary/preview/build.py`).

## Run the targeted checks

From the worktree root, with the shared compose PostgreSQL reachable:

```bash
.venv/bin/python manage.py test multimedia.web.tests.ServiceEntryViewTests --keepdb
.venv/bin/python manage.py test tests.e2e.test_entries.EntryModalE2ETests --keepdb
```

`ServiceEntryViewTests` holds the server-rendered first-paint pin; `EntryModalE2ETests` holds
the Add/Edit modal pins, including the unchanged save refusal and the full-picker states.
Use the main checkout's venv (this worktree has none) and a unique `DATABASE_URL` database
name if another session is running tests against the shared server.

## What to look at by hand

1. Open a dated Tata Ibadah service from the home page and choose **Add Song**.
2. With no song, the Verses section is gone (0 px).
3. Search `Kosong` (the empty song) and pick it: the `Verses` label and a small bordered
   panel appear; its only line is `This song has no verses`; no tiles, helper or All/Clear.
4. Press Save: the dialog stays open with `This song has no verses: pick another song.`
5. Pick a song with verses: the full picker returns with verse 1 ticked.
6. Open an existing song entry whose song has no verses: the same summary-only state is
   present before the script runs.
