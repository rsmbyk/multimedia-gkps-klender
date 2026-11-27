# Preview: A Go To still names itself with no service under it

`live preview at http://127.0.0.1:8765/projector` — the slice worktree's own server. Hard-reload
after a JS edit; a bare `/projector` follows the shared display state, so clear `gkps-display` in
localStorage between scenarios.

The harness `probe.py --base http://127.0.0.1:8765 --query 'Jahowa'` drives the real projector find
(`g`, query, Enter) and prints the cue's boxes and text.

## States

1. **No service, passage** — open `/projector` with no stored service, press `g`, search a chapter,
   press Enter. The cue names the passage, shows its edition in `.cue-translation`, and Back reads
   `back to service`. The stage shows the detour, not the empty notice.
2. **Service with no entries, song** — open `/projector?service=<empty>`, press `g`, search a song,
   press Enter. The cue names the song and draws one `.cue-bait` per bait. Press a bait: the cue
   keeps naming the song and the pressed key follows the screen.
3. **No service, Back** — press the cue's Back. The state loses `goto`, the detour leaves the stage,
   the empty notice returns and the cue has no Go To controls.
4. **Populated service** — open `/projector?service=<service with entries>` and repeat 1–3. The cue
   uses the service's entry list exactly as before; Back returns to the entry it stood on.
5. **Dock-started Go To** — start the Go To from `/obs/dock` while the projector has no entries; the
   projector's cue is identical to state 1 or 2.

## Measured read-back (420×800, after the fix)

- Cue at (32, 756) 280 × 24; prefix at (73, 756) 259.6 × 24 reading
  `HAL 1 Jahowa Sihol Pujionku ·`.
- Seven `.cue-bait` buttons (`1`–`7`); Back at (502.9, 761) 129 × 16 reading `back to service`.
- Before the fix the same probe reads an empty prefix, no flip, zero baits and an empty Back while
  the detour paints — see `../spec.md` `## UI/UX`.
