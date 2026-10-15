# Plan 091: Quiet controls for the mirrored service projector

- **Status:** Accepted
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-094
- **Bump:** minor
- **Approved look:** [interactive preview](./preview.html) and [gallery](./preview-gallery.html)
- **Go To amendment:** Accepted; [approved single-suggestion preview](./preview-goto-autocomplete.html)
- **Search clear amendment:** Accepted; [approved two-field preview](./preview-search-clear.html)
- **Untitled Text cue amendment:** Draft; [revised running-text preview pending approval](./preview-cue-running-text.html)

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

## Draft amendment: clip untitled Text cue labels

An untitled Text entry uses its first content line as its cue label. Two adjacent untitled entries can consume the bottom HUD together, leaving the count and next arrow hard to scan. The [revised running-text preview](./preview-cue-running-text.html) starts both labels at a 50-character limit, keeps the next label immediately after the count, and lowers their **shared** limit only when the combined cue would cross the minimum 10vw clearance before the keyboard button. On hover, only the hovered label runs repeatedly to reveal its full first line; at rest both remain clipped and quiet. No hover tooltip appears. The owner confirmed the inline order and clarified the overflow-triggered limit; this latest preview awaits review. Apply this only to first-line labels in the corner cue. Keep full labels in the service list and underlying projector data.

The [Draft amendment](./spec.md#draft-amendment-clip-untitled-text-cue-labels) requires revised-preview approval and explicit Draft acceptance before product code. Targeted projector tests should cover adjacent long entries, repeat and stop behavior, reduced motion, count and next-entry visibility, and narrower viewports.
