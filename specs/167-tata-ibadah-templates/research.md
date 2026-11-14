# Research: a Tata Ibadah is a service or a template

**Spec**: `specs/167-tata-ibadah-templates/spec.md`
**Unknowns remaining**: 0

All twelve decisions below rest on code reads of the tree this branch was cut from
(`develop` at 1.23.2) and on the measurements the preview recorded in the spec's `## UI/UX`.

## D001 — The type is a stored field, derived only when a writer omits it

- **Decision**: `TataIbadah.kind` — `SERVICE = 0`, `TEMPLATE = 1` — a `SmallIntegerField` with the
  choice list, a DB `CheckConstraint` pairing it with `date`, and a `save()` that (a) derives the kind
  from the date when the instance is being inserted and no kind was set, and (b) refuses any change of
  kind on an existing row.
- **Rationale**: today the type *is* the emptiness of `date` — `_tatib_groups` branches on
  `filter(date__isnull=True)` (`multimedia/web/reading/views.py:843`) and `TatibView.get_context_data`
  sets the panel mode the same way (`:1914`). That makes the type a side effect: any writer that sends no
  date silently produces a template, and an editor can clear a date and turn a service into one. A stored
  field makes the pairing explicit and lets one constraint hold it. Deriving on insert keeps A10 true —
  the API, the forms and the tests that never learned the field still produce a template from a date-less
  create — while a row that names a kind cannot disagree with its date.
- **Alternatives considered**: (a) keep deriving from `date IS NULL` and add no field — rejected: the
  spec's FR-001/FR-002 ask for a value chosen at creation and never changed, which a derived value cannot
  promise; (b) a nullable `is_template` boolean — rejected: a flag that can disagree with the date needs
  the same constraint, and reads worse in every query; (c) a separate `Template` model — rejected: the
  entries, the panel and the media references are the same rows, and duplicating them would fork the
  entry machinery.
- **Provenance**: research (`views.py:843`, `:1914`; `multimedia/tatib/models.py:8-27`).

## D002 — Fill-in and choice are entry kinds with a target kind and a parent

- **Decision**: two new `ServiceEntryKind` values — `FILL_IN = 5`, `CHOICE = 6` — plus
  `ServiceEntry.fill_kind` (which kind the slot resolves to) and `ServiceEntry.parent` (a self-FK to the
  choice an option belongs to, `related_name='options'`, `CASCADE`). An option is an ordinary entry of
  the slot's kind with `parent` set.
- **Rationale**: the spec's FR-008/FR-009 make a fill-in "a title and one kind, no content" and a choice
  "a title, one kind, ordered options", and every downstream consumer already speaks `ServiceEntry` — the
  stage builder, the media reference query, the reorder endpoint, the projector and the panel. Two new
  kinds keep all of that working with one extra field and one nesting level, and the option rows keep
  their own `citation()`/`resolve()`, so an option previews through exactly the path a normal entry does.
  A separate model would need its own payload, its own reorder, its own media references and its own
  copy path for four fields of behaviour.
- **Alternatives considered**: (a) a `ChoiceOption` model — rejected as above; (b) storing options as
  JSON on the choice row — rejected: options are complete entries that must preview through the existing
  Preview and be copied into the generated service as entries; (c) a generic `parent`/`child` tree of any
  depth — rejected: the spec allows one level, and depth would make the order and the copy path
  ambiguous.
- **Provenance**: research (`multimedia/tatib/models.py:98-232`, `entries.py:18-24`).

## D003 — A slot is resolved by validating, not by saving

- **Decision**: the kind's New modal, opened from a slot, posts to a new
  `POST /editor/entry/validate/` instead of `/editor/entry/new/save/`. The endpoint binds the same
  `ServiceEntryForm` subclass against the submitted data, answers `{ok: true, value: {…}}` with the
  label/meta the row shows, and echoes the raw form data back; **nothing is written**. The client keeps
  that data per slot and replays it to the generate endpoint at **Create**.
- **Rationale**: FR-019 and US3/AC10 require the template to be byte-identical after a generation, and
  the modal may be abandoned at any step — a save-on-pick design would have to write the resolution
  somewhere, and every "somewhere" is a lie: on the template (mutates it), in a staging table (leaves a
  row behind on abandon), or in the browser only (the citation still has to come from the server, because
  a song's title and a passage's citation are server facts). Validating through the *same* form keeps one
  source of truth for every per-kind rule — `ServiceEntry.clean()` plus the form — and the replay at
  Create re-validates rather than trusting the client.
- **Alternatives considered**: (a) save the resolution as a draft entry on the template and delete it on
  abandon — rejected: a crash, a closed tab or a killed browser leaves the template mutated, and SC-004
  is measured on the rows; (b) a separate `SlotResolution` table — rejected: it duplicates every per-kind
  field and every rule, and the spec says the generated service holds ordinary entries; (c) render the
  summary client-side from the form's own values — rejected: the citation needs the database.
- **Provenance**: research (`views.py:303-337`, `:484`; `entries.py:203-213`).

## D004 — One transaction, one endpoint, the template's order

