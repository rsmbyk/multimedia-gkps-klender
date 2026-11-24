# Fold: passage search comboboxes

**Spec**: `specs/238-passage-search-pickers/spec.md`
**Branch**: `feat/238-passage-search-pickers`

## Capability record

`docs/spec/reading.md` gained `reading/R59` — "The passage entry's Book, Chapter and From verse
use the song search combobox" — with scenarios for Book search, Chapter/From verse search and
dismissal keeping the saved value. The slice id `238-passage-search-pickers` was prepended to
the file's `slices` header; `last folded` stays 2026-11-24.

## Release record

- `VERSION`: `1.36.23` → `1.36.24` (patch), declared at Plan and applied on the slice branch.
  Re-check against origin/develop immediately before merging.
- `CHANGELOG.md`: one `Changed` line under `Unreleased`, naming ITEM-253 and spec 238.
- Board: ITEM-253 to be created and closed pre-merge on the slice PR (repo practice: spec and
  board close on the same PR; no follow-up board PR).

## Source changes

- `multimedia/web/templates/reading/_entry_form.html` — three button triggers became search
  inputs with empty-state hints; To verse and the translation toggle untouched.
- `static/web/entries.js` — `wireSearchCombo` helper, cascade integration, aria reset in
  `closeMenus`, Escape value guard.
- `static/styles/design/components.css` — `.is-active` tint and disabled search-field tone.

## Tests and records

- `tests/e2e/test_passage_search_pickers.py` — 9 acceptance tests for US1–US4.
- `tests/e2e/test_entry_pickers.py` — stale trigger selectors migrated to the search fields.
- `specs/238-passage-search-pickers/` — spec, checklists, research, data model, contracts,
  quickstart, plan, tasks, analysis, converge, fold and live preview probes.

## Durable memory

A fact recording the new picker contract and the two test modules was filed to the vault under
Agent Memory's Anteroom for later curation.
