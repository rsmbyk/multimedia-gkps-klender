# Research: a preview's play shortcut paints nothing on the dialog's edge

**Spec**: `specs/159-preview-body-ring/spec.md`
**Unknowns remaining**: 0

## D001 — A state class on the body, and one rule that reads it

- **Decision**: the space handler adds `is-shortcut` to the preview body as it toggles the player;
  one declaration next to the body's existing focus rule suppresses the ring for that class:

  ```css
  .preview__body.is-shortcut:focus-visible { outline: none; }
  ```

- **Rationale**: the ring is painted by `:focus-visible`, and `:focus-visible` cannot be turned off
  while the element holds focus — the only ways to unpaint it are to move focus or to override the
  declaration. Moving focus is out (FR-003, below). The class is the smallest thing that changes what
  is painted and nothing else: no layout, no other preview, no other state.
- **Alternatives considered**: *move focus to the play button on open* — rejected: the body would stop
  holding focus, so `preview.js:476-484`'s arrow-key scroll (spec 071) would never fire, and a ring
  would still be painted, merely 48px round instead of 920px wide. *Blur the body on the first space* —
  rejected: focus would fall to the dialog root, the same arrow-key loss, and a blur mid-keypress is a
  trap for the next Tab. *Reuse `.focus-restore-quiet`* — tempting, since it already carries
  `outline: none !important` and is cleared on Tab by `focus.js`, but its own comment scopes it to
  "focus restored by a modal or shell refresh" (spec 058); using it for "the shortcut is in use" would
  make that comment false. Same effect, wrong name. *Narrow the ring to bodies that scroll* — a
  different change, excluded by the spec's assumptions.
- **Provenance**: research — code read of `preview.js:470-484`, `:579-592`, `focus.js:22`,
  `components.css:490`, `:2093`; the five-step focus measurement in the spec.

## D002 — The class is cleared on open, on Tab and on close

- **Decision**: one helper adds or removes `is-shortcut` on the preview body; the class is removed
  when a preview opens, on any `Tab` inside the dialog, and when the dialog closes.
- **Rationale**: `.preview__body` is a single element reused by every preview — `content.innerHTML` is
  replaced, the element is not (`_preview_modal.html:11`). A class left on it would suppress the ring
  in the *next* preview, and after the dialog closes and reopens. The Tab clear is what makes panel A
  hold: the indicator returns to a reader who navigates, and the body never loses focus (FR-002).
- **Alternatives considered**: clearing only on Tab — leaves the class on the body between previews,
  the trap above; putting the class on the dialog instead of the body — the rule would then need a
  descendant test and would outlive the body's own replacement; a timer — a state that fixes itself
  after a delay is a state that is wrong until it does.
- **Provenance**: research — `_preview_modal.html:11` (one body element), `preview.js:621`
  (`content.innerHTML = ''` on close), `preview.js:571` (the modal's own keydown listener, already
  catching every key).

## D003 — The test measures the painted outline, not `:focus-visible`

- **Decision**: the E2E asserts the body's *computed outline* (`none` after a space press, and
  `2px solid rgb(28, 92, 60)` at offset `-2px` once Tab reaches it). It does not assert
  `:focus-visible`, which stays `true` throughout by design.
- **Rationale**: under D001 the body keeps focus — FR-003 depends on it — so the browser keeps
  matching `:focus-visible`; what changes is that the rule no longer paints. `:focus-visible` is a
  browser-internal flag, not something a person can see, and asserting it would fail against a
  correct fix. `getComputedStyle(body).outlineStyle` is the painted result.
- **Alternatives considered**: a screenshot diff — it would catch the ring, but a 2px inset line is a
  poor ink budget for a pixel diff and it cannot say *which* state was showing; asserting the class
  name — tests the mechanism rather than the behaviour, and would pass on a page that paints anyway;
  asserting `:focus-visible` false — the trap above.
- **Provenance**: research — the preview's own readout (`specs/159-preview-body-ring/preview/`):
  panel A shows `fv=true, outline=none` in the exact state SC-001 describes.
- **Flagged for gate 2**: SC-001's *How it is measured* cell says "`:focus-visible` false and computed
  outline `none 0px`". The criterion ("shows no focus indicator") holds; the `:focus-visible` half of
  that cell cannot, and the test follows this decision. Either the cell is narrowed at gate 2 or the
  criterion is restated at Specify.

## D004 — A new E2E module on the audio-display fixture

- **Decision**: `tests/e2e/test_preview_body_ring.py`, built on the fixture shape of
  `test_audio_display.py` (a `MediaIdentity` per family, the entry point serving `127.0.0.1:63174`),
  with five cases: audio, video, Tab reinstates, keyboard-open keeps it until space, and a second
  preview after a close.
- **Rationale**: `test_entry_preview.py` owns this surface but has no media fixture, and
  `test_audio_display.py` already opens an audio preview through the real click path
  (`test_preview_plays_seeks_and_closes`) — the ring needs the same route, one more assertion. A
  module of its own keeps the ring's five states together and leaves the existing modules to prove
  FR-003 and FR-004 by staying green.
- **Alternatives considered**: adding cases to `test_audio_display.py` — that module is about playback
  and seeking, and the ring is a different behaviour; adding media setup to `test_entry_preview.py` —
  it would drag a companion stub into a module that deliberately has none.
- **Provenance**: research — `tests/e2e/test_audio_display.py:33-90`, `tests/e2e/test_entry_preview.py`
  (no media fixture), the route pattern at `test_audio_display.py:70`.

## D005 — `bump: patch`

- **Decision**: `patch` — 1.22.10 → 1.22.11, applied in the pre-merge commit.
- **Rationale**: a defect fixed on a shipped surface, with nothing added to the API or the capability
  tree beyond the requirement that now describes it. VER-10's mapping: a fix is `patch`.
- **Alternatives considered**: `minor` — nothing new is offered to the user; `none` — a user-visible
  behaviour changes, which VER-05 excludes.
- **Provenance**: versioning rules VER-03, VER-04, VER-10; `VERSION` at `1.22.10` on develop.