- **Decision**: `POST /tatib/<template_id>/generate/` takes `{name, date, slots: [{entry, kind, data}]}`,
  re-binds each form from `data`, then inside one `transaction.atomic()` creates the `TataIbadah` and walks
  the template's rows in order: an ordinary entry copies as an entry, a fill-in is replaced by its
  resolved entry, a choice by its chosen option, and a legacy `TataIbadahItem` copies as the same legacy
  row. Any invalid slot aborts the whole create with a 400 naming the slot.
- **Rationale**: the order is the template's (`order_number` shared by entries and legacy rows —
  `entries.next_order_number` reads both), so the copy has to be one walk, not an insert per client call;
  a partial create on a bad slot would leave a service the operator has to delete by hand. The endpoint
  also re-checks that every fill-in and choice *is* settled: the client's **Next** rule is UI, and the
  server must not accept an unsettled order from a stale tab.
- **Alternatives considered**: (a) create the service empty and let the client add entries one by one
  through the existing save endpoint — rejected: an abandoned sequence leaves a half-built service, and
  the per-entry endpoint writes `order_number` one at a time; (b) a `generate` flag on the existing new-
  entry endpoint — rejected: the service does not exist yet, and the `tatib` query parameter would point
  at the template.
- **Provenance**: research (`views.py:484-560`; `entries.py:236-245`).

## D005 — A template is refused at every projection entry point

- **Decision**: `service_projector` resolves the requested id and drops a template to the empty display
  (`service = None` before `_projector_data`); `obs_dock` filters on the stored kind rather than on the
  date; `tatib.html` renders **Use template** in place of both projector controls when the service's kind
  is template.
- **Rationale**: the guard has to hold where the payload is built, not only where the button is hidden —
  `/projector?service=<template>` is a URL anyone can open, and the dock builds its own list from a query
  the page cannot influence. The dock already filters `date__isnull=False`
  (`views.py:1361-1363`), so today's behaviour is right by accident; after D001 the filter should name the
  type so a future writer cannot make a dated template.
- **Alternatives considered**: (a) a 404 for a template id — rejected: the projector's own contract is an
  empty display for an unknown service, and a 404 would leak the difference; (b) client-side hiding only —
  rejected, the payload would still carry the order.
- **Provenance**: research (`views.py:1320-1380`).

## D006 — Media retention and download need no change; the slice pins them

- **Decision**: change nothing in `media_references`/`sync_references`/`media_manifest`; record FR-023 and
  FR-024 as the invariant they already satisfy.
- **Rationale**: `media_references` (`views.py:388-400`) builds `uses` from every active Tata Ibadah entry,
  dated or not, so a template's media is already "used" and never gets a removal deadline
  (`local_media.py:231-250`). `media_manifest` (`views.py:404-419`) filters `date__gte=today`, and a
  template's `NULL` date fails it, so its files are never auto-downloaded. Both queries are keyed on the
  entry's kind and the service's date, not on any type flag, so D001 and D002 leave them correct.
- **Alternatives considered**: (a) add a `kind=TEMPLATE` exclusion to the manifest — rejected: redundant,
  and it would read as if the date filter did not already exclude templates; (b) count template media as
  "unused" so it can be evicted — rejected by the owner's rule.
- **Provenance**: research (`views.py:388-419`; `local_media.py:231-250`, `:330-336`).

## D007 — Copy as template is a server clone, not a client round-trip

- **Decision**: `POST /tatib/<id>/copy-as-template/` creates a template with the same name and no date,
  clones every entry in order — and, when the source is itself a template, its fill-ins, choices and
  options — and answers `{id}`; the client then navigates to that template's page with `?mode=template`.
- **Rationale**: a client-side clone would post N entry payloads and could fail halfway; the clone is a
  single transaction over rows that are already server-side, and it is the only place that decides what
  "copy" means (FR-021: nothing is converted). The confirmation lives in the Edit modal's header, so the
  endpoint is reached from a dialog whose subject is a stored service.
- **Alternatives considered**: (a) reuse the generate endpoint with an all-ordinary template — rejected:
  generate creates a *dated service* and asks for a name and date; copy creates a template with neither;
  (b) duplicate through the API's existing create — rejected: it would create the service and then every
  entry in separate calls, with no transaction.
- **Provenance**: research (`views.py:484-560`; `spec.md` FR-020…FR-022).

## D008 — The type switcher rides in the form partial, as two chips

- **Decision**: the New Tata Ibadah form renders a two-chip group — **Normal**, **Template** — above the
  fields, posting a hidden `kind`; the Template chip hides the date field, and on an existing record the
  chips are absent and the form names the type in text. The chips reuse the `aria-pressed` pattern the
  text modal's screen-mode and the passage modal's edition chips already use
  (`_entry_form.html:12-15`, `:56-59`).
- **Rationale**: the modal body is fetched as a fragment and swapped wholesale
  (`_editor_modal.html:1-17`; `editors.js` loads `editor/<kind>/new/`), so the switcher has to live in the
  fragment to survive a validation round-trip. One pattern for every chip row keeps the CSS and the JS
  handler shared.
