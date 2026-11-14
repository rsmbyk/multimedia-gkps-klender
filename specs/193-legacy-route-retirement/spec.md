# Feature Specification: Retired Addresses

**Slice**: `specs/193-legacy-route-retirement`
**Branch**: `feat/193-legacy-route-retirement`
**Created**: 2026-11-14
**Status**: Accepted (Gate 1, 2026-11-14)
**Input**: "redirect all the old obs docks to the new one. and the old overlays to a new transparent
page (we dont want leftover cleanup on the obs to display something weird while streaming). —
redirect everything under /home/, /songs/, /tatib/, /manage/ to / (root) — move everything from the
old version to a new archive route/urls. we will invalidate that on the next release after today.
after we confirm this release has no problem"

## User Scenarios & Testing

### US1 — A scene left over from the old OBS setup shows nothing embarrassing (P1)

**Why this priority**: Tonight the app stops carrying three docks and four overlay sources, and
somebody's scene file will still hold one. Opened live, an old address that still answers 200 paints
a page this release no longer maintains — a half-loaded old dock, or a caption left over from last
Sunday — and that painting is what the congregation sees. It is the only failure in this slice that
reaches the stream.

**Independent Test**: With the old addresses still in a scene, load each one: every dock lands on
the one dock, every overlay source lands on a page that paints only a corner note, and no old page renders.

**Acceptance scenarios**

1. **Given** a browser source pointing at `/obs/bible/dock` (or `/obs/songs/dock`, or
   `/obs/tatib/dock`), **When** the scene opens, **Then** the address answers 302 to `/obs/dock` and
   the source shows the one dock.
2. **Given** a browser source pointing at any old overlay source — `/obs/bible/source`,
   `/obs/songs/source`, `/obs/tatib/source`, `/obs/project/source` — **When** the scene opens,
   **Then** the address answers 302 to `/obs/blank`.
3. **Given** `/obs/blank` is open in a source, **When** it finishes loading, **Then** the only thing
   it has painted is one small note in the bottom-right corner naming the source as retired; the
   rest of the frame is the scene behind it.
4. **Given** the old overlay's settings page `/obs/project/settings`, **When** it is opened,
   **Then** it answers 302 to `/` like the rest of the retired surface — the release leaves no old
   address answering a page of its own.

### US2 — An old web address still finds the site (P1)

**Why this priority**: `/home/` was the home while maintenance was on and `/manage/` was the whole
back office, with years of bookmarks between them. The release closes both, and a bookmark that
404s reads as a broken site on the day a release is judged.

**Independent Test**: Request `/home/` and a handful of `/manage/…` addresses; each answers 302 to
`/`, and the reading addresses `/songs/` and `/tatib/` still answer 200 where they are.

**Acceptance scenarios**

1. **Given** a bookmark to `/home/`, **When** it is opened, **Then** it answers 302 to `/` and the
   home renders there.
2. **Given** a bookmark under `/manage/` — the root, a songs editor, a service editor — **When** it
   is opened, **Then** it answers 302 to `/`.
3. **Given** the reading app, **When** its own addresses `/songs/`, `/songs/<song>/`, `/tatib/` and
   `/tatib/<service>/` are opened, **Then** they answer as they do today; the retirement does not
   reach them.
4. **Given** an editor save whose return address is `/songs/` or `/tatib/`, **When** the save
   completes, **Then** the reader lands on the reading page, unchanged.

### US3 — The old version is reachable from one namespace, for one release (P2)

**Why this priority**: This release moves a year of addresses at once. The owner wants a namespace
that resolves an address written against the old version, and wants to withdraw it once this release
is known good. It is P2 because nothing in the app depends on it — it is a safety net for a person.

**Independent Test**: Request `/archive/` plus one old path under each retired prefix; each answers
302 to the live address that replaces it, and none of them renders a page of its own.

**Acceptance scenarios**

1. **Given** `/archive/`, **When** it is opened, **Then** it answers 302 to `/`.
2. **Given** `/archive/home/`, **When** it is opened, **Then** it answers 302 to `/`.
3. **Given** `/archive/manage/songs/12/`, **When** it is opened, **Then** it answers 302 to `/`, in
   one hop — not to `/manage/songs/12/` first.
4. **Given** `/archive/songs/`, **When** it is opened, **Then** it answers 302 to `/songs/`.
5. **Given** `/archive/obs/songs/source`, **When** it is opened, **Then** it answers 302 to
   `/obs/blank`, in one hop.
6. **Given** any `/archive/…` address, **When** it is opened, **Then** the answer is 302 and not
   301, so the next release can withdraw it without evicting a browser's cache.

### Edge Cases

- **When** an old OBS address is requested with a trailing slash (`/obs/bible/dock/`), **Then** it
  answers the same 302 as without one.
- **When** `/obs/dock`, `/obs/source/overlay` or `/projector` is requested, **Then** it answers as it
  does today — the retirement covers the old section addresses and nothing else.
- **When** a retired address carries a query string (`/home/?from=mail`), **Then** the redirect
  keeps it.
