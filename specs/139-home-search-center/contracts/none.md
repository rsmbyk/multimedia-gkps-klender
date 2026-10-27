# Contracts: The landing search field sits on the window's middle

**Slice**: `specs/139-home-search-center` · **Interface**: `none` — stated, not absent.

The project exposes no interface this slice touches: no route, no REST endpoint, no template context,
no JavaScript API. The landing page's served HTML is byte-identical before and after (the preview's
`before-home.html` and `after-home.html` differ only by one `<link>`), and the slice adds no endpoint.

The one thing another part of the codebase can depend on is the set of class names the stylesheet
addresses, which this slice does not rename:

| Name | Where it lives | What this slice does to it |
| --- | --- | --- |
| `.stage` | `multimedia/web/templates/reading/base.html:405` | adds two custom properties and expresses its `padding` with them |
| `.search-home` | `base.html:406` | `flex` → `grid`; `min-height` derives from the stage's tokens |
| `.search-home__inner` | `base.html:407` | block → three-row grid |
| `.search-home__logo` | `base.html:409` | pinned to row 1, aligned to its end |
| `.search-home__form` | `base.html:410` | pinned to row 2 |

Nothing else reads these names — no script selects them for geometry (`reading.js` selects
`#globalSearch` and `#searchQuery` by id, untouched), and no template renders a class from them.
