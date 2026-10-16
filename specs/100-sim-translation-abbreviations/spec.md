# Spec: Use the requested SIM book abbreviations

- **ID:** 100
- **Status:** Accepted; Amendment A accepted and implemented
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
Dan=Dan  Hos=Hos  Yoe=Joe  Amo=Amo  Oba=Obj  Yun=Jon  Mik=Mik  Nah=Nah  Hab=Hab
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
- Projector Go To carries a unique TB or SIM code's edition into the suggestion and opened
  passage. A code shared by both editions returns one result per edition through the existing
  result cycling. Suggestions use the matched edition's full book name, adding a muted/dimmed
  `· TB` or `· SIM` suffix when both names are identical. A missing position in one matched
  edition does not create a substitute result from the other edition. The translation flip
  control remains available after opening a passage.
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

## Amendment A: projector Go To follows matched edition abbreviations

**Accepted by the project owner on 2026-10-16.** This amendment changes only the Go To
abbreviation behavior. All other Spec 100 requirements remain unchanged.

### Search, labeling, and selection rules

- An exact canonical `Book.name` code identifies TB; an exact translation abbreviation identifies
  its own edition. When one code uniquely identifies an edition, the Go To suggestion uses that
  edition's full translated book name and selecting it opens that edition's passage.
- When the same code identifies both TB and SIM, return one result for each edition. Selecting a
  result opens its corresponding edition, and both results remain reachable through the existing
  result-cycling behavior.
- Use the matched edition's full translated book name in each result label. If both results have
  the same full book name, append `· TB` or `· SIM` to distinguish them; render that edition suffix
  in muted/dimmed text. When the full names differ, the names already distinguish the results.
- Full-name search and other Go To matching behavior remain unchanged. If a matched edition has no
  verses at the requested chapter or verse, do not show a result from the other edition as a
  substitute. Keep the translation flip control after opening a passage.

### Acceptance scenarios

#### Scenario: SIM abbreviation suggests and opens the SIM passage

- **Given** the projector library has SIM verses for Panguhum chapter 1
- **When** the operator searches `Pah 1`
- **Then** the suggestion reads `Panguhum 1`
- **When** the operator selects that suggestion
- **Then** the detour opens the SIM text for Panguhum 1

#### Scenario: TB abbreviation suggests and opens the TB passage

- **Given** the projector library has TB verses for 1 Tawarikh chapter 2
- **When** the operator searches `1Ta 2`
- **Then** the suggestion reads `1 Tawarikh 2`
- **When** the operator selects that suggestion
- **Then** the detour opens the TB text for 1 Tawarikh 2

#### Scenario: Abbreviated verse references keep the matched edition

- **Given** the requested edition contains the referenced chapter and verse
- **When** the operator searches an edition-specific code followed by a verse reference
- **Then** the result label uses that edition's full book name and selection opens that edition
  at the requested verse

#### Scenario: A shared code returns both editions with disambiguated labels

- **Given** `Rut` is the code for the same book in TB and SIM, both editions have the full book
  name `Rut`, and both have chapter 1
- **When** the operator searches `Rut 1`
- **Then** the existing result cycling exposes one `Rut 1` result for TB and one for SIM
- **And** their labels read `Rut 1 · TB` and `Rut 1 · SIM`, with the edition suffix muted/dimmed
- **When** the operator selects each result
- **Then** the TB result opens TB and the SIM result opens SIM

Preview: [Projector Go To edition preview](./preview.html#projector-goto-amendment).

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
  `static/web/projector-library.js`, `static/web/projector.js`, and
  `static/styles/design/projector.css`.
- This spec supersedes the TB-only mini-tile requirement in accepted spec 092 and the
  corresponding mini-tile assertion in accepted spec 099. Their remaining edition-state
  contracts continue to apply.
