# Data model: the live entry header's corners follow its pin state

No data-model change. The slice edits paint state (a CSS class), a DOM-only clone of an existing
header, and two list-level slots in the dock runner. No model, field, migration, endpoint or
persisted state is added or changed.

The display state written by the pin's click is the same centre act the existing control uses
(R15); this slice does not introduce a new write.
