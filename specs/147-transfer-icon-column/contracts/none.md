# Contracts: none

**Spec**: `specs/147-transfer-icon-column/spec.md`

This slice exposes no external interface. It changes one CSS declaration on a class the page already
draws; there is no endpoint, payload, template variable, stored value or event.

- No route is added or changed.
- No JSON shape from the local companion (`/transfers`, `/files`, `/status`) is read differently.
- No `localStorage` key is added or re-read.
- No template variable is added to `media_library.html` or `base.html`.

The one contract that does change is internal and CSS-shaped: `.media-transfers__mark` is 32px and
`flex: none`. It is stated in `plan.md` and proved by the E2E in `quickstart.md`.
