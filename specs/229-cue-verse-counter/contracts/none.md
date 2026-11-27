# Contracts: A passage cue carries its current and end verse

`none` — no HTTP, model, script or event interface changes.

The projector's existing payloads gain read-only fields: each scripture screen carries `verse`,
and its entry carries `verse_start`/`verse_end`. The chapter Go To payload is untouched — its
`editions[code].verses[].n` already carries every verse number. `gkps-display.goto` and the
`{type: 'goto'}` channel message keep their current shapes; no new message, event or control is
added.
