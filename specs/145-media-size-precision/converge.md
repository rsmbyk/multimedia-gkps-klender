# Convergence: a media size reads in the unit that still shows its number

**Spec**: `specs/145-media-size-precision/spec.md`
**Passes**: 2 of 3

## Pass 1 — 2026-10-28

| Gap | Type | Requirement | Evidence |
| --- | --- | --- | --- |
| `media-handoff.js` kept its formatter as a one-line delegation instead of losing it, and nothing calls it. | `contradicts` | US2/AC2 | `grep -n '\bfmt\b' static/web/media-handoff.js` returned line 19 after Implement |
| The `200 MB` and `GB` labels were reachable only through the `node` one-liner in `quickstart.md`, so the traceability row for FR-001 claimed more than the suite ran. | `partial` | FR-001 | the test asserted uploads up to 1,000,000 B; `200,000,000` and `1,000,000,000` were not asserted anywhere the suite runs |

**Outcome**: 2 findings, both fixed in this pass — the dead formatter is deleted, and the test now asserts
`window.gkpsFormatSize(200000000) === '200 MB'`, `(1000000000) === '1 GB'` and `(0) === '0 B'` against the
shipped function on the shipped page.

## Pass 2 — 2026-10-28

Every row re-checked by the method it declared:

| Requirement | Method | Result |
| --- | --- | --- |
| FR-001 | `test` | `test_media_size_reads_in_the_smallest_unit_that_shows_a_number` — `12.3 KB`, `512 B`, `1 MB`, `200 MB`, `1 GB`, `0 B` |
| FR-002 | `test` | same test — `1 MB` for 999,999 B (promoted), `2 KB` for 2,048 B (no trailing `.0`) |
| FR-003 | `test` | card and library drawn by the same function; `test_media_library_row_and_total_use_the_chosen_label` reads the rows and the Total |
| FR-004 | `test` | `Image · 512 B` |
| SC-003 | `inspection` — checked by inspection | live preview at `http://127.0.0.1:8821/tatib/149/`: `12.3 KB` on the card and in the library row |
| SC-004 | `manual` — checked by hand | computed style read on the live page: `12px/18px`, weight 400, `rgb(100, 99, 87)`, box `87.22px` for `Image · 12.3 KB` |

**Outcome**: Converged — nothing remains.

## Accepted gaps

<!-- none -->
