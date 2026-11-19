# Data model — spec 205 (dock centre pace)

No entities, no migration, no storage change. The change is two motion constants and one curve in
`static/web/obs-dock.js`.

## Invariants

- One re-centring pace (`CENTRE_MS = 200`) and one curve (`ease`, sine in-out) are shared by
  `glideScroll`, `glideRow` and the crossing morph's carried scroll. They must not diverge.
- The hand block-toggle's pace (230 ms) and curve (`easeInOut`) are independent and unchanged.
- Reduced motion bypasses every glide (instant jump); the list's ends clamp; a wheel/pointerdown
  cancels a glide and ends following. All unchanged.
- No display-state, selection or mode semantics change — only the timing of the centring motion.