# Research: A song with no verses is named, not mistaken for no song

**Spec**: `specs/162-song-verse-empty-state/spec.md`
**Unknowns remaining**: 0

## D001 — the fact that decides the line is the picked song, not the number of checkboxes

- **Decision**: the Verses summary is told which song the form holds (`#id_song`) and states the two
  worlds apart: no song → `Pick a song first`; a song with no boxes → `This song has no verses`.
- **Rationale**: zero checkboxes is the only signal `verseSummary` reads today, and it is produced by
  both worlds — the modal at rest (`#entry-verses` renders empty) and a song whose verses answer is
  `{"verses": []}`. The picked song is already in the form as a hidden input, so the distinction is
  available without a second request.
- **Alternatives considered**: reading the song option's label (it may be stale after a failed
  fetch); extending the verses endpoint to say `has_verses: false` (a second source for a fact the
  empty list already states — rejected under D005); inferring from the trigger's own text (circular).
- **Provenance**: research

## D002 — the statement is also server-rendered

- **Decision**: `SongEntryForm` exposes whether its chosen song carries no verses, and the template
  writes the statement for the first paint; the script then keeps it current.
- **Rationale**: the form fragment is a server response. Rendering `Pick a song first` there for a
  form whose Song field already names a song is a contradiction in the artifact itself — visible to a
  test that asserts the server render, and to a screen-reader announcement before the script runs.
  Measured on develop: `GET /editor/entry/new/?kind=song&tatib=149` renders
  `<span data-verses-summary>Pick a song first</span>` and `#id_song` empty, so today the two agree;
  the disagreement appears only after a song is picked, and the edit route is where the server can be
  wrong on its own.
- **Alternatives considered**: script-only (a fragment that is wrong on its own); template logic over
  `form.verses.field.choices` inline (works, but hides the rule in a template expression and cannot be
  tested without rendering).
- **Provenance**: research

## D003 — the save refusal is decided where the verses rule already lives

- **Decision**: `ServiceEntry.clean` names the song when the entry's song has no live verses, and
  keeps `Keep at least one verse in the service.` when the song has verses and none was kept.
- **Rationale**: the rule "a song entry keeps at least one verse" is the model's
  (`multimedia/tatib/models.py:167`), not the form's; putting the cause there means every writer — the
  modal, the API, a fixture — gets the same two sentences. The live page confirms the model error
  already reaches the Verses field (`dialog[open] .editor__error` reads
  `Keep at least one verse in the service.` after Save), so no plumbing is added.
- **Alternatives considered**: a form-level `clean_verses` (a second home for one rule; the API writes
  entries without that form); a view check (the third home).
- **Provenance**: research

## D004 — one test per layer, each proving a different sentence

- **Decision**: a model test for the two refusals; a web test for the server-rendered fragment of an
  edit form whose song has no verses; an E2E test for the modal — pick, read, save.
- **Rationale**: the three sentences live in three places (model, template, script). A single E2E
  would pass with the template still wrong (the script overwrites it before any assertion), and a
  single unit test cannot see the script at all.
- **Alternatives considered**: E2E only (leaves FR-002 unproven); unit only (leaves FR-001 and FR-003
  unproven — they are the script's).
- **Provenance**: research

## D005 — the verses endpoint stays as it is

- **Decision**: `entry_song_verses` keeps answering `{"verses": [...], "title": …}`; an empty list
  means a song with no verses.
- **Rationale**: the answer is already correct and is consumed by the same script that renders the
  checkboxes; a boolean beside it would be a second way to say the same thing, which is the drift
  this repo has ruled out before (`docs/process` C-SDD-* on one home per fact). The consumers are
  three: `loadVerses`, its E2E fixtures, and the new statement.
- **Alternatives considered**: `{"verses": [], "has_verses": false}` (redundant); a 404 for a
  verse-less song (a song without verses is a normal song, not a missing resource).
- **Provenance**: research

## D006 — the fixture is a real song with nothing in it

- **Decision**: the E2E suite gains a hymn song with no `Verse` rows (`KJ 901 Kosong`) and the unit
  suite an edit fixture created through the ORM, because the form and the model both refuse to write
  one.
- **Rationale**: the state is reachable in the product (seven songs in the local library carry no
  live verses — pks 1774, 1852, 1886, 1905, 1906, 1879, 1731), so the test data must contain it;
  a mock would prove nothing. The edit fixture has to bypass `full_clean` because the model rule this
  slice keeps refuses it — `ServiceEntry.objects.create` does exactly that, as `objects.create` never
  calls `clean`.
- **Alternatives considered**: a soft-deleted verse (a different state, already covered by
  `test_a_deleted_included_verse_is_omitted_and_warned`); a stub response in the browser test
  (TDD-04: the endpoint is ours, and the real one answers in one query).
- **Provenance**: research
