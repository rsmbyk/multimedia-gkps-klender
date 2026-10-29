# Feature Specification: the Media Library and the transfer history group by age

**Slice**: `specs/146-media-and-transfer-age-buckets`
**Branch**: `feat/146-media-and-transfer-age-buckets`
**Created**: 2026-10-28
**Status**: Accepted (owner, gate 1, 2026-10-28)
**Input**: "can you do the same date grouping to media library and the transfer history as the one in tata
ibadah list: last 30 days, earlier this year, older. but, for transfer history, add two more buckets:
today (last 24 hour) and last week (last 7 days)" — sent with two screenshots: `/media-library/` on
`localhost:63404`, whose list runs `28 OKTOBER 2026`, `25 OKTOBER 2026`, `19 OKTOBER 2026`, and the same
page with its `Transfers` dialog open, whose nine rows carry no date and no heading at all.

**Preview**: `static preview at specs/146-media-and-transfer-age-buckets/preview/preview.html` — the
Media Library list and the Transfers dialog, assembled from the page's own markup, class names and frozen
stylesheets, over a fixture set that reaches every bucket, with the real companion snapshot one control
away.

## What the two surfaces do today

| surface | groups by | heading | example |
| --- | --- | --- | --- |
| Media Library list | the file's upload **date** | `28 OKTOBER 2026` per day | eight files draw four headings, one of them over a single row |
| Transfers dialog | nothing — active first, then newest finished | — | nine rows in one undifferentiated stack |

The Tata Ibadah sidebar stopped grouping by calendar unit in spec 132 and groups by **age** — `Upcoming`,
`Last 30 days`, `Earlier this year`, `Older` — with the present day taken in `Asia/Jakarta` (`reading/R9`).
Spec 132's own Assumptions named "the media library's date lane" as out of scope. This slice takes it,
and the transfer history, which never had one.

## User Scenarios & Testing

### US1 — The Media Library list groups by age, not one heading per day (P1)

**Why this priority**: a per-day heading answers "which day" — a question the row's own meta line already
answers (`Image · 28 Oktober 2026 · 7 KB`). What the heading is asked for is "how old is this", and a
heading per day produces one-row groups as soon as the library holds a few files: the companion's eight
files draw four headings, one of them over a single row, and under age they draw one.

**Independent Test**: open `/media-library/` with files uploaded today, twelve days ago, forty days ago and
last year; the list draws `Last 30 days`, `Earlier this year`, `Older`, in that order, each over its own
rows, and no date-shaped heading anywhere.

**Acceptance scenarios**

1. **Given** files uploaded on the last thirty-one days, **When** the list draws, **Then** they sit under
   one `Last 30 days` heading.
2. **Given** a file uploaded forty days ago in the present calendar year, **Then** it sits under
   `Earlier this year`.
3. **Given** a file uploaded in an earlier calendar year, **Then** it sits under `Older`.
4. **Given** a bucket with no file, **Then** neither its heading nor its spacing is drawn.
5. **Given** the list sorted by upload date ascending, **Then** the buckets run oldest first and the rows
   inside each stay oldest first.

### US2 — The transfer history says when a transfer happened (P1)

**Why this priority**: the Transfers dialog is opened to answer "did it go, and how long ago". Today it
prints a name and `Completed` and nothing else — a transfer from ten minutes ago and one from three weeks
ago are the same row.

**Independent Test**: open the Transfers dialog over the companion's nine transfers, aged by hand across
five buckets; each heading appears once, in order, over the rows it owns.

**Acceptance scenarios**

1. **Given** a transfer started within the last twenty-four hours, **Then** it sits under `Last 24 hours`.
2. **Given** one started between one and seven days ago, **Then** `Last 7 days`.
3. **Given** one started between seven and thirty days ago, **Then** `Last 30 days`.
4. **Given** one started more than thirty days ago in the present calendar year, **Then**
   `Earlier this year`.
5. **Given** one started in an earlier calendar year, **Then** `Older`.
6. **Given** an active transfer, **Then** it still draws above every finished one, inside its own bucket.
7. **Given** a bucket with no transfer, **Then** no heading is drawn for it.

### US3 — Both surfaces say ages the same way as the Tata Ibadah list (P2)

**Why this priority**: three lists in one application naming the same three buckets differently is the
defect class spec 132 closed between the reading panel and the operator dock. The words `Last 30 days`,
`Earlier this year` and `Older` are already in the product; a second spelling of them is a second thing to
learn.

**Independent Test**: read the three surfaces' headings side by side; the shared three are identical
strings, drawn in the same case, and only the transfers' two extra buckets have words of their own.

**Acceptance scenarios**

1. **Given** the Media Library, the Transfers dialog and `/tatib/` are open, **Then** the buckets they
   share read `Last 30 days`, `Earlier this year`, `Older` in all three.
2. **Given** the labels are written in sentence case in the markup, **Then** the stylesheet alone draws
   them uppercase, so assistive technology reads the words.

### Edge Cases

