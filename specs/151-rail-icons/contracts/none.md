# Contracts — none

**Spec**: `specs/151-rail-icons/spec.md` · **Date**: 2026-10-29

This slice exposes no interface. It adds no endpoint, no payload field, no header, no template
variable, no context key, no event, no hook and no stored value.

The only names it touches are already internal to the page:

- the five rail destinations' markup (`base.html`), unchanged in count, order, `aria-label`, `data-tip`
  and `href`;
- the `data-kind-icon` attribute a stage row already carries (`scripture`, `song`, `text`);
- `window.gkpsMediaIcon(family)` — the same function, the same families, one path changed;
- `entries.js`'s `EMPTY_ADD_ICONS` — the same keys, one path changed.

The REST API (`/api/…`) is untouched.
