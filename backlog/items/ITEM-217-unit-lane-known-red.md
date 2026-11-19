---
id: ITEM-217
status: backlog
title: 'Eight unit-lane tests are red on develop'
type: fix
priority: P1
effort: M
created: 2026-11-19
updated: 2026-11-19
spec:
branch:
pr:
issue:
closed_at:
closed_reason:
bump:
release_version:
---

# ITEM-217: Eight unit-lane tests are red on develop

## Summary

The push-step run of the whole unit lane (`manage.py test multimedia`) found eight failures that
are identical on `develop` with the running slice's change reverted. They span the legacy tatib
API payload, image and video projection contracts, the projector's rendered voices, the tatib
template slot endpoints and the projector's shortcuts sheet. Nobody owns them yet, so the next
session inherits them; this card records the evidence and the list.

## Notes

- Command: `manage.py test multimedia --keepdb --noinput`, throwaway database `gkps204`, after
  `manage.py collectstatic --noinput` in the worktree. **543 tests, 8 failures, 0 errors.**
- Provenance: the same lane at `origin/develop` (`4b25e796`) with `static/web/obs-dock.js` reverted
  to the base produced the identical eight failures (and the same nine manifest errors before
  `collectstatic`). The slice under test changed one client-side statement, so it cannot reach
  these Python assertions.
- The nine `Missing staticfiles manifest entry` errors seen before `collectstatic` are
  environmental, not product defects: this worktree had no `_static/`. They clear once the
  manifest exists, and are not part of this card.
- The full browser matrix (756 E2E methods) was not run in that session; the dock's own seven-module
  lane ran 89 tests with two reds already carded as `ITEM-215`.

### The eight

| Test | Assertion |
| --- | --- |
| `multimedia.tatib.tests.LegacyTatibApiCompatibilityTests.test_legacy_tatib_list_keeps_its_route_and_payload_fields` | `Items in the first set but not the second: 'kind'` |
| `multimedia.tatib.tests.ServiceEntryTests.test_image_projection_is_one_image_screen` | `2 != 1` |
| `multimedia.web.test_media.VideoDisplayContractTests.test_video_has_a_screen_and_a_rest_in_service_order` | `Couldn't find '<h3>Audio</h3>' in response` |
| `multimedia.web.test_speaker_voices.RenderedVoicesTests.test_songs_and_scripture_stay_ordinary_on_the_projector` | `'<p class="screen__line">P: bait satu</p>' not found` — the page renders the passage fixture instead |
| `multimedia.web.test_tatib_templates.SlotEndpointTests.test_generate_replaces_slots_in_order` | `400 != 201` |
| `multimedia.web.test_tatib_templates.SlotEndpointTests.test_options_live_under_their_choice` | `400 != 200` |
| `multimedia.web.test_tatib_templates.SlotEndpointTests.test_validate_answers_the_row_and_writes_nothing` | `400 != 200` |
| `multimedia.web.tests.ServiceProjectorTests.test_the_shortcuts_sheet_names_audio_and_video_in_groups_of_their_own` | group lists differ: expected `[['Service', 'Song', 'Passage'], ['Library passage', …]]`, got `[['Service', 'Song', 'Image and PDF', 'Audio and Video'], …]` |

Three families look like test drift after a behaviour change (the shortcuts sheet's groups, the
legacy payload's `kind`, the voices fixture); the slot endpoints' three 400s look like one request
contract change; the image and video counts look like the rest-screen rule. Each needs its own
attribution before a fix — a spec per family, not one sweep.

## Acceptance sketch

- Each of the eight is attributed: the test is stale, or the behaviour regressed.
- The lane runs green, or every remaining red has a card of its own with the base evidence.

## Links

- Found while delivering spec [204](../../specs/204-dock-entry-open-reset/spec.md) (card ITEM-216).
- Related: [ITEM-215](ITEM-215-dock-follow-known-red.md) (the dock-follow E2E reds),
  [ITEM-184](ITEM-184-known-red-e2e.md) (the browser-suite reds).
