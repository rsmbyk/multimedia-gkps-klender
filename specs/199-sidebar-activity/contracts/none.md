# Contracts: The first sidebar's idle rule, restored and set to fifteen minutes

**Spec**: `specs/199-sidebar-activity/spec.md`

`none` — the reading page is server-rendered HTML whose only external surfaces (the reading
routes, the static `reading.js` it links) keep their existing contract. This slice changes where a
DOM listener runs, when a timer restarts and one constant: no endpoint, no request or response body,
no storage key, no event crossing a process boundary is added, changed or removed.
