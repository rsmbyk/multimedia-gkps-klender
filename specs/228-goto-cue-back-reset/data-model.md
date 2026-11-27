# Data Model: Back clears the Go To from the cue over an empty stage

`n/a — no entities; the change clears existing DOM nodes when the stage holds no screens.`

The only state involved is the existing `gkps-display.goto` field, already specified in
`docs/spec/display-state.md`. Nothing in it changes; the projector reads it and resets its cue.
