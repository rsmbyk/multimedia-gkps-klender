# Research — spec 195

Every decision carries provenance. Nothing here was decided from recollection; each reads the code or measures the page.

## D001 — The lyric fit is a measured JS loop, not CSS

**Decision**: shrink the caption's `font-size` in obs-overlay.js until the block paints ≤ 2 visual lines, floor 11px.
**Rationale**: no CSS primitive counts *visual* lines after wrapping (`text-wrap: balance` balances breaks; it cannot cap rows). The projector's one-screen text (spec 029) already established the measure-and-fit pattern.
**Alternatives**: a smaller fixed `cqw` size (fails the "already fits paints as accepted" requirement); CSS `min()` against line count (does not exist).
**Provenance**: `obs-overlay.css:43-65` (caption block), `docs/spec/overlay.md` R2 scenarios, spec 029's fit pattern; preview fixture measured (2.00 lines at 13.2px after fit; unchanged at 17.9px).

## D002 — The re-read discovery is a timed re-read of the projector islands

**Decision**: overlay and dock poll `/projector?service=<id>` (`no-store`) every 10 s while a service is on air and the page is visible; a changed payload invalidates the per-service cache and repaints only when the painted model changed. The channel's `update` message also drops the cache for same-browser surfaces.
**Rationale**: OBS runs its own browser, separate from the editing browser (owner, 2026-11-15) — no BroadcastChannel or storage event can reach it. The islands are the painted truth, so polling them cannot miss a write path (entry edits, lyric edits, reorders, media renames all show up).
**Alternatives**: a `revision` field + tiny endpoint (needs `updated_at` columns on three models and a bump in every write path — a missed bump is exactly the bug again); server push (needs new transport; the app is deliberately server-free for display state).
**Provenance**: `obs-overlay.js:263-290` (per-service cache), `obs-dock.js:69-105` (same cache), `display.js:422-431` (`editor:saved` → `update` message; projector already re-reads at `projector.js:1795`).

## D003 — The verses contract aligns client-side

**Decision**: `entry_song_verses` returns `{id, number}` pairs; `renderVerses` submits `id` values with `number` labels and `data-number` attributes; `verseSummary` reads `data-number`. The server form keeps verse-ID choices.
**Rationale**: spec 189/migration 0014 made IDs the storage; the checklist was the one client still speaking numbers. Re-accepting numbers server-side would silently accept a stale entry's numbers and re-introduce the migration's dropped-value class of bug.
**Alternatives**: server accepts both (ambiguous contract); keep numbers and convert on save (second mapping to maintain).
**Provenance**: `entries.py:124-175`, `entries.js:711-796`, `views.py:1074-1079`, `migrations/0014_verse_refs_to_ids.py`.

## D004 — US2's CSS is the accepted preview block, ported verbatim

**Decision**: `.editor__head` (flex space-between, gap 16px, margin 0 0 16px, padding 0 0 14px, hairline rule) and `.editor__copy-btn` (34px tall, 13px pad, 1px divider, radius 8, 13px/560, hover border+bg, focus ring) move from `specs/167.../preview/preview.css` into `components.css`; the title inside the head is neutralized (`margin/padding/border: 0`).
**Rationale**: gate 1 accepted those numbers; the product sheet simply never received them. The base `.editor__title` (margin 0 0 16px, padding 0 34px 14px 0, border-bottom — spec 006) keeps its box through the head for every modal, since the head now carries it.
**Alternatives**: restyle the button alone (leaves it under the title — the reported defect).
**Provenance**: `components.css:679-683`, `specs/167-tata-ibadah-templates/preview/preview.css:139-149`, spec 167 UI/UX line "137.8×34".

## D005 — The badge hide joins the date-hide rule

**Decision**: extend the `@media (hover: hover)` rule at `components.css:1425-1428` with `.book__today`, same reveal set (`li[data-editor-kind]:hover` + `:focus-within`).
**Rationale**: the badge and the date share the trailing edge and the same obscuring problem; spec 190 already accepted the date hide, so the badge inherits the exact rule rather than a new interaction.
**Alternatives**: hide on the anchor's hover only (misses the keyboard reveal); reflow the row (moves the accepted badge geometry).
**Provenance**: `components.css:1420-1446`, spec 190 FR-004.

## D006 — date-picker binds on `shell:page`, document-wide

**Decision**: `date-picker.js` adds `document.addEventListener('shell:page', () => initialize(document))`.
**Rationale**: the reading shell swaps the stage in place and announces it on `shell:page` (`reading.js:1818`); the generate dialog arrives on that seam, so the picker must bind then, over the whole document (the dialog is not inside `#editorContent`). The per-picker ready guard keeps rescans cheap and idempotent.
**Alternatives**: dispatch `date-picker:initialize` from reading.js (a second seam for the same fact); scope the existing event to `document` (equivalent outcome, but the event is editors.js's fragment seam — leave it scoped).
**Provenance**: `date-picker.js:58-71, 283-289`, `reading.js:1526, 1818`, `display.js:420` (the same seam's other consumer).
