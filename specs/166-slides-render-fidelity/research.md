# Research — spec 166

Every decision below was measured on this machine, on the reported deck
(`95a90f31…`, *Slide Warta Jemaat GKPS Klender Tgl 25 Oktober 2026.pptx*), against a reference render
of the same deck. **Unknowns remaining: 0.**

The reference is LibreOffice 26.2.6.3 on the host with `fonts-crosextra-carlito` installed. It is the
best available stand-in for PowerPoint: it is the same import path and the same export filter the
product uses, and the operator's own Impress screenshots are made with it.

## D001 — Move the image to Debian trixie for LibreOffice 25.2

**Decision.** Base the image on `python:3.12-slim-trixie`, which carries LibreOffice **25.2.3.2**.

**Rationale.** Measured, converting the deck and rendering each page at 96 dpi, RMSE against the
reference per page (lower is closer):

| page | 1 | 2 | 3 | 4 | 5 | 10 | 12 | 15 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 7.4 + Carlito | 8906 | 6543 | 11657 | 11560 | 4598 | — | — | — |
| 25.2 + fonts | **1823** | **1762** | **6872** | **6354** | **37** | — | **0** | **4647** |

The residual on pages 3, 4, 10 and 15 is sub-pixel: their words land within **0.7 pt** of the
reference, so the distance is antialiasing, not layout. On page 2 the table words are identical to
the reference to four decimals (`Minggu` at x 641.853496, y 8.777335 in both).

**Alternatives rejected.** *Stay on bookworm (7.4)* — the reported deck's band still wraps its amounts
and the tables stay 250–460 pt off; the complaint would not be fixed. *Hand-install 25.2 into
bookworm* — a downloaded `.deb` set that Debian does not support and that breaks on the next library
bump. *Ship a LibreOffice AppImage* — a 400 MB blob in the repo, unsignatured by Debian, and the same
maintenance problem.

**Provenance.** Measured here 2026-10-30; `python:3.12-slim-trixie` exists and `requirements.txt`
installs on it unchanged (Django 4.0.1, psycopg2 2.9.9, pypdf 5.9.0 verified in a clean container).

## D002 — Install the metric-compatible families and name the mapping explicitly

**Decision.** Install `fonts-crosextra-carlito`, `fonts-crosextra-caladea` and `fonts-noto-core` beside
`fonts-liberation`, and ship a fontconfig file that states the mapping rather than leaving it to
fontconfig's defaults.

**Rationale.** Today `fc-match Calibri` inside the image answers **Liberation Mono**. With Carlito
installed it answers Carlito — but the default Debian rules resolve *unlisted* families by family
order, which is how a proportional request landed on a monospace face in the first place. The shipped
file names every family the decks use, so the answer is a property of this deployment and not of
whatever fontconfig package happens to be installed:

| requested | drawn in | why |
| --- | --- | --- |
| Calibri, Calibri Light | Carlito | Carlito is metric-compatible with Calibri |
| Cambria | Caladea | metric-compatible |
| Arial | Liberation Sans | metric-compatible |
| Arial Narrow | Liberation Sans Narrow | metric-compatible |
| Times New Roman | Liberation Serif | metric-compatible |
| Courier New | Liberation Mono | metric-compatible |
| Britannic Bold, Berlin Sans FB Demi | Noto Sans Bold | no free metric equivalent; a proportional substitute, never a mono one |

**Alternatives rejected.** *Rely on Debian's `30-metric-aliases.conf`* — it maps Calibri→Carlito only
when Carlito is installed, and says nothing about the display faces; the failure mode observed here is
exactly an unlisted family. *Add only Carlito* — leaves `Britannic Bold` on whatever fontconfig picks.

**Provenance.** `fc-match` inside the running media container and inside a fresh trixie image,
2026-10-30; the deck's own font inventory read from `ppt/slides/*.xml`.

## D003 — The conversion command does not change

**Decision.** Keep `prlimit --as=2G --fsize=400M`, `--headless --convert-to pdf:impress_pdf_Export`,
the private `-env:UserInstallation` profile, the 120 s ceiling and the process-group kill.

**Rationale.** The command is not the defect; the renderer behind it is. Changing it would make the
slice's cause harder to read and would reopen the limits that spec 117 chose on purpose.

**Provenance.** `multimedia/local_media.py:416-435`; spec 117's decisions are unchanged by 25.2.

## D004 — The derivative's identity covers what changes the render

**Decision.** Key the derivative on **LibreOffice version + font inventory + a revision constant**
instead of the version alone.

**Rationale.** Today the key is `sha256(libreoffice --version)` (`local_media.py:362`). The operator
already has this deck converted; the fix would ship and the same wrong PDF would keep being served,
because the image's version did not change in their eyes (it changes here only because of D001). A
font installed later under FR-004 would reproduce the same trap. The font inventory is the sorted
family names `fc-list` reports, read before the conversion.

**Alternatives rejected.** *Bump a constant by hand on every change* — the constant is included, but
alone it relies on somebody remembering. *Delete the derivative directory on boot* — throws away
conversions that are still correct and makes the first projection of every service slower.

**Provenance.** `local_media.py:345-382`; the existing key test (`test_local_media.py:191`) already
asserts that a version change produces a new file.

## D005 — The operator's fonts are a mounted directory, re-scanned at start

**Decision.** Mount a host directory read-only at `/usr/share/fonts/operator` (compose variable
`GKPS_FONTS_DIR`, defaulting under the user's data directory) and run `fc-cache -f` from the
entrypoint when it exists.

**Rationale.** `Britannic Bold` and `Berlin Sans FB Demi` are Office fonts; they cannot be shipped, and
the operator has them. A mount keeps them out of the repository and out of the image, survives a
rebuild, and needs no code path: fontconfig finds them, and D004 notices.

**Alternatives rejected.** *Copy them into the image at build* — a proprietary font in a git-tracked
build context. *`docker cp` into a running container* — lost on every `up -d`.

**Provenance.** Owner's Clarify answer, 2026-10-30.

## D006 — The build refuses a monospaced fallback

**Decision.** A build step runs the same `fc-match` assertions the spec states and fails the build if
any listed family answers a face whose name ends in `Mono`.

**Rationale.** Every cause here is configuration, and configuration regresses silently. The guard is
four lines and turns "we fixed the fonts" into something the next image cannot undo by accident.

**Provenance.** The failure this slice fixes: `fc-match Calibri` → `LiberationMono-Regular.ttf`.

## D007 — Tests: one behaviour is the code's, the rest is the image's

**Decision.** Unit-test the derivative identity (fonts, version, revision, and the unchanged
convert-once behaviour) and extend the existing real-Impress test to assert that a converted deck
embeds no monospaced face. The image's font mapping and its build guard are `inspection`: they are
properties of a built artefact, not of a Python function.

**Rationale.** TDD governs behaviour the code owns. A test that shells out to `fc-match` inside a
developer's host would test the developer's machine, not the image.

**Provenance.** `test_local_media.py:169-207`; the repo's split between domain tests and E2E.

## D008 — The reported deck is the acceptance artefact, not a fixture

**Decision.** Keep the deck out of the repository. Its measurements are recorded in the spec and the
preview; the reproducible check on a fixture is the identity test and the no-mono assertion.

**Rationale.** The deck is 2.7 MB, carries names of congregation members, and belongs to the
operator's media library, not to the source tree.

**Provenance.** The conversion path already keeps uploads out of git (`.gitignore`, media root
`/var/lib/gkps-media`).
