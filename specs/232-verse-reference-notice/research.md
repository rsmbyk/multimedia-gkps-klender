# Research: verse reference notice

## Decision / Rationale / Alternatives / Provenance

- **Decision** — Render the note as the first child of `.editor__actions` in the server fragment, and
  scope a neutral disabled state to `.editor__delete`.
  **Rationale** — `songs_verse.js:249-253` fetches `/editor/verse/<pk>/` and replaces `#editorContent` on
  every open, so the fragment is the only place the note survives a reopen. The existing row is
  `justify-content: flex-end`; giving the note `margin-right: auto` keeps the three buttons right without
  changing their order.
  **Alternatives** — (1) Append the note below the row as today: rejected, that is the reported problem.
  (2) Draw it in `songs_verse.js` after fetch: rejected, lost on the next open and duplicated in two
  renderers. (3) Fade the red button less: rejected, still reads as a danger action.
  **Provenance** — `multimedia/web/templates/reading/_editor_form.html:73-82`,
  `static/web/songs_verse.js:247-277`, `static/styles/design/components.css:847-867`.

- **Decision** — Reuse `named_service_count`; do not recompute or rename it.
  **Rationale** — `_editor_fragment_context` already loops `ServiceEntry` rows of kind `SONG` for this
  song and counts those whose `verses` contains the verse id (`views.py:176-186`). The page-level count at
  `views.py:2452` is song-wide and is not the modal's value.
  **Alternatives** — passing a new context variable: rejected, duplicates a query for the same fact.
  **Provenance** — `multimedia/web/reading/views.py`, `multimedia/web/reading/verses.py:116-129`.

- **Decision** — Wrap at `max-width: 650px`; the note takes a full-width line above the buttons.
  **Rationale** — measured in the preview: at 420px an inline note is squeezed to 99 × 72 (four lines)
  while the buttons occupy 246px of a 352px row. With the wrap the note is one 352 × 18 line and the
  buttons keep their own 38px row.
  **Alternatives** — shortening the copy at narrow widths: rejected, it drops the reason the button is
  disabled; shrinking the buttons: rejected, it changes every editor at that breakpoint.
  **Provenance** — `preview/README.md`, preview measurements at 840×900 and 420×900.

- **Decision** — No motion and no new token.
  **Rationale** — the note arrives with the fetched fragment; animating it would add a phase to a one-step
  explanation. All colours come from `--rail-bg`, `--divider`, `--head-ink`, `--ink`.
  **Alternatives** — a tinted warning banner (preview C): rejected by the owner in favour of B.
  **Provenance** — owner's preview choice 2026-11-23; `static/styles/design/tokens.css:20-45,87-113`.

## Unknowns remaining

0.
