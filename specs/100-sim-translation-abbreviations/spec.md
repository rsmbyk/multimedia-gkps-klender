# Spec: Use the requested SIM book abbreviations

- **ID:** 100
- **Status:** Accepted
- **Item:** ITEM-100
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Preview:** [./preview.html](./preview.html)
- **Bump:** patch

## Intent

Give SIM books their own short codes while retaining their full Simalungun names. Make the
Bible sidebar, testament headings, three named book searches, and Bible verse heading use
the appropriate edition.

## Scope

### In scope

- Store the owner's 66 SIM short codes on existing database rows and in fresh Bible seed data.
- Show the selected edition's code in each Bible mini-sidebar tile, online and from a saved copy.
- Show the selected edition's testament names in the Bible sidebar and passage book picker.
- Accept both TB and SIM codes in the Bible sidebar filter, projector Go To, and new/edit
  passage book picker.
- Show the full name of the edition actually supplying the visible verses above a Bible chapter.
- Translate only the three main sidebar rail popups for the remembered Bible edition.
- Preserve existing full book names, verse data, sidebar navigation, and edition persistence rules.

### Out of scope

- Renaming canonical `Book.name` keys or replacing full `BookTranslation.translation` names.
- Changing Bible verse text or projection content.
- Changing how long a Bible edition choice persists under accepted spec 099.
- Changing when the Bible seed workflow runs during deployment.

## Data contract

- `BookTranslation.translation` stays the full translated book name: for example, TB “Kejadian”
  and SIM “1 Musa.” A per-translation abbreviation stores SIM “1Mu” separately.
- The existing canonical `Book.name` is the TB short code, such as “Kej.” If a book has no SIM
  abbreviation, its mini tile may use that TB code as a fallback.
- The 66 SIM abbreviations below map to existing canonical `Book.name` keys. Case and digits
  are part of the value:

```text
Kej=1Mu  Kel=2Mu  Ima=3Mu  Bil=4Mu  Ula=5Mu
Yos=Jos  Hak=Pah  Rut=Rut  1Sa=1Sa  2Sa=2Sa
1Ra=1Ra  2Ra=2Ra  1Ta=1Kr  2Ta=2Kr  Ezr=Esr  Neh=Neh  Est=Est
Ayb=Job  Mzm=Psa  Ams=Pod  Pkh=Par  Kid=Dod  Yes=Jes  Yer=Jer  Rat=Tan  Yeh=Hes
Dan=Dan  Hos=Hos  Yoe=Joe  Amo=Ams  Oba=Obj  Yun=Jon  Mik=Mik  Nah=Nah  Hab=Hab
Zef=Sef  Hag=Hag  Zak=Sak  Mal=Mal
Mat=Mat  Mrk=Mrk  Luk=Luk  Yoh=Joh  Kis=Lah  Rom=Rom  1Ko=1Ko  2Ko=2Ko  Gal=Gal
Efe=Epe  Flp=Pil  Kol=Kol  1Te=1Te  2Te=2Te  1Ti=1Ti  2Ti=2Ti  Tit=Tit  Flm=Plm
Ibr=Heb  Yak=Jak  1Pt=1Pt  2Pt=2Pt  1Yo=1Jo  2Yo=2Jo  3Yo=3Jo  Yud=Jud  Why=Pak
```

- A data migration adds and fills the abbreviation on existing SIM rows in place, retaining
  their primary keys and `Verse` foreign keys. The Bible seed keeps the current full-name file
  and adds this abbreviation mapping. Re-running the seeder updates the same SIM row without
  creating another translation row.
- The saved offline Bible library includes the SIM abbreviation. A previously saved library
  without that field remains readable and uses the existing TB code until refreshed.

## Edition and label rules

- The Bible sidebar uses the last deliberate TB/SIM choice in the current page visit, as in
  spec 099. It keeps that preference through in-page menu switches, chapter navigation, and
  Back/Forward. A normal full reload starts from TB; an explicit `?ed=sim` URL starts from SIM.
- In TB, mini tiles show the canonical TB codes. In SIM, they show the matching SIM codes.
  Changing edition updates visible tiles in place, including a mini sidebar already open.
  Expanded rows continue to show full TB and SIM names in their existing positions and order.
- Bible sidebar group headings use “Perjanjian Lama” and “Perjanjian Baru” in TB, and
  “Padan na Basaia” and “Padan na Baru” in SIM. The passage book picker uses the same headings
  for its own TB/SIM toggle: new passage starts on TB; editing a saved SIM passage starts on SIM.
- If a chapter has no verses in the remembered edition, the existing verse fallback remains.
  Sidebar mini codes and group headings continue to follow the remembered choice. The heading
  above the verses follows the edition whose text is actually visible.
- On a Bible chapter, the stage book name and browser page title use the full name of the visible
  verse edition: for example, “Kejadian 1” in TB and “1 Musa 1” in SIM. They update on a live
  toggle, direct URL load, in-page navigation, Back/Forward, and saved-copy rendering.
- The initial server response for an explicit edition URL shows its correct mini codes,
  testament headings, and verse title even before JavaScript runs.
