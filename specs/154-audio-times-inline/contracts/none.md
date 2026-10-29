# Contracts: none

**Spec**: `specs/154-audio-times-inline/spec.md` · **Created**: 2026-10-29

This slice changes the markup and CSS of one rendered line. It exposes no external interface: no HTTP
route, no API payload, no companion endpoint, no event, no storage format. The preview markup travels to
the browser inside the page's own `<script type="text/template" class="entry__preview-src">` block, so
there is not even a response shape to pin.

`none` — declared, not absent.
