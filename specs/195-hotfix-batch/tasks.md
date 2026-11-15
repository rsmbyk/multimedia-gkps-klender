# Tasks — spec 195

Ordered by user story. `[P]` means order-independent, not concurrent; the run states the order it used.

## Setup

- [x] T01 [US4] Write the failing view test: `entry_song_verses` answers `verses` as `{id, number}` pairs (`multimedia/web/tests.py`)
- [x] T02 [US4] Make it pass: `views.py entry_song_verses` returns the pairs

## US4 — the verses contract (test first, then the client)

- [x] T03 [US4] [P] Write the failing form tests: `SongEntryForm` accepts verse IDs, refuses verse numbers with the model's refusal alongside; the verses widget renders `data-number` on every option (`multimedia/web/tests.py`)
- [x] T04 [US4] Make them pass: per-option `data-number` widget + form wiring (`multimedia/web/reading/entries.py`)
- [x] T05 [US4] `entries.js`: `renderVerses` renders value=`id`, label=`number`, `data-number`; `verseSummary` reads `data-number`; both renders agree
- [x] T06 [US4] Converge: parity already held via `.editor__verses > div` + `label` styling — no CSS change needed (computed `inline-flex / center / 7px / 14px` on a server-rendered row)

## US1 / US2 — sidebar badge, editor header

- [x] T07 [US1] [P] `components.css`: the badge joins the date-hide rule (same media guard, same reveal set); comment updated
- [x] T08 [US2] [P] `components.css`: port `.editor__head` + `.editor__copy-btn` from spec 167's preview; neutralize the title inside the head

## US3 — the generate dialog's date picker

- [x] T09 [US3] `date-picker.js`: bind on `shell:page` over the whole document; verify the deep-link path is untouched

## US5 / US6 — the overlay

- [x] T10 [US5] `obs-overlay.js`: `fitCaption` (shrink to ≤ 2 visual lines, floor 11px, measured per paint) + refit on resize
- [x] T11 [US6] `obs-overlay.js`: drop the per-service cache on the `update` message; a 10 s re-read while on air and visible
- [x] T12 [US6] `obs-dock.js`: the same `update` drop + 10 s re-read, rebuilding stops and repainting through `sync`

## Polish (delivery)

- [x] T13 Fold: `docs/spec/overlay.md` R2 modified (two-line cap), R1 extended (timed re-read); `docs/spec/reading.md` deltas for US1 (row actions reveal), US2 (R37 header numbers), US3 (R36 picker binds on the swap path), US4 (checklist speaks IDs, summary in numbers); `fold.md`
- [ ] T14 Delivery: `VERSION` 1.32.1, `CHANGELOG.md` Fixed × 6, board cards → In progress/Done per the seams, PR draft → ready (push on the owner's word only)
