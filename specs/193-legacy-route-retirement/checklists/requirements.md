# Routing Checklist: Retired Addresses

**Spec**: `specs/193-legacy-route-retirement/spec.md` · **Created**: 2026-11-14 · **Depth**: Standard

- [x] CHK001 Is every retired address named by its exact path, or does a prefix (`/manage/`) leave the
  reader to guess its members? [Clarity, Spec §Requirements FR-002]
- [x] CHK002 Is it stated that every address answers 302 and none 301, together with why the
  release claims nothing permanent? [Measurability, Spec §Requirements FR-009]
- [x] CHK003 Is the trailing-slash case required for every OBS address, or only stated as an edge
  case for three of them? [Coverage, Spec §Edge Cases]
- [x] CHK004 Is "in one hop" defined well enough to be measured — does it name the destination that
  counts as a single hop? [Clarity, Spec §Success Criteria SC-004]
- [x] CHK005 Is the archive's expiry expressed somewhere a future agent will look, or only in the
  card's notes? [Completeness, Gap]
- [x] CHK006 Does any requirement contradict `/songs/` and `/tatib/` being retired, given the input
  named them? [Consistency, Spec §Assumptions]
- [x] CHK007 Is `/obs/blank` specified by what it must paint *and* by what it must not contain, with
  each prohibition observable in a response body? [Measurability, Spec §UI/UX]
- [x] CHK008 Is it stated what happens to a retired address under `MAINTENANCE_MODE`, where `/`
  answers 503 rather than 200? [Coverage, Spec §Edge Cases]
- [x] CHK009 Is the query-string rule stated for every redirect class, or only for `/home/`?
  [Consistency, Spec §Requirements FR-001–FR-008]
- [x] CHK010 Is "one greppable block per URLconf" measurable — does it name what a reviewer looks
  for? [Ambiguity, Spec §Requirements FR-010]
- [x] CHK011 Does the spec say what the archive does with an address nothing answers, rather than
  leaving that to the plan? [Completeness, Spec §Edge Cases]
- [x] CHK012 Is the assumption that the old code cannot be archived as running code sourced, or
  asserted from memory? [Traceability, Spec §Assumptions]
- [x] CHK013 Are object-level scenarios enough for US1, or does the story also need the case where
  the source is already open when the release lands? [Coverage, Spec §User Scenarios US1]
- [x] CHK014 Is the meaning of "the note marks the source without being read" tied to properties a
  test can read — one painted text node, `display:none` on the reveal, a stated colour — or left to
  a screenshot? [Measurability, Spec §UI/UX]
- [x] CHK015 Does the spec name the surface that inherits the old overlay settings, so FR-005 is
  checkable rather than a preference? [Clarity, Spec §Requirements FR-005]
- [x] CHK016 Is the risk of leaving `multimedia/obs/` in the tree addressed — static files still
  served, templates still renderable by a future route? [Coverage, Gap]
- [x] CHK017 Are the success criteria free of implementation words (mirror, 302, 301) where the
  outcome matters more than the mechanism? [Consistency, Spec §Success Criteria]
- [x] CHK018 Is the ordering between the reading pages' addresses and the retirement stated as a
  non-regression, with the four addresses named? [Coverage, Spec §Requirements FR-007]
- [x] CHK019 Is it clear that `/archive/` is not a second front door — that nothing in the app links
  to it? [Clarity, Spec §User Scenarios US3]
- [x] CHK020 Are the owner's three answers recorded with their date, so a later reader can tell a
  decision from a default? [Traceability, Spec §Clarifications]
