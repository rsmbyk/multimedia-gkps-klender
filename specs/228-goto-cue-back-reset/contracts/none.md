# Contracts: Back clears the Go To from the cue over an empty stage

`none` — no HTTP, model, script or event interface changes.

The `{type: 'goto'}` message and the `gkps-display.goto` field keep their existing shape. The cue's
DOM (`#cue-prefix`, `#cue-baits`, `#cue-progress`, `#cue-next`, `#cue-next-name`) is unchanged; only
its contents when no entry and no detour exist change.
