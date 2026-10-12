# Plan 065: Hold the service entry highlight while its modal is open

- **Status:** Accepted
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-068
- **Bump:** patch

## Why

The entry highlight is CSS-only: `:hover`, or deliberate focus inside the entry.
`showModal()` puts a backdrop over the page and moves focus into the dialog, so
the entry loses both the moment Preview, Edit, or Delete opens. The highlight
fades while the modal is still showing, and the operator loses track of which
entry the modal is about. Spec 061 only covered the state after close.

## Scope / edges

**In:** origin entry background and control visibility while its modal is open,
for pointer and keyboard opening, current and legacy rows.

**Out:** add-row reveal, sidebar editors, modal content, after-close behaviour.

## Approach

1. Add an explicit `is-modal-origin` state class to the entry that owns the
   opening control (`trigger.closest('.tatib__item, .tatib__eos')`).
2. CSS: join `.tatib__item.is-modal-origin` / `.tatib__eos.is-modal-origin` to
   the existing background rule and `.is-modal-origin .entry__acts` to the
   existing `opacity: 1` rule. No new tokens, sizes, or motion.
3. `preview.js`: mark right before `showModal()`; release in the `close`
   listener before focus restoration.
4. `entries.js`: `markOrigin()` at both `showModal()` call sites (`load()` after
   a successful fetch, `confirmDelete()`); `releaseOrigin()` in the `close`
   listener. Marking at open time means a failed fetch cannot strand the class.
   Add-row openers have no owning entry, so nothing is marked.
5. Save/delete refresh replaces the stage DOM, so no class survives it.

## TDD

- Domain/app tests: N/A; no domain or server behaviour changes.
- E2E first (red): extend `tests/e2e/test_tatib_hover.py`, `TatibHoverE2ETests`.
- Targeted local command: `python manage.py test tests.e2e.test_tatib_hover.TatibHoverE2ETests`.
- Full suite and full browser E2E run only in push/CI.

## Risks

- The held class must not outlive the modal: release on every `close`, and the
  shared editor dialog's close also fires for sidebar editors, where releasing
  a missing origin is a no-op.
- The held state must not fight spec 061: release before restoring focus so the
  after-close selectors decide the resting state.
