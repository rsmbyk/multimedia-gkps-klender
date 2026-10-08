# Plan 026: Keep editing while projecting, and keep the display in step

- **Status:** Accepted (owner, 2026-10-08)
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-028
- **Bump:** minor

## Why

While a Tata Ibadah is on screen the operator has one hand tied:

1. **The edit ban.** `static/web/display.js` exposes `window.gkpsDisplay.locked()`, and
   `static/web/entries.js` and `static/web/reorder.js` silently refuse add / edit / delete /
   reorder while this browser is projecting. The lock is **client-side only** — the server has no
   projection guard — so this is the shell declining the click, nothing more.
2. **Reorder is transactional.** `static/web/reorder.js` runs a *mode*: a drag only previews, and
   nothing is written until **Save**, with a **Discard** and a leave-confirm dialog
   (`window.gkpsUnsaved`, `beforeunload`).
3. **The projector is stale until asked.** Each screen is baked into the projector's HTML at load;
   only the **Update the current state** button posts `{type:'update'}` and makes
   `static/web/projector.js` re-read the page. No write endpoint notifies anything.

The operator wants to keep working while projecting, have a drop take effect at once, and have the
display follow every change without pressing Update.

## Scope / edges

**In:**

- Remove the client-side edit ban for entry add / edit / delete (new entries *and* legacy old rows)
  and for reorder.
- Make a reorder take effect immediately on drop (and on a keyboard grip move): write the new order
  at once, with no mode, no Save/Discard, and no leave prompt.
- After every successful add / edit / delete / reorder, have the running projector re-read, so the
  on-screen content follows.

**Out:**

- OBS browser sources and second-laptop fan-out (would need server push).
- Server-side projection state, new endpoints, or any change to the `web-entry-reorder` contract.
- Any OBS dock / source / settings page, and the legacy DRF API shapes.
- The **Update the current state** button — it stays as the manual re-read for edits made from
  another browser or screen.
- Any UI/a11y change beyond removing the reorder mode's chrome.

## Approach

### (A) Lift the edit ban

- `static/web/entries.js` — delete the delegated click guard that consults
  `window.gkpsDisplay.locked()`; all add / edit / delete controls work while projecting.
- `static/web/reorder.js` — delete the lock check that refuses a reorder.
- `static/web/display.js` — drop the lock surface (`locked()`, `refuse()`, the reason string) from
  `window.gkpsDisplay`. Keep the display state, the Project / Stop projecting toggle, `sync()`, the
  heartbeat and its watchdog, and the channel.

### (B) A reorder applies on drop

- `static/web/reorder.js` — remove the reorder *mode*: its state, the Save/Discard listeners, the
  leave-confirm dialog handlers, `window.gkpsUnsaved`, and the `beforeunload` guard. Keep the drag
  and keyboard gestures, the live sidebar preview, the pane following, and the morph.
  - On a **drop**, and on a **keyboard move**, POST the current order to the existing endpoint
    (`web-entry-reorder`, the same `{tatib, entries:[{entry, order_number}]}` body the mode's Save
    used), then fire `editor:saved`.
  - **Serialise the writes:** one request in flight at a time; keep only the newest order and send
    it when the current one settles, so a burst of drops cannot land out of order.
  - **Throttle the keyboard:** a held arrow key coalesces to the final order before one write.
  - Keep a slim `[data-reorder-group]` carrying `data-reorder-endpoint` and `data-reorder-for`, plus
    a status line for a failed write.
- `multimedia/web/templates/reading/base.html` — remove the Save and Discard buttons; keep the group
  as the endpoint/status carrier.
- `multimedia/web/templates/reading/tatib.html` — delete the `#reorderConfirm` dialog.
- `static/web/reading.js` — drop the `window.gkpsUnsaved` check from its in-page `navigate()`.

### (C) The projector follows every change

- `static/web/display.js` — one hook: on the `editor:saved` event, when this page's service is the
  one being displayed, post `{type:'update'}` on the channel. The existing **Update the current
  state** button calls the same code.
  - `editor:saved` already fires after an entry save/delete (`entries.js`), after a sidebar editor
    save (`editors.js`), and — newly — after a reorder write, so this one seam covers every case.
- `static/web/projector.js` — add cache-busting to the update read (`{cache:'no-store'}` or a
  timestamped query) so two close updates cannot show the previous page.

## TDD

- Domain / app tests: `multimedia/web/tests.py` — the reorder pane renders the endpoint carrier and
  no longer renders the Save / Discard buttons or the confirm dialog. The `web-entry-reorder`
  endpoint tests are unchanged (its contract does not move).
- E2E: `tests/e2e/test_projector.py` — editing is allowed while projecting; the display follows an
  add, edit, delete and reorder without pressing Update; Update still works.
  `tests/e2e/test_reorder.py` — a drop and a keyboard move persist with no Save, and leaving or
  switching never prompts.

## Risks

- **Losing the safety net.** Removing the lock lets a projecting browser edit the very service on
  screen; that is the requested behaviour, and the projector always re-reads from the server, so it
  cannot show a phantom order.
- **Write races.** Rapid drops must serialise to the newest order, or a late response could
  reintroduce a stale one.
- **A stale update read.** The projector's un-cached fetch is the fix; without it a follow-up update
  can render the previous page.
- **Test churn.** The old lock and mode are encoded in spec 006's slice-3/slice-4 E2E; those cases
  are rewritten, and the specs they assert against are amended so the contracts stay truthful.
