# Loading feedback on rail, sidebars and stage — research notes

**Question:** how should the reading shell show that a rail click or a sidebar row is fetching, without making operators think the site is frozen?

**Status:** research only. No app code, preview, spec or board changed by this note. Sources are first-party design systems/specifications unless labelled otherwise.

## 1. Timing: acknowledge at once, delay the indicator

- The click itself should be acknowledged on the next frame; withheld visual feedback is what makes a page feel unresponsive.[5] That acknowledgement does not have to be a spinner — the selected state can do it.
- Human-factors limits are ~0.1 s for direct manipulation, ~1 s for uninterrupted flow, and ~10 s for sustained attention.[1] Between 0.1 and 1 s no special progress feedback is normally needed, but past 1 s the system should indicate it is working.[1]
- Thresholds differ by system: Material starts a loading indicator at 200 ms and switches to a progress indicator after 5 s.[17][18]
- Primer suppresses loading states under 1 s, uses indeterminate feedback for 1–3 s and determinate for 3–10 s.[23]
- Fluent uses <1 s none, 1–3 s spinner, >3 s progress bar or text.[21]
- Concrete delays from production systems: Stripe recommends 200–300 ms for data fetches and 100 ms for view transitions;[27] VS Code's progress UI starts after a 0.5 s delay to avoid flicker.[29]
- A percent-done display in the 2–10 s range is counterproductive because it flashes faster than users can track it.[1]
- A looped spinner is for roughly 2–10 s, not below 1 s and not beyond 10 s;[3] beyond 10 s give an estimated completion and a way to interrupt.[1][4]

