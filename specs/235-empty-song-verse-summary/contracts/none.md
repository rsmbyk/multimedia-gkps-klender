# Contracts: An empty song names itself in the Verses section

**none**

The slice adds no external interface: no route, no request/response shape, no stored format
and no public JavaScript API. `/editor/entry/songs/` and `/editor/entry/song/<id>/verses/`
keep their existing contracts, and the `verses` form field keeps submitting IDs.

The `data-empty` attribute on `.editor__verse-panel` is an internal DOM contract between the
template, `entries.js` and `components.css` inside this repo; it is documented in
`data-model.md` rather than treated as an interface.
