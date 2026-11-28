# Fold — spec 255

Date: 2026-11-28

Capability touched: `docs/spec/reading.md`.

Operations:
- **added** — `reading/R67`, "A template's Use template progress persists for seven days", with four
  scenarios (a new browser session resumes, the seven-day boundary, the button mark, Create consumes
  the draft).
- **modified** — `reading/R64`'s session-scoped statement is now superseded by R67 for the store and
  lifetime; R64 stays as the record of what spec 253 shipped, and R67 states the current rule.

Before: the `reading` capability carried R1–R66 (spec 257 took R66). After: R1–R67, with R67 stable
and not reusing a number. `last folded` stays 2026-11-28 and `255-use-template-progress-persist` is
prepended to `slices`.

No behaviour change beyond R67: the generate POST payload, the template records and R36 are
untouched. The leave confirmation's wording changed from "this browser session" to "this browser for
seven days" to match the new lifetime.