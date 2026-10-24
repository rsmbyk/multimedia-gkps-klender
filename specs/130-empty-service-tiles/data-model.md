# Data model

`n/a` — nothing is stored or transmitted by this slice. The block is derived state: the server template
reads `items` (empty), the saved renderer reads the cached service's `items` array (empty), and the
delete-rebuild counts the DOM rows that are left. No model, serializer, view signature or fragment contract
changes.
