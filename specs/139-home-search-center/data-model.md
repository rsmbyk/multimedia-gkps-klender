# Data model: The landing search field sits on the window's middle

**Slice**: `specs/139-home-search-center`

No entity, no migration, no stored value. The slice changes where one element is painted; the landing
page's markup, its template context and its routes are untouched.

The boxes involved, with the values the change moves (Chromium, 1440×900):

| Box | Owner | Today | After |
| --- | --- | --- | --- |
| `.stage` content box | `components.css` `.stage` | 40 .. 836 | 40 .. 836 (unchanged) |
| `.search-home` | `.search-home` | absolute 40 .. 836, 796 tall | same box, still 796 tall |
| `.search-home__inner` | new grid | 178 tall, centred as a block | stretched to 796, three rows |
| `.search-home__logo` | logo rule | 96×96 at 349 | 96×96 at 300 (row 1, aligned to its end) |
| `.search-home__form` | form rule | 610×56 at 471 | 610×56 at 422 (row 2, the middle line) |

Nothing else is derived from these boxes: no script reads them, no template renders them, and no test in
the suite asserts the landing page's vertical position today.
