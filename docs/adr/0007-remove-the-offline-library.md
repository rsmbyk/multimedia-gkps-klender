# ADR 0007: Remove the offline library; the projector fetches on selection

## Status

Accepted

## Context

ADR 0003 kept a complete, revisioned copy of the public library in the browser (16.89 MB on this
database) behind a service worker, so reading and projection could survive a dropped connection.
The copy also served the projector's Go To: the panel searched the local Bible and song data and
built its detour from it.

That copy carried a maintenance cost out of proportion to what it bought. It was a second content
store with its own revision protocol and generation commits; every reading navigation painted the
saved page first and replaced it when the server's arrived, which is the path behind a run of
freshness defects; and it made the projector depend on a completed download before its Go To could
list anything. The team reads and projects on a machine with a live connection, and an offline copy
that is subtly stale is worse than a page that says the network is down.

## Decision

Remove the offline library whole: the IndexedDB store, the service worker and its shells, the four
`/offline/…` and `/service-worker.js` routes, the rail's status control and panel, the saved-copy
paint in reading navigation, the projector's saved-service fallback, and the tests that pinned them.
The app is online-only; a dropped connection is the browser's to report.

The projector's Go To keeps its lookup in the browser but changes its source: a page-memory index
fetched once when the page loads (books with their editions' chapter and verse counts, songbooks,
song titles — 102 KB on this database, no verse text), re-fetched by the page's Update. Choosing a
result fetches the whole chapter in both editions, or the whole song, and the page refuses every key,
click and dismissal until it paints; a step that leaves the loaded chapter is the same fetch under
the same lock.

## Consequences

- One content store, one freshness rule: what a page shows is what the server answered.
- The Go To's search costs one request per page load instead of a 16.89 MB download; its content
  costs one request per selection or chapter crossing, measured at ~31 ms of server and database
  time on this stack plus the network leg.
- A verse step inside a loaded chapter is local; a chapter or book crossing waits for a fetch, and
  the projector shows that wait in the panel row and beside the shortcuts button.
- A returning browser is cleaned on its next page load: the service worker is unregistered, its
  cache deleted and the database dropped.
- Offline reading and projection are gone. If they are ever wanted again, they are a new decision
  and a new ADR, not a restoration of this machinery.
- ADR 0003 is superseded, not deleted; its record stays as the account of why the copy existed.
