# Data Model: a Tata Ibadah is a service or a template

**Spec**: `specs/167-tata-ibadah-templates/spec.md`

## Entities

### TataIbadah

| Field | Type | Constraints | From |
| --- | --- | --- | --- |
| `id` | int | primary key | existing |
| `name` | char(64) | required | existing |
| `kind` | small int | `0` Service · `1` Template; set at insert, never written again; default `0` | FR-001, FR-002 |
| `date` | date | required when `kind=0`, must be empty when `kind=1` | FR-002, FR-003, FR-004 |
| `is_active` | bool | default true; unchanged by this slice | existing |
| `created_at` | datetime | auto | existing |

**Relationships**: `TataIbadah` 1—n `ServiceEntry` (`service_entries`), and 1—n `TataIbadahItem`
(`tataibadahitem_set`, legacy) — both share one `order_number` sequence.

**Validation**
- `clean()` and `save()` both refuse `kind=SERVICE` with no date and `kind=TEMPLATE` with one (FR-002).
- `save()` derives the kind when an insert names none — no date → `TEMPLATE` — so every existing writer
  keeps working (A10), then refuses a change of `kind` on an existing row (FR-001).
- DB `CheckConstraint`: `(kind = 0 AND date IS NOT NULL) OR (kind = 1 AND date IS NULL)`.

**State transitions**: `created (kind fixed) → edited (name, date within the kind) → deleted/archived`.
`kind` never changes; the only path from Service to Template is a copy (FR-020…FR-022).

**Migration**: `002x_tataibadah_kind` adds the field nullable, backfills `TEMPLATE` where `date IS NULL`
and `SERVICE` elsewhere, then makes it non-null, adds the constraint. No entry is touched (FR-006).

### ServiceEntry

| Field | Type | Constraints | From |
| --- | --- | --- | --- |
| `kind` | small int | existing `0…4`, plus `5` Fill-in and `6` Choice | FR-007, FR-008, FR-009 |
| `fill_kind` | small int, null | required for `5`/`6`; one of `0` (text), `1` (passage), `2` (song), `4` (media) | FR-008, FR-009 |
| `parent` | FK self, null | set only on an option; must point at a `CHOICE` entry of the same Tata Ibadah; `CASCADE` | FR-009 |
| `title` | char(64) | optional; the slot's title/note, and the choice's title | FR-008, FR-009 |
| `order_number` | positive int | unchanged, shared with legacy rows | existing |

**Relationships**: a `CHOICE` entry 1—n options (`related_name='options'`), each an ordinary entry of the
choice's `fill_kind`. A `FILL_IN` entry has no children.

**Validation** (`ServiceEntry.clean()`)
- `kind in (FILL_IN, CHOICE)` requires `tatib.kind == TEMPLATE`; a Service refuses both (FR-010).
- `kind in (FILL_IN, CHOICE)` requires a `fill_kind`, and no content of its own (FR-008).
- An option (`parent` set) must belong to the same Tata Ibadah as its parent, must be the parent's
  `fill_kind`, and must not itself be a `FILL_IN`/`CHOICE` (FR-009).
- A `FILL_IN`/`CHOICE` may have zero options; the type is valid, the generation is not (FR-015, edge case).
- Everything the existing per-kind rules say stays exactly as it is — a choice's song option is a song
  entry, and it validates like one.

**State transitions**: `authored on a template → copied into a generated service as its own kind`.
A fill-in never reaches a service; a choice becomes its chosen option (FR-018).

## Invariants

- **INV-1** — `kind` and `date` agree on every Tata Ibadah, at every write (FR-002, SC-001).
- **INV-2** — `kind` of a Tata Ibadah never changes after insert (FR-001).
- **INV-3** — a fill-in or choice exists only on a template (FR-010).
- **INV-4** — an option's kind equals its choice's `fill_kind`, and its Tata Ibadah is the choice's (FR-009).
- **INV-5** — a generated service contains no `FILL_IN`, no `CHOICE` and no entry with a `parent` (FR-018,
  SC-006).
- **INV-6** — generating or copying leaves the source's rows untouched, field for field (FR-019, SC-004).

## Not modelled

- **A slot's resolution before Create.** Nothing is stored: the modal holds the validated form data in the
  browser and the generate endpoint replays it (D003). A "draft resolution" row would have to be deleted on
  abandon, and an abandoned modal must store nothing (FR-019).
- **Generated-from provenance.** A generated service does not record which template it came from: the spec
  asks for no such link, and a dangling reference to a deleted template would be a new failure mode. If a
  later slice wants "used by" reporting, it adds the field with its own requirement.
- **A template's own projection state.** Templates never reach the display (FR-012), so no display-side row,
  flag or payload represents one.
