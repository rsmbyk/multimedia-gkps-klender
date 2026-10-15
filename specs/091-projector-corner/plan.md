# Plan 091: Quiet controls for the mirrored service projector

- **Status:** Accepted
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-094
- **Bump:** minor
- **Approved look:** [interactive preview](./preview.html) and [gallery](./preview-gallery.html)
- **Go To amendment:** Accepted; [approved single-suggestion preview](./preview-goto-autocomplete.html)
- **Search clear amendment:** Accepted; [approved two-field preview](./preview-search-clear.html)
- **Untitled Text cue amendment:** Accepted; [approved running-text preview](./preview-cue-running-text.html)
- **Corner cue typography amendment:** Accepted; [approved 550-weight preview](./preview-cue-running-text.html)
- **Shared corner colors amendment:** Accepted; [approved state preview](./preview-cue-state-colors.html)
- **Go To morph amendment:** Accepted; [approved motion preview](./preview-goto-morph.html)
- **Number-only Go To amendment:** Draft; [approved numeric preview](./preview-goto-number-substring.html)

## Why

The service projector is mirrored to the hall. The operator sees the same framebuffer as the congregation, so opening the editor or another dock to check the next item or make an unplanned jump becomes visible to everyone. The existing projector has basic stepping keys but no quiet, complete way to identify the current place, browse the order, or find an unplanned passage or song.

## Scope

Give the service projector one subdued bottom corner with its position, next entry, entry-list button, and shortcut button. Complete keyboard navigation, find, translation switching, and library detours. Add equivalent mouse paths for the ordinary projector actions, including direct entry and bait jumps. Make the header and lyric stage follow the approved sizing rules. Keep HUD and pointer inactivity behavior separate from intentionally hiding the HUD with C.

The reference preview demonstrates geometry, color, and interaction; its five sample entries are illustrative. Production uses the active service order and content. The OBS projection source, old docks, service editor, stored passage translation, and a second-screen control surface are out of scope.

## Approach

Keep all controls on the projector page. Reuse the existing service-order data and passage/song search parsers where possible. Keyboard and mouse call the same navigation operations, so either input can operate the projector alone. Put the invisible 40/20/40 mouse zones only above the 64px bottom band. Make modal and entry-list overlays intercept clicks without navigating beneath them.

Use plain arrows for the current screen or verse; Shift for a song bait or detour chapter; Ctrl for a service entry or detour book. Leave browser-reserved Ctrl+Page Up/Down alone. Preserve the current service position during library detours; Escape returns to it after closing any open find or popup. Request keyboard lock when the page enters JS fullscreen so a short Escape can stay on the page where the browser supports it; a held Escape and browser F11 remain browser-controlled.

## Validation and risk

Add targeted domain/application tests for corner labels, screen counts, rests, translation, and direct jumps. Add targeted projector E2E for all named keyboard and mouse paths, overlays, inactivity, and fullscreen fallback. Test at the 1366×768 reference size and a smaller viewport. The quiet controls remain visible on the projected wall; the 32px horizontal inset, dim palette, and lack of idle motion are deliberate.

## Accepted amendment: one-suggestion Go To

The current G popup paints every match as a row. Book-and-number prefixes can return dozens of valid matches, making that list slow to scan on a mirrored projector. Keep the accepted Go To search rules and result ordering, but show one current suggestion and its position in the result set. Up/Down replaces that suggestion; Enter or a click opens it. The query remains editable while cycling.

The [approved interaction preview](./preview-goto-autocomplete.html) uses the projector's normal sans-serif typography and subdued palette, with no terminal prompt glyphs or monospaced styling. It is sample data only; production results still come from the existing lookup endpoint. The amendment changes the G popup only, not the J service list, search ranking, projector navigation, or saved service content.

