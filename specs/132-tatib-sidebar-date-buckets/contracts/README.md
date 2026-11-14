# Contracts — none

This slice exposes no external interface. What it changes is internal to the repository's own templates
and to the browser:

- the panel's `tatib_groups` context — read by `_tatib_panel.html` alone;
- the dock's `groups` context — read by `obs_dock.html` alone;
- the `data-bucket` attribute — read by `static/web/reading.js::nodeIdentity` as an identity key, and by
  nothing else (no stylesheet, no test outside this slice's own, no route).

No HTTP endpoint, no API shape, no database column and no message changes. The saved renderer recomputes
its buckets from the stored library rather than consuming a contract from the server.
