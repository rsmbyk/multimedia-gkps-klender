# Preview — the companion's configuration page

Static preview for `specs/192-companion-origin-page/spec.md` (UI/UX). Open `index.html` over
`file://`, or through the desktop chat's `::preview` directive. No server, no dependencies — the
desktop frame's theme variables style it; opened directly the page themes itself.

The page mock is functional: add, edit, delete, the exact-origin validation (first broken rule
named), duplicates refused, renumbering after a delete. The set persists in this browser only
(localStorage) — the real page persists in the companion's volume.

The withdrawn launcher-prompt design is preserved beside it: `terminal.html` (with
`terminal.css` / `terminal.js`) — the walk-through of the prompt, the live setup simulator and the
transcripts that shaped the grammar now carried by the page's form.

## States

| State | Shows |
| --- | --- |
| First run | The empty state said outright: only this page and the local seeds may use the companion |
| Add | A valid origin joins the list in submission order; a broken rule is named under the form |
| Duplicate | `that origin is already recorded` — as an add or as an edit of another row |
| Edit | The row becomes an input with `Save`/`Cancel`, validated by the same rules |
| Delete | The row is removed and the list renumbers; deleting the last origin returns to the empty state |
| Local seeds | `Always allowed on this computer` — the two compose seeds, read-only |
| Fonts | The directories the converter sees with family counts; zero said outright |

## Not in the mock

The companion's enforcement side (403 naming this page, no CORS headers) and the web app's
surfacing of that refusal — both specified (FR-003, FR-008), verified at Implement.
