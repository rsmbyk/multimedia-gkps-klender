# Data Model: the dock's Go To

**Spec**: `specs/185-dock-goto/spec.md`

## Entities

### DisplayState — `localStorage['gkps-display']`

| Field | Type | Constraints | From |
| --- | --- | --- | --- |
| `service` | number \| null | the Tata Ibadah on air; null = nothing | display-state/R1 |
| `screen` | number | the service's own screen; frozen while a goto is up | FR-001, FR-015 |
| `on` | boolean | whether words are up, for whatever is on air | FR-002 |
| `translation` | `'TB'` \| `'SIM'` \| null | the service's own edition; frozen while a goto is up | FR-001, FR-008 |
| `at` | number | when this browser last wrote it | spec 119 |
| `session` | string \| null | the browser session that wrote it; a mismatch reads as no state | FR-003 |
| `goto` | Goto \| null | what is on air instead of the service; null = the service | FR-001 |

### Goto — `state.goto`

Two shapes, discriminated by `kind`.

| Field | Type | Constraints | From |
| --- | --- | --- | --- |
| `kind` | `'song'` \| `'passage'` | anything else reads as no goto | FR-001 |
| `song_id` | number | song goto only; the id `/projector/goto/song/<id>/` answers | FR-001 |
| `index` | number | song goto only; the screen index inside the song's payload | FR-001 |
| `book_id` | number | passage goto only | FR-001 |
| `chapter` | number | passage goto only | FR-001 |
| `verse` | number | passage goto only | FR-001 |
| `translation` | `'TB'` \| `'SIM'` | passage goto only; the edition **shown**, which `flip` changes | FR-002, FR-015 |

**Relationships**: DisplayState 1—0..1 Goto — a service with a goto up is still one display, and
the goto never outlives the state. A Goto 1—1 payload — it names one song payload or one chapter
payload, which every reader fetches for itself (D003).

**Validation**: a stored value whose `goto` is not an object, or whose `kind` is neither `song` nor
`passage`, or whose numbers do not parse, is read as `goto: null` and the service's screen is
painted (spec's corrupt-state edge case). A song goto with no `index` reads as index 0; a passage
goto with no verse reads as the chapter's first.

**State transitions**: `none → goto` (`goTo`, or the projector's `G`), `goto → goto` (`stepGoto`,
`flip`, a block row click), `goto → none` (`back`, `show`, `moveTo`, `release`), and
`anything → none` when the browser session changes (spec 184's gate, no new code).

### Query — the find band's own state (page memory, never stored)

| Field | Type | Constraints | From |
| --- | --- | --- | --- |
| `open` | boolean | the band is a layer over the dock; false at rest | FR-018 |
| `query` | string | what is typed; the lookup runs on it | FR-005 |
| `rows` | array | the lookup's matches, in its own order | FR-005 |
| `choice` | number | which match `Enter` takes | US1/AC3 |
| `status` | `'idle'` \| `'loading'` \| `'ready'` \| `'failed'` | what the result row says | FR-006 |

**Not modelled**: the query is deliberately not in `gkps-display` — it is one operator's typing on
one surface, and a second dock must not inherit it.

### Block — the list's content while a goto is up (derived, never stored)

| Field | Type | Constraints | From |
| --- | --- | --- | --- |
| `label` | string | the goto's name in the projector's own words (`NKB 43 Sinar Matahari Pagi`, `Matius 5:3`) | FR-007 |
| `rows` | array | song: bait heads + one row per screen; passage: one row per verse | FR-007 |
| `current` | number | the row on air, carrying the live tint | FR-007 |
| `editions` | string[] | a passage's editions, so `T` has something to flip | FR-015 |

## Invariants

- While `goto` is not null, `screen` and `translation` do not change. (FR-015, FR-008)
- `goto` survives only inside one browser session: a stored state whose `session` does not match
  reads as `{goto: null}` and the service fields with it. (FR-003, SC-004)
- The stored state carries no verse text and no lyric: no word of the opened chapter appears in
  `localStorage['gkps-display']`. (FR-001, SC-005)
- Exactly one thing is on air: `goto` null means the service's `screen`; `goto` non-null means the
  goto, and no surface paints both. (FR-011, US2/AC1)
- Every goto change is one state write with a new `at`, so two surfaces acting at once settle on the
  later write. (spec's concurrent-start edge case)

## Not modelled

- **The fetch cache.** Which payload a surface already holds is page memory, rebuilt on reload; the
  state never records it (D003).
- **The recording lock.** Whether the projector refuses its own `G` because a recording plays is the
  projector's runtime state (projector/R5), not display state.
- **The band's geometry.** Sizes live in the spec's `## UI/UX` and the stylesheet, not in data.
