# Convergence: Retired Addresses

**Spec**: `specs/194-legacy-route-retirement/spec.md`
**Passes**: 2 of 3

## Pass 1 — 2026-11-14

| Gap | Type | Requirement | Evidence |
--- | --- | --- | --- |
| R1 — retired addresses answer 302 to their successor | `missing` | A retired address SHALL answer exactly one 302 to its live successor (`/obs/dock`, `/obs/blank`, `/home/`, every `/manage/…` → `/`). | `docs/spec/routing.md` R1; `multimedia/retirement.py` table + `routes()`, `successor()`, `redirect()`; URLconf blocks in `multimedia/urls.py`, `multimedia/obs/urls.py`, `multimedia/web/urls.py`; tests `RetiredWebRouteTests::test_each_old_dock_answers_302_to_the_one_dock`, `test_every_manage_address_answers_302_to_the_root`, `test_each_old_source_answers_302_to_the_blank_page`, `test_the_old_settings_page_answers_302_to_the_root`. |
| R2 — old version reachable for one release via `/archive/…` | `missing` | `/archive/<old path>` answers 302 to the live successor in one hop, never a protocol-relative host. | `archive()` in `multimedia/retirement.py`; `re_path(r'^archive(?:/(?P<rest>.*))?$', retirement.archive, name='web-archive')` in `multimedia/urls.py`; test `test_the_archive_answers_the_successor_in_one_hop`. |
| R3 — `/obs/blank` is a live surface with a corner watermark note | `missing` | `/obs/blank` returns 200 with `Cache-Control: no-store`, carrying only the text `Old OBS source` at 20% white plus a soft shadow; hover reveals `Switch to /obs/source/overlay`. No script/image/stylesheet link. | `multimedia/web/templates/reading/obs_blank.html` (identical to `preview/blank.html`); inline `<style>` with `.retired` class; view `obs_blank(request)` in `multimedia/web/reading/views.py`; test `test_the_blank_page_is_transparent_and_uncached`, E2E `test_the_note_is_a_watermark_until_hovered`. |

All three were written up as **added** capability in `docs/spec/routing.md` (R1–R3) during T028 fold.

## Pass 2 — 2026-11-14

**Outcome**: Converged — nothing remains.

## Accepted gaps
None. The full checklist `checklists/requirements.md` was ticked 20/20 (CHK001–CHK020). All FR-001 through FR-011 traceable via `grep -rn 'spec 194'`; coverage 100%, markers 0, findings 0 CRITICAL / 2 HIGH / 1 MEDIUM / 1 LOW.

## Cap reached
**Decision**: Accept — close out this slice.
**Recorded on**: 2026-11-14
