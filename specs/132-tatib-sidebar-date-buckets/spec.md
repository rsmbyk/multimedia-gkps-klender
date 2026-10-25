# Feature Specification: The Tata Ibadah list groups by age, not by month

**Slice**: `specs/132-tatib-sidebar-date-buckets`
**Branch**: `feat/132-tatib-sidebar-date-buckets`
**Created**: 2026-10-25
**Status**: Accepted (owner, gate 1, 2026-10-25; the plan, tasks, analysis and the 22-item checklist
accepted at gate 2 the same day)
**Input**: "i want you to change the date group header in tataibadah sidebar to the followings (i still
need suggestion on the naming part tho): upcoming (today or later) · last months (last 30 days) · earlier
this year (older than 30 days but still in the current calendar year) · anything older" — sent with a
screenshot of the Tata Ibadah sidebar at `localhost:63404/tatib/148/`, whose dated list runs `OKTOBER 2026`,
`AGUSTUS 2026`, `JULI 2026`, `JUNI 2026`, `MEI 2026`.

## User Scenarios & Testing

### US1 — The dated list reads as a schedule (P1)

**Why this priority**: the panel is opened to find the service being prepared or the one just past. A
month header answers "which calendar month" — a question nobody asks of a list whose rows already print
their own full date — and it puts a service from three days ago and a service from six weeks ago under the
same heading.

**Independent Test**: open `/tatib/` with services dated today, next week, ten days ago, forty days ago and
last year; the panel shows four headings in order — `Upcoming`, `Last 30 days`, `Earlier this year`,
`Older` — each holding its own rows.

**Acceptance scenarios**

1. **Given** services dated today and later, **When** the panel opens, **Then** they sit under
   `Upcoming`.
2. **Given** services dated one and thirty days before today, **When** the panel opens, **Then** they sit
   under `Last 30 days`.
3. **Given** a service dated thirty-one days before today in the same calendar year, **When** the panel
   opens, **Then** it sits under `Earlier this year`.
4. **Given** a service dated in an earlier calendar year, **When** the panel opens, **Then** it sits under
   `Older`.
5. **Given** a bucket with no rows, **When** the panel opens, **Then** neither its heading nor its
   separator is drawn.

### US2 — Today is at the top of Upcoming (P1)

**Why this priority**: the service being run today is the row an operator reaches for, and the existing
descending order buries it beneath every future service.

**Independent Test**: with services dated today, tomorrow and two months out, the panel's first rows are
today's, then the two-month-out service, then tomorrow's.

**Acceptance scenarios**

1. **Given** services today and later, **When** `Upcoming` is read top to bottom, **Then** today's rows
   come first, then the remaining ones farthest date first.
2. **Given** two services on the same date, **Then** the later-created one comes first, as today.
3. **Given** any other bucket, **When** it is read top to bottom, **Then** the newest date comes first and
   ties break on creation time, as today.

### US3 — The dock's picker names dates the same way (P2)

**Why this priority**: the operator dock lists the same services. Two surfaces that label the same dates
differently make the operator re-learn the list between the reading page and OBS.

**Independent Test**: open `/obs/dock` against the same data and read four headings identical to the
reading panel's.

**Acceptance scenarios**

1. **Given** the same services, **When** `/obs/dock` opens, **Then** its picker shows the four buckets
   under the same labels and in the same order.
2. **Given** a service dated today, **Then** its dock row keeps its today mark, and a future one keeps its
   upcoming mark.

### US4 — The saved copy groups the same way (P2)

**Why this priority**: a saved `/tatib/` page is rebuilt from the cached library. If its renderer still
sorts by month, the list reorders itself the moment the page works offline — the defect class specs 106,
122 and 129 each closed on another surface.

**Independent Test**: render `/tatib/` from the saved library and compare its headings and row order with
the server route's.

**Acceptance scenarios**

1. **Given** a synced library, **When** `/tatib/` is rendered from it, **Then** the four headings and
   their rows match the server page.
