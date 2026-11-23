# Contracts: a created Template opens on the stage

**Spec**: `specs/234-open-created-template/spec.md`

none — the editor save response (`record_kind`, `created`) and the shell's in-place `navigate()`
are existing internal interfaces; this slice only chooses a different URL for one of them. No HTTP
endpoint, payload shape, storage schema or public interface changes.
