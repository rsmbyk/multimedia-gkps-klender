# Feature Specification: No empty groups after the last row is deleted

**Slice**: `specs/252-empty-date-group`
**Branch**: `fix/252-empty-date-group`
**Created**: 2026-11-28
**Status**: Accepted — gate 1, 2026-11-28 (permission to plan only)
**Capability read before writing**: `docs/spec/reading.md` (the sidebar/date-bucket requirements; no
requirement yet covers an emptied group, so this slice adds one rather than modifying an existing `R<n>`)
**Input**: "when you delete the last item from a date group, that date group still visible with no children. i encountered it in services sidebar, but you should check for every occurrence of date groups."

## User Scenarios & Testing

### US1 — A service date bucket leaves with its last service (P1)

**Why this priority**: This is the reported defect. Deleting the last service in `Last 30 days` removes
the row but leaves `<section class="group" data-bucket="last-30-days">` and its heading painted until
the next full navigation. A heading with no children promises content that is not there.

**Independent Test**: On the live preview, delete both services of one bucket through the real editor
dialog. The bucket's section count goes 1 → 0 on screen, the sibling bucket stays at 1, and a reload
agrees. The unmodified control server stays at 1 on screen.

**Acceptance scenarios**

1. **Given** a service sidebar with two services in `Last 30 days` and one in `Earlier this year`,
   **When** both recent services are deleted through their row delete buttons,
   **Then** the `last-30-days` section and its heading are absent on screen and the older section remains.
2. **Given** the same deletions, **When** the page is reloaded,
   **Then** the server renders no empty `last-30-days` section either.
3. **Given** a filter that leaves only one row of a bucket visible,
   **When** that visible row is deleted,
   **Then** the bucket is hidden while the filter is on and returns when the filter is cleared.

### US2 — The same rule holds for every grouped, deletable surface (P2)

**Why this priority**: The owner asked for an audit of every occurrence, not a sidebar-only patch. The
unheaded Kidung groups carry separator styling, so a leftover section also draws a stray rule; template
mode emits an empty group on a fresh render even after every template is gone.

**Independent Test**: Delete the last ordinary songbook on the live preview — sections go 2 → 1 while
the control stays at 2. Delete both templates — sections go 1 → 0 on screen and after reload; the
control stays at 1 in both states.

**Acceptance scenarios**

1. **Given** one hymn songbook group and one ordinary songbook group,
   **When** the last ordinary songbook is deleted,
   **Then** exactly one `section.group` remains and no separator is left behind.
2. **Given** two templates in template mode,
   **When** both are deleted,
   **Then** no `Templates` group is rendered on screen or on reload.
3. **Given** a grouped surface with no delete path (Bible testaments, OBS dock, Media Library age buckets,
   transfer history, search results, projector controls, entry pickers),
   **When** the surface renders, **Then** it keeps its existing rule of emitting only groups with rows.

## Edge Cases

- Deleting a row that is on the reading stage triggers a full shell refresh instead of in-place removal;
  the server render path must drop empty groups on its own.
- A group whose remaining rows are all filtered out is hidden, not removed, so clearing the filter restores it.
- A deleted row outside any `section.group` (a song in the song list, a service entry) keeps its existing
  behaviour untouched.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | The client delete path SHALL retire the owning `section.group` when its last `.book` row is removed. | `reading/R64` |
| FR-002 | With a filter active, the client delete path SHALL hide a group whose surviving rows are all hidden and SHALL restore it when the filter is cleared. | `reading/R64` |
| FR-003 | The template-mode server render SHALL emit a `Templates` group only when at least one template exists. | `reading/R64` |
| FR-004 | No other grouped surface SHALL change: the existing renderers already skip empty groups and have no in-place delete of grouped rows. | `reading/R64` |

### Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | Four E2E pins go red on the unfixed base and green on the slice | `tests.e2e.test_empty_date_group` |
| SC-002 | Neighbouring delete and sort suites keep their prior state | `tests.e2e.test_deleted_stage` green; the one sort error is byte-identical on unmodified base |
| SC-003 | The empty-group rule covers every grouped surface | file/line survey in `research.md` |

## UI/UX

**Preview shape**: live, served from the real worktree code path.
`live preview at http://127.0.0.1:8776/tatib/` (and `/tatib/?mode=template`, `/songs/`);
control at `http://127.0.0.1:8777/`. Both servers were up during measurement; the probe is
`specs/252-empty-date-group/preview/probe.py`, results in `probe-results.jsonl` and
`probe-results-base.jsonl`. Every state below is reachable by clicking the real row delete button and
typing in the real sidebar filter.

| State (1440×900, dark, 1×) | Control = unmodified `1c86096f` | Preview = slice worktree |
| --- | --- | --- |
| Date bucket sections before → after last delete | 2 → **2** (`Last 30 days` still painted) | 2 → **1**; `last-30-days` = 1 → **0**, `earlier-this-year` = 1 |
| Date bucket after reload | `last-30-days` = **0** (server already drops it) | `last-30-days` = **0** |
| Template sections before → after last delete | 1 → **1** (empty `Templates` heading) | 1 → **0** |
| Template sections after reload | **1** | **0** |
| Songbook sections before → after last delete | 2 → **2** | 2 → **1** |
| Filtered bucket: filter on → last visible delete → cleared | visible → **visible** → visible | visible → **hidden** → visible |
| Visible book rows in the filtered bucket | 1 → **0** → 2 | 1 → **0** → 2 |

The values are DOM section counts, heading text and `is-hidden` class state — not adjectives. No spacing,
colour or typography changes; the only visual difference is the disappearance (or filter-hiding) of an
empty group.

## Assumptions

1. The `<section class="group">` wrapper is the group on all grouped sidebar surfaces; the song list and
   service entries are flat lists with no date heading, so they are out of scope. This default was taken
   because no owner answer was needed to scope a reported sidebar defect.
2. The report concerns the reading sidebar; the live probes above were local, not production. Production
   confirmation is a manual task after deployment, not a gate-1 claim.
3. The fix is a `patch` bump: a user-visible defect is repaired, with no endpoint, schema or route change.
4. **Chronology of this re-run**: an earlier attempt implemented and committed before the gates. That
   commit was reset to `1c86096f` before this pack was written; the preview edit is present in the
   worktree uncommitted, which the live-preview-first rule allows. No commit precedes Fold in this run.
5. Card `ITEM-269` was authored by the agent from the owner's report and sits in `Speccing`; only the
   owner promotes it to `Ready` at gate 1.

## Clarifications

None. Specify produced no `[NEEDS CLARIFICATION]` markers: the owner's report named the surface, the
"every occurrence" scope was settled by inspecting the codebase, and the preview settled the observable.
