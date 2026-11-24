# Data Model: entry modal title band

**Spec**: `specs/240-entry-modal-title/spec.md`

## Entities

No persisted entity, model, migration, form, serialiser or endpoint changes. The
product change is one scoped CSS rule plus its narrow override.

## Existing boxes the rule relies on

| Box | Current source | Role |
| --- | --- | --- |
| `.editor__title` (`#editorTitle`) | `multimedia/web/templates/reading/_entry_form.html:2` | the heading rendered directly in `#editorContent`, with no wrapper |
| `.editor__head` | `_editor_form.html:4`, `_slot_form.html`, `_old_item_form.html` variants | the header row used by record editors; absent from the entry form |
| `[data-editor-size="large"]` | `_entry_form.html:3` on text Create/Edit and media Create | selects the 840×760 frame and the title-band rules |
| `.editor:has(...) .editor__head` | `components.css:544` | spec 226's inset and divider for head-bearing editors |
| `.editor:has(...) .editor__title` | `components.css:545` and media query | zero-padding reset that caused the regression |

**Relationships**: the title is a sibling of the form inside `.editor__content`.
The scoped selector keys off a descendant form carrying the large marker and the
absence of a head in the same dialog. **Validation**: none. **State transitions**:
none — the rule applies whenever a large headerless form is loaded.

## Invariants

- Large headerless titles read 26px x / 21px y from the dialog at ≥651px wide;
  18px / 17px below 650px. Band 72.5px / 64.5px, one 1px rule (FR-001/002, SC-001/003).
- Head-bearing editors keep the spec-226 reset: head padded `20px 26px 14px`,
  title padding and border `0px`, one ruled box (FR-003, SC-002).
- Compact dialogs, loading states and screen-reader titles are untouched (FR-004).

## Not modelled

- No new CSS variable, state flag, template wrapper or script hook.
