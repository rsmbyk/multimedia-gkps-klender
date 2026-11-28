# Data model — spec 253

No Django model, migration or endpoint. The only new state is a client-side record in
`sessionStorage`.

## Template progress (browser session)

```
key:   gkps:generate:<templateId>
value: {
  v: 1,                       // record shape; other versions are ignored
  step: 1 | 2,                // which step the modal was on
  settled: {
    "<slotEntryPk>": {
      // a fill-in, from the editor's `editor:saved` detail
      label: string,
      data:  object           // the validate response, JSON-serialisable
    },
    // or a choice pick
    "<slotEntryPk>": {
      label: string, main: string, mute: string,
      title: string, body: string, option: number
    }
  },
  name: string,               // step-2 Name field
  date: string                // ISO yyyy-mm-dd from the hidden date input
}
```

- One key per template; no cross-template document.
- Written on: `editor:saved` for a pending slot, a chooser pick, name `input`, date `change`, and the
  Next/Back step transitions.
- Removed on: a successful Create response.
- Read on: every modal open. Unknown slot ids and records with `v !== 1` are discarded.
- Lifetime: the browser session (`sessionStorage`), not the disk-backed `localStorage`.

## Unchanged entities

- `tatib.ServiceEntry` / `tatib.Tatib` records: never written by this slice. FR-009 depends on it.
- The POST payload built by `submit()`: unchanged — saved progress is re-applied to the same dialog
  state, then submitted exactly as before.
