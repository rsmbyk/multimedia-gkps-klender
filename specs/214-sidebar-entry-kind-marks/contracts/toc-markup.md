# Contract: the contents row's mark column

**Spec**: `specs/214-sidebar-entry-kind-marks/spec.md`

No URL, API shape, form field or response changes. The contract worth writing down is the markup
seam, because three suites read `#chList` by class and attribute.

## The row's new shape

```html
<a class="songrow" data-i="…" data-num="…" data-txt="…">
  <span class="songrow__c">3</span>
  <span class="songrow__mark" aria-hidden="true" data-mark="song">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" …>…</svg>
  </span>
  <span class="songrow__t">…</span>
</a>
```

A slot's mark adds the modifier:

```html
<span class="songrow__mark songrow__mark--slot" data-mark="fill_in">
  <svg viewBox="0 0 20 20" …>frame + +/◎</svg>
  <span class="slot__badge" aria-hidden="true" data-kind-badge="song">
    <svg viewBox="0 0 12 12" …>…</svg>
  </span>
</span>
```

| Guarantee | Why it is a contract |
| --- | --- |
| one `.songrow__mark` per `a.songrow`, as its second child | tests count marks per row and check the column's order |
| `data-mark` is one of `text` · `scripture` · `song` · `media` · `fill_in` · `choice` | the E2E distinguishes the kinds by this value |
| `data-kind-badge` is one of `text` · `scripture` · `song` · `media`, or absent | the slot modifier is checked by attribute and glyph |
| `aria-hidden="true"` on the wrapper, with no control inside | FR-004; the row's accessible name is unchanged |
| the mark uses no `.entry__kind-icon` class | spec 144's sidebar/dock exclusion test stays green for the stage class |
| `li.toc__eos` carries no `.songrow__mark` | the divider keeps its rule and its 13px box |

## What must NOT change

| Untouched | Guarded by |
| --- | --- |
| `.songrow__c`'s left edge, vertical centring and `data-num` text | spec 063, `tests/e2e/test_toc_number_centering.py` |
| the three-line clamp, `…` and `overflow-wrap` on `.songrow__t` | spec 135, `tests/e2e/test_text_wrap.py` (`.songrow__t` case) |
| wrapping at the pane edge | spec 137, `tests/e2e/test_text_wrap.py` |
| the dock's entry list and the projector's entry list | FR-008, `tests/e2e/test_stage_kind_marks.py` |
| spec 213's `.slot__mark > svg` frame rule on the stage | no stage markup or CSS is edited |
