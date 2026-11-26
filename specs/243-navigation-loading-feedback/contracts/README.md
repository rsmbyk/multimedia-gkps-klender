# Contracts — spec 243

**Spec**: `specs/243-navigation-loading-feedback/spec.md`

## Interfaces exposed by this slice

none — no route, URL, payload, event name or storage key changes. The navigation
links keep their real `href`s and the fetch still sends
`X-Requested-With: fetch` with same-origin credentials.

## Internal contracts tightened

- `navigate(url, opts)` gains an optional `opts.source` (the clicked element) and
  is the only place that sets or clears the pending state. Existing `opts.kind`
  values keep their meaning; a helper maps them to list-only vs stage-write.
- A second `navigate()` call cancels the live fetch when either fetch writes to
  the stage, or when the live fetch is list-only. It coexists with the live
  stage write only when the new fetch is list-only. The old
  `pendingNavigation` queue is removed.
- The clicked item carries `aria-disabled="true"` and the dim-only class until
  its own request settles; the stage carries `aria-busy="true"` only for a
  stage-write request.
- Section bars are children of `#panel`, `#chapters` and `.stage`, positioned
  at `top: 0` of those roots. Only sections the fetch will update show a bar.
- The live region exists empty from first paint, is polite, and announces one
  opening message and one settlement message per activation.

## Not exposed

No new API, no new template variable, no new CSS token, no new localStorage key.
`shell:page` and the editor feedback channel are unchanged.
