# Feature Specification: the first sidebar's idle rule, restored and set to fifteen minutes

**Slice**: `specs/199-sidebar-activity`
**Branch**: `fix/199-sidebar-activity`
**Created**: 2026-11-18 · **Revised**: 2026-11-18 (widened at the owner's word — the drag-end
restart of the same 072 clause; SDD-25 re-entry at Specify), then again the same day to move the
wait itself to fifteen minutes
**Status**: Draft — Gate 1
**Input**: the owner's request, 2026-11-18 — "can you make sure it is captured from the intended
events? i dont want any unknown behavior here" — then, on the first gate-1 pack, "widen it": fold
the drag-end restart (and the rest of 072's deferral clause it belongs to) into this slice rather
than a card of its own — and "also increase the timer to 15 minutes".

This restores the rule spec 072 already accepted, and changes one number inside it: the wait becomes
fifteen minutes instead of sixty seconds. The activity model is 072's, not a new one; that rule is
the definition of "intended" for this slice, quoted verbatim in Clarifications.

## User Scenarios & Testing

### US1 — Scrolling the first sidebar restarts its interval, however the operator scrolls (P1)

**Why this priority**: spec 072 names scrolling in the first panel as activity. Wheel and keyboard
scrolling already restart the interval; dragging the scrollbar does not, because the `scroll`
listener sits on `#panel` while the scroller is its descendant `#panelBody`, and `scroll` does not
bubble. The panel can therefore collapse while the operator is still dragging its scrollbar — the
one scrolling gesture that is pure pointer work and produces no `wheel`. Fifteen minutes makes the
miss rarer, not smaller: the event 072 named is the one event the code never sees, and the defect
returns the moment anyone shortens the wait again.

**Independent Test**: open the Bible panel at a wide viewport, wait 30 s, set the list's
`scrollTop` (the event a scrollbar drag emits), wait 14 min 59 s — the panel is still open — wait
1 s more — it collapses to mini. On `develop` it collapses before that wait is over, because the
scroll restarted nothing.

**Acceptance scenarios**

1. **Given** an eligible open first panel and 30 s of quiet **When** the operator drags the list's
   scrollbar **Then** the interval restarts at that scroll: the panel is still open 14 min 59 s
   later and collapses exactly 15 min after the scroll.
2. **Given** the same panel **When** the operator scrolls it with the wheel **Then** the interval
   restarts, as it already does today — the fix must not regress the working path.
3. **Given** the panel's list focused **When** the operator scrolls it with PageDown / arrow keys
   **Then** the interval restarts (through `keydown`, and now also through the scroll it causes).
4. **Given** the panel **When** scrolling reaches either end and produces no scroll event **Then**
   nothing restarts — at the end of the list there is no scrolling to count.

### US2 — An interaction that holds the collapse gives a full interval when it ends (P1)

**Why this priority**: 072's clause is two-sided: defer while an interaction is underway, *restart
the interval when that interaction ends*. Today only the first half is general. The expiry re-check
restarts the interval only when the interaction outlived it; an interaction that ends before expiry
leaves the old deadline standing. So a reorder drag started at 14 min and released at 14 min 5 s
still collapses the panel 55 s after the release, and an operator who just acted watches the sidebar
go for no reason they can see.

**Independent Test**: on a Tata Ibadah service, wait 30 s, drag an entry's grip and release it, then
wait 14 min 59 s — the panel is still open — and 1 s more — it closes. On `develop` it collapses
during that wait, because the release restarted nothing.

**Acceptance scenarios**

1. **Given** an eligible open first panel and 30 s of quiet **When** the operator drags a service
   entry's grip and releases it before the interval expires **Then** the interval restarts at the
   release: the panel is still open 14 min 59 s later and collapses at 15 min.
2. **Given** the same state **When** the drag is still held when the interval expires **Then** the
   collapse is deferred as today, and the release restarts a full interval — the same outcome, now
   at one moment instead of one moment plus the poll's slack.
3. **Given** a dialog opened from the panel **When** it closes before the interval expires **Then**
   the interval restarts at the close. Focus returns to the opener in the panel, which already
   restarts it through `focusin`; a close that restores focus elsewhere restarts it through the same
   new rule, so the two paths agree.
4. **Given** an open modal or a drag **When** it ends after the collapse was already deferred
   **Then** the operator gets a full interval from the moment it ends, not the remainder of an
   interval that expired while they were busy.

### US3 — The activity surface stays exactly the rail and the first panel (P2)

**Why this priority**: the request is as much about what must *not* reset the timer as about what
must. Today that boundary is a comment's worth of intent; this slice makes every exclusion
observable and pins it with a test, so a future edit cannot quietly widen or narrow it.

**Independent Test**: scroll the second sidebar (the chapter/song list) for the full interval — the
first panel collapses on schedule. Do the same over the reading stage — same result. Open a dialog
and type in it for the full interval — the panel stays open (deferral), and a full interval starts
when the dialog closes.

**Acceptance scenarios**

1. **Given** an eligible open first panel **When** the operator scrolls the second sidebar for a
   full interval (15 min) **Then** the first panel collapses on schedule — the second sidebar is not
   an activity surface (072: "second sidebar content … out of scope").
2. **Given** the same state **When** the operator scrolls or points at the reading stage for a full
   interval **Then** the first panel collapses on schedule — the stage is not an activity surface.
3. **Given** a dialog open from the panel **When** the operator types in it and 15 min pass **Then**
   the panel stays open and the interval restarts only after the dialog closes (unchanged from
   today).
4. **Given** the narrow layout **When** the drawer is open and the operator scrolls it **Then** no
   timer is armed at all (unchanged: the timer is cancelled below 720 px).

### Edge Cases

- **When** a page is loaded and left alone **Then** the first panel collapses after fifteen quiet
  minutes rather than sixty quiet seconds. Only the number moved: eligibility, deferral, the 1 s
  expiry poll and the resulting mini/closed states are untouched, and every activity still restarts
  the whole fifteen minutes.
- **When** an in-page navigation scrolls the list programmatically (centring the current book or
  hymn) **Then** that scroll counts as activity. It is indistinguishable from an operator scroll,
  it happens only in response to an operator action, and it can only extend an interval that was
  just restarted by that same action.
- **When** the panel is ineligible — closed, mini, a different section than the stage, or a narrow
  viewport **Then** activity cancels any pending timer and arms nothing; the guards are unchanged.
- **When** the tab is hidden at expiry **Then** the collapse is skipped; on return a fresh interval
  starts (unchanged).
- **When** a scroll arrives while a modal, dialog or `.is-dragging` gesture is up **Then** it
  restarts nothing on its own; the deferral holds the collapse and a full interval follows the
  interaction (unchanged).
- **When** a scroll event fires on the rail — which has no scroller at wide width — **Then** it
  restarts the interval like any other rail activity; the listener is uniform across both surfaces
  so a future rail scroller needs no code change.
- **When** one deferred interaction ends in the same tick another begins (a dialog closes and a
  modal opens) **Then** the pair is treated as one continuous deferral — the collapse stays held and
  no interval restarts until the second ends. Conservative on purpose: the panel never collapses
  while something holds it, and the operator still gets a full interval at the end.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | The idle interval SHALL restart on any of exactly six events observed on `.rail` or `#panel` (the element or a descendant): `pointerdown`, `pointermove`, `keydown`, `focusin`, `wheel`, `scroll`. No other event SHALL restart it. | `reading/R44` (new) |
| FR-002 | `scroll` SHALL be observed in the **capture** phase on both surfaces, so a scroll of any descendant scroller counts. Today the only scroller in the first panel is `#panelBody`; this includes a scrollbar-thumb drag and keyboard scrolling, which emit `scroll` without `wheel`. | `reading/R44` (new) |
| FR-003 | A `focusout` that leaves the panel SHALL restart the interval; focus moving within the panel SHALL NOT (it is already activity through `focusin`). This rule is unchanged and stays on the panel only. | `reading/R44` (new) |
| FR-004 | Activity on any element outside those two surfaces SHALL NOT restart the interval — in particular the second sidebar (`#chapters`, its `.ch__body` scroller), the reading stage (`#read`, `#readBody`), global search results, the media library, dialogs and modals. Scrolling or pointing at them is not sidebar activity. | `reading/R44` (new); 072's out-of-scope list |
| FR-005 | Collapse SHALL still be deferred while a control inside the panel has focus, a modal or dialog is open, or a drag gesture is underway; the deferred expiry SHALL re-check every 1 s. Deferral itself is not activity and SHALL NOT restart the interval while it lasts. | `reading/R45` (new); 072's first clause |
| FR-006 | The interval SHALL be armed only while the viewport is wider than 720 px, `html[data-nav]` is `open`, and the first panel's section matches the reading stage's section. Otherwise activity SHALL cancel any pending timer and arm none. | `reading/R44` (new) |
| FR-007 | A hidden tab SHALL cancel the timer and becoming visible SHALL arm a fresh interval. | `reading/R44` (new) |
| FR-008 | The idle delay SHALL be 900 000 ms — fifteen minutes, replacing the 60 000 ms 072 chose — and the narrow cut-off SHALL stay 720 px. No setting, query parameter, data attribute or notification SHALL be added: the number SHALL exist once, as `IDLE_COLLAPSE_DELAY` in `static/web/reading.js`. | `reading/R44` (new) |
| FR-009 | The six events SHALL be written once per surface as a fixed list in `static/web/reading.js`, bound to `.rail` and `#panel` only; no `document`- or `window`-level activity listener SHALL be added, so widening the surface is always a deliberate edit with a test. | `reading/R44` (new) |
| FR-010 | The **end** of a deferral SHALL restart the interval in full at that moment: focus leaving the panel, `.is-dragging` clearing, a modal or dialog closing. An interaction that ends before expiry SHALL NOT leave the old deadline standing. The end SHALL be read from the deferral condition itself — its state or attribute turning false, or the element's own lifecycle notification — never as a seventh activity event and never by widening the activity surface to the element that held it. | `reading/R45` (new); 072's second clause |

### Key Entities

- **Activity surface** — the two elements whose events restart the interval: `<aside class="rail">`
  and `<aside class="panel" id="panel">`. Both are siblings; neither contains the other, the second
  sidebar, or the stage.
- **Idle interval** — one `setTimeout` at 900 000 ms (fifteen minutes), cleared and re-armed by each
  activity event and by each deferral end; only one is ever pending.
- **Delay** — the single constant `IDLE_COLLAPSE_DELAY` in `static/web/reading.js`; nothing else in
  the app, the markup or the URL may set it.
- **Deferral** — the four conditions that hold an expiry (focus inside the panel, `.ui.modal.visible`,
  `dialog[open]`, `.is-dragging`); it delays the collapse and then gives a fresh interval.
- **Deferral end** — the moment that set of conditions turns false again: focus leaves, the modal or
  dialog closes, the drag clears. It restarts the interval in full (FR-010) and is read from the
  condition itself, not from any pointer, key or scroll event.
- **Eligibility** — the three guards re-checked when arming and at expiry (wide viewport, `data-nav
  = open`, panel section equals stage section).

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | A scroll of the first panel's list restarts the fifteen-minute interval: still open at 899 s after the scroll, collapsed at 900 s. | New E2E — fails on `develop`, passes on this slice. |
| SC-002 | Wheel, pointer, keyboard and focus activity keep restarting it exactly as before, now at the new length. | Existing idle E2E (`test_rail_activity_restarts_sidebar_idle_timeout`, focus/modal/drag/narrow tests) with their fake-clock spans scaled to 900 s. |
| SC-003 | Scrolling the second sidebar or the stage for a full interval does not restart it — the panel collapses on schedule at 900 s. | New negative E2E for the second sidebar (and the stage where it can scroll). |
| SC-004 | Modal, dialog and drag still defer the collapse and a full interval follows. | Existing `test_dialog_defers…`, `test_drag_defers…`, scaled. |
| SC-005 | The wait is fifteen minutes: a page loaded and left alone collapses at 900 s, not at 60 s, and no setting, label or notification offers to change it. | Every idle E2E reads 899 000 / 900 000; `grep` finds the delay once, in `static/web/reading.js`. |
| SC-006 | A reorder drag released before the interval expires restarts it: still open 899 s after the release, collapsed at 900 s. | New E2E — fails on `develop`, passes on this slice. |
| SC-007 | A deferred interaction that outlives the interval still ends with a full interval — measured from the moment it ends, not up to one poll tick later. | Existing `test_drag_defers…` and `test_dialog_defers…` with their pins moved to 899 s/900 s after the interaction (the old numbers encoded the 1 s poll's slack). |
| SC-008 | Nothing else visible changes: the 720 px cut-off, the eligibility guards, the mini/closed outcomes and the existing transition all stay. | Full `tests/e2e/test_reading.py`; no control or class added. |

## UI/UX

n/a — nothing is drawn differently. The delay is deliberately longer — fifteen minutes instead of
one — but that is a timing change, not a visual one: the cut-off, the deferral, the resulting panel
state (mini for Alkitab, closed otherwise), the transition and every control stay as they are, and
no setting is added to expose the number. The slice changes whether an event the browser already
dispatches is observed, when the interval restarts after an interaction ends, and how long it runs.

## Assumptions

- **A1 — "intended" is spec 072's sentence, not a new model.** Pointer use, keyboard use, focus
  changes, or scrolling in the main rail or first panel counts as activity. This slice restores
  that sentence; it does not add a seventh event or a new surface.
- **A2 — a scroll is a scroll, whatever produced it.** The rule is about the event, not the input
  device: scrollbar thumb, wheel, keyboard and touch all count when they scroll the first panel.
  This is why the fix is a capture-phase listener rather than a `wheel`-only workaround.
- **A3 — the second sidebar stays out.** 072 put "second sidebar content" out of scope, and its
  collapse is not tied to the first panel's timer. Recorded here and pinned by SC-003 so the
  exclusion is a decision, not an accident.
- **A4 — the stage stays out.** 072 listed "the reading stage" out of scope; it is a separate
  surface with its own reading behaviour.
- **A5 — dialogs defer, they do not reset — until they close.** An open dialog holds the collapse
  (072). Closing it returns focus to the opener inside the panel, which already restarted the
  interval through `focusin`; FR-010 makes the same restart happen when focus returns elsewhere, so
  the dialog path stops depending on where focus lands. Its events are outside the activity surface
  by construction (`#editorModal` is a sibling of `#panel`).
- **A6 — programmatic scrolls count.** `scrollIntoView`/`scrollTop` produce the same `scroll` event
  as an operator drag and cannot be told apart without inventing a suppression flag. They occur only
  on operator navigation (centring the current book), where the same action already restarted the
  interval.
- **A7 — the rail has no scroller at wide width** (`.rail__menu` only scrolls inside the narrow
  drawer, where no timer is armed). Binding `scroll` on the rail is still uniform and free, and
  covers a future rail scroller.
- **A8 — `scroll` does not bubble.** The defect's mechanism; verified in the browser by SC-001's
  test failing on `develop` for the missing reset, not for a missing element.
- **A9 — patch bump.** The level maps from what changed (VER-10): the slice restores 072's rule and
  moves one constant inside it. It adds no capability (`minor`), breaks nothing (`major`), and
  removes nothing; `VERSION` moves at Fold. The changelog carries a `Fixed` line for the activity
  and deferral repair and a `Changed` line for the fifteen-minute wait.
- **A10 — the restart is immediate, and the pins move.** The old up-to-1 s wait came from the
  expiry poll, not from a rule. Restarting at the moment the interaction ends makes the collapse
  land exactly one interval later, so `test_drag_defers_sidebar_idle_collapse_then_restarts` and
  `test_dialog_defers_sidebar_idle_collapse_then_restarts` must assert open at 899 s and closed at
  900 s instead of open at one interval and closed at one interval plus a second. The tests keep
  their purpose; the slack they asserted was the bug, and the poll only remains for the expiry path.
- **A11 — the deferral end is not a seventh activity event.** FR-010 watches the four deferral
  conditions turn false. It may observe them directly — focus leaving the panel, `[open]` leaving
  the dialog, `.visible` / `.is-dragging` leaving their elements — but it SHALL NOT turn
  `pointerup`, `dragend`, a click or a scroll in `#chapters`, a dialog or a modal into activity: no
  listener that restarts the interval may live there, and a pointer move or a scroll in those places
  still restarts nothing (FR-004). The mechanism is chosen at Plan, with one constraint on it: the
  restart lands when the condition clears, not on a later poll tick, or the 899/900 s pins in A10
  are wrong and the test would be asserting the poll's slack again.
- **A12 — fifteen minutes is the owner's number, not a derived one.** It replaces 072's sixty
  seconds at the owner's request of 2026-11-18, and it stays a hardcoded constant: no setting, no
  query parameter, no per-page attribute (072 put "a new persistent timeout setting" out of scope,
  and this slice keeps that exclusion). The intended consequence is that a normal service will
  almost never reach the end of the interval — every rail or panel action restarts the full fifteen
  minutes — so the collapse now belongs to the long, quiet reading stretch. That is the point of
  the change, not a side effect to tune away.
- **A13 — 072 has no capability record, and this slice writes one.** `docs/spec/reading.md` begins
  at spec 126 and folds older behaviour only as a later slice touches it, so the idle rule — live
  since v1.8.0 — is unrecorded there. Fold adds `reading/R44` (the interval and its activity
  surface) and `reading/R45` (the deferral and its end), stating the rule as it now stands, with
  fifteen minutes rather than sixty seconds. They are new requirements, not a modification of an
  existing one, and the change to 072's number is recorded in this slice's Clarifications.

## Clarifications

### Session 2026-11-18

- Q: what may restart the idle interval? → A: spec 072's domain rule, verbatim: "Start or reset the
  idle interval while the first panel is open. Pointer use, keyboard use, focus changes, or
  scrolling in the main rail or first panel counts as activity." The six events in FR-001 are that
  sentence's implementation; nothing beyond it counts.
- Q: is a scrollbar drag "scrolling"? → A: yes. It emits `scroll` and no `wheel`; the current
  listener misses it. The capture-phase binding in FR-002 is the smallest change that makes the
  promise true for every way of scrolling the panel.
- Q: should the second sidebar start counting? → A: no. It was out of 072's scope and stays out;
  the exclusion is now written in FR-004 and pinned by SC-003 instead of implied by the markup.
- Q: does this change anything the operator can see? → A: no — see UI/UX. Only the moment the
  interval restarts changes, and only for scrolling that was already meant to count.
- Q (owner, on the first gate-1 pack): while dragging a service entry to reorder it, does the
  counter reset? → A: not while dragging — the grip is in the second sidebar, and `.is-dragging`
  defers. But the release restarted only when the drag outlived the interval, which is half of 072's
  "restart the interval when that interaction ends". Owner's answer: **"widen it"** — fold the
  deferral-end restart into this slice (FR-010, US2, SC-006/SC-007) rather than a card of its own.
- Q: does FR-010 make the second sidebar an activity surface after all? → A: no. The restart happens
  because a deferral ended, not because of anything the operator did in `#chapters`: a pointer move
  or a scroll there still restarts nothing (FR-004). Only a drag that was already holding the
  collapse produces a restart, and only when it ends.
- Q: does the same clause change modal and dialog timing? → A: it makes the rule uniform. Closing a
  dialog already restarted the interval whenever focus returned to its opener in the panel; FR-010
  covers the case where it does not, and stops the two paths disagreeing. Nothing is drawn
  differently either way.
- Q (owner, same day): "also increase the timer to 15 minutes." → A: FR-008 moves
  `IDLE_COLLAPSE_DELAY` to 900 000 ms. It supersedes 072's sixty seconds on that one number while
  keeping its activity and deferral rule intact; every idle E2E's fake-clock span scales with it;
  no setting is added, by 072's own exclusion and by the owner's "no unknown behavior".
- Q: is fifteen minutes a new capability or a change inside one? → A: a change inside the same rule.
  The delay is a constant of the interval 072 defined, not a new behaviour area; the capability file
  gains the rule for the first time (A13) and states it at fifteen minutes.
- Q: what happens during a service longer than fifteen quiet minutes? → A: the panel collapses once,
  exactly as 072 says, and the rail reopens it with a fresh interval. Fifteen minutes is long enough
  that this is the exception rather than the service's rhythm — which is why the number moved.

No `[NEEDS CLARIFICATION]` markers remain; no open decision is outstanding.
