# Data model: A whisper of a tint on an open entry header

**Spec**: `specs/206-dock-expanded-tint/spec.md`

**No entities.** The slice changes one CSS declaration. No model, migration, fixture, template,
storage key or endpoint is touched. The state the rule reads — `aria-expanded` on `.entryrow` — is
already written by spec 198's `paintEntry()` and already exposed to assistive technology.

The only shapes involved are the two colours and their relationship:

| Value | Light | Dark |
| --- | --- | --- |
| `--rail-bg` (the row's surface) | `#EDEAE3` | `#232019` |
| `--ink` | `#1F1F1D` | `#F5F3EE` |
| Wash — rail 96 %, ink 4 % | `#E5E2DB` (8-level step) | `#2B2822` (8–9) |
| Hover face — `--icon-hover-bg` | `#DDDAD3` (16-level step) | `#37342E` (20) |
| Live fill — `--sidebar-selected-bg` | `#B9D7C9` | `#393F4F` |
