# Spec 095: Immediate editor opening during form loads

- **ID:** 095
- **Status:** Accepted
- **Item:** ITEM-098
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** patch
- **Approved UI preview:** [./preview.html](./preview.html)

## Intent

When an operator opens an Add/Edit form on a slow connection, the modal should respond to the click immediately and show that the form is loading. Repeated clicks or late network responses must not queue extra modals or reopen one the operator has closed.

## Scope

### In scope

- Public-reading Add/Edit forms for songbooks, songs, and Tata Ibadah opened from sidebars.
- Current and legacy service-entry Add/Edit forms.
- The loading, success, cancellation, failure, and retry states while fetching form HTML.

### Out of scope

- Delete confirmations and mutation requests after a form is loaded.
- Edit-dependent options loaded inside an already-open form.
- Offline write queuing and unrelated admin editors.
- Changes to the shared toast's appearance or timing.

## Domain rules

- Each activation starts at most one form request. While any covered editor load is active, further activation cannot start another request or queue another modal.
- The existing editor modal opens synchronously on the initiating activation and shows its loading state while the request is pending.
- A successful active response replaces the loading content in the same modal and focuses the first usable form control.
- Dismissing a loading modal by Cancel, Esc, or backdrop aborts the request when supported and always invalidates its response. A canceled or stale response cannot open, close, or replace an editor and does not show an error toast.
- A failure from the current active request closes the loading modal and shows the existing “Could not load editor” toast. The loading state is released so another activation can retry.
- Once form HTML has loaded, the existing form fields, validation, and save behavior remain unchanged.

## UI details

- Match the [approved interactive preview](./preview.html). Keep the loading state inside the same centered editor modal used by the loaded form.
- **Size / spacing:** modal width is `min(490px, viewport width - 32px)`, maximum height is viewport height minus 40px, with a 1px divider border, 14px radius, and 24px content padding. The loading region has an 80px minimum height. Center the spinner and label horizontally and vertically as a single group. Place the 18×18px spinner above the label with a 10px gap. Keep the actions row below with an 18px top margin, 16px top padding, and the existing divider. Cancel is 38px high with 18px horizontal padding and a 9px radius.
- **Position / layout:** center the modal in the viewport over the existing dimmed backdrop. The loading spinner occupies its own row above the text. Keep the editor heading above the loading region and Cancel aligned to the lower-right in the actions row. Preserve this layout on narrow screens while respecting the modal's viewport width and height limits.
- **Colors / typography:** use the app's canvas and ink tokens, muted text token for the 14px regular “Loading editor…” label, divider token for the spinner track and modal borders, and the existing green accent for the spinner's leading arc. The heading is 20px semibold with 1.25 line height. Use the existing modal shadow and overlay; the approved preview shows a `0 20px 55px` shadow and an `#1618148a` backdrop. Match light and dark themes.
- **States:** pending shows the spinner, accessible loading text, and Cancel. Loaded state shows the existing form. Failure closes the modal and shows the existing failure toast. Cancel/Esc/backdrop closes the modal and returns focus according to existing editor behavior. Keep an accessible focus indicator and announce the loading text as a polite status.
- **Responsive behavior:** at viewport widths below the modal's maximum, use the available width minus 32px and constrain height to the viewport minus 40px. Keep spinner and label centered and actions reachable without horizontal overflow.
- **Motion:** rotate the spinner linearly once every 800ms. Follow reduced-motion preferences by stopping the rotation; the static spinner and loading text remain visible.

## Acceptance scenarios

### Scenario: immediate response on a slow form load

- **Given** a covered Add/Edit form request takes time to return
- **When** the operator activates its sidebar or entry control
- **Then** the editor modal opens immediately with the centered spinner above “Loading editor…” and a Cancel action
- **And** the status is announced without announcing each spinner frame

### Scenario: repeated activation while loading

- **Given** a covered editor is already showing its loading state
- **When** its opener or another covered Add/Edit control is activated again
- **Then** no duplicate request or queued modal is created, and the active loading state remains unchanged

### Scenario: successful form response

- **Given** a covered editor is loading
- **When** its current request succeeds
- **Then** the same modal replaces the loading state with the returned form without closing and reopening
- **And** focus moves to the first usable form control

### Scenario: cancel and stale response

- **Given** a covered editor request is still pending
- **When** the operator closes the modal with Cancel, Esc, or the backdrop and the old response later arrives
- **Then** the modal stays closed, no other editor is changed, and no failure toast is shown
- **And** the operator can open another editor immediately, whose response cannot be overwritten by the stale request

### Scenario: failed request and retry

- **Given** the active form request fails, including while offline
- **When** the failure is handled
- **Then** the loading modal closes and the existing “Could not load editor” toast appears
- **And** a subsequent activation starts a fresh request and can open the requested form

### Scenario: preserve loaded editor behavior

- **Given** a form has loaded successfully
- **When** the operator edits or submits it
- **Then** existing fields, validation, and save behavior remain unchanged

## Traceability

- **Domain/app tests:** none; this is browser-side request and modal coordination.
- **E2E:** `tests/e2e/test_immediate_editor_open.py`.
- **Implementation:** shared editor-load coordination in `static/web/editors.js` and `static/web/entries.js`, using the existing reading modal and toast infrastructure.
