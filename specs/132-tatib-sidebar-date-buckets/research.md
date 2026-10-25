# Phase 0 — Research: the Tata Ibadah list groups by age

**Spec**: `specs/132-tatib-sidebar-date-buckets/spec.md`
**Unknowns remaining: 0**

## D-001 — The rule is computed at render time, never stored

**Decision**: `TataIbadah.date` stays the only stored fact; the bucket is derived on every render from
that date and the present day.
**Rationale**: a stored bucket is wrong by midnight — a service dated today becomes yesterday without
anything being written, and a migration would have to rewrite every row daily.
**Alternatives**: a `bucket` column (rejected: staleness plus a nightly job); a `created_at`-based rule
(rejected: the service's date is the fact the panel is about).
**Provenance**: research — the existing panel already derives its heading from `service.date`
(`multimedia/web/reading/views.py::_tatib_groups`).

## D-002 — One server helper owns the rule; both server surfaces call it

**Decision**: a new module `multimedia/web/reading/date_buckets.py` holds the bucket keys, the labels, the
thirty-day window, the `Asia/Jakarta` present day and the grouping function. `_tatib_groups()` (the reading
sidebar) and `obs_dock()` (the dock picker) both build their groups through it, keeping their own row
shapes.
**Rationale**: the two surfaces already disagreed on nothing but the shape of a row, and the owner asked
for them to name dates the same way. Two copies of a rule that will be edited is how they drift.
**Alternatives**: keep `obs_dock`'s own loop (rejected: the same rule written twice); move both onto one
template (rejected: the dock rows carry marks the sidebar does not, and the dock's markup is its own
accepted design).
**Provenance**: research — `views.py::obs_dock` and `views.py::_tatib_groups` each build a month key today.

## D-003 — The present day is `Asia/Jakarta`

**Decision**: the bucket boundary uses `timezone.now().astimezone(ZoneInfo('Asia/Jakarta')).date()`.
**Rationale**: the congregation's calendar day is WIB. Under the project's UTC `TIME_ZONE`, a service dated
today would stop counting as today at 07:00 WIB, and one dated yesterday would still count as today until
then — a wrong heading for seven hours of every day.
**Alternatives**: `timezone.localdate()` (rejected: the setting is UTC); `settings.TIME_ZONE` changed to
`Asia/Jakarta` (rejected: out of scope, and every stored timestamp's rendering would move with it).
**Provenance**: the repository already takes the Jakarta day for media eligibility and inventory
(`views.py` ×3, `multimedia/local_transfers.py`), so the panel follows the same convention.

## D-004 — The saved renderer carries its own copy of the rule

**Decision**: `static/web/offline-render.js` computes the present day with
`Intl.DateTimeFormat('en-CA', {timeZone: 'Asia/Jakarta'})` and applies the same boundaries in JavaScript.
**Rationale**: the saved page is rebuilt in the browser from the cached library and has no server to ask;
every other date rule on that path is already a JavaScript copy (month names, short dates, panel copy).
**Alternatives**: asking the origin for its buckets (rejected: the offline path must not need the network);
saving the bucket with the page (rejected: D-001 — it is stale the next day).
**Provenance**: specs 106/122/129 established the duplication pattern and the parity requirement.

## D-005 — The group key is renamed `data-month` → `data-bucket`

**Decision**: a group section carries `data-bucket="upcoming|last-30-days|earlier-this-year|older"`; the
`data-month` attribute disappears from both renderers, and `static/web/reading.js`'s reconciler whitelist
(`nodeIdentity`) names the new attribute.
**Rationale**: the key no longer identifies a month, and `nodeIdentity` is what keeps a group's DOM node
across an in-page navigation — leaving the old name there documents a lie and invites a later reader to
re-add a month key.
**Alternatives**: keep `data-month` with a bucket value (rejected: misleading); drop the key (rejected: the
reconciler would then match groups by position only, so a bucket disappearing would rewrite the whole list).
**Provenance**: `reading.js::nodeIdentity` lists the attributes; `_tatib_panel.html` and
`offline-render.js::servicePanel` set them.

## D-006 — Labels are written in sentence case, uppercased by the stylesheet

**Decision**: the markup carries `Upcoming`, `Last 30 days`, `Earlier this year`, `Older`;
`.group__head`'s `text-transform: uppercase` draws the capitals.
**Rationale**: the accessible name is the text content, so the panel should not shout `EARLIER THIS YEAR` at
a screen reader; the drawn form is a styling decision, and the stylesheet already owns it.
**Alternatives**: write the labels uppercase (rejected: the name follows); a `aria-label` per heading
(rejected: a second copy of the same string to keep in step).
**Provenance**: `.group__head` in `static/styles/design/components.css`; the month headings were sentence
case in the markup for the same reason.

## D-007 — Today's rows lead `Upcoming` through a stable sort, not a second query

**Decision**: rows are read in the existing order (`-date`, `-created_at`) and `Upcoming` is then sorted
with the single key `service.date != today`; the sort is stable, so today's rows come first in creation
order and the future keeps its farthest-first order.
**Rationale**: one pass, no second query, and the tiebreak the panel already had is preserved by the stable
sort rather than reimplemented.
**Alternatives**: two queries, one for today and one for the future (rejected: two round-trips for a
partition); `CASE WHEN` ordering in SQL (rejected: the panel's other orderings are built in Python, and this
keeps the window literal).
**Provenance**: research on the existing query in `_tatib_groups` (order `-date`, `-created_at`).
