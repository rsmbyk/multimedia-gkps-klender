# Plan 061: Clear stale service entry highlight after modal dismissal

- **Status:** Accepted
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-063
- **Bump:** patch

## Why

Preview, Edit, and Delete modal dismissal restores DOM focus into a service entry.
The unconditional `.tatib__item:focus-within` background and
`.entry__acts:focus-within` visibility treat restored focus as interaction, leaving
an unhovered entry highlighted and sometimes its controls visible.

## Scope / edges

**In:** service entry background and control visibility after modal dismissal;
preserve real hover, deliberate keyboard focus, and touch access.

**Out:** sidebar styling, add-row reveal, modal content, data operations, layout,
and global changes to focus restoration for other editors.

## Approach

1. Add focused browser regressions for Preview, Edit, and Delete cancellation.
2. Refine entry selectors to distinguish quiet restored focus from deliberate
   keyboard focus. Reuse the existing `focus-restore-quiet` mechanism; do not blur
   the active element or redirect focus to a hidden sink.
3. If necessary, preserve entry-modal opening modality in `preview.js` and
   `entries.js` so a keyboard-opened modal returns to visible keyboard focus,
   while pointer-opened modal restoration remains quiet. Keep changes scoped to
   entry flows rather than changing all editors through the shared helper.
4. Carry entry keyboard-restoration intent through `editor:saved` and the
   `reading.js` refresh so saves/deletes retain visible focus after DOM replacement.
5. Exercise Escape as well as pointer dismissal: closing a pointer-opened modal
   with Escape must not alone turn restored focus into a persistent highlight.
6. Validate both themes, hover after restoration, Tab/Shift+Tab, and coarse touch.

## TDD

- Domain/app tests: N/A; no domain or server behavior changes.
- E2E: extend `tests/e2e/test_tatib_hover.py`, class `TatibHoverE2ETests`.
- Targeted local command: `python manage.py test tests.e2e.test_tatib_hover.TatibHoverE2ETests` in the configured project environment.
- Full-suite and full browser E2E run only in push/CI.

## Risks

- Removing all focus highlighting would regress keyboard use.
- Quiet focus can be on the entry itself or a descendant button; cover both.
- Post-save DOM replacement can restore focus again; assert the settled state.
- Hover must override quiet restoration when the pointer actually returns.
- Existing spec 025 makes all automatic restoration quiet. Spec 061 explicitly
  refines that rule only for keyboard-opened service entry modals, as shown in
  the approved preview; other editor behavior remains governed by spec 025.
