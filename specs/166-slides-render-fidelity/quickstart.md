# Quickstart — spec 166

Contracts: [`contracts/http.md`](contracts/http.md) · data model: [`data-model.md`](data-model.md).

## 1. The image's font mapping (inspection, inside the built image)

```sh
docker compose build media && docker compose up -d media
docker exec multimedia-gkps-klender-media-1 sh -c \
  'for f in Calibri "Calibri Light" Cambria Arial "Arial Narrow" "Times New Roman" "Britannic Bold" \
        "Berlin Sans FB Demi"; do printf "%-22s %s\n" "$f" "$(fc-match -f "%{family}" "$f")"; done'
```

Every line must name a proportional family; none may contain `Mono` except `Courier New`.

## 2. The version floor (inspection)

```sh
docker exec multimedia-gkps-klender-media-1 libreoffice --version   # 25.2 or newer
```

## 3. The reported deck (manual, on the operator's machine)

Convert the deck through the running companion, then compare it with the reference render placed
beside it in the preview:

```sh
curl -sS -H "Origin: http://localhost:63404" \
  "http://127.0.0.1:63174/v1/slides/<sha256>" -o deck.pdf
pdftoppm -r 96 -png deck.pdf deck
```

Open `preview/index.html`: page 1's title must read 477 × 199 px, page 3's words within 1 pt, page 2's
band 5 words. The measured numbers are in `spec.md` §UI/UX.

## 4. The tests

```sh
python manage.py test multimedia.test_local_media --keepdb
```

Named cases:

- `test_converter_identity_changes_when_the_fonts_change` — new
- `test_converter_identity_changes_when_the_version_changes` — the existing
  `test_converter_version_changes_cache_key`, kept
- `test_real_impress_converts_verified_pptx_when_installed` — extended with the no-mono assertion
- `test_slide_display_keeps_original_identity_and_reuses_private_pdf`,
  `test_concurrent_slide_requests_share_one_conversion` — unchanged

## 5. What cannot be run here

- **PowerPoint.** There is none on this machine, so the golden render is LibreOffice 26.2 with the same
  font mapping, and the deck's own Impress view is the tolerant target.
- **The operator's fonts.** `Britannic Bold` and `Berlin Sans FB Demi` are not on this machine; their
  effect is verified by mounting any TTF into `/usr/share/fonts/operator` and watching the identity
  change, not by measuring the deck's cover.
