# Tasks 105: Keep media navigation selection feedback in sync

- **Status:** Accepted (2026-10-17)
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. -->

## Acceptance checklist

- [x] Spec accepted by the project owner on 2026-10-17
- [x] Local branch `feat/105-media-navigation-feedback` created from the current feature stack;
      `develop` is an ancestor of the branch head

## Implementation sequence (after Draft acceptance)

### Task 1: Animate the selected media source

Write the E2E regression first, then add the thumb.

- **Acceptance:** The selected tab, visible panel, and thumb position agree in both directions;
  keyboard activation still works; reduced motion leaves selection functional without a running
  transition.
- **Verify:** Targeted E2E coverage in `tests/e2e/test_media_library.py`, including computed thumb
  position before and after selection and a reduced-motion context.
- **Dependencies:** Spec acceptance.
- **Files likely touched:** `tests/e2e/test_media_library.py`,
  `multimedia/web/templates/reading/_entry_form.html`, `static/styles/design/components.css`.
- **Estimated scope:** Small.
- **Status:** Complete. The thumb is decorative, uses the existing active theme colors and easing,
  tracks the selected tab in both directions, and has no transition under reduced motion.
- **Verification:** The browser regression covers pointer selection, keyboard activation, both
  thumb directions, panel visibility, and reduced-motion behavior.

### Task 2: Keep the Media Library rail state in sync

Write the navigation regression first, then update the retained rail link as the shell applies a
new page.

- **Acceptance:** Direct load, in-place navigation away, and Back / Forward each set
  `aria-current="page"` only on the Media Library destination; existing section expansion and
  panel state remain unchanged.
- **Verify:** Targeted E2E coverage in `tests/e2e/test_media_library.py` for Bible, Songs, and
  Tata Ibadah destinations and history restoration.
- **Dependencies:** Spec acceptance.
- **Files likely touched:** `tests/e2e/test_media_library.py`,
  `multimedia/web/templates/reading/base.html`, `static/web/reading.js`.
- **Estimated scope:** Small.
- **Status:** Complete. Main menu clicks clear the retained link immediately; applying a destination
  page synchronizes it from that page's server-rendered marker, including history traversal.
- **Verification:** The browser regression covers Bible, Songs, and Tata Ibadah menu selection,
  plus a Tata Ibadah destination and Back / Forward restoration.

### Checkpoint: Targeted browser verification

- [x] Run the Media Library E2E tests and confirm both tab and rail-state scenarios pass.
- [x] Confirm no regression to Bible, Songs, or Tata Ibadah menu expansion / panel state.
- [x] Fill Traceability in `./spec.md`.

## Delivery checklist

- [x] Confirm `feat/105-media-navigation-feedback` is based on the current Spec 104 feature stack;
      `develop` is an ancestor of the branch
- [x] Verify the stacked PR path: Spec 104 targets Spec 103, Spec 103 targets `develop`, and this
      implementation PR targets Spec 104 until its parent merges
- [x] Set `bump: patch` on the ITEM and spec header
- [x] Update ITEM + [`backlog/board.md`](../../backlog/board.md) in the implementation PR
- [x] Add `VERSION` / changelog patch entry and set `release_version` in the ITEM in the same PR
- [ ] Conventional Commit and draft PR linking `./spec.md`

## Done when

- [x] All acceptance scenarios in `spec.md` hold
- [x] Targeted E2E tests are green
- [x] Board, tasks, and version metadata are complete in the implementation PR
