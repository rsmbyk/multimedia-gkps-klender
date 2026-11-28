# Research — spec 253

## D1 — Storage is `sessionStorage`

- **Decision**: Persist progress in `window.sessionStorage`; never in `localStorage`, a cookie or a
  server record.
- **Rationale**: The owner scoped the feature to the browser session — "the progress is lost when the
  browser session is closed". `sessionStorage` gives exactly that lifetime while surviving reloads
  and the reading shell's in-page stage swap, which `localStorage` would outlive and in-memory state
  would not survive.
- **Alternatives**: `localStorage` (rejected — outlives the session); plain module state (rejected —
  lost on reload); server-side per user (rejected — the owner chose session-only and the repo has no
  account-scoped draft model).
- **Provenance**: Owner answer, Clarify 2026-11-28; MDN `sessionStorage` lifetime.

## D2 — One key per template

- **Decision**: `gkps:generate:<templateId>`, where `<templateId>` is the dialog's existing
  `data-generate-tatib` value.
- **Rationale**: The owner asked that "each template can save their own progress". A per-template key
  makes independence structural, and lets Create clear exactly one record without scanning others.
  The dialog already carries the id, so no new server data is needed.
- **Alternatives**: one JSON map of all templates under a single key (rejected — clearing one
  template means rewriting the whole map, and a malformed value loses every template); key by name
  (rejected — names are editable and not unique).
- **Provenance**: Owner request; `reading/_generate_modal.html:6` (`data-generate-tatib`).

## D3 — Record shape and stale-slot filtering

- **Decision**: Store `{ v: 1, step, settled, name, date }`. On restore, ignore a record whose `v` is
  not 1, and keep only settled slot ids still present in the current dialog.
- **Rationale**: Slot ids are database pks and stable in practice, but a template can be edited
  between visits. Dropping unknown ids satisfies FR-005 without touching the record. The version
  field lets a later shape change ignore old records instead of misreading them.
- **Alternatives**: trust the saved object wholesale (rejected — a deleted slot paints a row that no
  longer exists and inflates "all settled"); migrate old shapes (rejected — there are none yet).
- **Provenance**: FR-003, FR-005; `generate.js` `refresh()` counts only rows in the current dialog.

## D4 — Write on change, never on open

- **Decision**: Call the save routine from `editor:saved`, the chooser pick, the name/date input
  handlers and the Next/Back transitions. Do **not** save from `reset()` or `open()`.
- **Rationale**: `open()` calls `reset()`, which would overwrite the restored state before it is
  read if saving lived there. Writing only on genuine changes also keeps a clean close free of a
  stored record, which is what the dirty check keys on.
- **Alternatives**: save on every `refresh()` (rejected — refresh runs during restore); save only on
  close (rejected by the owner, who chose continuous save).
- **Provenance**: Owner answer, Clarify 2026-11-28; `generate.js:334–365` (`reset`, `open`).

## D5 — A second layer, reusing the existing confirm component

- **Decision**: Add `data-generate-leave` markup using `.generate__confirm-layer` /
  `.editor__confirm`, with **Stay** and **Leave** buttons. No new CSS rules.
- **Rationale**: The same modal already renders a Create confirmation with these classes; the new
  layer gets identical geometry and theme tokens for free. A native `confirm()` cannot name the
  template or match the app's dialog treatment.
- **Alternatives**: reuse the Create confirm with dynamic text (rejected — it would share visibility
  state with Create and blur the two distinct questions); new standalone component (rejected —
  duplicates 17px/13px and padding rules already in `generate.css:159–175`).
- **Provenance**: SDD-06 (preview built from existing components); `generate.css:158–175`.

## D6 — One close funnel, with existing precedence kept

- **Decision**: Route Cancel, backdrop click and the `cancel` (Esc) event through one `attemptClose()`.
  Inside `cancel`, keep today's order: chooser first, then the Create confirm, then the leave confirm,
  then the dirty check.
- **Rationale**: Three paths currently dismiss the dialog in three places; without a funnel one of
  them would bypass FR-006. The precedence already in `bindModal()` must survive so Esc on a chooser
  still closes only the chooser.
- **Alternatives**: intercept `close()` only (rejected — `cancel` can dismiss a `<dialog>` directly,
  and the event must be prevented before that happens).
- **Provenance**: `generate.js:24–43`, `generate.js:367–372`; FR-006.

## D7 — `bump: patch`

- **Decision**: Declare `patch`, applied in the pre-merge delivery commit.
- **Rationale**: This adds a behaviour inside an existing flow, comparable to the recent feat slices
  238/248/250, all `patch`. Spec 167, which created the template type and generate flow outright,
  declared `minor`; this does not create a new capability.
- **Alternatives**: `minor` (rejected — overstates an incremental enhancement); `none` (rejected —
  the change is user-visible).
- **Provenance**: `specs/{238,248,250}/plan.md` bump lines; VER-10.

## D8 — Verification lane is browser E2E

- **Decision**: Cover every `Verified by: test` row in a Playwright E2E module; no new unit tests.
- **Rationale**: The repo's TDD scope note puts domain and application rules under Django tests and
  user-visible acceptance under Playwright `LiveServerTestCase`. This slice is entirely client-side
  interaction, with no domain rule to isolate.
- **Alternatives**: JS unit tests (rejected — no JS test runner in the repo); manual-only (rejected —
  the behaviours are scriptable).
- **Provenance**: `docs/PROCESS.md` Tests part, repo block; `tests/e2e/test_tatib_templates.py`.

## Unknowns

Zero. No question was deferred; the ambiguity scan found no open item that research could not settle.
