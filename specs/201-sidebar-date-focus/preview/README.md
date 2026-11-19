# Preview — spec 201

`index.html` is a static preview built from the app's own materials, not a drawing:

- the row markup is a capture of the first group from `#panelBody` on the running Tata Ibadah
  sidebar (`rows.html`, captured at base `92edc752`);
- `assets/tokens.css` and `assets/components.css` are copied verbatim from that base commit —
  linking the working tree would turn the TODAY column into a second PROPOSAL the moment the fix
  lands;
- the harness (`body.pv`, the two panels, the buttons and the readout) and the two candidate rule
  blocks are the only authored style. Every proposal rule is in the `<style>` block, tagged with
  the panel it belongs to.

**What to press:** in each panel, press *At rest*, *Hover*, *Click row (pointer away)* and
*Click elsewhere*. The readout prints the computed `display` of the date, whether the row matches
`:focus-within`, which element holds focus, the pencil's opacity and the row's measured height.
Today's panel keeps the date hidden in the *Click row* state; the proposal paints it again. Hover
hides the date in both panels.

`build.py` rebuilds `index.html` from `rows.html` and the base commit's stylesheets;
`probe.py` drives all four states in both panels and asserts the difference.

**What a static page cannot show:** navigation and anything fetched. The click state is produced by
focusing the real `.book` link, because a click's only effect on this rule is where focus lands;
the preview deliberately does not follow the link's `href`. The hover state is simulated with a
class that carries the same declarations as `li:hover` — a static page cannot hold a pointer.
Keyboard focus on the pencil/trash is covered by the spec and will be asserted by the E2E at Plan;
it is not simulated here.