- The three main sidebar rail hover/focus popups use the remembered Bible edition, even while
  another section is open. TB reads “Alkitab,” “Kidung,” and “Tata Ibadah”; SIM reads “Bibel,”
  “Doding,” and “Agenda.” Their accessible link names follow the same labels. A normal full
  reload uses the existing TB default, and an explicit SIM URL starts with the SIM labels.
  Other rail popups and other uses of these words stay unchanged.

## Search rules

- The Bible sidebar filter matches full TB/SIM names and both short codes in either edition,
  preserving its case-insensitive substring behavior and current filter text.
- Projector Go To resolves a TB or SIM code followed by a chapter or verse reference to the
  same canonical book and position. It preserves the existing result count, navigation, and
  projected translation choice.
- The new and edit passage book picker filters by both full names and both short codes in
  either toggle state. Filtering does not change the selected book or stored translation.
- A book with no SIM abbreviation remains findable by its TB code and full names.

## Acceptance scenarios

### Scenario: Existing and fresh databases keep both SIM names

- **Given** 66 existing SIM translations with full names and related verses
- **When** the abbreviation migration runs, or a fresh database is initialized with the Bible seed
- **Then** each SIM row has the exact short code above while its full name and verse relations remain
- **And** running the seeder again updates those rows without introducing duplicate translations

### Scenario: Mini sidebar follows the remembered edition

- **Given** a Bible chapter has both TB and SIM and its mini sidebar shows “Kej” in TB
- **When** the reader selects SIM
- **Then** the same mini tile shows “1Mu” while the expanded row retains the full “1 Musa” name
- **And** the SIM code remains after an in-page menu switch, chapter navigation, or Back/Forward
- **When** the page is fully reloaded without an edition URL
- **Then** the mini tile returns to “Kej,” as specified by spec 099

### Scenario: A missing SIM chapter preserves the remembered sidebar choice

- **Given** SIM was selected and the next chapter has TB verses only
- **When** that chapter opens
- **Then** the sidebar still uses SIM codes and headings where available
- **And** the verse-page heading names the TB book whose text is visible
- **When** a later SIM-capable chapter opens
- **Then** SIM text, its full heading, and its mini code return without another toggle

### Scenario: Testament headings follow their local edition

- **Given** the Bible sidebar or a new/edit passage book picker is showing TB
- **When** its edition changes to SIM
- **Then** the two group headings read “Padan na Basaia” and “Padan na Baru”
- **When** its edition changes to TB
- **Then** the headings read “Perjanjian Lama” and “Perjanjian Baru”
- **And** opening an existing SIM passage starts its picker with the SIM headings

### Scenario: Sidebar filter matches either abbreviation

- **Given** the Bible sidebar contains the first book in either edition
- **When** the reader filters by “Kej” or “1Mu”
- **Then** the same book remains visible, online and from a saved copy
- **And** changing edition does not clear the filter or disturb sidebar navigation state

### Scenario: Projector Go To matches either abbreviation

- **Given** the projector has Bible data for the first book
- **When** the operator searches “Kej 1” or “1Mu 1,” including a verse reference
- **Then** both queries resolve to the same book and position under existing Go To behavior

### Scenario: New and edit passage pickers match either abbreviation

- **Given** the passage book picker is open in either TB or SIM
- **When** the operator filters by “Kej” or “1Mu”
- **Then** the same book remains available with its current full primary and secondary names
- **And** clearing the filter restores all books without changing the selected translation

### Scenario: Chapter title matches visible text

- **Given** a chapter has TB “Kejadian” and SIM “1 Musa” verses
- **When** it opens through a normal link, `?ed=sim`, Back/Forward, or saved-copy reading,
  or the reader toggles the edition
- **Then** its stage heading and browser title use “Kejadian 1” with TB text and “1 Musa 1”
  with SIM text

### Scenario: Main sidebar popups follow the remembered Bible edition

- **Given** the three main rail buttons show “Alkitab,” “Kidung,” and “Tata Ibadah” in TB
- **When** the reader chooses SIM and hovers or focuses those buttons, including after switching
  to Kidung or Tata Ibadah within the page
- **Then** their popups and accessible names read “Bibel,” “Doding,” and “Agenda” respectively
- **When** the reader switches back to TB
- **Then** only those three popup labels and accessible names return to their TB wording

## Traceability

- Data and server tests: `tests/test_bible_translation_seed.py`, `multimedia/web/tests.py`.
- E2E: `tests/e2e/test_reading.py`, `tests/e2e/test_entry_pickers.py`,
  `tests/e2e/test_projector.py`, `tests/e2e/test_offline_library.py`.
- Planned implementation: `multimedia/bible/models.py`, a new Bible data migration,
  `raw/bible/book_abbreviations/SIM.json`, `scripts/bible_seeder.py`,
  `multimedia/web/reading/search.py`, `multimedia/web/reading/views.py`,
  `multimedia/web/reading/entries.py`, `multimedia/web/reading/offline.py`,
  `multimedia/web/templates/reading/_books_panel.html`,
  `multimedia/web/templates/reading/base.html`,
  `multimedia/web/templates/reading/_entry_form.html`, `static/web/reading.js`,
  `static/web/entries.js`, `static/web/offline-render.js`, and
  `static/web/projector-library.js`.
- This spec supersedes the TB-only mini-tile requirement in accepted spec 092 and the
  corresponding mini-tile assertion in accepted spec 099. Their remaining edition-state
  contracts continue to apply.
