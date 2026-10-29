# Data model: the preview's verse tabs get their own row

**Spec**: `specs/153-preview-tabs-row/spec.md`

No entity, no server state, no payload change. The slice re-parents one element and moves one focus call,
so the only model is the dialog's own DOM:

```
dialog.preview                        column flex; width min(44rem, 100vw - 32px)
├── div.preview__head                 title band, min-height 52px, rule unless a visible band follows
│   └── span.preview__title           the identity lifted from the payload (spec 085); ellipsis, one line
├── div.preview__versetabs            the band: present only for a song with > 1 verse; carries the rule
│   └── div.preview__tabs[role=tablist]   one 30px .preview__tab per verse, one selected
└── div.preview__body#previewContent  the scroller; tabindex=0; now the dialog's initial focus
```

Invariants this slice creates:

1. **The title band contains no focusable element.** `.preview__head` holds the title span alone, so it is
   never the reason focus lands somewhere.
2. **The tab band's presence is the head's rule condition.** The same `hidden` attribute that shows the
   band removes the head's rule (`:has(+ .preview__versetabs:not([hidden]))`), so the two cannot disagree.
3. **The body is the dialog's first focus target and its last tab stop.** With a visible tab band, Tab on
   the body returns to the selected tab; without one, the browser's own order stands.

Nothing is persisted and no request is added or removed: the payload the pane hands the dialog
(`script.entry__preview-src`) is unchanged.
