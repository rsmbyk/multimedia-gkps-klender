# Research: Retired Addresses

**Spec**: `specs/194-legacy-route-retirement/spec.md` (Accepted, Gate 1 2026-11-14)
**Phase 0** · **Written**: 2026-11-14
**Unknowns remaining**: 0

## D001 — One retirement table, read by three URLconfs and the archive

- **Decision**: Every retired address lives in one tuple in `multimedia/retirement.py`,
  `(old path without its leading or trailing slash, successor)`. `multimedia/obs/urls.py`,
  `multimedia/web/urls.py` and the archive each read it, and each carries one marked block that
  says what it builds from it.
- **Rationale**: The archive has to answer the same mapping the direct routes answer; two copies
  drift, and a drifted archive is a place a reader lands somewhere the direct address would not.
  One table also makes the next release's removal mechanical: delete the module, three reference
  lines and `/archive/` (FR-010). It serves FR-010's purpose — the next release removes it without
  reading the app — better than three independent tables would, and each consumer keeps a visible
  `spec 194` block so a grep still finds every place.
- **Alternatives considered**: a block per URLconf, each listing its own paths — rejected: three
  copies of one mapping. A redirect app (`django.contrib.redirects`) — rejected: a database table
  for nine static addresses, a migration, and an admin surface, none of which this slice wants.
- **Provenance**: research

## D002 — Every answer is 302

- **Decision**: All retired addresses, and every `/archive/` address, answer 302. `permanent=False`
  is written explicitly on every `RedirectView`, with a comment naming the reason.
- **Rationale**: The owner asked at gate 1 whether a retired address could be used again later.
  Server-side yes; in a browser that already cached a 301, no — it stops asking. So this release
  claims nothing final and the next release decides per address (Clarifications, 2026-11-14).
  A bare 302 is not heuristically cacheable (RFC 9110 §15.1 lists 301 and 308 among the
  heuristically cacheable codes; 302 is not), so no client needs evicting either way.
- **Alternatives considered**: 301 for the seven OBS addresses — the first draft; withdrawn by the
  owner. 301 with `Cache-Control: max-age=0` to force revalidation — rejected: a 301 whose
  permanence the response denies is a contradiction, and revalidation for redirects is not
  uniformly honoured.
- **Provenance**: `owner decision` (gate 1, 2026-11-14) — the question was asked because 301 and
  302 differ only in what other people's caches are allowed to assume.

## D003 — Both slash forms are registered, so every address answers in one hop

- **Decision**: Every retired path is registered twice — `/obs/bible/dock` and `/obs/bible/dock/`
  — and `/manage` is matched by `re_path(r'^manage(?:/.*)?$')` so it matches with or without the
  slash. `/home` and `/home/` are both registered. `/archive` and `/archive/` likewise.
- **Rationale**: `APPEND_SLASH` is on (`CommonMiddleware`, `multimedia/settings.py:70`) and the
  default is `True`. Without the second registration, `/obs/bible/dock/` would answer
  `301 → /obs/bible/dock → 302 → /obs/dock`: two hops, and a 301 doing it — exactly what FR-009
  and SC-004 forbid, and the 301 would be the only one left in the slice.
- **Alternatives considered**: `APPEND_SLASH = False` — rejected: it is a global setting serving
  the whole app, changed to protect nine addresses. A middleware that rewrites trailing slashes —
  rejected: the same global reach, in more code.
- **Provenance**: research

## D004 — `/manage/` retires by prefix, at the URLconf, before any view

- **Decision**: `path('manage/', include('multimedia.web.manage.urls'))` is replaced by one
  `re_path` naming `/` as the destination. The `multimedia/web/manage/` package and its URLconfs
  stay in the tree, unreachable.
- **Rationale**: FR-002 covers *every* address under `/manage/`, and the include's own surface is
  not enumerable from the URLconf a reviewer reads — the prefix rule is the only statement that
  covers a bookmarked `/manage/songs/12/` without listing what the app once served. It also removes
  the whole back office in one line rather than route by route.
- **Alternatives considered**: keep the include and 302 each of its routes — rejected: nine
  redirects where one prefix does, and a route added to that package would silently stay live.
- **Provenance**: research

## D005 — `/obs/blank` belongs to the live OBS surface, not to the retirement

- **Decision**: `/obs/blank` is registered in `multimedia/urls.py` beside `/obs/dock` and
  `/obs/source/overlay`, renders `multimedia/web/templates/reading/obs_blank.html`, and sets
  `Cache-Control: no-store`. Its markup and stylesheet are inline in that template — no
  `{% static %}`, no shared stylesheet, no font, no image.
- **Rationale**: The retirement is temporary; `/obs/blank` is not. It is where a scene that still
  holds an old source lands, and it has to keep answering after `multimedia/obs/` and `/archive/`
  are deleted next release. Placing it in the obs URLconf would delete it with the retirement.
  Inline markup keeps the response one request with nothing to fail: a browser source that cannot
  load a stylesheet still paints the note, and the note is the whole page.
- **Alternatives considered**: a template under `multimedia/obs/templates/` — rejected: deleted
  with the app next release. A static HTML file under `static/` — rejected: WhiteNoise would serve
  it without the header FR-006 requires, and it would not be a view the tests can name.
- **Provenance**: research

## D006 — The archive strips its prefix, then answers from the table

