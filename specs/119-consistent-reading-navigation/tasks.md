# Tasks 119: Consistent reading navigation across saved and server data

- **Status:** Accepted
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

## Checklist

- [x] Spec accepted by Ronald.
- [x] Reproduce stale Tata Ibadah rail list and same-day ordering with a controlled older saved generation; record requests and DOM against direct online load.
- [x] Reproduce saved rail lists, songbook child list, item-stage/sidebar mismatch, Bible chapter refresh, and in-page versus direct search results with current source assets.
- [x] Compare direct load, normal reload, and hard reload; all returned the current service list.
- [x] Check history behavior for a service opened from a rail menu; no distinct data bug found.
- [ ] Extend regression coverage to remaining route variants and interaction states during implementation.
- [x] Red: focused ordering/serialization test for services with creation order different from ID order.
- [x] Green: serialize canonical sort metadata and align offline ordering with Django.
- [x] Red: browser tests from `/home/` for stale rail rows and search results; existing tests cover failed online fetch and navigation state.
- [x] Green: make online reading routes settle on current data while preserving live UI state.
- [x] Run targeted Django and browser checks; no styling changed.
- [x] Complete traceability and version/changelog; ITEM/board PR metadata follows PR creation.
- [x] Open draft PR against `develop` ([#368](https://github.com/rsmbyk/multimedia-gkps-klender/pull/368)).
- [ ] Run required exact-head CI before merge.

## Done when

- [ ] Every acceptance scenario in `spec.md` passes.
- [ ] Online click, normal refresh, and hard refresh agree on the same route after loading settles.
- [ ] Offline browsing retains the saved fallback and canonical order.
