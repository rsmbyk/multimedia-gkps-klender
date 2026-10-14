# Plan 091: Quiet controls for the mirrored service projector

- **Status:** Accepted
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-094
- **Bump:** minor
- **Approved look:** [interactive preview](./preview.html) and [gallery](./preview-gallery.html)

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
