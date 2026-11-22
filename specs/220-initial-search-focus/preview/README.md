# Empty search landing focus preview

**Spec**: `specs/220-initial-search-focus/spec.md`
**Shape**: static
**Open**: `specs/220-initial-search-focus/preview/index.html` opened directly

## Run

```sh
# Open specs/220-initial-search-focus/preview/index.html in a browser; no server is needed.
```

## States to click through

| State | How to reach it | What to look for |
| --- | --- | --- |
| Empty landing | Initial load, or choose **Empty landing** from the lower-right preview-state menu | Search field has DOM focus, stays empty, and the page does not scroll. The stage is byte-identical on `/`, `/search/`, `/bible/`, `/songs/` and `/tatib/`, so this one state stands for all five; only the rail section behind it differs. |
| Landing with keyboard input | Type without clicking the field | Text goes into the landing field; no submit occurs until Enter or the Search button. |
| Sample results | Type a value and submit, or choose **Sample results** from the preview menu | Captured server-rendered `garam` results are visible; the compact field is not focused. Matching is not simulated. |
| Results back to landing | Choose **Empty landing** | Results hide, the query clears as for a fresh landing, and focus returns to the landing field. |
| Dark theme | Open the lower-right menu and choose **Switch to dark theme** | Existing project dark tokens and the same focus state are used. |
| Responsive | Resize to 1440×900, 720×900, 390×844 and 320×568 | Landing geometry remains the existing layout; results compact-bar offsets remain 46px (desktop) / 82px (≤720px), and the results section begins at 128px / 164px. |

## Live or static

This static preview uses the captured public reading shell, its real class names and server-rendered `garam` result markup, the project's stylesheets, tokens and bundled logo. The preview-only script switches landing/results state and models the focus boundary. It does not query the search endpoint or simulate search matching. It is appropriate because the proposed change affects focus in an existing shell and does not change server-rendered data or APIs.
