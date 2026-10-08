---
id: ITEM-034
status: in_review
title: 'Preview a service entry''s full content in a modal'
type: feat
priority: P2
effort: L
created: 2026-10-08
updated: 2026-10-08
spec: specs/032-entry-preview-modal/spec.md
branch: feat/032-entry-preview-modal
pr:
archived_at:
archive_reason:
bump: minor
release_version: 1.3.0
---

# ITEM-034: Preview a service entry's full content in a modal

## Summary

Give each service entry on the Tata Ibadah page a preview button that opens a read-only modal
showing the entry's whole content — a text's full words, a passage's full text, or a song's selected
lyrics — so the operator can read what the pane only abbreviates, without leaving the page.

## Modal behaviour

- **View-only.** No inputs, nothing to edit; it only shows the entry's content.
- **No header.** The modal carries no title bar.
- **Scrollable.** Long content scrolls inside the modal rather than growing past the viewport.
- **Sticky close.** A close button stays at the bottom of the modal.
- **Dismisses** on a click on the overlay (outside the modal) and on **Esc**.
- **Focus, done right.** Must not reproduce the stale focus/outline bugs the sidebars had
  (spec 025 / ITEM-027, ITEM-016): the trigger must not keep a lingering outline/hover state after
  the modal closes, and focus should return to the trigger deliberately, not leave a stray outline.

## Content, per kind

- **Text** — the whole text that the pane hid (clipped/ellipsized, ITEM-033). The preview button is
  only shown when there is hidden text, i.e. the text is long enough to be clipped.
- **Passage (scripture)** — the full passage text, with its reference(s) at the top.
- **Song** — the song's info (songbook and song title) and all the selected verses' lyrics,
  separated into tabs. The tabs are centered horizontally and scrollable when there are many.
- **Section break** — carries no content; assumed to have no preview (see open questions).

## Notes

- **Entry actions.** The controls live in `multimedia/web/templates/reading/tatib.html`
  (`entry__acts`); a preview button joins them. Text entries and legacy text rows both need it.
- **Where the content comes from.** `ServiceEntry.resolve()` (`title`, `body`), `_scripture_body()`,
  and `citation()` in `multimedia/tatib/models.py` already answer the full text per kind; the pane
  deliberately shows a passage/song by reference only (`shows_text` in `reading/views.py`), so the
  modal needs its own path to the whole body.
- **Modal infrastructure.** See `static/web/editors.js` and the editor fragment flow for the
  existing modal pattern; this one is read-only and needs its own no-header/sticky-close shape.
  Decide whether the content is rendered inline (hidden) with the page or fetched on demand.
- **Focus guard.** Reuse the approach from spec 025 ("quiet modal focus") rather than the sidebar's
  earlier focus/outline behaviour.
- **Legacy rows.** `TataIbadahItem` (old text/END_OF_SECTION rows) share the pane; decide if legacy
  text rows get the same preview.

## Open questions

- Which kinds show the button — text / passage / song only, or also section breaks?
- Content rendered with the page (hidden) or fetched when the modal opens?
- Song tabs: one per selected verse; what label (verse number)?
- Does a very long text use the modal's scroll only, or its own clamp plus scroll?
- Is the Esc/overlay dismissal shared with the existing editor modals, or independent?

## Acceptance sketch

- Each eligible entry shows a preview button.
- Text: opens the full text; button only appears when the pane clipped something.
- Passage: opens the full passage text with the reference above it.
- Song: opens the songbook/title and all selected lyrics in centered, scrollable tabs.
- The modal is view-only, headerless, scrolls, and has a sticky close button.
- Clicking the overlay or pressing Esc closes it, and no row is left with a stale focus outline.

## Links

- Spec: [032 — Entry preview modal](../../specs/032-entry-preview-modal/spec.md)
- Related items: ITEM-033 (clamped pane text), ITEM-027 / spec 025 (quiet modal focus),
  ITEM-016 (stale row-edit visibility)
