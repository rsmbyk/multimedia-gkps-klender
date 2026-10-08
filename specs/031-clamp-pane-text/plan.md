# Plan 031: Clamp a text entry in the Tata Ibadah pane

- **Status:** Draft
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-033
- **Bump:** patch

## Why

The pane prints every line of a text entry (and a legacy text row), so one long text pushes the rest
of the running order down the page. Show only the first **three** lines, hard-truncated with a
trailing "…", so the pane stays a readable running order. The hidden words remain reachable through
the entry preview (spec 032).

## Scope / edges

**In:**

- The pane shows at most three lines of a text entry's body; a longer one is hard-truncated — the
  trailing lines are dropped and a literal "…" is appended (the owner's hard truncation; not a CSS
  line-clamp).
- Blank lines count toward the three.
- An entry that was truncated is marked so the preview affordance knows there is hidden text
  (spec 032).
- Applies to text entries and legacy text rows alike (both go through `_paragraphs()`), including the
  single-screen text kind (spec 029).

**Out:**

- Scripture and song rows, which already show only their reference in the pane.
- Other reading panes (Bible, Kidung).
- The preview's own content, which shows the full text (spec 032).

## Approach

- `multimedia/web/reading/views.py` — where the pane builds an item's lines (`_paragraphs()` and the
  `paras` block in `_tatib_items()`), hard-truncate to the first three lines and append "…" to the
  last kept line; set a `clipped` flag on the block. Define the limit as a module constant.
- `multimedia/web/templates/reading/tatib.html` — nothing needed for the clamp itself; the preview
  button (spec 032) keys off the `clipped` flag.
- Implemented where the lines are built rather than measured in the browser: the lines are discrete
  `<p class="tatib__tx">` elements, the pane re-renders server-side on every navigation and save, and
  hard truncation needs no measurement. This is the owner's chosen "hard truncation, not CSS clamp".

## TDD

- Domain/app tests: `multimedia/web/tests.py` — a body of more than three lines renders only the
  first three with a trailing "…"; blank lines count; a body of three lines or fewer renders in full
  with no "…"; a legacy text row is clamped the same way; a text is marked clipped only when it was
  truncated.
- E2E: no new file required; the pane assertions live in `multimedia/web/tests.py`.

## Risks

- **Hiding the operator's cue.** A text can be a liturgist's private cue; clamping three lines is the
  owner's chosen budget, and the preview keeps the whole text reachable.
- **Interacting with the projector.** The pane clamp must not leak into the projector, which shows
  the full body (spec 006 / 029) — the two paths use different builders.
