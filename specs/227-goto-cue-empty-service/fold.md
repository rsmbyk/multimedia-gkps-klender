# Fold: A Go To still names itself with no service under it

**Capability**: `docs/spec/projector.md`
**Folded at**: 2026-11-23

## Delta

| Type | Requirement | Change |
| --- | --- | --- |
| `modified` | `projector/R2` | The full R2 block is replaced below. Its empty-stage rule is kept; the Go To scenario now states that the cue names the passage or song and carries its controls when the stage holds no screens, whether no service is open or the service has no entries. |

### Replacement block for `projector/R2`

```markdown
### R2 — The projector page renders from its own response alone

The projector SHALL paint the screens the server sent with the page. It SHALL NOT read a saved
service, wait for a library update, or promise a saved copy in its empty state; a service with no
items SHALL show the empty state. The empty state SHALL be painted only while the stage holds
nothing: while a Go To detour is on the stage the empty notice SHALL NOT be painted and SHALL take no
room in the stage's layout, so the detour is laid out in the full stage; closing the detour SHALL
bring the notice back when the service still holds nothing. A re-read that ends with screens SHALL
hide the notice in that same render, and one that ends with none SHALL leave it visible.

The corner cue SHALL name the Go To and offer its controls even when the stage holds no screens —
no service open, or a service with no entries. It SHALL show the passage or song label, a passage's
translation flip, a song's bait buttons, the screen progress and a Back control naming the service.
An empty service SHALL NOT suppress these just because its entry list is empty; the check for a
detour SHALL run before any early return caused by that empty list. Closing the Go To over an empty
service SHALL restore the notice and leave no Go To controls in the cue.

#### Scenario: a service with items
- WHEN the projector opens for a service
- THEN its screens are the response's, and no other store is read

#### Scenario: a service with no items
- WHEN the projector opens for a service holding nothing
- THEN it shows its empty state, naming no saved copy

#### Scenario: a Go To passage or song over an empty service
- WHEN a Go To detour paints over a service with no items
- THEN the empty notice is not painted, takes no room, and the detour is fitted to the full stage
- AND the cue names the passage or song and offers its translation flip or bait keys and Back
- AND closing the detour brings the notice back

#### Scenario: a Go To with no service open
- WHEN a projector that holds no service paints a Go To detour
- THEN its cue names the passage or song and offers the same controls as over an empty service

#### Scenario: a re-read that brings the first screens
- WHEN the page re-reads its service and the response carries screens
- THEN the empty notice is hidden in the same render
- AND a re-read that carries no screens leaves it visible
```

## Drift guard

- **Files changed in this capability**: `docs/spec/projector.md` (header + R2 block).
- **Declared no behaviour change**: no — the blank cue of a Go To over zero screens becomes a cue
  naming the Go To with its controls; that is the behaviour change gate 2 approved.
