# Research: every grouped surface, checked for empty-group survival

**Question**: after deleting the last row of a group, can a heading or section remain with no children?
**Exits at**: zero unknowns.

## Survey

| Surface | Group markup | Empty rows rendered? | In-place delete? | Verdict |
| --- | --- | --- | --- | --- |
| Tata Ibadah service date buckets | `multimedia/web/templates/reading/_tatib_panel.html:2` (`section.group[data-bucket]`) | No — `multimedia/web/reading/date_buckets.py:57` returns only buckets holding rows | Yes — `static/web/editors.js:284` | **Affected client-side** |
| Template panel | same template, no `data-bucket` | **Yes** — `_tatib_groups()` in `multimedia/web/reading/views.py:1274` always appended `Templates` | Yes — same `applyDelete()` | **Affected on both paths** |
| Songbook groups (hymn / ordinary) | `multimedia/web/templates/reading/_songbooks_panel.html:4`; separator via `.group + .group` | No — `_songbook_groups()` skips empty lists (`views.py:1228-1232`) | Yes — same `applyDelete()` | **Affected client-side** |
| Bible testament groups | `multimedia/web/templates/reading/_books_panel.html:2` | Fixed old/new groups from the book index (`views.py:1163-1197`) | No delete button in the template | Not affected |
| OBS dock service buckets | `multimedia/web/templates/reading/obs_dock.html:86` | No — `views.py:1907-1913` uses `date_buckets.groups()` | No row delete in `static/web/obs-dock.js` (the `delete` hits are cache keys at 541 and 2225) | Not affected |
| Media Library age buckets | `static/web/media-library.js:106-116` | No — `window.gkpsAgeBuckets.group()` filters empties (`static/web/age-buckets.js:77-90`) | No in-place delete; list rebuilt with `replaceChildren()` | Not affected |
| Transfer history buckets | `static/web/media-handoff.js:64,82` | No — same `gkpsAgeBuckets.group()` | No in-place delete; `replaceChildren()` | Not affected |
| Search result groups | `multimedia/web/templates/reading/search.html:12` | No — `_search_groups()` skips empty kinds (`views.py:2179-2200`) | No delete | Not affected |
| Projector controls groups | `multimedia/web/templates/reading/projector_controls.html:54-112` | Static markup | No delete | Not affected |
| Service entry add/delete rows | `static/web/entries.js:90-113` | Not date-grouped; flat list | Yes, but removes only row and add marker | Not affected |

## Decisions

### D001 — Fix the shared client path, not each template
**Rationale**: all three affected surfaces go through `applyDelete()`; retiring the row's own
`section.group` there covers dated buckets, the template group and the unheaded songbook groups with one
change. **Alternatives**: a per-template delete callback — more sites to keep in sync for no
behavioural gain. **Provenance**: codebase inspection of the delete call sites (see survey).

### D002 — Hide, do not remove, a group whose surviving rows are filtered out
**Rationale**: `applyFilter()` owns visibility (`static/web/reading.js:949-963`); removing a section would
lose rows that should return when the filter is cleared. `is-hidden` is the filter's own vocabulary.
**Alternatives**: remove and rebuild the section on filter clear — duplicates the renderer in script.
**Provenance**: live preview measurement: control stays visible after the last visible delete while the
slice hides, then restores on filter clear (`probe-results*.jsonl`).

### D003 — Server fix only where a fresh render could still be empty
**Rationale**: `date_buckets.groups()` and `_songbook_groups()` already skip empty groups; only
`_tatib_groups()` does not. **Alternatives**: add empty-group guards to all renderers — changes code
that already behaves correctly. **Provenance**: survey rows for service buckets, songbooks and templates;
confirmed by control-preview after-reload counts (template = 1, bucket = 0).

### D004 — `bump: patch`
**Rationale**: a user-visible defect is repaired; no interface, schema or route changes. **Alternatives**:
`none` would hide a user-visible repair from the changelog; `minor` overstates it. **Provenance**:
owner report (defect) plus survey (no new surface added).

## Unknowns

None. The owner's "every occurrence" was resolved by inspecting all ten grouped surfaces and by the
live control/preview comparison; no question needed the question tool.