- **Alternatives considered**: (a) a client-side toggle outside the form — rejected: it would be lost on
  every server-rendered error re-render; (b) a native `<select>` — rejected: the app has no select in any
  modal and the spec names the passage/text modals as the pattern.
- **Provenance**: research (`_editor_form.html`, `_entry_form.html`, `editors.js`).

## D009 — A Normal cannot lose its date; the control is dropped, not hidden

- **Decision**: the tatib form omits the `Clear date` button (`_editor_form.html:20`) behind a form flag,
  and both the form and the model refuse a Normal with no date and a Template with one.
- **Rationale**: FR-003/FR-004 ask for a date that cannot be emptied, and a hidden-but-present button is
  one CSS change away from returning. A server-side refusal is the actual rule; the missing button is how
  the operator learns it. The template form has no date field at all, so the button has nothing to clear.
- **Alternatives considered**: (a) keep the button and answer with a validation error — rejected: the
  spec says no control empties it; (b) `required` on the date input — rejected: the input is a hidden
  field driven by the picker (`editors.py:57-63`), so `required` would never fire.
- **Provenance**: research (`_editor_form.html:12-40`; `editors.py:53-63`).

## D010 — Legacy rows are copied as legacy rows

- **Decision**: the generate and copy walks read both `service_entries` and `tataibadahitem_set` by
  `order_number` and copy a legacy row to a legacy row; a retired section-break entry copies as an entry.
- **Rationale**: older services still carry `TataIbadahItem` rows (spec 006 kept them beside the entries),
  and `next_order_number` already reads both sets for one order. Converting them on copy would change what
  the operator sees without asking; the spec's edge case says they are ordinary entries — muted in step 1
  and copied in order.
- **Alternatives considered**: (a) convert legacy text rows into `ServiceEntry(TEXT)` on copy — rejected:
  a copy converting content is exactly what FR-021 forbids; (b) refuse to generate from a template with
  legacy rows — rejected: templates are made from real services, and those can be old.
- **Provenance**: research (`models.py:28-44`; `entries.py:236-245`).

## D011 — The API never writes the type

- **Decision**: `TataIbadahSerializer.kind` becomes `read_only`; `create()` derives the kind from the
  submitted date, `update()` drops any posted kind; `fields = '__all__'` stays.
- **Rationale**: A10 says the model API keeps reading every Tata Ibadah and gains no surface; a writable
  `kind` would be a new one, and it would let a client make a dated template the constraint then rejects
  with a 500 rather than a field error. Read-only keeps the payload identical for existing consumers and
  adds one key.
- **Alternatives considered**: (a) expose `kind` as writable with validation — rejected: a create that
  names both a date and Template is a contradiction the API has no vocabulary for; (b) exclude the field
  from the serializer — rejected: a client reading the list could no longer tell a template from a
  service.
- **Provenance**: research (`multimedia/api/tatib/serializers.py:33-40`).

## D012 — One new client file, and no new dependency

- **Decision**: the generate modal's behaviour goes in `static/web/generate.js`, a plain IIFE using the
  same `fetch`/`FormData` helpers the entry modals use; the markup is a Django fragment
  (`reading/_generate_modal.html`) rendered only on a template's page; the styles join
  `static/styles/design/` in a new `generate.css`. No library, no build step.
- **Rationale**: the app is server-rendered with vanilla JS and already fetches its modal bodies
  (`editors.js`); the generate modal is one more fragment over the same machinery. The preview's numbers
  (frame 840×760, footer 69px, chooser 560×261.3, add bar 455.2×35.6) are the CSS targets, so the file has
  a measured specification rather than invented spacing.
- **Alternatives considered**: (a) fold the behaviour into `entries.js` — rejected: that file is 1023
  lines and owns the stage's own controls; (b) a small framework (Alpine/htmx) — rejected: no dependency
  is added for one modal, and the repo has none.
- **Provenance**: research (`static/web/editors.js:1-60`; spec `## UI/UX`).

## D013 — Two test modules, one per altitude

- **Decision**: server rules in `multimedia/web/test_tatib_templates.py` (model, forms, endpoints,
  projection guard, media queries); the flow the operator drives in `tests/e2e/test_tatib_templates.py`
  (Playwright, Python) against a live dev server on a throwaway database.
- **Rationale**: the repo splits the same way for every slice — `multimedia/web/test_*.py` for Django
  `TestCase` units and `tests/e2e/` for the browser. The class-level rules (kind pairing, option
  validation, atomic generate) are cheapest as units; **Next**'s disabled state, the chooser and the
  empty-choice row are only honest in a browser.
- **Alternatives considered**: (a) everything as E2E — rejected: the atomicity and constraint cases are
  database facts, and a browser test for them is slow and indirect; (b) everything as unit tests —
  rejected: the spec's UI states (FR-013…FR-019) are the slice's point and are measured in the DOM.
- **Provenance**: research (`multimedia/web/test_media.py`, `tests/e2e/test_entries.py`).

## Open

<!-- empty: Phase 0 is finished -->