The owner accepted the [amendment in the spec](./spec.md#accepted-amendment-one-suggestion-go-to). Targeted browser tests cover result counting, replacement and wraparound, query preservation, and no-match/overlay behavior. The main risk is making large reference-prefix result sets hard to navigate; the counter and cycling keep every result reachable without drawing extra attention to the projection.

## Accepted amendment: projector search clear controls

The J service list and G Go To fields currently rely on the browser's search-clear affordance, which does not match the public reading sidebars. Use the same stroked × icon and 26px circular button as those sidebar filters, adapted to the projector palette. Show it only for non-empty input; clearing must dispatch the existing input event and leave keyboard focus in the field. This affects only the two projector search inputs and their existing results, with no change to matching, navigation, or overlay behavior.

The owner approved the [interactive two-field preview](./preview-search-clear.html) and accepted the [amendment](./spec.md#accepted-amendment-projector-search-clear-controls). Targeted projector browser tests check both clear buttons, live result reset, focus, and the hidden empty state.

## Accepted amendment: running untitled Text cue labels

An untitled Text entry uses its first content line as its cue label. Two adjacent untitled entries can consume the bottom HUD together, leaving the count and next arrow hard to scan. The [approved running-text preview](./preview-cue-running-text.html) starts both labels at a 50-character limit, keeps the next label immediately after the count, and lowers their **shared** limit only when the combined cue would cross the minimum 10vw clearance before the keyboard button. On hover, only the hovered label runs repeatedly to reveal its full first line; at rest both remain clipped and quiet. No hover tooltip appears. The owner confirmed the inline order, clarified the overflow-triggered limit, and approved this revised preview. Apply this only to first-line labels in the corner cue. Keep full labels in the service list and underlying projector data.

The owner approved the revised preview and explicitly accepted the [amendment](./spec.md#accepted-amendment-running-untitled-text-cue-labels). Targeted projector tests cover adjacent long entries, repeat and stop behavior, reduced motion, count and next-entry visibility, and narrower viewports.

## Accepted amendment: quieter corner cue typography

The bottom HUD's 650-weight cue text draws more attention than needed, while the 400-weight preview looked too thin. The owner chose the 550-weight preview. Set all cue text to 550, and make only the resting current and next untitled Text labels slightly dimmer. Preserve hover, selected, highlighted, active, and focus colors, as well as the count, separators, arrows, list icon, and keyboard button colors. The keyboard button is SVG artwork, so changing text font weight does not change its strokes. This is a visual-only amendment; keep cue geometry, running-text fitting and animation, and navigation behavior.

The owner accepted the [amendment](./spec.md#accepted-amendment-quieter-corner-cue-typography). Explicit state selectors preserve next-entry highlights; targeted browser coverage checks resting, hovered, highlighted, and narrow-viewport cue states.

## Accepted amendment: shared corner control colors

The prior color amendment dimmed only untitled Text first-line labels. The owner clarified that all resting cue text and the service-list and keyboard icons should share the same subdued color, then approved a [state preview](./preview-cue-state-colors.html) covering the keyboard, next entry, bait, translation, entry list, and split count. Use one palette for these controls: `#514D47` at rest, `#817D74` on hover, and `#E8E4DC` when highlighted, pressed, or open. The keyboard button never gains a background fill. The split count remains highlighted. Keep the accepted 550 text weight, geometry, fitting, running-label behavior, navigation, and visible keyboard-focus outline. The owner accepted the [amendment](./spec.md#accepted-amendment-shared-corner-control-colors). Explicit state precedence protects highlights; targeted browser checks cover the major cue types and input states.

## Accepted amendment: Go To morph animation

The G passage/song popup appeared and disappeared abruptly while the shortcut sheet and service list already used a restrained 180ms morph. The owner approved the [Go To motion preview](./preview-goto-morph.html) and accepted the [amendment](./spec.md#accepted-amendment-go-to-morph-animation). The Go To panel now uses the service list's 6px vertical travel, `.99` scale, opacity transition, 180ms duration, and `--display-ease` timing on both open and close. Its transparent full-output overlay remains click-intercepting throughout the closing transition. Reduced-motion preference omits animation. Search, selection, results, and projector position remain unchanged; a rapid reopen cancels the old close timer. Targeted browser tests cover those transition edges.

## Draft amendment: number-only Go To substring search

A bare song number currently finds only exact-number matches. The owner approved the [numeric search preview](./preview-goto-number-substring.html) where a number-only query such as `12` finds numbered songs containing those digits anywhere in the number, across active songbooks: `12`, `120`, `121`, `212`, `312`, and so on. Show exact numbers first, then numbers starting with the query, then numbers containing it later; use numeric order and a stable songbook/title tie-breaker within tiers. Keep all matches available to the existing single-suggestion Up/Down cycler and counter rather than cutting the set to 12. Preserve book-qualified number-prefix searches, title searches, Bible references, and the exclusion of lyric or verse-body matches. The main risk is very broad numeric queries producing large sets; the counter and ordered cycling keep the result set navigable without a larger popup.
