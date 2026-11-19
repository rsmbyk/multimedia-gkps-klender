# Contracts: The dock's bucket head owns the strip above its label

**Spec**: `specs/197-dock-bucket-head-pin/spec.md`

`none` — the dock page is server-rendered HTML whose only external surfaces (`/obs/dock`, the static
stylesheet it links) keep their existing contract. This slice changes a stylesheet's internal geometry: no
endpoint, no event, no storage key, no message between surfaces is added, changed or removed.