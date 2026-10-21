# Plan 122: Saved reading page parity

- **Status:** Accepted
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-122
- **Bump:** patch

## Why

With a saved library, opening several reading routes from a menu or sidebar first shows client-rendered markup that differs from the same URL after reload. A later online refresh corrects some of it, but the mismatch is visible to the operator and remains when offline.

## Scope / edges

**In:** Parity of saved Home, Bible, Kidung, Tata Ibadah, and search reading views with their server-rendered equivalents, including filter placeholders, accessible sidebar headings, songbook references, song heading, empty-service actions, and related sidebar/stage markup. Preserve online freshness and offline use from Spec 119.

**Out:** New visual design, ordering or data freshness changes, projector/OBS, and editor save behavior (separate ITEM-121).

## Approach

Compare the browser DOM immediately after saved-library navigation with a reload of the same route. Make the saved renderer and page reconciliation produce the server's intended content and structure. Audit Home, Bible, Kidung, Tata Ibadah, and search list/detail paths so the same shell fields stay consistent across entry points.

## Verification

- Browser regression: seed/sync a saved library, navigate through first and second sidebars, compare the immediate saved render, settled online render, reload, and offline render at the same URL.
- Django checks for any serialized metadata needed to render the correct songbook heading.

## Risks

- Saved documents are built from a cached shell; correcting labels in the wrong layer may affect Bible pages or preserve stale state. Compare each section with server markup and test offline behavior explicitly.
