# Data Model: The first sidebar's idle rule, restored

**Spec**: `specs/199-sidebar-activity/spec.md`

## Entities

None. The slice changes *when* one existing `setTimeout` is cleared and re-armed; no record is
created, read, written or sent. There is no model, no migration, no request body and no browser
storage key.

## Invariants

- **At most one idle interval is pending.** `scheduleIdleCollapse` calls `cancelIdleCollapse` before
  it arms, and every restart path goes through `scheduleIdleCollapse` (FR-001, FR-010).
- **An armed interval exists only while eligible.** Narrow viewport, `html[data-nav] !== 'open'` or
  a panel/stage section mismatch arms nothing and cancels what was pending (FR-006).
- **A held deferral gives a full interval at its end.** While focus is in the panel, a modal or
  dialog is open, or `.is-dragging` is set, expiry does not collapse; when the last of the four
  clears, the interval restarts in full at that moment (FR-005, FR-010).
- **The delay is one value.** `IDLE_COLLAPSE_DELAY` is the only source of the 900 000 ms span, and
  nothing outside `static/web/reading.js` can set it (FR-008).

## Not modelled

- **The operator's intent.** The rule counts events and the deferral conditions, not what the
  operator meant by a scroll; a programmatic scroll counts the same as a dragged thumb (spec A6),
  and inventing a suppression flag would be a second, unstated model.
- **The deferral's duration.** Nothing records when a drag or dialog began; only whether one of the
  four conditions is currently true, and whether one was held across an expiry.
