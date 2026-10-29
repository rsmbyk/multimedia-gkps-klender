# Convergence: the projector's image placeholder waits for the image to fail

**Spec**: `specs/157-projector-image-missing-glyph/spec.md`
**Passes**: 2 of 3

## Pass 1 — 2026-10-29

Every row of `plan.md`'s traceability table was checked by the method it declares: the `test` rows
against the runs below, the `inspection` rows against the code and the preview, and the one `manual` row
against what can be run before the merge.

| Gap | Type | Requirement | Evidence |
| --- | --- | --- | --- |
| The live projector readout cannot be taken on the branch: the compose `web` service serves `develop`, and a worktree server is refused by the companion's origin allow-list (`multimedia/local_media.py:447`). | `partial` | SC-001, SC-002 (manual row) | The pack already carries it as its one `manual` row; the post-merge command is in `preview/README.md` and task T019. |

**The runs.** `tests.e2e.test_image_display` — 6 tests, `OK`, including both new cases and the untouched
404 case. Before the change the two new cases failed on
`AssertionError: Locator expected to be hidden / Actual value: False`, the placeholder resolving to
`unexpected value "visible"` — red for the right reason, then green.

**The neighbouring modules.** `tests.e2e.test_audio_display`, `test_video_display` and `test_pdf_display`
— 18 tests, 16 green, 2 red: `test_untitled_preview_and_projector_idle_display_off` and
`test_navigation_and_display_off_stop_and_reset_video`, both on
`body[data-showing]` staying `true` after display-off is asked. They are card `ITEM-140`'s. Measured again on
the base commit's own two files (`24a6d6d2`, this slice's changes reverted): both fail the same way,
`Actual value: true`, in 19.1s — so they are `develop`'s and not this slice's. `data-showing` is written
at `projector.js:403` and `:1164`, neither of which the diff touches (`:204`, `:221`, `:233`). Not a gap
between this code and this spec's requirements.

**The diff.** One attribute on the image box's placeholder (`projector.html:46`), two toggles
(`projector.js:220`, `:232`) and one reset in `clearImageScreen` (`:205`). No CSS, no `media-image.js`, no
audio/video/PDF/slides path, no preview modal, no route or payload — FR-003, FR-006 and the four edge
rows were read in that diff and hold.

**Outcome**: 1 finding, dispositioned as the pack's `manual` row and task T019; no code change required.

## Pass 2 — 2026-10-29

**Outcome**: Converged — nothing remains. The one finding is a measurement deferred past the merge, not a
gap between the code and a requirement. Every `inspection` row was marked *checked by inspection* in
`plan.md`.

## Accepted gaps

<!-- none: the single finding is a deferred measurement with a scheduled task, not an accepted gap -->

## Cap reached

<!-- not reached: pass 2 converged -->
