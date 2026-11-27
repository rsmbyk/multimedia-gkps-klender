# Preview: Add verse sits beside Project in the song header

**Spec**: `specs/231-add-verse-in-header/spec.md`
**Shape**: `live`
**Open**: `http://127.0.0.1:8772/songs/1880/` and `/songs/1909/`

## Run

```sh
bash preview/serve.sh 8772
```

`serve.sh` builds `DATABASE_URL` at runtime from the compose `web` container, so no credential is
stored in the repo.

## States to click through

| State | How to reach it | What to look for |
| --- | --- | --- |
| with verses | open `/songs/1880/` at 1440×900 | Add verse 111×34 at x=1157, y=42; Project 96×34 at x=1276; no dashed row below the lyrics |
| empty | open `/songs/1909/` | header has only the eyebrow; one 112×38 Add verse in the centre invitation |
| hover / focus | hover, then Tab to, the header button | existing `.verse-add__btn` hover and focus rings |
| click | click the header Add verse | `#editorModal` opens with `New verse` |
| read-only | open a hymn song such as `/songs/1613/` | no header actions |
| responsive | resize to 560px | Add verse stays in the header; Project is hidden by its pre-existing rule |

## Live or static

**Live** is served from the project: its own route, components and tokens, running. This slice is
live because the gates depend on server-rendered `verse_rows` and `can_edit_verses`, and the click
opens the real editor dialog.

## What is not a preview

A screenshot, a static image and a recording are not previews.
