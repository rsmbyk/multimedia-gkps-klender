---
id: ITEM-213
status: done
title: 'A long word wraps in the dock runner''s service title and entry headers'
type: fix
priority: P1
effort: S
created: 2026-11-19
updated: 2026-11-19
spec: 203
branch: fix/203-dock-long-word-wrap
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/541
issue: 540
closed_at: 2026-11-19
closed_reason: merged into develop (PR #541)
bump: patch
release_version: 1.35.0
---

# ITEM-213: A long word wraps in the dock runner's service title and entry headers

## Summary

The operator dock's runner paints an unbroken run of text straight past the box that owns it. A
service named with 64 `h` characters runs 328px past its own title box and under the head's three
buttons; a pasted URL used as an untitled Text entry runs 178px past its header; the same URL inside
the open block runs 107px past its screen row. The runner body grows a horizontal scrollbar
(`scrollWidth` 591 against `clientWidth` 456 at a 456px panel).

A run that already carries break opportunities is fine — the 137-character hyphenated filename in
the same service wraps to four lines with zero spill. Only the unbroken run overflows.

## Notes

- Measured on the owner's own service 149 (`h`×64, dated 2026-10-25) at a 456×1087 panel, dark, 1×:
  `specs/203-dock-long-word-wrap/preview/shots/before/measure.json`.
- The reading page already holds this rule (`reading/R13`, spec 137) and the dock's own picker
  already wraps a service name (`.servicerow__n { overflow-wrap: anywhere }`). The runner is the
  gap: `.serviceline`, `.entryrow__t` and `.screenerow` all compute `overflow-wrap: normal`.
- Sibling surfaces measured clean on the same service at 456px: `/tatib/149/` (title, item heads,
  body), `/projector?service=149`, `/obs/source/overlay` — zero spill, zero document overflow.
- Two runner labels declare their own cut and must keep it: `.nextband__label` and
  `.offstrip__label` (`white-space: nowrap` + ellipsis).

## Acceptance sketch

- No painted text past its own box in the runner's title, entry headers or screen rows, at a narrow
  and a wide panel; the runner body scrolls vertically only.
- A name or filename that already fits keeps its exact line count, height and width; the chevron
  keeps its trailing place and the two truncating labels keep truncating.

## Links

- Spec: [203](../specs/203-dock-long-word-wrap/spec.md)
- Related items: the reading page's own wrap rule is `reading/R13` (spec 137)
