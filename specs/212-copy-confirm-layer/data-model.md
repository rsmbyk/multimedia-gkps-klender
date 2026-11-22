# Data model — spec 212

**No entity added, changed or removed.** This slice is stylesheet and test work: no model field, no
migration, no endpoint, no serializer, no template variable.

For the record, the two records the surface reads are unchanged from spec 167:

- **`tatib.TataIbadah`** — `name`, `date` (null for a template), `kind`, `is_active`. Read to render the
  modal's title (`Edit template` / `Edit Tata Ibadah`) and to decide whether `Copy as template` is
  offered (`copy_url` present on both kinds).
- **`tatib.ServiceEntry`** — untouched; the copy endpoint clones them and is not modified here.
