# Data model — spec 255

No Django model, migration or endpoint. The state is a browser-local record; this slice changes its
store and lifetime, not its fields.

## Template progress (browser disk)

```
key:   gkps:generate:<templateId>
store: window.localStorage
value: {
  v: 2,
  step: 1 | 2,
  settled: { "<slotEntryPk>": <fill-in state | choice state> },   // unchanged from spec 253
  name: string,
  date: string,          // ISO yyyy-mm-dd
  savedAt: number        // Date.now() at the last write; the 7-day clock
}
```

- **Lifetime**: 168 h from `savedAt`. `liveRecord(id)` returns `null` and removes the key when
  `Date.now() - savedAt > 168h`; `v !== 2` is treated the same way.
- **Writes**: every settled slot, choice pick, name `input`, date `change`, Next and Back rewrites
  the record with a fresh `savedAt` (the clock slides).
- **Removal**: a successful Create; expiry on read; the start-up sweep removes expired keys.
- **Legacy**: a `sessionStorage` record from spec 253 is not read. `clearSaved()` also removes that
  key when present, as housekeeping.

## Button state (transient DOM, not stored)

| Field | Values | Meaning |
| --- | --- | --- |
| `data-draft` | `"true"` / absent | the button is marked with the saved dot |
| `aria-label` | `"Use template, draft saved"` / absent | the accessible name carries the state |
| child span `.read__draft-dot` | present, `aria-hidden="true"` | the 7 × 7 px dot; shown only when `data-draft="true"` |

## Unchanged entities

- `tatib.ServiceEntry` / `tatib.Tatib` records: never written by this slice (FR-009, R36).
- The POST payload from `submit()`: unchanged.