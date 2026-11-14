# Research: the Media Library and the transfer history group by age

**Slice**: `specs/146-media-and-transfer-age-buckets` · **Phase 0** · 2026-10-28

Every decision below names where it came from. Owner decisions are marked as such; nothing here was
decided against evidence.

## D1 — One shared browser rule, in `static/web/age-buckets.js`

**Decision.** A new classic script, `static/web/age-buckets.js`, defines one IIFE and exposes
`window.gkpsAgeBuckets`. `media-library.js` and `media-handoff.js` both call it and neither computes a
bucket itself.

**Rationale.** The repo's browser code is classic scripts loaded per page by `base.html`, each an IIFE
exposing a single global — `window.gkpsMediaIcon` (`static/web/media-stage.js:13`),
`window.gkpsMediaHandoff` (`static/web/media-handoff.js:153`). A new file in that shape needs no build
step and no module loader. The drift this slice exists to prevent is a repo fact, not a hypothesis: spec
132 had to add a commit (`f586591a`) because the dock and the reading panel ordered and marked the same
services differently, and the panel and dock still each hold their own copy of the bucket rule (the Python
`date_buckets.py` for the server panel; `static/web/obs-dock.js` renders from server data).

**Alternatives rejected.** *Duplicating the rule in both files* — the exact failure mode above, two copies
that agree only until the next edit. *An ES module* — the page loads classic scripts; `type="module"`
changes load and error semantics, and a module cannot be opened from `file://` for the static preview.
*A bundler* — the repo has no front-end build step and this is 60 lines.

**Provenance.** Repo convention (`base.html` script block, `static/web/*.js` shape); spec 132's record.

## D2 — The Media Library's windows are the Tata Ibadah list's, in days

**Decision.** A file's bucket is the number of whole calendar days between its upload day and the present
day in `Asia/Jakarta`: `0–30` is `last-30-days`, `31+` in the same calendar year is `earlier-this-year`,
anything else `older`.

**Rationale.** `multimedia/web/reading/date_buckets.py` already defines exactly this (`RECENT_DAYS = 30`,
`bucket_key`); `reading/R9` states it. Two lists in one application must not disagree about what
"earlier this year" means.

**Alternatives rejected.** *Using the transfer ladder's rolling instants for files too* — a file has a
day-granular meaning ("uploaded on the 19th"), and R9's boundary is a day boundary; a rolling window would
move a file between buckets during the day it sits exactly thirty days back.

**Provenance.** `reading/R9`; `date_buckets.py`; owner's request ("the same date grouping as the tata
ibadah list").

## D3 — The transfer ladder is rolling, and a transfer is dated by its start

**Decision.** `last-24-hours` is `now − started_at < 24h`; `last-7-days` is `< 7 days`; `last-30-days` is
`< 30 days`; then the Jakarta calendar year decides between `earlier-this-year` and `older`.

**Rationale.** The request defines the two new rungs as durations ("today (last 24 hour)", "last week (last
7 days)"). `db` rows carry `started_at` and `ended_at` as UTC ISO strings with an offset
(`multimedia/local_transfers.py:16-17`, `:56-58`), and an active transfer has no `ended_at` — so the start
is the only instant every row has. `Date.parse` handles the offset-bearing ISO string in every supported
browser.

**Alternatives rejected.** *`ended_at` as the row's date* — unavailable for active rows, and it would move
a running transfer's bucket at the moment it finished. *Calendar days for the two new rungs* — that would
make `Last 24 hours` a misnomer and contradict the request's own wording.

**Provenance.** Owner's request; `local_transfers.py`; `tests/e2e/test_media_library.py`'s routed fixtures.

## D4 — The transfers list needs a bucket-index sort; the file list does not

**Decision.** `renderTransfers()` computes each row's bucket key first, then sorts by (bucket index,
active first, `ended_at` descending, `id` descending) and draws a heading when the bucket changes.

**Rationale.** The file list's order (`uploaded_at` descending) is already monotonic in age, so a
key-change check is enough. The transfers list is not: `TransferManager.list()` puts *active* rows first
regardless of when they started (`local_transfers.py:43-45`), so an active upload started three days ago
would be drawn above a finished row from ten minutes ago and the ladder would run
`last-7-days → last-24-hours`, printing the same heading twice. Sorting by bucket index makes the heading
sequence structurally correct; "active first" then applies inside its own bucket, which is what FR-011
says.

