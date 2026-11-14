# Contracts: the companion's configuration surface

**Spec**: `specs/192-companion-origin-page/spec.md`

The companion's HTTP surface grows four things; everything else (`/v1/status`, `/v1/files`,
`/v1/transfers`, `/v1/slides/*`, import/inspect, settings, references, auto-downloads) is
unchanged.

## Page

| | |
| --- | --- |
| `GET /` | serves `multimedia/companion_page.html` as `text/html; charset=utf-8`, `Cache-Control: no-store` |

Served whenever the `Host` is one of the loopback forms (`127.0.0.1:<PORT>`, `localhost:<PORT>`) —
regardless of the recorded set, in every start mode. A request with a foreign `Host` or an
`Origin` that is neither absent nor the companion's own origin gets the standard 403 (FR-004).

## Config endpoints (same authorisation as the page; no media token)

| Endpoint | Method | Body | Success | Failure |
| --- | --- | --- | --- | --- |
| `/v1/origins` | GET | — | `200 {"recorded": […], "seeds": […]}` | — |
| `/v1/origins` | POST | `{"origin": "…"}` | `200 {"recorded": […]}` | `400 {"error": "<first broken rule>"}` · `409 {"error": "that origin is already recorded"}` |
| `/v1/origins/<n>` | PUT | `{"origin": "…"}` | `200 {"recorded": […]}` | `400` as above · `404 {"error": "no origin <n> is recorded"}` |
| `/v1/origins/<n>` | DELETE | — | `200 {"recorded": […]}` | `404 {"error": "no origin <n> is recorded"}` |
| `/v1/fonts` | GET | — | `200 {"directories": [{"path", "source", "families"}]}` | — |

`recorded` is the ordered, renumbered set (FR-002); the broken-rule strings are the exact form
lines fixed in the spec's UI/UX (`an origin carries no path, query or trailing slash`, …).
`seeds` is the read-only compose-provided pair.

## Refusal payload (all other requests, unchanged scope)

```json
{"error": "Origin is not allowed. Record this computer's origins on the companion's page at http://127.0.0.1:<PORT>/."}
```

Sent with status 403 and no CORS headers (FR-003). The message is built from `PORT`.

## Enforcement rule

Allowed ⇔ `Host` is a loopback form **and** `Origin` ∈ (env seeds ∪ recorded set) — evaluated per
request (FR-003). Everything else about requests is unchanged.

## Web surfacing contract

`static/web/media-library.js`: when the status fetch fails and the failure carries the companion's
message, the status popup shows that message beside the `Unavailable` label; without a message,
today's bare `Unavailable` stays (FR-008).
