# Data model

`n/a — no stored state. A group is a rendered <section class="group"> derived from its rows.`

The delete endpoints, models and migrations are unchanged; the only server edit is a conditional in
`_tatib_groups()` that suppresses an empty rendered group. See [contracts/none.md](contracts/none.md).
