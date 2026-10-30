# Contracts: the dock fills whatever panel it is given

**none** — the slice adds and changes no interface. `/obs/dock` keeps its URL, its template
(`reading/obs_dock.html`), its context (`groups`, `page_title`), its markup and its `data-` hooks
(`data-service`, `data-name`, `data-date`, `data-onscreen-for`, `data-bucket`); the display protocol
(`gkps-display` in localStorage, the `gkps-service-display` channel) and the overlay and projector
routes are untouched. What changes is one declaration in the dock's own stylesheet — the panel's
maximum width and its centring margin — and nothing else.
