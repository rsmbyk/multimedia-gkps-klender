# ADR 0003: Use a saved shell and revisioned browser library for offline reading

## Status

Accepted

## Context

The public reader and the service projector need to keep opening Bible, song, and Tata Ibadah
content when connectivity is interrupted. Fetching a new HTML page for each in-app navigation also
adds latency and prevents navigation after disconnection. Legacy OBS docks and editor routes must
keep their existing network behavior.

## Decision

Keep complete public reading data in transactional, revisioned IndexedDB generations. A sync stages
changed chunks and makes them visible only after the whole generation is validated; a failed update
leaves the last complete generation available. Use a service worker with an explicit route allowlist
to provide only the public reading shell and the service-projector shell with their required assets.
In-page reading navigation renders from the saved library and refreshes only the current content data
asynchronously. Projector Go To and detours read the same committed local library.

Do not queue edits while offline, cache legacy OBS/editor pages, or make the browser copy
authoritative. The root `/` is the empty-search index unless maintenance mode is explicitly enabled.

## Consequences

- After the first complete online sync, included routes can open directly from the saved shells and
  content while offline.
- Incremental sync transfers only changed chunks and preserves the prior generation on failure.
- Browser storage eviction or an incomplete initial download means offline readiness cannot be
  claimed; the status UI reports that state.
- Editors continue to write to Django when online and retain their existing network behavior.
- Only the two allowlisted shells are guaranteed to open offline; future pages require an explicit
  scope decision.
