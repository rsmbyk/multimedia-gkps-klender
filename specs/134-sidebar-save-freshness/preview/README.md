# Preview: Keep reading views current after sidebar edits

**Spec**: `specs/134-sidebar-save-freshness/spec.md`
**Route**: `http://127.0.0.1:8770/tatib/1/` (disposable preview data)

## Run

From the repository root, run:

```sh
specs/134-sidebar-save-freshness/preview/run_preview.sh
```

The script migrates an isolated SQLite database under `/tmp`, seeds one editable Tata Ibadah,
songbook, and song, then serves the current project on port `8770`. Stop it with Ctrl+C; the temporary
database and static directory are removed. `GKPS_PYTHON` can point to a Python environment that has
the repository dependencies installed.

## States to click through

| State | How to reach it | What to look for |
| --- | --- | --- |
| Active Tata Ibadah edit | Open `/tatib/1/`; edit the Tata Ibadah row from the first sidebar and save a changed name | Current code updates the stage heading while the first-sidebar row keeps the old name; the accepted behavior is that both show the saved name. |
| Active song edit | Open `/songs/1/`; edit the song from the second sidebar and save a changed title | Current code updates the stage heading while the second-sidebar row keeps the old title; the accepted behavior is that both show the saved title. |
| Active songbook edit | Keep `/songs/1/` open; edit its songbook from the first sidebar | Current code updates the songbook heading but leaves its first-sidebar row stale. |
| Search result | Open `/search?q=Preview`, select Kidung in the rail, open the matching songbook and edit the matching song | Current code refreshes the sidebar row but leaves the matching search result stale. |
| Unrelated stage | Open `/bible/1/1/`, select Kidung, and edit the songbook row | The Kidung list refreshes while the Bible chapter stays open. |

This is a live preview, not a screenshot or mockup. The reproduction states use the same editor save
path that the proposed behavior changes. Saving only changes the disposable preview database; it does
not touch the shared development database.

## Live preview or mockup

**Live preview** — the current project route and components. The change is behavioral: the visible
content after a save is the subject of the review, and the surrounding UI is unchanged.

## What is not a preview

A screenshot, a static image, and a recording are not previews at either tier.
