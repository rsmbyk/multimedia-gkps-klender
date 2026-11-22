# Data model

None. Focus is transient browser state: this slice stores nothing, adds no record, no key and no
interface. The tab-local search snapshot (`sessionStorage`, `gkps-search-entry:<id>`) is read as it is
today and is not written by the focus behaviour.