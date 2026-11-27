# Fold: Back clears the Go To from the cue over an empty stage

**Capability**: `docs/spec/projector.md`
**Folded at**: 2026-11-23

## Delta

| Type | Requirement | Change |
| --- | --- | --- |
| `modified` | `projector/R2` | The Go To cue rule now also requires the cue to be cleared when the Go To ends over an empty stage, and a scenario names the reset after Back. The revision adds the idle HUD rule and its scenario below. The rest of R2 is unchanged. |

### Replacement block for the Go To cue paragraph and scenarios

```markdown
The corner cue SHALL name the Go To and offer its controls even when the stage holds no screens —
no service open, or a service with no entries. It SHALL show the passage or song label, a passage's
translation flip, a song's bait buttons, the screen progress and a Back control naming the service.
An empty service SHALL NOT suppress these just because its entry list is empty; the check for a
detour SHALL run before any early return caused by that empty list. Closing the Go To over an empty
service SHALL restore the notice and leave no Go To controls in the cue: its label, translation flip,
bait buttons, progress and Back SHALL all be cleared, and Back SHALL be hidden, unpressed and
unnamed. This reset SHALL hold for every path that ends the Go To — the projector's cue, the dock's
Back and an idle re-read — because each reaches the same cue renderer.

#### Scenario: a Go To with no service open
- WHEN a projector that holds no service paints a Go To detour
- THEN its cue names the passage or song and offers the same controls as over an empty service

#### Scenario: Back over an empty stage
- WHEN a Go To over a stage with no screens ends, from the projector's cue or the dock's Back
- THEN the cue names neither the passage nor the song and carries no flip, baits, progress or Back
- AND the empty notice returns while no service holds entries

While the stage holds no screens and no Go To is up, the idle stage SHALL NOT offer phantom
controls. The corner cue SHALL NOT display its centre-dot separator or its next button, leaving no
visible cue text and no lone right-arrow icon. The edge and centre mouse zones SHALL take no pointer
events, so clicks cannot step, hide or show, and their custom cursors SHALL not be drawn; the pointer
SHALL NOT auto-hide. A click on the screen SHALL still fullscreen the window, and the service-list
button, keys sheet and find band SHALL remain usable. While a Go To detour is up over the same stage,
its spec 227 cue and controls SHALL be unchanged.

#### Scenario: an idle empty projector
- WHEN the projector has no service open, or a service with no entries, and no Go To is up
- THEN the cue shows no separator, no next and no text
- AND the mouse zones take no pointer events and the pointer stays visible
- AND a click still fullscreens and the service list, keys and find still open

#### Scenario: an idle empty projector with a Go To up
- WHEN a Go To detour paints over the same stage
- THEN the idle rules do not apply to its cue, which names the passage or song with its controls
```

## Drift guard

- **Files changed in this capability**: `docs/spec/projector.md` (header + the R2 cue paragraph and
  scenarios).
- **Declared no behaviour change**: no — the stale Go To information after Back is replaced by an
  empty cue; that is the behaviour change gate 2 approved.