2. **Given** the saved page opened on a later day, **Then** the buckets follow the day it is opened, not
   the day it was saved.

### Edge Cases

- **When** today is early in January, **Then** `Earlier this year` may hold nothing while `Last 30 days`
  holds December's services: an empty bucket is omitted, never printed with a zero.
- **When** a service is dated today, **Then** it is `Upcoming`, not `Last 30 days`.
- **When** a future service crosses into the next calendar year, **Then** it stays in `Upcoming`.
- **When** the owner types a filter that empties a bucket, **Then** that bucket hides and its separator
  goes with it, as the other panels already do.
- **When** template mode is on (`?mode=template`), **Then** the undated list is unchanged: one
  `Templates` heading over names sorted A–Z.
- **When** the panel is read by a screen reader, **Then** each heading stays a heading and the list keeps
  its order; the bucket names reach assistive technology as `Upcoming`, `Last 30 days`, `Earlier this
  year`, `Older` — never the uppercase form the stylesheet draws.
- **When** a bucket's rows are all filtered out, **Then** the heading hides with them and the next
  heading's divider is not left floating.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | The dated Tata Ibadah list groups its rows into four buckets, in this order and under these labels: `Upcoming`, `Last 30 days`, `Earlier this year`, `Older`. The labels are written in sentence case and drawn uppercase only by the stylesheet, so the accessible name keeps its words. | `reading/R9` |
| FR-002 | A service's bucket is decided from its date and the present day: today or later is `Upcoming`; one to thirty days before today is `Last 30 days`; more than thirty days before today in the same calendar year is `Earlier this year`; anything else is `Older`. | `reading/R9` |
| FR-003 | "Today" is the present calendar date in `Asia/Jakarta`, the congregation's own day, not the server's UTC date. | `reading/R9` |
| FR-004 | `Upcoming` lists today's rows first, then the remaining future rows farthest date first; ties break on creation time, newest first. Every other bucket lists newest date first with the same tiebreak. | `reading/R9` |
| FR-005 | A bucket with no rows draws neither a heading nor a separator; the groups drawn are always in the order of FR-001. | `reading/R9` |
| FR-006 | The operator dock's picker (`/obs/dock`) groups by the same four buckets, in the same order, under the same labels, and marks a today row with the same `Today` badge the panel uses, in place of its former row tints. | `reading/R9` |
| FR-007 | The saved renderer draws the same four buckets, in the same order, under the same labels, with the same row order, computing its present day in `Asia/Jakarta` so a page opened later buckets by that day. | `reading/R5` |
| FR-008 | The month heading and the `data-month` group key are gone from both renderers and from the in-page reconciler; a group carries `data-bucket` with its bucket key (`upcoming`, `last-30-days`, `earlier-this-year`, `older`). | `reading/R9` |
| FR-009 | The panel filter still works across the buckets: typing hides non-matching rows, a bucket left with no visible row hides itself and its separator, and clearing the field restores both. | `reading/R9` |
| FR-010 | Template mode is unchanged: one `Templates` heading over the undated services sorted by folded name. | `reading/R9` |
| FR-011 | The heading's typography, sticky position, padding, colour and the separator rule are unchanged; only the text and the group key change. | `reading/R9` |
| FR-012 | A row dated today carries a `Today` badge between its name and its date, drawn as a small uppercase chip on the action accent (`--active-bg` with `--active-ink`); the badge is the only mark that distinguishes it, and the row's accessible name ends `— today`. No other row carries one. | `reading/R9` |
| FR-013 | The saved renderer draws the same badge, from the same present day, so a saved page and the server page mark the same rows. | `reading/R5` |

### Key Entities

- **Date bucket** — one group of the dated Tata Ibadah list. Identity `key` (`upcoming` · `last-30-days` ·
  `earlier-this-year` · `older`), `label`, and its rows. Computed per render from the service's `date` and
  the present day; never stored, never written to the database.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | The four labels appear in order, once each, when all four have rows | read from the served markup of `/tatib/` |
