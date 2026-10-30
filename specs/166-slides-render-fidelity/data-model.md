# Data model — spec 166

No database table, model, migration or payload changes. The slice touches one stored artefact and the
identity that names it.

## Derived PDF

| Field | Value |
| --- | --- |
| Path | `<media root>/derived-slides/<sha256>-<key>.pdf` |
| `<sha256>` | the source deck's SHA-256, as today — the derivative is named after the file it came from |
| `<key>` | 16 hex characters of `sha256(identity)`, where `identity` is defined below |
| Lifecycle | written once per identity; reused while the identity holds; removed with its source (`remove()` → `_purge_slides()`), and by nothing else |
| Validity | a file counts only if it is a PDF (`%PDF-` head, `%%EOF` tail), at most 400 MB, and opens with at least one page — unchanged |

**Invariants**

1. Two requests for the same deck under the same identity produce one file and one conversion.
2. Two requests for the same deck under different identities produce two files; either may be served,
   the newer one wins by being requested after the identity changed.
3. A failed or timed-out conversion writes no file (it is written to a temporary directory and moved
   into place only after the validity check).
4. The library's own record — `files` row with `sha256`, `name`, `family`, `size`, `uploaded_at`, the
   `reference_inventory` protection and the 30-day deadline — is untouched by any of this.

## Converter identity

```
identity  = libreoffice --version  ⏎  CONVERTER_REVISION  ⏎  font inventory
key       = sha256(identity).hexdigest()[:16]
```

| Part | Source | Why it is in the identity |
| --- | --- | --- |
| `libreoffice --version` | `subprocess.run(['libreoffice', '--version'])`, unchanged | the import and layout engine decides where text lands |
| `CONVERTER_REVISION` | a module constant, `1` at this slice | a change to the export command or a deliberate re-render, without waiting for a version bump |
| font inventory | the sorted family names `fc-list : family` reports, read before each conversion | a font added under FR-004 changes the render exactly as much as a version bump |

**Invariants**

1. The identity is read before the conversion and is not re-read for that conversion.
2. If `fc-list` is missing or fails, the inventory is the empty string and the key still changes with
   the version — the conversion never fails because of the identity.
3. The identity is computed under the same lock as the conversion, so two concurrent requests cannot
   see two identities for one render.

## Font mapping

| Field | Value |
| --- | --- |
| Where | `/etc/fonts/conf.d/99-gkps-slides.conf` in the image |
| Contents | one `<alias>` per family the decks use, from the table in `research.md` D002, plus generic families bound to proportional faces |
| Read by | fontconfig, and therefore LibreOffice; the application never parses it |
| Change procedure | edit the file, `fc-cache -f`, rebuild the image; the identity then changes because the inventory did |

## Operator font directory

| Field | Value |
| --- | --- |
| Host path | `${GKPS_FONTS_DIR}`, defaulting to the user's data directory rather than the repository |
| Container path | `/usr/share/fonts/operator`, read-only |
| Contents | TTF/OTF files; nothing is parsed or validated by the application |
| Activation | `fc-cache -f` from `docker/entrypoint.sh` when the directory exists; absent or empty means today's behaviour |
