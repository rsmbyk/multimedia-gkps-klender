# Spec 075: Repeat a service-entry flash after it finishes

- **ID:** 075
- **Status:** Accepted
- **Item:** ITEM-078
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** patch

## Intent

Let the operator identify the same service entry on the Tata Ibadah page again by activating its sidebar row after the previous flash completes.

## Scope

### In scope

- Service-entry quicklinks in the Tata Ibadah second sidebar and the matching reading-stage entry flash.
- Pointer and keyboard activation, repeated clicks, and navigation that replaces the stage.

### Out of scope

- The longer sidebar reveal flash, other reading sections, and changes to the service order.

## Domain rules

- An eligible row activation scrolls the stage entry into view and starts the existing flash when no stage flash is active.
- While a stage flash is active, additional service-entry row activations do not restart it, start another flash, or queue a later one.
- On `animationend`, remove the flash class and release the guard. The next activation of that row or another row can flash normally.
- If the stage is replaced or the animation is suppressed for reduced motion, release the guard without waiting for an event from a detached or nonanimating node.
- A completed reorder gesture remains excluded from row activation.

## UI details

- **Approved preview:** [Sidebar follow-ups interactive preview](../072-sidebar-idle-collapse/preview.html), “Tata Ibadah” service-entry rows.
- **Size / position:** No layout or row geometry change.
- **Colors / typography:** Reuse `--active-flash` and existing stage text styles.
- **States:** Keep the current `tatibFlash` stage animation: 1.3 seconds, existing easing, held tint through 30% then transparent. During it, further row activations leave the active flash uninterrupted. After it, another click visibly replays the cue.
- **Responsive behavior:** The same rule applies wherever the service-entry list is available; preserve the current narrow-screen scroll/jump behavior.
- **Motion:** Honor reduced motion; a suppressed animation cannot lock out future activation.

## Acceptance scenarios

### Scenario: Repeat after completion

- **Given** a service entry has just flashed after its sidebar row was activated
- **When** the flash completes and the operator activates that row again
- **Then** the entry scrolls into view and flashes a second full time.

### Scenario: Activation during flash

- **Given** a stage entry is currently flashing
- **When** the operator activates the same or another service-entry row
- **Then** the current flash runs to completion without restarting or queuing another flash.

### Scenario: Stage changes

- **Given** a flash was active before navigation or stage replacement
- **When** the operator opens another Tata Ibadah page and activates a row there
- **Then** the new row can flash; no stale guard blocks it.

## Traceability

- Domain/app tests: N/A.
- E2E: `tests/e2e/test_reading.py` covers repeat after completion, clicks during an active flash, stage replacement, keyboard activation, and reduced motion. `tests/e2e/test_reorder.py` verifies a completed drag does not activate the quicklink or flash the stage entry.
- Implementation: `static/web/reading.js` owns the active flash lifecycle and releases it on animation completion, cancellation, reduced motion, or stage replacement. The existing `tatibFlash` animation in `static/styles/design/components.css` is reused.
