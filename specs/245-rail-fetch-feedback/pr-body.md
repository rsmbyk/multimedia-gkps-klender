**Why:** the Search and Media Library rail tiles had no in-page pending feedback — Media Library was a plain document link with a dead-looking wait, and Search's fetch showed neither a locked tile nor a stage placeholder.

**What changed:** both rail tiles now fetch through the reading shell's navigation. The clicked tile locks (SVG opacity 0.45, `aria-disabled`), a 3px bar runs at the reading stage's top with `aria-busy`, and the stage carries a placeholder built from the destination's own markup — Search results, Search home (including a skeleton inside the input), or Media Library (skeleton filters, sorter, grouped file rows and action bars). The previous search shell is hidden while the skeleton is up. Direct Media Library loads get a loading count and a spinner above the text until the companion and references settle. The Media Library companion's local allow-list accepts port 8787 for slice-server review via a checked-in Compose override; repo Compose config is untouched.

**Capability:** new `reading/R62`, extending `reading/R61`. **Bump:** patch. **Card:** ITEM-260.

## Test plan

- `tests.e2e.test_navigation_pending` — 24 tests green (red-first for each new rule).
- Capability batch A (nav freshness, rail marks, targeted reading, home search, filter pill, age buckets) — 45 green.
- Capability batch B (`test_media_library`, `test_reading`) — 141 tests; 3 reds reproduce on unmodified develop (ITEM-137, ITEM-156, ITEM-262) and 2 branch-owned focus reds were fixed.
- `manage.py test multimedia` — 569 tests, 9 failures; the identical 9 occur on unmodified `fa452197` (ITEM-217's eight plus ITEM-261).
- Full browser matrix (962 E2E methods) was not run; no CI workflow exists in this repo, so these are manual lanes.
- Preview probe and chat-frame verifier pass; live server at 127.0.0.1:8787 used for before/after measurements.

Refs #626
