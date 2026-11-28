# Research — spec 255

## D1 — `localStorage` with a `savedAt` timestamp

- **Decision**: Store each template's record in `localStorage` under the existing
  `gkps:generate:<templateId>` key, as `{ v: 2, step, settled, name, date, savedAt }`.
- **Rationale**: The owner asked for progress that survives the browser session; `localStorage`
  survives both reloads and browser restarts. It has no native expiry, so `savedAt` carries the
  seven-day rule and is checked on read.
- **Alternatives**: `sessionStorage` (rejected — dies with the session, the current behaviour);
  a cookie (rejected — 4 KB limit, sent on every request, and not needed by the server); IndexedDB
  (rejected — async ceremony for one small record); a server record (rejected — no accounts and the
  owner scoped this to the browser).
- **Provenance**: Owner request; MDN `Window.localStorage`.

## D2 — `v: 2`, and no migration from the session store

- **Decision**: Read only `v: 2` records. A `sessionStorage` record left by spec 253 is ignored, not
  adopted.
- **Rationale**: The shape is the same but the store and the lifetime rule are not. The session
  feature reached `develop` today and production does not carry it, so no operator has work worth
  migrating; adopting records would add a code path with no real user. A version field still lets a
  future shape change ignore old records.
- **Alternatives**: migrate on first read (rejected — no production users, extra test surface);
  keep reading `sessionStorage` as a fallback (rejected — two sources of truth for one button mark).
- **Provenance**: FR-001; spec 253 shipped to `develop` only.

## D3 — The clock slides on every save

- **Decision**: `save()` always writes `savedAt: Date.now()`, and every write path calls `save()`.
- **Rationale**: The owner chose "seven days since the last change". Because spec 253 already saves
  on every slot, choice, name, date and step change, the clock slides for free.
- **Alternatives**: a fixed `createdAt` (rejected by the owner); a separate `expiresAt` field
  (rejected — one timestamp is enough and cannot disagree with itself).
- **Provenance**: Owner answer, Clarify 2026-11-28; FR-002.

## D4 — Expiry is enforced on read and swept on load

- **Decision**: `liveRecord(id)` removes and returns `null` for a record older than 168 h, and a
  `pruneExpired()` pass removes all expired `gkps:generate:*` keys at start-up and after a stage
  swap.
- **Rationale**: A record nobody opens would otherwise sit in storage forever, and the button mark
  is computed from storage at paint time — a stale record would paint a mark that the modal then
  refuses to restore. The sweep is over a handful of keys, so cost is negligible.
- **Alternatives**: prune only the current template (rejected — expired keys from other templates
  linger); a timer (rejected — unnecessary; the record is only observed on load and on save).
- **Provenance**: FR-003; `static/web/generate.js` init.

## D5 — The button carries its own template id

- **Decision**: Add `data-generate-tatib="{{ service_id }}"` to the `[data-generate-open]` button in
  `tatib.html`, and paint its mark from that value.
- **Rationale**: The modal already knows the id, but the mark must exist before the modal is opened
  and after an in-place stage swap replaces both nodes. Giving the button the id keeps the paint
  independent of the dialog's lifecycle.
- **Alternatives**: read the id from the modal (rejected — couples button paint to dialog sync);
  parse it from `data-generate-url` (rejected — string surgery on a URL that could change).
- **Provenance**: `tatib.html:14`, `_generate_modal.html` (`data-generate-tatib`).

## D6 — Repaint on `shell:page`

- **Decision**: Paint at load and on the shell's `shell:page` event, and after `save()` / `clearSaved()`.
- **Rationale**: The reading shell swaps the stage in place and dispatches `shell:page` once the new
  markup is in the document (`reading.js:2221`); without a listener the mark would be missing until a
  reload. `save()`/`clearSaved()` keep it live while the modal is open.
- **Alternatives**: a `MutationObserver` (rejected — heavier and broader than one event the shell
  already emits); paint only on open (rejected — the mark is pointless if it appears after a click).
- **Provenance**: `reading.js:2221`; FR-006, FR-008.

## D7 — The mark is a state attribute plus an accessible name

- **Decision**: `data-draft="true"` on the button drives a `::after` dot (or a child span); the dot
  is `aria-hidden`, and the button's `aria-label` becomes "Use template, draft saved" only while the
  mark shows, removed when it does not.
- **Rationale**: FR-007 forbids a colour-only signal; the visible label stays "Use template" so the
  action does not change, and the accessible name carries the state. Removing the attribute in the
  unmarked state keeps the original accessible name intact.
- **Alternatives**: change the visible label (variant B — the owner rejected it); `title` only
  (rejected — not reliably announced); `aria-describedby` (rejected — more DOM for one phrase).
- **Provenance**: Owner choice of variant A; FR-006, FR-007.

## D8 — `bump: patch`

- **Decision**: Declare `patch`, applied in the pre-merge delivery commit.
- **Rationale**: An incremental change inside the template-generate flow, the same class as spec 253
  and the neighbouring feat slices, all `patch`. It creates no new capability.
- **Provenance**: `specs/253-use-template-progress/plan.md`; VER-10.

## Unknowns

Zero. Both owner questions were answered; research settled the rest.