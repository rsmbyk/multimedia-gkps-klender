# versioning

**capability**: `versioning`
**last folded**: 2026-11-28
**slices**: `254-entity-versioning`

The concurrent-edit guard for the product's own write paths. A version is a counter on a row, not a
history: it names the state a writer opened so a stale write can be refused.

### R1 — Every tracked row carries a version

`TataIbadah`, `TataIbadahItem`, `ServiceEntry`, `Book`, `Song` and `Verse` SHALL each carry an integer
`version` starting at 1, including rows that predate this capability.

#### Scenario: a row is created
- WHEN any tracked row is created
- THEN its version reads 1

#### Scenario: migration of existing rows
- WHEN the migration completes
- THEN every pre-existing tracked row reads version 1 and no other stored value changes

### R2 — A no-op save leaves the version alone

A successful write SHALL increase the row's version by exactly one only when a stored value changes; a
save with identical values SHALL leave the row and its version untouched.

#### Scenario: identical values
- WHEN a form is saved without changing a field
- THEN the version is unchanged

### R3 — A stale write is refused

Every write to an existing tracked row SHALL carry the version the writer opened. A mismatch SHALL
return HTTP 409 and write nothing.

#### Scenario: two editors at version 5
- WHEN the second editor posts expected version 5 after the first write made the row version 6
- THEN the second write is refused and the row stays at version 6

### R4 — The check and the write are one act

The version comparison and the write SHALL share one transaction and a row lock; propagated service
rows SHALL be locked in primary-key order.

### R5 — Creates check their parent

A create SHALL NOT require an expected version for the new row, but a create inside a service SHALL
carry and check the parent service's version.

### R6 — Song changes reach every service that uses them

Any accepted change to a song or its verses SHALL increase the version of every active dated service and
template whose song entry names a live verse of that song.

### R7 — The conflict answer is machine-readable

A conflict response SHALL carry `error`, `message` and `current_version`. Presentation of the conflict
is outside this capability.