- **When** the note sits over a bright slide, **Then** the 20% line is effectively swallowed and only
  its shadow remains, which is the intended reading: on air it must not compete with the slide. The
  hover state restores it on any background.
- **When** `/archive/` names an address no live page answers (`/archive/nowhere/`), **Then** it
  answers 302 to `/nowhere/`, and that address answers 404 there as it would unarchived — the
  archive never answers 404 on the destination's behalf.
- **When** `MAINTENANCE_MODE` is on, **Then** `/home/` still answers 302 to `/` and `/` still serves
  the maintenance notice; the retirement holds whatever the maintenance switch says.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | `/home/` SHALL answer 302 to `/`, keeping any query string. | `new: routing` |
| FR-002 | Every address under `/manage/` SHALL answer 302 to `/`, keeping any query string. | `new: routing` |
| FR-003 | `/obs/bible/dock`, `/obs/songs/dock` and `/obs/tatib/dock` SHALL answer 302 to `/obs/dock`, with or without a trailing slash. | `new: routing` |
| FR-004 | `/obs/bible/source`, `/obs/songs/source`, `/obs/tatib/source` and `/obs/project/source` SHALL answer 302 to `/obs/blank`, with or without a trailing slash. | `new: routing` |
| FR-005 | `/obs/project/settings` SHALL answer 302 to `/`, with or without a trailing slash. | `new: routing` |
| FR-006 | `/obs/blank` SHALL answer 200 with a transparent document whose only painted element is one small note in the bottom-right corner, naming the page as a retired OBS source, and `Cache-Control: no-store`. | `new: routing` |
| FR-006a | The note SHALL mark the source without being read on air: at rest one line at 20% white that an operator recognises as a watermark, and the identifying instruction — where to point the source instead — only while the pointer is over it, where the line turns legible. | `new: routing` |
| FR-006b | `/obs/blank` SHALL carry no script, no image, and no text beyond the note. | `new: routing` |
| FR-007 | `/songs/`, `/songs/<song>/`, `/tatib/` and `/tatib/<service>/` SHALL keep the answers they give today. | `new: routing` |
| FR-008 | `/archive/` and every address under it SHALL answer 302 to the successor of the old address it names, in one hop. | `new: routing` |
| FR-009 | No retired route and no archive address SHALL answer 301 this release: every one answers 302, so no browser caches a move this release does not claim is final. | `new: routing` |
| FR-010 | The retirement SHALL be one greppable block per URLconf, so the next release removes it without reading the app. | `new: routing` |
| FR-011 | `/songs/books`, `/songs/books/<id>` and `/songs/songs/<id>` SHALL keep answering 301 and SHALL point at `/songs/`, `/songs/book/<id>/` and `/songs/<id>/` — never at a `/manage/` editor this release retires. | `new: routing` |

### Key Entities

None — the slice changes which addresses answer and where they send the request; it stores nothing
and reads no model.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | No address of the old OBS app renders a page | 7 of 7 old addresses answer 302: 3 docks to `/obs/dock`, 4 sources to `/obs/blank`, the settings page to `/` — and 0 of them render an old template |
| SC-002 | A leftover OBS source paints one line and nothing else | `/obs/blank` body carries 1 painted text node at rest (its reveal line is `display:none`), 0 `<script` and 0 `<img`; background transparent on both `html` and `body` |
| SC-003 | The reading pages are untouched | 4 of 4 — `/songs/`, `/songs/<song>/`, `/tatib/`, `/tatib/<service>/` — answer 200 |
| SC-004 | Every retired address answers in one hop | The `Location` of each retired address and of each legacy `/songs/books*` move resolves to a 200; 0 two-hop chains |
| SC-005 | The whole retirement can be revisited next release without a cache eviction | 0 of the retired and archived answers are 301; all are 302 |

## UI/UX

**Static preview at `specs/193-legacy-route-retirement/preview/index.html`** — `/obs/blank`'s exact
response body, `preview/blank.html`, in three frames: a checkerboard, a dark stage and a bright
slide. The dark and bright frames are the judgement the note has to survive — seen by an operator
who is looking for it, gone for a viewer who is not.

One visible surface is new: a transparent page carrying a single note. `/obs/blank`:

- **Layout / position**: nothing is laid out except the note, fixed 16px from the right and bottom
  edges; `margin:0; padding:0` on `html` and `body` so the browser's default 8px frame is not
  painted onto the scene.
- **Size / spacing**: note type 12px/1.4 at weight 500; on hover the plate takes 5px/9px padding and
  a 6px radius, 2px above the second line.
- **Colour / typography**: system-ui; `rgba(255,255,255,.2)` at rest with a
  `0 1px 2px rgba(0,0,0,.55)` shadow; on hover `rgba(255,255,255,.95)` on a
  `rgba(20,20,18,.82)` plate.
- **States**: rest — one line, `Old OBS source`, as a watermark: present on a mid or dark scene,
  swallowed by a white one. Hover — the plate, the line at full strength, and the instruction
  `Switch to /obs/source/overlay`; focus · active · disabled · error · loading — not applicable, the
  page has no control. Empty — the page has no empty state; the note is always there.