**Alternatives rejected.** *Keeping the SQL order and drawing headings on key change* — duplicates and
out-of-order headings. *Changing `TransferManager.list()`* — the companion's ordering also feeds the rail,
which has no buckets, and the fix belongs where the drawing happens.

**Provenance.** `local_transfers.py:41-47`; the rail's active-first contract (`static/web/media-handoff.js:38-49`).

## D5 — Headings are drawn by the existing render functions, in their existing class

**Decision.** The list keeps `h2.media-library__group` and gains `data-bucket`; the dialog takes a new
`h3.media-transfers__group` with the same numbers. No new component, no new sheet.

**Rationale.** `.media-library__group` is already the list's heading (`components.css:619`) and its numbers
are the ones a reader has been seeing. The dialog's `h2` is `Transfers`, so its bucket headings must be
`h3` — a heading level below the dialog's own title, as every other modal in the app does.

**Alternatives rejected.** *Reusing `.media-library__group` inside the dialog* — it is named for the list
and the dialog is a different surface; a shared class would have to be renamed for both, which is a
rename of a style that shipped. *A larger, sturdier divider treatment* — the request is about grouping,
not about a new visual weight.

**Provenance.** `components.css:619`, `:2751-2757`; `media_library.html`'s dialog markup.

## D6 — Verification through the browser, with `now` passed in as an argument

**Decision.** `fileKey(row, now)` and `transferKey(row, now)` take the present instant as an optional
second argument, defaulting to `Date.now()`. Every edge is asserted by calling the rule with an explicit
`now` through `page.evaluate`; the rendered lists are asserted with fixtures dated well inside each
bucket.

**Rationale.** Playwright's `page.clock` is available, but installing it also freezes the page's two
`setInterval` loops (`poll` 2s, `reconcile` 60s, `media-handoff.js:155`) and the 150ms dialog animations, so
each test would have to drive the clock to reach a settled page. An argument is cheaper, and it makes the
edge assertions exact instead of "close enough to midnight". Fixtures placed hours away from an edge keep
the rendering tests independent of the run's real date.

**Alternatives rejected.** *`page.clock.install()`* — see above. *Server-side rendering of the buckets* —
the Media Library is drawn in the browser from the loopback companion; there is no server page to render.
*Freezing time in production code via a settings value* — a test seam in shipped code, and the repo's
pattern for the 132 Python rule is an injected `today` argument, which this mirrors.

**Provenance.** `media-handoff.js:155`; `tests/e2e/test_media_library.py`'s routed-companion pattern;
`date_buckets.py`'s `today=None` argument.

## D7 — The rail's flyout draws no headings

**Decision.** When the dialog is opened from the transfer rail (`source === 'rail'`), bucket headings are
not drawn; when it is opened from the Media Library's clock control (`source === 'library'`), they are.

**Rationale.** The rail is a progress popover: it shows the active transfers, and a divider marking what
has arrived since it was last opened (`media-handoff.js:38-57`). Its fallback list, shown when nothing is
active, is the same dialog with no history framing. Headings there would add five labels to a view whose
question is "is it done yet".

**Alternatives rejected.** *Headings in both* — five headings over one or two rows in a popover.
*Two render paths for the same dialog* — already the case for the divider; adding one branch is smaller.

**Provenance.** `media-handoff.js:35-65`; the rail's `data-tip="Transfer progress"` in `base.html:131`.

## D8 — `bump: patch`

**Decision.** `VERSION` moves one patch level at delivery, with one `### Changed` changelog line.

**Rationale.** Neither surface is new: the list exists and regroups, the dialog exists and gains headings.
`VER-10` maps a new capability to `minor`; what ships here is a change to how two existing lists group
their rows, which is the level spec 132 took for the same class of change (`1.20.10 → 1.20.11`). The new
`R22`/`R23` requirements are the capability tree's bookkeeping of a behaviour change, not a new surface.

**Provenance.** `VER-10`; `CHANGELOG.md` 1.20.11; `specs/132-tatib-sidebar-date-buckets/spec.md`.

## Open unknowns

None. Every question above is decided from the code, the capability file or the owner's request.
