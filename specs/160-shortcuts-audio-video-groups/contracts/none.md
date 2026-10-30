# Contracts: Audio and video name their play/pause key

**Spec**: `specs/160-shortcuts-audio-video-groups/spec.md`

## Interfaces exposed by this slice

**none** — no route, no endpoint, no payload, no template variable, no DOM id or class, no event and
no stored value is added, removed or re-shaped. `GET /projector?service=<id>` answers the same page;
the sheet inside it draws two groups more and one row fewer.

## Not exposed

The sheet's content is a contract with the operator's eyes, not with a program. Its markup classes
(`.sheet`, `.stack`, `.group`, `.row`, `.fn`, `.combo`, `.chord`, `.k`) are unchanged, and no script
reads them: `static/web/projector.js` selects the sheet only as `.keys` (the button) and by the
`keys-open` body class.

## What a test may nevertheless read

The rendered HTML of the projector page, which is where the requirements land — headings, rows,
labels and the Space cap — so the sheet's content is verifiable without a browser.