- **Motion**: none.
- **Responsive**: the note is fixed to the frame's corner at every size; nothing else responds.

Every other outcome of this slice is a redirect to an existing screen, which is that screen
unchanged.

## Assumptions

- **`/songs/` and `/tatib/` stay live.** The request named them alongside `/home/` and `/manage/`,
  but in the shipped app they are the hymn reader and the service reader — rail destinations in
  `base.html:104` and `:120`, and `static/web/editors.js:318-322` returns to them after an editor
  save. Read literally the request would remove two of the app's four sections, so it was put to
  the owner before the spec: keep them. Recorded in Clarifications.
- **`/obs/project/settings` goes to `/`.** The request named the docks and the overlays, not the old
  overlay's settings page. Two answers were offered and both were declined in favour of the request's
  own rule — everything old goes to the root — so the retired surface has exactly one destination
  family: the successor page, or `/`.
- **The site has no not-found screen, and this slice does not add one.** With `DEBUG = False` Django
  answers bare `Not Found` text; a proper page was drafted at gate 1 and withdrawn when
  `/obs/project/settings` was pointed at `/` instead. It is carded as its own demand rather than
  carried here.
- **The archive is a redirect table, not a copy of the old version.** The old code cannot run
  against the migrated database (0.7.0's views read columns its own migrations dropped, e.g.
  `Book.lang`), so "archive" can only mean *where the old address goes*, which is what the owner
  chose at the first gate.
- **Every answer in this slice is a 302, including the retired addresses.** The owner asked at
  gate 1 whether an old address could be used again later: on the server yes, in a browser that
  already saw a 301 no, because the browser stops asking. So this release claims nothing permanent —
  each old address stays a name the site may take back, and the next release, once this one is
  known good, decides per address between a 301 and reuse. A bare 302 is not heuristically cacheable,
  so no client needs evicting either way.
- **The next release's decision is a card, not a silent default.** Permanence is not implied by
  this release; whoever removes the archive records what each address became.
- **The note is a watermark, not a banner.** The owner asked for a page that identifies itself to
  the operator without being read by the congregation, then pinned the resting weight at 20%
  white — at which the line is a hint on a dark or mid scene and gone on a white slide. That is the
  trade the owner chose and the reason the identifying instruction lives one hover away; OBS's
  *Interact* gives a source a pointer. A readable plate at rest would be on air during every
  service.
- **The old code stays in the tree, unreachable.** `multimedia/obs/` and `multimedia/web/manage/`
  stop answering here and are deleted with the archive next release, so this release carries no
  large deletion that would have to be reverted.
- **`/songs/books*` keep their 301 and are re-pointed.** The first draft of this spec said they
  "already 301 to the reading addresses, and are not touched". They do not: they name
  `web-songs-books`, `web-songs-songs` and `web-songs-verses`, which are mounted under `/manage/`.
  Retiring `/manage/` would therefore turn each of them into a two-hop chain ending at `/` — an
  address that used to land on a song list would land on the home page. FR-011 re-points them at
  the reading pages; their status stays 301 because those moves were published as permanent before
  this slice, and re-labelling a move a browser has already cached changes nothing.
- **The archive's expiry is bookkeeping, not behaviour.** Removing it next release is a card and a
  line in `docs/spec/routing.md`, not a scheduled job.

## Clarifications

### Session 2026-11-14

- Q: Which of `/home/`, `/songs/`, `/tatib/`, `/manage/` should answer `/`? → A: only the dead and
  duplicate ones — `/home/` and `/manage/`; `/songs/` and `/tatib/` stay live.
- Q: What should the temporary archive be? → A: a redirect map only: `/archive/<old path>` answers
  the equivalent live page.
- Q: Where should the old OBS sources point? → A: a new blank page at `/obs/blank`.
- Q: Where should `/obs/project/settings`, which the request did not name, go? → A: `/` — the
  request's own rule for old addresses. A proper 404 page was drafted from the first answer and
  withdrawn with the second; the site still answers bare `Not Found` text, recorded as Assumption
  and carded separately.
- Q: Should `/obs/blank` paint nothing at all? → A: no — it carries a note that identifies it, so
  an operator notices a source is wrong, "but do not make it too noticeable to the viewer". The
  note is a corner watermark at rest with its instruction revealed on hover.
- Q: In which language, and how strong at rest? → A: English, and 20% white at rest — the words
  `Old OBS source`, with `Switch to /obs/source/overlay` on hover. Both were pinned by the owner;
  the copy of every other sentence on the page stays as it is.
- Q: If an old address is wanted again later, can it be reused after answering 301? → A: not
  reliably in a browser that cached the 301, so **every address in this slice answers 302** and the
  next release decides what becomes permanent. The seven OBS addresses and the archive were
  originally drafted as 301; the owner replaced that with one temporary answer for all of them.

No `[NEEDS CLARIFICATION]` markers were written; the input's three questions were answered on the
record above before the spec was drafted.
