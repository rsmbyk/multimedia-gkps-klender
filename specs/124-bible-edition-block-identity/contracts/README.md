# Contracts: Keep a chapter's verse text when the reading page updates in place

**Spec**: `specs/124-bible-edition-block-identity/spec.md`

## Interfaces exposed by this slice

none — the correction is inside a browser script's node-identity lookup; no request, response, event, or
public function contract changes.

## Not exposed

The reconciler's internals (`nodeIdentity`, `reconcileChildren`) stay private to `static/web/reading.js`;
the slice changes which attribute identifies a node, not what any caller may pass or expect.
