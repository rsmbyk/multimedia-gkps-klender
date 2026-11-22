# Preview: Add song with the songbooks sidebar closed

**Spec**: `specs/222-add-song-parent-closed/spec.md`
**Shape**: static
**Open**: `specs/222-add-song-parent-closed/preview/index.html` opened directly

## Run

none: open the file directly. It links the project's real `tokens.css`, `fonts.css` and
`components.css` from `static/styles/design/`.

## States to click through

| State | How to reach it | What to look for |
| --- | --- | --- |
| both open | open the page | `#songAdd` is `display: flex`, 38px high; `#panelAdd` is visible |
| current CSS, parent closed | click **Close songbooks only**, then **Current CSS** | `#chapters` stays visible but `#songAdd` is `display: none`, 0px high — the reported bug |
| proposed CSS, parent closed | click **Close songbooks only**, leave **Proposed CSS** selected | `#songAdd` stays `display: flex`, 38px high; `#panelAdd` is `display: none` |
| parent mini | click **Mini parent** while the songs list is open | same proposed result with `data-nav="mini"` |
| songs list closed | click **Close songs** | no visible `.editor-add` |
| hymn / no book | click **No songbook** | the rendered button carries `disabled` and stays visible when the parent is closed |
| responsive | resize to 1000×800, then 390×844 | the button follows the visible songs list at each breakpoint |

## Live or static

**Static** — assembled from the reading shell's own markup, class names and stylesheets, with
only the candidate selector in `preview.css` and the comparison toggles added. It shows CSS
state; it cannot show a fetch, the editor POST or uploaded media — those stay covered by the
product's E2E suite.

## What is not a preview

A screenshot, a static image and a recording are not previews.