- **Decision**: `successor(path)` returns the table's destination for a retired address — by
  prefix first (`/manage`), then by exact match — and otherwise the path it was given. The view
  strips `/archive`, calls `successor`, keeps the query string, and answers `HttpResponseRedirect`
  (302). `/archive/` → `/`; `/archive/nowhere/` → `/nowhere/`; `/archive/manage/songs/12/` → `/`.
- **Rationale**: One hop for every address, including the unknown ones, because the destination is
  computed rather than followed. The fallback is what makes `/archive/` a namespace rather than a
  list: anything that is not retired is simply where it always was, so a `/songs/<song>/` link from
  an old page still works. The spec's edge case (`/archive/nowhere/` → `/nowhere/`, which then
  404s) falls out of the same rule instead of needing its own branch.
- **Alternatives considered**: `include()`-ing the live URLconfs under `/archive/` — rejected:
  that renders pages, which US3 forbids, and would answer 200 where the spec says 302. A dict of
  full paths only — rejected: `/archive/songs/117/` would 404 in the archive rather than reach the
  live song.
- **Provenance**: research

## D007 — The three legacy `/songs/books*` 301s are re-pointed (spec correction)

- **Decision**: `/songs/books`, `/songs/books/<id>` and `/songs/songs/<id>` keep answering 301, and
  their destinations change from the `/manage/` editors to the reading pages that carry the same
  content: `/songs/`, `/songs/book/<id>/`, `/songs/<song>/`. The same three rules live in
  `retirement.successor()`, so `/archive/songs/books` lands on `/songs/` rather than chaining
  through the 301 it would otherwise name.
- **Rationale**: The spec's Assumption said these "already 301 to the reading addresses, and are
  not touched". They do not: they name `web-songs-books`, `web-songs-songs` and `web-songs-verses`,
  which are mounted under `/manage/` (`multimedia/web/songs/urls.py:8-10`). Retiring `/manage/`
  therefore turns each of them into a two-hop chain ending at `/` — an address that used to land
  on a song list would land on the home page. Re-pointing removes the chain and keeps the address
  useful. Their status code stays 301: those moves were already published as permanent, and
  re-labelling a move already cached changes nothing.
- **Alternatives considered**: leave them chained to `/` — rejected: the addresses were published
  as "this list moved", not "this list is gone". Answer 302 like everything else — rejected: these
  redirects predate the slice and are not part of the retirement's temporary namespace. Leave the
  archive to chain through them — rejected: `/archive/songs/books` would answer 302 to an address
  that then 301s, which is the two-hop chain SC-004 exists to prevent, and the archive is exactly
  where an old `/songs/books` link would arrive.
- **Provenance**: research — a spec Assumption corrected at Plan; shown at Gate 2 as FR-011.

## D008 — Tests: one Django module for the table, one Playwright module for the browser

- **Decision**: The address table, the one-hop rule, the blank page's body and headers, and the
  archive all land in `multimedia/web/tests.py`, replacing `LegacyObsRouteCompatibilityTests`. The
  browser-visible half — a legacy source landing on the blank page, the note's resting colour and
  its hover state — lands in `tests/e2e/test_retired_routes.py` (`StaticLiveServerTestCase`,
  Playwright, skipping cleanly when Playwright is absent).
- **Rationale**: A redirect is state, not paint: Django's client sees the status and the
  `Location`, and the test runs in a second. The note is paint: its 20% white and its
  `display:none` second line are computed styles, and a screenshot proves nothing a test can
  assert. Splitting at that line keeps the E2E module to what only a browser can show.
- **Alternatives considered**: E2E for every address — rejected: twelve browser starts to assert
  status codes the test client already asserts. Unit-only — rejected: the note's hover state is
  FR-006a, and no test client can see it.
- **Provenance**: research

## D009 — `bump: minor`

- **Decision**: `minor` — 1.30.0 → 1.31.0. The card carries `bump: minor` and the release today
  promotes that number rather than setting its own.
- **Rationale**: The slice adds a user-visible capability (`/obs/blank`, `/archive/`, a documented
  retirement) and removes addresses. The repo's own record classifies a route removal as `minor`:
  `## [1.20.0]` carries `### Removed` for `/obs/service/<id>/`, `/lookup/` and `/detour/`, and the
  unreleased block carries the same for `/offline/…`. VER-10 reads a breaking change as `major`;
  this slice follows the repo's precedent instead, and the divergence is recorded here so Gate 2
  sees it rather than finding it in a changelog afterwards. The owner's release today is 1.31.0.
- **Alternatives considered**: `major` (2.0.0) on VER-10's literal reading — rejected: it would
  claim an API break for nine addresses that answered pages nobody could keep using (the old OBS
  app's code cannot run on the migrated database, D010 of the spec's assumptions), and it would
  disagree with the number the owner is releasing. `patch` — rejected: a new route and a new
  namespace are not a fix.
- **Provenance**: research + `owner decision` (the release number)

## D010 — The verification split

- **Decision**: `20 test · 3 inspection · 2 manual`.
- **Rationale**: Every FR and SC names a test except FR-010 (a reviewer reads the marked blocks),
  the note's legibility over a bright slide and a dark stage (two frames of the static preview,
  read by eye), and the OBS scene itself (a person loads the old source in OBS and looks at the
  stream, which no runner can do).
- **Alternatives considered**: declaring the OBS scene `inspection` — rejected: opening OBS and
  watching the browser source is an act with steps, not a look at a file.
- **Provenance**: research

## Open

None. Every question Phase 0 raised was answered by the repository; the one that was not — the
status code — was put to the owner at Gate 1 and is recorded in the spec's Clarifications.
