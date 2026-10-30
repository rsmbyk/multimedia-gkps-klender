---
id: ITEM-181
status: backlog
title: 'A Tata Ibadah is a service or a template'
type: feat
priority: P1
effort: L
created: 2026-10-30
updated: 2026-10-30
spec: specs/167-tata-ibadah-templates/spec.md
branch: feat/167-tata-ibadah-templates
pr:
issue:
closed_at:
closed_reason:
bump:
release_version:
---

# ITEM-181: A Tata Ibadah is a service or a template

## Summary

Today a "template" is only a Tata Ibadah whose date is empty: `_tatib_groups` picks the Templates list with
`date__isnull=True` (`multimedia/web/reading/views.py:843`) and `TatibView` picks the panel mode the same way
(`:1914`), while the editor's help text tells the operator to leave the date empty (`editors.py:60–62`). The
type is therefore an accident of the data and anything can be projected. The slice makes it an explicit type
chosen when the Tata Ibadah is created — Normal (with a date) or Template (without, and never changeable) —
and gives a template the two entries a skeleton needs: fill-ins and choices. A template is completed into a
dated service through a two-step generate flow, and can never be projected.

## Notes

- The owner's decisions (2026-10-30): fill-ins and choices are added with two new add-row buttons; a choice's
  options are added from the choice's row as indented child entries; the generate modal is two steps — resolve
  every slot, then Next to the normal Tata Ibadah form; copying a service as a template does not convert its
  entries, it only makes a skeleton whose fill-ins and choices are added by hand.
- The add row's geometry is load-bearing (spec 143, and the E2E pins in `tests/e2e/test_tatib_entry_controls.py`
  and `test_tatib_hover.py`): two more buttons on the template's add row have to be measured at narrow widths.
- The projection guard touches `service_projector` (`views.py:1334–1338`), the projector-window control
  (`tatib.html:10–34`) and the OBS dock's service list.

## Acceptance sketch

- New Tata Ibadah: a Normal/Template switcher at the top; Template has no date field; Normal cannot save without one.
- Template page: `+ Fill-in` and `+ Choice` in its add rows; a choice carries its options as child rows.
- Project controls are replaced by **Use template**; a template never reaches the projector or the dock.
- Copy as template: offered from the Edit modal for either type, confirmed first, irreversible.
- Use template: step 1 resolves every slot (Next disabled until all are settled), step 2 is the normal form,
  Create is confirmed and leaves the template unchanged.

## Links

- Spec: [167](../../specs/167-tata-ibadah-templates/spec.md)
- Related items: ITEM-018 (the custom date picker), ITEM-022 (the Sunday default), ITEM-028 (live projection)
