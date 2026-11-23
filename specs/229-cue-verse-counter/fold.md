# Fold: A passage cue carries its current and end verse

**Capability**: `docs/spec/projector.md`
**Folded at**: 2026-11-23

## Delta

| Type | Requirement | Change |
| --- | --- | --- |
| `added` | `projector/R16` | A new requirement: a passage cue carries a `current/end` counter after the reference, from the entry's verse bounds for a service passage and from the loaded chapter's last verse for a Go To; non-scripture cues carry none. Five scenarios below. |

### Added block for `projector/R16`

```markdown
### R16 — A passage cue carries its current and end verse

The projector's corner cue SHALL place a `current/end` verse counter after a passage reference and
before the translation flip, separated by centre dots, whenever a Bible passage is displayed. For a
service scripture entry the current number SHALL be the verse on the active screen and the end
number the entry's end verse, or its start verse when no end is stored; stepping through the passage
SHALL move the current number and keep the end. For a passage Go To the current number SHALL be the
verse painted and the end number the last verse of the chapter currently loaded in the edition in
use; a verse step, a chapter crossing and an edition flip SHALL all keep the counter derived from
that chapter. A single-verse passage SHALL read `n/n`. A song, text, break or media cue SHALL carry
no counter, and a chapter with no verses SHALL carry none rather than `n/0`. The counter SHALL be
text inside the existing cue label — no new control, token, size or colour — so the 24px band, the
centre alignment and the translation flip are unchanged. (spec 229)

#### Scenario: a service passage steps
- WHEN a service passage spanning verses 3–5 shows verse 3
- THEN the cue reads `Matius 5:3-5 · 3/5 · TB`, then `4/5`, then `5/5`, with the reference held

#### Scenario: a single verse
- WHEN a passage with no stored end verse shows its only verse
- THEN the cue reads `Matius 5:3 · 3/3 · TB`

#### Scenario: a chapter Go To
- WHEN a Go To chapter of three verses shows verse 1
- THEN its cue reads `Matius 5:1 · 1/3 · TB`, and stepping gives `2/3` and `3/3`

#### Scenario: the chapter changes
- WHEN the Go To crosses into the next chapter
- THEN the end number is that chapter's last verse, and an edition flip leaves the counter alone

#### Scenario: another kind of cue
- WHEN a song, text, break or media screen is showing
- THEN the cue has no verse counter at all
```

## Drift guard

- **Files changed in this capability**: `docs/spec/projector.md` (header + the R16 block appended
  after R15).
- **Declared no behaviour change**: no — a passage cue now carries a counter it did not before;
  that is the behaviour change gate 2 approved.
- **Before / after counts**: 15 → 16 requirements; 0 → 5 scenarios in this slice's block.
