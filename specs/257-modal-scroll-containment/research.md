# Research: where a modal's wheel goes when its own view stops

**Question**: which scrollport receives a wheel once an open modal's inner view has no range left,
and what is the smallest rule that keeps the scroll inside the modal layer?
**Exits at**: zero unknowns.

## Survey — scrollports inside and behind a dialog

| Scrollport | Where | Default in base | Verdict |
| --- | --- | --- | --- |
| Editor content | `components.css` `.editor__content` | `overscroll-behavior: auto` | **Leaks** at end and at zero range |
| Editor date popover | `components.css` `.editor__date-calendar` | `auto` | **Leaks** to the editor or document |
| Picker options | `components.css` `.editor__picker-options` | `auto` | **Leaks** to the editor content (measured 0 → 341) |
| Media entry library panel | `components.css` `.media-entry__panel--library` | `auto` | **Leaks** inside the media editor |
| Preview body | `components.css` `.preview__body` | `auto` | **Leaks** at end and at zero range |
| Transfers list | `components.css` `.media-transfers__list` | `auto` | **Leaks** to the dialog/document |
| Service-media list | `components.css` `.service-media__list` | `auto` | **Leaks** to the dialog/document |
| Generate body | `generate.css` `.generate__body` | `auto` | **Leaks** inside the Generate dialog |
| Chooser list | `generate.css` `.choose__list` | `auto` | **Leaks** inside Generate |
| Reading sidebar / chapter list | `components.css` `.panel__body`, `.ch__body` | already `contain` | No change needed |
| Toasts | `components.css` `.edit-toasts` | already `contain` | No change needed |
| Dock lists | `obs-dock.css` two scrollports | already `contain` | No change needed |
| Document | `html`/`document.scrollingElement` | `overflow: visible` while a dialog is open | **Leaks** (600 → 1700, 600 → 2360) |

A top-layer dialog does not chain to a sibling pane: a scrollable `.panel__body` stayed at 0 while a
dialog's short content passed the wheel through. The two real leak paths are the document and nested
scrollports inside the dialog.

## Decisions

### D001 — Hold the document, and contain every modal scrollport
**Rationale**: the probe showed containment on `.editor__content` alone stops the end-of-range case
(600 → 600) but **not** the zero-range case (600 → 2360) nor the wheel over the header (600 → 2360).
Only `:root:has(dialog[open]) { overflow: hidden }` covered all three; containment on the inner
scrollports additionally stops picker → editor chaining.
**Alternatives**: containment alone (measured incomplete); `overflow: hidden` on the dialog itself
with `overscroll-behavior: contain` (measured: header and zero-range cases still chained to 2360);
a JS `wheel` listener with `preventDefault()` (new behaviour to own, and it would suppress the inner
scroll unless carefully scoped).
**Provenance**: the two live probes before gate 1 (`preview/probe.py`, containment variant probe),
with the numbers frozen in `spec.md` `## UI/UX`.

### D002 — Key the hold on `dialog[open]`, not on a script-maintained class
**Rationale**: every modal in this app is a native `<dialog>`; a selector on its open state covers
dialogs shown by any script, nested confirmations and small error dialogs without touching JS.
**Alternatives**: add/remove a `body` class in `showModal()`/`close()` wrappers — one more state to
keep honest, and the app has several independent call sites (`editors.js`, `preview.js`, `entries.js`,
`generate.js`, `media-library.js`, `media-handoff.js`, `songs_verse.js`).
**Provenance**: the seven `showModal()` call sites found in `static/web/`.

### D003 — Name the modal scrollports explicitly for containment
**Rationale**: `dialog[open]` alone cannot help a fixed picker menu that is a DOM descendant of the
editor; each named scrollport also needs `contain` so its parent does not move when it reaches its end.
The list above records every `overflow-y: auto` inside a dialog; already-contained reading/dock
scrollports are left alone.
**Alternatives**: a blanket `* { overscroll-behavior: contain }` — would change the reading lists and
the dock, which already have their own contract. **Provenance**: CSS survey and the nested case.

### D004 — `contain`, not `none`
**Rationale**: `contain` preserves the element's own scrolling and only stops propagation; `none`
also suppresses overscroll effects and was not asked for. **Alternatives**: `overscroll-behavior: none`
on the root — would not stop a wheel from scrolling the root itself. **Provenance**: CSS behaviour and
the measured inner maxima (617, 512, 870) staying reachable after the change.

### D005 — Behaviour test in a real browser, not a CSS-text assertion
**Rationale**: the contract is about where a wheel goes, so the test must dispatch wheel input over
real dialog markup and read both scroll offsets. **Alternatives**: assert the rule string in the
stylesheet — tests structure, not behaviour, and would pass even when Chromium still chains.
**Provenance**: repo convention (`tests/` Playwright E2E via `StaticLiveServerTestCase`) and TDD-05.

### D006 — Control CSS comes from the base commit, not a hand-written copy
**Rationale**: the static preview's "before" column must stay the base; `build_preview.py` reads
`components.css` from `1cd9f081` and the worktree at build time. **Alternatives**: link the live
control server's stylesheet — an in-chat preview frame loads `srcdoc` in an opaque origin and relative
assets never resolve. **Provenance**: the repo's preview convention and the frame's known behaviour.

### D007 — `bump: patch`
**Rationale**: a user-visible defect is repaired; no endpoint, schema or route changes.
**Alternatives**: `none` would hide the repair; `minor` overstates it. **Provenance**: owner report
and the CSS-only scope.

### D008 — Card and tracker anchor wait for the delivery word
**Rationale**: `ITEM-277` is created at `ready` now, but the anchor issue is a remote write and the
owner has not given a push/delivery word. **Alternatives**: create the issue at gate 1 — an
unauthorised remote side effect for a pack that has not passed gate 2. **Provenance**:
C-SDD-BOARD's "create before the first push" timing and the repo's push rule.

## Unknowns

None. Each named scrollport was found by CSS survey, each candidate fix was measured against the two
live servers, and the remaining scope questions were settled by the owner's gate-1 accept.