- **When** a file is uploaded today, **Then** it is `Last 30 days` — the Media Library has no bucket of its
  own for today, because an upload cannot be in the future and today's uploads are the newest row of the
  same window.
- **When** a transfer is still running, **Then** it is bucketed by the moment it started, so a long upload
  that began yesterday is reported under yesterday's age while it draws above the finished rows.
- **When** sorting by file size, **Then** no bucket heading is drawn: the rows are not in age order, so an
  age heading over them would group rows that are not adjacent.
- **When** a filter or the `Unused` chip leaves a bucket with no visible row, **Then** that bucket's
  heading hides with it.
- **When** today is early in January, **Then** `Earlier this year` may hold nothing while `Last 30 days`
  holds December's files: an empty bucket is omitted, never printed with a zero.
- **When** the transfer list is drawn in the rail's progress flyout, **Then** it keeps its own shape — the
  active rows and the seen divider — and draws no bucket headings; the headings belong to the dialog.
- **When** the companion is unavailable, **Then** the two empty states (`Local library unavailable on this
  computer.`, `No transfers yet.`) are unchanged.
- **When** a heading is read by a screen reader, **Then** it is a real heading at the level its surface
  already uses — `h2` in the list, `h3` under the dialog's `Transfers` — and its name keeps sentence case.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | The Media Library list groups its rows by upload age into three buckets, in this order and under these labels: `Last 30 days`, `Earlier this year`, `Older`. The shared labels are the Tata Ibadah list's own strings. | `reading/R20` |
| FR-002 | A file's bucket is decided from its upload day and the present day: today through thirty days ago is `Last 30 days`; older than thirty days and in the present calendar year is `Earlier this year`; anything else is `Older`. | `reading/R20` |
| FR-003 | The present day is the congregation's calendar day in `Asia/Jakarta`, as `reading/R9` requires, so a file uploaded at 06:00 WIB does not change bucket at 07:00. | `reading/R20` |
| FR-004 | A bucket with no file draws neither a heading nor its spacing; the buckets drawn stay in the order of FR-001. | `reading/R20` |
| FR-005 | Bucket headings are drawn only while the list is sorted by upload date; a size sort draws none. Ascending date order reverses the bucket order so the list still reads oldest first. | `reading/R20` |
| FR-006 | The heading is the list's existing `h2.media-library__group` — same type, class, size, colour, weight, letter-spacing, case transform and margins — carrying its bucket key as `data-bucket` (`last-30-days`, `earlier-this-year`, `older`); the per-date heading and its day key are gone. | `reading/R20` |
| FR-007 | The type chips and the `Unused` chip still filter the list; a bucket left with no visible row hides its heading, and clearing the chips restores both. | `reading/R20` |
| FR-008 | A row is unchanged: icon, filename, `Type · full date · size` meta line, its service links or its `Unused · …` line, the cloud control and the remove button. | `reading/R20` |
| FR-009 | The Transfers dialog groups its rows by age into five buckets, in this order and under these labels: `Last 24 hours` (started within the last 24 hours), `Last 7 days` (24 hours to 7 days), `Last 30 days` (7 to 30 days), `Earlier this year` (more than 30 days, present calendar year), `Older` (anything else). | `reading/R21` |
| FR-010 | A transfer's bucket is decided by the instant it started, and the three rolling windows are measured from the moment the dialog draws, not from a calendar boundary. | `reading/R21` |
| FR-011 | Active transfers still draw above finished ones; the bucket a transfer belongs to is its start time's, so an active row draws at the top of the bucket it started in. | `reading/R21` |
| FR-012 | Inside a bucket, rows keep today's order: finished rows by end time newest first, ties by id newest first. | `reading/R21` |
| FR-013 | A bucket heading in the dialog is an `h3.media-transfers__group` under the dialog's existing `h2`, drawn on the list's heading numbers (12px, `--head-ink`, uppercase through the stylesheet, letter-spacing `.07em`), and carrying its bucket key as `data-bucket` (`last-24-hours`, `last-7-days`, `last-30-days`, `earlier-this-year`, `older`). | `reading/R21` |
| FR-014 | The rail's progress flyout keeps its own shape — active rows, then the seen divider — and draws no bucket headings. | `reading/R21` |
| FR-015 | A transfer row is unchanged: direction glyph, name, and its state (`Completed`, `Cancelled`, `Failed`, or the percentage while active). No per-row date is added; the heading carries the age. | `reading/R21` |
| FR-016 | The two surfaces compute their buckets through one shared browser rule, so the Media Library, the Transfers dialog and any later surface cannot drift apart, and the bucket keys are the ones FR-006 and FR-013 name. | `reading/R21` |
| FR-017 | The empty states are unchanged, and a bucket heading is never drawn over an empty list. | `reading/R20`, `reading/R21` |

### Key Entities

- **Age bucket** — one group of a list. Identity `key`, `label`, and its rows. Computed per render from a
  row's own day or instant and the present day; never stored, never written to the companion's database.
