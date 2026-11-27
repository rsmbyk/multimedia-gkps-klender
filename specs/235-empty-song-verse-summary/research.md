# Research: An empty song names itself in the Verses section

## Decisions

**D001 — Keep the section, hide only its body.** The picked-but-empty state keeps the
`Verses` label and the bordered `.editor__verse-panel`; a `data-empty="true"` attribute on the
panel drives CSS that removes the helper/All–Clear row, the tile grid and the readout, and
the summary drops its separator. **Rationale**: the request names the *section* and *only the
summary row part*, which maps onto the panel already in `_entry_form.html`.
**Alternatives**: a bare sentence outside the panel (rejected — that is not the section), a
hidden label with a visible panel (rejected — the label belongs to the section and spec 210's
`[data-verse-field]:has(...)` rule already ties them). **Provenance**: accepted preview,
owner Gate 1 2026-11-24; repo code `_entry_form.html:199-215`, `components.css:2720-2788`.

**D002 — Drop the summary's bottom rule in the empty state.** `.editor__verse-summary`
normally carries `margin-bottom: 8px; padding-bottom: 8px; border-bottom: 1px solid
var(--divider)` as a separator above the body rows. With those rows gone the rule would hang
in the panel's empty lower half. **Rationale**: a separator needs content on both sides.
**Alternatives**: keep the rule (rejected as a dangling mark), shrink the panel but keep the
rule (rejected — same mark). **Provenance**: accepted preview readout `rule=0px`, `panel=38.9px`.

**D003 — No new motion phase.** The existing 200ms `grid-template-rows` reveal still carries
no-song → picked-song. The empty ↔ populated swap changes `data-empty` in the same frame as
the pick, so the body rows appear or disappear without a staged follow-up. **Rationale**: the
product's one curve stays one action; the request says nothing about motion.
**Alternatives**: a second reveal on the body rows (rejected — introduces a visible pause
and a new state to maintain). **Provenance**: owner assumption at Gate 1; `entries.js:731-742`.

**D004 — First paint comes from the template, not the script.** The panel is `hidden` only
when no song is picked, and gets `data-empty="true"` when `form.song_has_no_verses` is true.
**Rationale**: the Edit form and a refused Add form are server-rendered, and FR-003 asks for
the state before any script runs. **Alternatives**: let `verseSummary()` add it on load
(rejected — first paint would flash the hidden state). **Provenance**: spec 162's split
between server-owned first paint and script-owned later lines; `entries.py:183-191`.

**D005 — No schema, endpoint or storage change.** `SongEntryForm.song_has_no_verses`, the
`{id, number}` JSON from `/editor/entry/song/<id>/verses/`, and the `verses` ID list are all
reused unchanged. **Rationale**: the change is presentational; the model already refuses an
empty song with its own message. **Alternatives**: a persisted `has_verses` flag (rejected —
duplicates a fact the field choices already hold; spec 162 made the same call).
**Provenance**: `docs/spec/reading.md` R30 and R43; spec 162 `research.md`.

## Unknowns

None. Every choice is either recorded in the accepted preview or covered by D001–D005.