| SC-002 | A bucket's edges hold at zero, thirty, thirty-one days and at the year boundary | unit tests on the bucket rule with a fixed present day |
| SC-003 | Today's rows lead `Upcoming` | unit test over the panel's group data, and a browser reading of the served page |
| SC-004 | The dock's picker shows the same four labels in the same order | read from the served markup of `/obs/dock` |
| SC-005 | The saved page matches the server page's groups and rows | browser suite comparing the two renders |
| SC-006 | Nothing else moves | the `multimedia.web` suite stays green; the reading E2E suites are run at the push step |

## UI/UX

- **Copy**: `Upcoming` · `Last 30 days` · `Earlier this year` · `Older`. At most four headings on the
  dated list; `Templates` alone in template mode.
- **Today badge**: the word `Today` in a 10px / 650 / letter-spacing .08em uppercase chip, padding
  `1px 7px 2px`, `999px` radius, no border, `var(--active-bg)` fill with `var(--active-ink)` ink — forest
  green on white in light, royal blue with navy ink in dark; it sits between the row's name and its date
  (`margin-left: auto`), so the name keeps its ellipsis. It keeps its own colours on a selected row.
- **Typography / position** (unchanged, measured on the running branch): `.group__head` 11.5px / weight
  650 / letter-spacing .10em / `text-transform: uppercase`, `--head-ink`, sticky at `top: 0`, padding
  `10px 8px 7px`, background `var(--canvas)`.
- **Separator** (unchanged): `.group + .group` — `2px solid var(--divider)`, `10px` margin-top, `10px`
  padding-top; a filtered-empty group removes it through `.group.is-hidden + .group`.
- **States**: a bucket present with rows · a bucket omitted (no rows) · a bucket hidden by the filter ·
  `Templates` in template mode. No new state, no new control, no motion.
- **Responsive**: the labels are the panel's own width; the longest, `EARLIER THIS YEAR`, is measured on
  the running branch against the 300px panel and the collapsed mini rail, where headings are not drawn.

## Assumptions

- **The row's own date label is unchanged** — `25 Okt 2026` — so a row still says its date; the heading
  only says how old the group is.
- **The bucket vocabulary is English**, like the rest of the panel's chrome (`No matching Tata Ibadah.`,
  `Add Tata Ibadah`), though the month names inside a row stay Indonesian.
- **The four buckets are a fixed set**, not settings: no preference, no per-user choice, no configurable
  window. Thirty days is written as a constant, not a form field.
- **The dock's month grouping is the same rule** and takes the same buckets, because the owner asked for
  both surfaces to name dates the same way; the dock keeps its own row markup and its today/upcoming
  marks.
- **The saved copy recomputes on open**: its buckets follow the day the page is read, not the day it was
  saved.
- **Out of scope**: the media library's date lane, the search results' ordering, and the editor's date
  picker — none of them groups services by age.

## Clarifications

### Session 2026-10-25

- Q: which label set? → ANSWERED: English, rule-shaped — `Upcoming` · `Last 30 days` · `Earlier this
  year` · `Older`. The draft's "last months" was rejected because the bucket is a rolling thirty days and
  no month name describes it honestly.
- Q: which order inside `Upcoming`? → ANSWERED: today's rows pinned first, then the rest of the future
  farthest date first.
- Q: does the OBS dock's picker take the same buckets? → ANSWERED: yes.
- Q: how is a today row marked, once it leads `Upcoming`? → ANSWERED: a `Today` badge between the
  name and the date — not a row tint. Its treatment was chosen from three rendered in both themes: the
  solid pill on the action accent (forest green / royal blue), not the outlined chip nor the dot.
- Q: what does the dock do with its today and upcoming tints? → ANSWERED: the today badge replaces
  them; the dock drops both tints, because `Upcoming` now names the future and the today tint was the
  token a selected row uses.
- Q: (not asked) does the saved copy follow? → ASSUMED yes: it is the same page offline, and specs 122/129
  already require the saved renderer to match the server route.
