# Spec 243 — navigation pending rules (accepted at gate 1)

These are the owner's rules for this slice. They were accepted at gate 1 with
preview v14; the accepted specification is `../spec.md`. No implementation is
authorized by the acceptance.

## Lock style decision

The clicked item's busy state is **dim only**: the rail icon stays in place at
reduced opacity, and a sidebar row dims. No spinner, `Opening…` label, edge
fill or fill ring. The stage bar and prefilled placeholder (for writes) remain
the only explicit loading signals. This replaces the spinner previously shown
in the rail and the row.

## R4 — Bars follow the updated section

A loading bar is drawn at the **very top edge** of the section whose content
the fetch will replace when it finishes. The reading page bar from R2 is one
instance of this rule.

- Clicking a rail menu updates the **first-level sidebar**; if that sidebar is
  open, a bar appears at its top. When the **second-level sidebar** is also open
  and will be refreshed, a second bar appears at its top.
- Clicking a first-level row (songbook / book) updates the **second-level
  sidebar**; a bar appears at its top.
- Clicking a second-level row that writes to the reading page uses the bar above
  the reading page, as already defined.
- A section that is closed, or that the fetch will not update, gets no bar.

The dim-only lock from the decision above still applies to the clicked item.

## R1 — The clicked item locks

- On activation of a rail or sidebar item, that item enters a busy/disabled
  state immediately.
- **Rail:** the icon stays in place at reduced opacity; no spinner or replacement glyph.
- **Sidebar row:** the row is disabled and its edit/delete/add controls are disabled too;
  neither the row nor those controls can be activated until its own fetch settles —
  success, failure or cancellation.
- Other items stay activatable, subject to R3.

## R2 — Fetches that change the reading page

A fetch that **writes content into the reading page** — opening a song, a
Bible verse/passage, or a Tata Ibadah service (including when reached from a
search result) — additionally:

1. disables the reading page (no interaction while it is pending),
2. shows a loading bar **above the reading page**, not at window top,
3. shows a placeholder in the reading page, pre-filled with whatever is already
   known from the sidebar: title, name, code, section label, etc.

Opening a rail section, a Bible chapter list, or a songbook fetches only a
list. It does **not** write to the reading page and follows the list-only rule
below. "Change the reading page" is about writes to the stage, not about which
panel fetched.

Local fetches that do **not** change the reading page — opening/switching a
rail or sidebar list, the current book's chapter toggle, a mode switch — apply
R1 only. They MUST NOT disable the reading page, show a bar, or replace any of
its content: whatever is being displayed stays exactly as it is. This was
clarified after the first rules draft; it is a refinement of R2, not a separate
stage class.

## R3 — Superseding clicks

- Activating another item while a fetch is in flight **cancels** that fetch and
  fetches the newly clicked item.
- Exception: if the in-flight fetch **would change the reading page**, it is
  cancelled only when the new fetch **would also change the reading page**.
  Otherwise the first fetch continues and the new item's own request proceeds
  alongside it.
- A cancelled item leaves its busy state at once. A cancelled stage-changing
  fetch releases the reading page only if no other stage-changing fetch is
  still pending.
- This replaces the present queue in `static/web/reading.js:1499-1504`
  (`navBusy` / `pendingNavigation`): a later stage-changing click supersedes
  rather than queues; a non-stage-changing click no longer waits behind a stage
  fetch.

## Correction to the labels used in v5/v6

The previews labelled rail clicks, chapter-list clicks and songbook clicks as
"→ page". That was wrong. Only song, verse/passage and service writes count as
stage-changing; rail, chapter list and songbook are list-only. The next preview
must relabel and rewire those scenarios before any gate.

Owner confirmation: the **chapter-number list is list-only**, while opening a
**verse/passage** from it is the write to the reading page.

## Delta from earlier rounds

- **v1 (global bar + row inset)** — the bar was at window top and no control was
  disabled. Now the bar sits above the stage only and the clicked item locks.
- **v2 (solid/dashed source marks + queue)** — marks described state but left
  controls clickable and queued the second click. Now the item is disabled and
  the second stage-changing click cancels the first.
- **v3 (strip / skeleton / placeholder rows)** — the destination got a busy
  state but the item and stage stayed interactive. Now the stage is disabled and
  its placeholder is seeded from sidebar data.
- **v4 (optimistic selection)** — the selection moved before the response. That
  is dropped: the operator gets a spinner on the clicked control instead.

## Relation to the research

First-party guidance (Primer, Wix) discourages disabling controls during
loading because it can hide focus and confuse assistive technology. This rule
deliberately overrides that for the reading shell: an operator must not be able
to re-trigger the same item while its fetch is live. The deviation is recorded
here so gate 1 can see it explicitly, not silently.

## Open detail

- The disabled sidebar row's exact visual (spinner placement and dimming) is
  still to be confirmed before the preview is built.
