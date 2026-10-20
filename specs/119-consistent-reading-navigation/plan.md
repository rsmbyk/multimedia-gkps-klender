# Plan 119: Consistent reading navigation across saved and server data

- **Status:** Accepted
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-119
- **Bump:** patch

## Why

An online in-page click currently prefers the saved IndexedDB renderer whenever a complete library exists. Only chapter, song, and service routes get a subsequent item-chunk fetch; list, book, home, and search routes can remain on an older generation. A full navigation asks Django first, so the two paths can visibly disagree. The offline Tata Ibadah renderer also sorts same-date services by ID while Django sorts by creation time.

Both discrepancies were reproduced in a temporary Playwright/Django test against current source assets on 2026-10-20. Starting at `/home/`, the test saved two dated services, added a third on the server, then opened the Tata Ibadah rail menu. The click showed only the two saved rows in ID order (`Newer ID`, `Older ID`) and made no `/tatib/` request. A direct online load of `/tatib/` showed all three rows in creation-time order (`Older ID`, `Newer ID`, `Added after save`). The offline renderer had returned the same two-row saved view before the click. This confirms both the stale menu and ordering causes. The test used `StaticLiveServerTestCase` so the browser loaded current source assets; the checkout's collected `_static/web/reading.js` is older and would give a false negative.

A second controlled browser pass froze manifest syncing after a complete saved generation, then changed a song title and service name, added a songbook/service, and added a verse. Tata Ibadah and Kidung rail menus, the songbook's child list, and in-page search remained on saved data; the rail menus made no page request. Opening an existing service or song fetched its chunk and updated the stage title, while its sidebar label remained old. Opening a Bible chapter fetched its chunk and showed the new verse. In-page search for the new verse differed from a direct server load of the same query. This reproduces the mixed-generation layout, not merely a stale snapshot in isolation.

The existing 21 offline reading browser tests pass after refreshing the checkout's ignored collected static assets; three focused projector browser tests also pass. The initial 21-test run against stale `_static` failed, so those failures are not current-source product evidence. The temporary audit tests were removed after recording results. No visual spacing mismatch was demonstrated; the confirmed layout inconsistency is old sidebar rows beside a current reading stage.

A final controlled pass showed that a direct `/tatib/` load, normal reload, and hard reload all displayed the current service list. The stale rail menu was therefore not a hard-refresh-only failure. Opening a service from that menu created a history entry; Back returned to `/home/` because rail-only section changes do not create history entries. No distinct history data bug was demonstrated. A separate projector Go To lookup remained stale until library sync; that independent path is recorded in Draft Spec 120 rather than this reading slice.

## Scope / edges

**In:** Public reading home, Bible, Kidung, Tata Ibadah, search, their first and second sidebars, and in-page/history navigation; online freshness and saved-copy fallback; ordering and layout parity for those surfaces.

**Out:** Projector/dock synchronization, editor write queues, new storage providers, a visual redesign, or cross-tab edition persistence.

## Approach

The controlled reproduction above is complete for the Tata Ibadah rail menu and same-date order. During implementation, extend it to the other named routes and compare normal and hard refresh explicitly.

Then make online navigation settle on current server data for every supported reading route while keeping the saved copy available if the request fails. Keep stale asynchronous responses from replacing a later click. Bring offline ordering and rendered structure into parity with the server's canonical rules. Preserve live sidebar, filter, scroll, search, focus, and Bible edition behavior during the update. Verify each route and interaction path in the browser; keep the offline library's atomic generation contract.

## TDD

- Domain/app: focused tests for the canonical service ordering and offline serialization data needed to reproduce it.
- E2E: saved generation followed by changed server data, every named route type, same-day ordering, failure fallback, navigation race, and refresh comparison.

## Risks

- A server response can arrive after the operator has opened another item; tie every update to the active navigation generation.
- Replacing a complete page can reset live controls; verify state preservation on the actual home-to-sidebar path.
- Offline remains intentionally a saved snapshot while disconnected; freshness claims apply only when the network request succeeds.
