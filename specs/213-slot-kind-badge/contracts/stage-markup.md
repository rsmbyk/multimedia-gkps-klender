# Contracts: a slot states the kind it resolves to

**Spec**: `specs/213-slot-kind-badge/spec.md`

No external interface changes: no URL, no API shape, no form field, no response. The slice adds
markup inside one existing partial. The contract worth writing down is the **markup seam**, because
three suites read this page by class and attribute.

## The slot mark's markup

```html
<span class="slot__mark" aria-hidden="true">
  <svg viewBox="0 0 20 20" …>…frame + +/◎…</svg>
  <span class="slot__badge" aria-hidden="true" data-kind-badge="song">
    <svg viewBox="0 0 12 12" fill="none" stroke="currentColor" …>…one glyph…</svg>
  </span>
</span>
```

| Guarantee | Why it is a contract |
| --- | --- |
| `.slot__mark` still contains exactly **one** direct `<svg>` — the frame | `#read .slot__mark > svg` sizes it; a second direct child would be stretched to 20px |
| the badge is `.slot__badge` with `data-kind-badge` = `text` · `scripture` · `song` · `media` | the E2E counts and distinguishes badges by that value; the preview's probes read it |
| the badge is **absent** (not empty) when the row's kind is unreadable | FR-007; an empty disc would read as a fifth kind |
| both the mark and the badge are `aria-hidden="true"` | FR-004; the row's accessible name is the kind label and the title |
| the badge's `<svg>` carries `fill="none" stroke="currentColor"` as attributes | D006 — the paint must not depend on which stylesheet loads |
| nothing inside the mark takes a pointer | the row's own hover and its controls own the pointer |

## What must NOT change

| Untouched | Guarded by |
| --- | --- |
| `stroke-dasharray: 2.8 2.4` and the `+` / `◎` path in `_slot_mark.html` | FR-003, SC-003 |
| `.slot__kind`'s words (`Fill-in · Song`, …) | FR-001's "the badge names the kind" is additive, never a replacement |
| `data-slot` and `data-slot-kind` on the row | `tests/e2e/test_tatib_templates.py` and `test_tatib_preview_parity.py` read both |
| every row's height, every title's `x`, the page's scroll height | FR-005, SC-004 |
| the Use template dialog and the sidebar | spec 144 FR-008; the dialog's slot row carries no mark at all |
