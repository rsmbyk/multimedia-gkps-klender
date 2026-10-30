# Tasks — spec 166

Order used: Setup → Foundational → US1 → US2 → US3 → Polish. `[P]` marks order-independent work; the
run is one agent in one thread, so the order below is the order taken.

## Setup

- [X] T001 Add `fonts-crosextra-carlito`, `fonts-crosextra-caladea` and `fonts-noto-core` to the
      `apt-get install` line in `Dockerfile`, moving the base image to `python:3.12-slim-trixie` —
      and `fonts-liberation-sans-narrow`, which trixie keeps out of `fonts-liberation`.
- [X] T002 Write `docker/slides-fonts.conf`: one `<alias>` per family in `research.md` D002, plus the
      generic families bound to proportional faces.
- [X] T003 Copy the file to `/etc/fonts/conf.d/99-gkps-slides.conf` in `Dockerfile` and run `fc-cache -f`.
- [X] T004 Mount `${GKPS_FONTS_DIR:-$HOME/.local/share/gkps-fonts}` at `/usr/share/fonts/operator`
      (read-only) on the `media` service in `docker-compose.yml`.
- [X] T005 Run `fc-cache -f` from `docker/entrypoint.sh` when `/usr/share/fonts/operator` exists.

## Foundational

- [X] T006 Write the failing test `test_a_monospaced_answer_is_a_violation` — `multimedia/test_local_media.py`,
      over `slide_fonts.violations` with a mapping that answers `Liberation Mono` for `Calibri` — and run
      it to see it fail (it returned `[]`).
- [X] T007 Add `multimedia/slide_fonts.py`: `FAMILIES`, `mapping()`, `violations()`, `main()`; make T006 pass.
- [X] T008 Run the guard from the `Dockerfile` after `COPY . .`, so a regressed mapping fails the build.

## US1 — a converted page lands where the deck draws it

- [X] T009 Build the image and read the mapping back: every family proportional, `Calibri` → Carlito,
      LibreOffice 25.2 or newer. `quickstart.md` §1–§2.
- [X] T010 Convert the reported deck through the built image and compare page 1's title ink, page 3's
      words and page 2's band against the reference (`quickstart.md` §3).
- [X] T011 Record the measured numbers in `converge.md`.

## US2 — a converter change re-renders what was already converted

- [X] T012 Write the failing test `test_converter_identity_changes_when_the_fonts_change` — same
      LibreOffice version, a different `fc-list` answer, two derivatives — and run it to see it fail
      (both requests resolved to one file).
- [X] T013 Add `CONVERTER_REVISION`, `font_inventory()` and `converter_identity()` to
      `multimedia/local_media.py`, and key `slide_pdf()` on the identity; make T012 pass. The real-Impress
      test also gained the no-monospaced-face assertion (`converge.md` F3).
- [X] T014 Keep `test_converter_version_changes_cache_key` green with its assertions unchanged.

## US3 — the operator can supply the faces only their Office has

- [X] T015 Drop a TTF into a directory mounted at `/usr/share/fonts/operator`, start the image, and read
      back both the new family and the new derivative key (`1ff909dc0f66d2b9` → `da61d371f6fe5fec`).
      Exercised with `docker run` rather than a full `docker compose up`, which needs `.env`'s
      production origin.
- [X] T016 Record the procedure in `docs/local-media-companion.md`, where the operator looks.

## Polish

- [X] T017 Update `docs/spec/media-library.md`: R2 (the mapping and the version floor), R3 (the identity),
      R4 (the operator's directory) — `fold.md` records the before/after counts.
- [X] T018 Add one `CHANGELOG.md` line under `## [Unreleased] → Fixed`, and move `VERSION` 1.23.2 → 1.23.3.
- [X] T019 Card `ITEM-178` on the board and add its row to the `In progress` column.
- [X] T020 Run `python manage.py test multimedia` (439 tests, OK) and record the result in `converge.md`.