**Reading for this app:** the pressed/selected row can acknowledge immediately; the visible busy state should be held back ~300 ms (Stripe's data-fetch value) so fast local fetches never flash. There is no percentage to report for a fragment fetch, so use an activity indicator, not a percent bar, unless a fetch exceeds ~5 s.

## 2. Placement: bind the sign to the region that changes

- Keep the navigation container mounted and interactive; put the loading state inside the component whose content is loading.[27] Stripe's explicit warning is that replacing the tab bar with a spinner removes navigation context and makes the app look broken.[27]
- VS Code changed view progress to appear on each view itself rather than at the top of the view container, "for a more direct connection between the long-running operation and its progress".[29]
- A linear progress indicator belongs on the edge of the loading container; the top-of-page position is for whole-page or group progress, not one item.[18] One indicator should cover a group rather than one per element.[18][23]
- Place the indicator nearest the content it stands in for and avoid layout shift when real content replaces it.[23] For new items beside existing content, put it in the empty space where the new content will appear, not over existing content.[17]
- For large areas with a predictable shape, a content skeleton preserves the shape and can improve perceived speed;[23] skeleton states are preferred over indicators for full-screen loads in Carbon.[25] GitHub's Primer recommends placeholder nodes for asynchronously loaded tree children, with a general indicator only as a fallback.[30]
- GitHub's engineering write-up argues that an instantly empty shell around missing content reads as broken; keeping structure painted first gives navigation context while the body catches up.[32]
- A toast is not the primary in-progress signal: VS Code calls global progress notifications a last resort and says progress belongs in context;[33] Primer assigns success/failure messaging to the completed stages of a loading lifecycle.[23]

**Reading for this app:** the rail and both sidebar panels should never be replaced or disabled while a fragment loads. The content pane that is actually waiting should carry the busy state. A global top bar is defensible only for whole-page work, which this is not.

## 3. Surface-by-surface pattern implied by the sources

| Surface | What stays | What changes |
| --- | --- | --- |
| Rail | Selected tile and its highlight; rail stays clickable[27] | No row animation. At most a small discreet status glyph if work is backgrounded, as VS Code uses in its status bar.[28] |
| First-level sidebar | Selected row keeps its tint; list stays interactive[27][33] | Placeholder child rows under the selected parent while its children load, per Primer's tree-view pattern;[30] or one small spinner in the list head. Not a coloured inset on the row itself. |
| Second-level sidebar | Selected row and scroll position stay | Same placeholder/inline treatment in that pane; one indicator for the group, not one per row.[18][23] |
| Reading stage | Last known content where it can be kept[32] | Skeleton matching the final shape (verse lines, song rows, service entries) or, for short waits, a centred activity indicator in the space the content will occupy;[17][23] no blank overlay. |
| Failure | Rail/sidebar state unchanged | A single failure message after settlement, with retry where possible — the lifecycle's final stage, not a spinner.[23][33] |

## 4. Accessibility requirements

- Mark the region being updated `aria-busy="true"` until loading finishes, then false; this batches assistive-technology announcements into one update.[13][8] WAI-ARIA says a progressbar describing a region should be referenced with `aria-describedby` and the region kept busy until loading completes.[26]
- An indicator needs a text name, possibly visually hidden.[23] `role="progressbar"` conveys that a request was received and work is progressing;[11] it is unnecessary if the visual is purely decorative and the status message carries the meaning.
- A `role="status"` live region is implicitly polite and atomic, so it announces without stealing focus.[10] Such a region must be rendered empty before it is updated, or it may not be announced at all.[9]
- Use polite, not assertive, for routine loading.[8][9]
- Do not move focus to a status update.[10] For newly loaded content, move focus only when the product's existing focus rules require it.[23]
- Honour reduced motion: keep the text/static indicator and stop rotation.[12][6]

## 5. Why the two earlier previews do not hold up

- The 3px global top bar: Material reserves that placement for whole-page/group progress, and VS Code explicitly moved progress off the container top onto the view.[18][29]
- The coloured row inset: none of the first-party sources supports marking navigation rows to show a fetch; the guidance is to keep the nav chrome stable and mark the loading region.[27][23]
- The edit-toast shape: a toast is a completion/failure channel or a last-resort global progress, not the routine signal for a navigation click.[33][23]
- A lone centred spinner in the stage can worsen perceived performance by making waiting salient; a layout-matched skeleton is the better default for a full reading pane.[36][23]

## 6. What to decide next

This note does not choose a final visual. The evidence narrows the decision to: keep the shell mounted and selected; delay the busy state ~300 ms; put a shape-matched skeleton or a small inline activity indicator in the pane that is loading; announce politely with `aria-busy` + a pre-rendered status region; and reserve toasts for failure. A revised preview should show those states on the rail, both sidebars and the stage before gate 1.

## Sources

[1] https://www.nngroup.com/articles/response-times-3-important-limits
[3] https://www.nngroup.com/articles/progress-indicators
[4] https://www.nngroup.com/articles/skeleton-screens
[5] https://web.dev/articles/inp
[6] https://web.dev/articles/prefers-reduced-motion
[8] https://www.w3.org/TR/wai-aria-1.2
[9] https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Guides/Live_regions
[10] https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/status_role
[11] https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/progressbar_role
[12] https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-reduced-motion
[13] https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Attributes/aria-busy
[17] https://m3.material.io/components/loading-indicator/guidelines
[18] https://m3.material.io/components/progress-indicators/guidelines
[21] https://fluent2.microsoft.design/wait-ux
[23] https://primer.github.io/design/ui-patterns/loading
[25] https://www.carbondesignsystem.com/building-blocks/core/components/loading/guidelines
[26] https://www.w3.org/TR/wai-aria-1.3
[27] https://docs.stripe.com/stripe-apps/patterns/loading
[28] https://code.visualstudio.com/api/ux-guidelines/status-bar
[29] https://code.visualstudio.com/updates/v1_44
[30] https://primer.github.io/design/components/tree-view
[32] https://github.blog/engineering/user-experience/rendering-huge-pull-requests-in-the-github-copilot-app
[33] https://code.visualstudio.com/api/ux-guidelines/notifications
[36] https://3perf.com/blog/notion
