# Preview: a passage cue carries its current and end verse

`static preview at specs/229-cue-verse-counter/preview/index.html` — open the file directly. It carries
the real corner-cue markup from `projector_controls.html` and links the project's own `tokens.css`
and `projector.css`; the only page-local CSS positions the comparison frames. No build, server or
database is involved.

**After** frames hold the proposed counter; **Before** frames hold today's cue. The *Next verse*
buttons step the counter the way the render will, so the moving number can be judged in place.

## States

1. **Service passage, `Matius 5:3-5`** — `3/5`, `4/5`, `5/5`; the reference holds and the flip stays.
2. **Passage Go To, chapter `Matius 5` with three verses** — `1/3`, `2/3`, `3/3`; the Go To
   reference follows the verse as it does today.
3. **Song cue** — no `.cue-verse`; baits and progress unchanged.
4. **Empty chapter** — no counter rather than `1/0` (spec FR-006; not drawn in this static page
   because it is a data state).

## Bound

The counter reads data the projector already loads (the entry's verse bounds, the chapter's verse
list), so this static page can show the result. A live check of the real route follows implementation.
