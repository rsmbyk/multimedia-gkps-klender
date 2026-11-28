# Fold — spec 253

Date: 2026-11-28

Capability touched: `docs/spec/reading.md`.

Operations:
- **added** — `reading/R65`, "A template's Use template progress survives a close", with four
  scenarios (settled work kept per template, resumed on open, a dirty close says so, and a
  successful Create consumes it).

Before: the `reading` capability carried R1–R64 (spec 252 took R64 first). After: R1–R65, with R65 stable and not reusing a
number. Header `last folded` moved from 2026-11-27 to 2026-11-28 and `253-use-template-progress`
was prepended to `slices`.

No behaviour change beyond R65: the generate POST payload, the template records and the existing
R36 rule (generating or abandoning leaves the template byte-identical) are untouched.
