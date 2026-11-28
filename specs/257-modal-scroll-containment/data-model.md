# Data model

`n/a — no stored state. The change is two CSS declarations in the shared design stylesheet.`

No model, migration, endpoint, session key or DOM attribute changes. The only behaviour added is a
root `overflow` state derived from `dialog[open]` and per-scrollport `overscroll-behavior` values.
See [contracts/none.md](contracts/none.md).
