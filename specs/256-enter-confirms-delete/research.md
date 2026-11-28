# Research: Enter accepts a delete confirmation

**Spec**: `specs/256-enter-confirms-delete/spec.md`
**Unknowns remaining**: 0

## D001 — The scope is the live reading application

- **Decision**: Add Enter handling to the five live destructive confirmations only: sidebar record,
  stage entry, stage old row, verse, Media Library removal. The old Fomantic delete modal templates
  (`songs/*/modals/delete-*.html`, `obs/templates/songs/dock/modals/delete-*.html`) are left alone.
- **Rationale**: `multimedia/retirement.py` redirects `/obs/songs/dock*`, `/manage/*` and the
  `/songs/books*` family to live successors (spec 194). The probe found 404/302 at those addresses
  and no live modal there; editing retired templates would ship code no page can reach.
- **Alternatives considered**: patch every delete modal in the tree — rejected because the patched
  copies would be unreachable and would suggest coverage the product does not have.
- **Provenance**: research (code and live URLs measured before gate 1).

## D002 — One shared handler, not five local ones

- **Decision**: `static/web/enter-delete.js` registers one capture-phase `keydown` listener on
  `document` and activates the single visible `[data-enter-delete]` control.
- **Rationale**: all five surfaces already own their delete logic on the target button; the keyboard
  rule is one cross-cutting behaviour. A marker keeps the handler independent of each surface's
  markup churn (entries.js rebuilds the confirm layer, songs_verse.js replaces `content`).
- **Alternatives considered**: five per-surface listeners (five copies of the same guard set, easy to
  miss a surface); editing vendored Fomantic `keyboardShortcuts` (retired surface plus a vendored
  file); focusing each Delete button on open (changes the owner's focus path and is undone by
  re-renders).
- **Provenance**: research.

## D003 — Focus does not choose the answer

- **Decision**: Enter activates the destructive control even when Cancel or the dialog body has
  focus; the default key action is suppressed so a focused Delete button cannot fire twice.
- **Rationale**: the owner's wording attaches Enter to the confirmation ("when a confirmation
  dialog/modal ... is up"), not to a control. The before probe had focus on `BUTTON#` for three
  surfaces and `BODY#` for verse, so focus-based rules would leave two of them broken.
- **Alternatives considered**: only handle Enter when the Delete button has focus — rejected: it
  preserves the reported gap. Let the browser handle it natively — rejected: Fomantic buttons are
  divs and the custom confirms do not focus themselves.
- **Provenance**: owner clarification + research.

## D004 — Guards keep one press to one deletion

- **Decision**: ignore repeated keydowns, Shift/Ctrl/Alt/Meta chords, already-default-prevented
  events, hidden layers, closed dialogs and disabled controls.
- **Rationale**: deletion is destructive; a held key or a chord used for another shortcut must not
  add a second write. `feedback.setDialogBusy` disables controls during an in-flight request, so the
  disabled guard also covers a second Enter while deleting.
- **Alternatives considered**: no guards — rejected because the existing in-flight guards live on
  the controls, not on the key event.
- **Provenance**: research.

## D005 — No schema, route or endpoint change

- **Decision**: the handler calls `.click()` on the existing control; all writes stay on the existing
  fetch/form handlers and keep their feedback, focus restoration and soft-delete behaviour.
- **Rationale**: the change is a key binding, not a new delete path; duplicating a write would risk
  divergence in the two implementations.
- **Alternatives considered**: a new `/editor/.../enter-delete` endpoint — rejected as an
  unnecessary interface with no state of its own.
- **Provenance**: research.

## D006 — Live preview, measured before gate 1

- **Decision**: serve the real worktree on port 8768 with its own seeded `gkps256` database; freeze
  the before/after counts in `## UI/UX`.
- **Rationale**: the confirmations are fetched or server-rendered and their actions write records; a
  static page could show the markup but not prove that one Enter sends one POST.
- **Alternatives considered**: static page with copied markup — rejected because it cannot exercise
  the fetch path the change controls.
- **Provenance**: research.

## D007 — Patch level

- **Decision**: `bump: patch`, declared at Plan and applied only in the pre-merge delivery commit.
- **Rationale**: a user-visible keyboard fix on an existing capability, not a new capability or a
  breaking change (VER-10).
- **Alternatives considered**: `minor` — rejected, no new capability; `none` — rejected, the change
  is visible to users.
- **Provenance**: research.

## D008 — Develop advanced while the slice was in flight

- **Decision**: keep the slice based on `1cd9f081`; rebase onto `origin/develop` (now `1d8f904e`,
  spec 257) before Fold and re-check `VERSION`, the card ID and `R<n>` then.
- **Rationale**: spec 257 landed during Specify with `VERSION` 1.37.12 and ITEM-277/R66. None of
  those touches Enter handling, but the delivery numbers must be read against the line the slice
  merges into.
- **Alternatives considered**: rebuild the slice from develop now — rejected, it would discard the
  measured preview chronology; the rebase at Fold is the smaller operation.
- **Provenance**: research.

## D009 — Version claim moved after the re-check

- **Decision**: take `1.37.14` at Fold, not the `1.37.13` guessed when the Plan was written.
- **Rationale**: sibling slice 254 first carried `VERSION` 1.37.13; develop then advanced with spec 255, which merged at 1.37.13 and claimed R67. 1.37.14 and R68 were free at the pre-merge re-check.
- **Alternatives considered**: keep 1.37.13 and let the two slices collide at merge — rejected; the pre-merge re-check exists to catch exactly this.
- **Provenance**: research.

## Open

<!-- empty; Phase 0 finished with zero unknowns -->