- **Transfer age ladder** — the five keys of FR-009 in their fixed order; the two recent rungs exist only
  here, the last three are the Tata Ibadah list's.
- **Present day** — the congregation's calendar day in `Asia/Jakarta`, from which both surfaces' day
  arithmetic starts.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | The Media Library draws exactly `Last 30 days`, `Earlier this year`, `Older`, once each and in order, when all three hold rows | browser reading of the served list with routed companion data |
| SC-002 | The bucket edges hold at zero, thirty, thirty-one days and at the year boundary, on a pinned present day | unit tests over the shared rule |
| SC-003 | The Transfers dialog draws its five buckets once each and in order when all five hold rows | browser reading of the served dialog with routed companion data |
| SC-004 | The transfer edges hold at twenty-four hours, seven days and thirty days, on a pinned clock | unit tests over the shared rule |
| SC-005 | The three shared labels are byte-identical across `/media-library/`'s list, its Transfers dialog and `/tatib/` | string comparison of the three served documents' headings |
| SC-006 | An active transfer draws above every finished row of its bucket | browser reading of the dialog |
| SC-007 | Nothing else moves: the `multimedia.web` suite stays green and the media-library browser suite is run at the push step | `manage.py test` |

## UI/UX

- **Copy**: `Last 30 days` · `Earlier this year` · `Older` on the list; the same three plus the two new
  rungs — `Last 24 hours` · `Last 7 days` — on the transfer history.
- **List heading** (unchanged, measured on the frozen stylesheet): `.media-library__group` — 12px, weight
  700, `letter-spacing` 0.84px (`.07em`), `text-transform: uppercase`, colour `--head-ink`
  (`rgb(100, 99, 87)` light), `margin: 28px 0 6px`.
- **Dialog heading** (new): `.media-transfers__group` — the same 12px / `--head-ink` / `.07em` / uppercase,
  `margin: 20px 0 2px`, and `4px` above the first heading so it does not push off the dialog's `22px`
  padding.
- **States**: a bucket with rows · a bucket omitted · a bucket emptied by a chip · `Unused` on · a size
  sort (no headings) · the rail flyout (no headings) · the companion unavailable (unchanged empty state).
  No new control, no count on a heading, no motion.
- **Dark**: the same headings with the dark palette — `--head-ink` over `--canvas`.
- **Responsive**: the list's heading is the list's own width; the dialog is `min(580px, 100vw - 32px)`, and
  the longest heading (`EARLIER THIS YEAR`) is measured inside it at 320px, where `.media-transfers__main`
  still ellipsizes its name to one line.

## Assumptions

- **The Media Library has no `Upcoming` bucket.** An upload's timestamp is never in the future, and the
  request named three buckets for this surface. A file uploaded today is the newest row of `Last 30 days`.
- **The Media Library has no `Last 24 hours` bucket** for the same reason, even though the transfer
  history gains one: the list already sorts newest first, so today's uploads are the top of the list either
  way.
- **The three shared buckets keep the Tata Ibadah list's windows** — thirty days, then the present calendar
  year — so "earlier this year" means the same thing in all three lists.
- **The transfer history's two extra buckets are rolling windows** — 24 hours and 7 days from the moment
  the dialog draws — because the request defines them as durations ("last 24 hour", "last 7 days"), not as
  calendar units.
- **Their labels are `Last 24 hours` and `Last 7 days`**, matching the windows the ladder names below them;
  the friendlier `Today` / `Last week` was offered and is still a one-word change (see Clarifications).
- **A transfer is dated by its start**, not its end: the start is the only instant an active transfer has,
  and it is the moment the operator began the transfer.
- **Size sorts keep no headings**: the request is about date grouping, and the size order is not an age
  order.
- **The rail's flyout keeps its shape.** It is a progress popover, not the history, and its seen divider
  already answers "which of these are new".
- **No saved copy exists for either surface.** The Media Library is drawn from the loopback companion in
  the browser and the Transfers dialog from the same companion; nothing in the saved-page renderer touches
  them, so this slice adds no saved-copy requirement.
- **Out of scope**: the Tata Ibadah list (already grouped, spec 132), the search results' ordering, the
  media picker inside an entry editor, and any change to how the companion stamps `uploaded_at`,
  `started_at` or `ended_at`.

## Clarifications

### Session 2026-10-28

- Q: the two new bucket labels — `Today` · `Last week`, or `Last 24 hours` · `Last 7 days`? → **ASKED,
  UNANSWERED** (the question tool timed out with no response). Recorded as the recommendation, per SDD-08's
  rule that a skipped question becomes a recorded assumption rather than a deferral: **`Last 24 hours` ·
  `Last 7 days`**. The reason is the one spec 132 used to reject "last months": a rolling window has no
  honest calendar name, and a transfer started at 23:00 yesterday would be drawn under `Today` while
  `Last 30 days` two rungs down names its window exactly. The preview still carries both sets behind a
  control, and gate 1 offers the answer as a change request.
