---
id: ITEM-196
status: in-review
title: "The companion's page manages this computer's origins"
type: feat
priority: P1
effort: M
created: 2026-11-14
updated: 2026-11-14
spec: specs/192-companion-origin-page/spec.md
branch:
pr:
issue: 506
closed_at:
closed_reason:
bump: minor
release_version:
---

# ITEM-196: The companion's page manages this computer's origins

## Summary

A projector computer's origin allowlist is that computer's own configuration, but today it is
frozen into compose at start from a required `.env` variable — so a fresh clone cannot even start
(`required variable GKPS_MEDIA_PRODUCTION_ORIGIN is missing a value`, observed on the OBS laptop,
2026-11-14). The direction (2026-11-14, chat): make the media companion serve a configuration page
where the operator adds, edits and deletes the origins and sees the font directories the converter
detects — the launchers stop knowing any origin variable at all.

## Notes

- The launcher-prompt design this slice began with (spec revisions of 2026-11-14: variable rename,
  prompted loop, edit/delete grammar) is withdrawn and recorded in the spec's Clarifications; what
  survives is the validation grammar (now the page form's) and the font listing in the start output.
- The page is served by the companion on its own loopback origin, so it needs no allowlist entry —
  reachable from the first second of a first-ever start.
- Enforcement becomes per-request over the union of the compose local seeds and the recorded set
  (stored in the companion's volume); a refusal names the page, and the web app surfaces that
  reason.
- The operator variable is removed everywhere — compose guard, `.env.example`, README, both docs,
  the compose tests; a dead `.env` line on already-configured laptops is documented as ignored.
- Effort moved S → M with the direction change (page + endpoints + runtime enforcement + compose/
  launcher simplification).

## Acceptance sketch

- Fresh checkout, no `.env`: the stack starts, `http://127.0.0.1:63174/` renders (empty state), one
  added production origin makes the production site's media picker reach the companion.
- The set persists across companion restarts and reboots; enforcement is per request.
- A request from an unrecorded origin: 403 naming the page, no CORS headers; the local seeds work
  with nothing recorded.
- The launcher has no origin logic; plain compose starts without `.env`; the start still names the
  mounted font directories.

## Links

- Spec: [192](../specs/192-companion-origin-page/spec.md)
- Related items: ITEM-186 (spec 182, the launchers and the machine requirements the stack already
  records), ITEM-195 (spec 191, restart policy — the previous local-stack slice)
