# Spec 059: Color liturgy speakers as a congregation cue

- **ID:** 059
- **Status:** Accepted
- **Item:** ITEM-061
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** minor

## Intent

The projection screen faces the congregation. Leader lines are a cue that the leader is speaking, so people know when they start. Those lines are dimmer than the ordinary off-white. Congregation lines stay that off-white, because that is the text they read. A joined line is also theirs to read and say, so it stays clear, and the color is what marks it as theirs. It stays quieter than the off-white.

The same mapping is used on every Tata Ibadah, on the projector, on the reading page in both themes, and in the entry preview.

## Scope

### In scope

- Text entries, single-screen text entries, and legacy text rows.
- The projector, the Tata Ibadah reading page (light and dark), and the entry preview.
- Leader, joined, and ordinary voices, with continuation inside one item.

### Out of scope

- Song lyrics, scripture verses, and section breaks. They stay the ordinary text color.
- Sidebar labels, search snippets, and the text `_first_line` returns.
- A third color for named groups (Bapa, Inang, Namaposo, and the rest). They use the ordinary color.
- Splitting two ordinary voices onto two screens. That stays an editing habit: a blank line already starts a new screen.
- The projector section header.
- Hover, focus, and motion on these lines.

## Domain rules

- **Three voices, one fixed palette.** `leader`, `join`, and ordinary. The ordinary voice is the default text color. A label keeps its voice in every entry and every Tata Ibadah.
- **Leader labels.** The whole line-start label, case-insensitive: `L`, `Liturgis`, `Litrugis`, `P`, `Paragenda`, `Pendeta`, `Pandita`, `Pdt`, `Pelayan`, `Pemimpin`, `Parambilan`. Bare `P` is the leader voice. `Pendeta`, `Pandita`, and `Pdt` match as those words.
- **Joined labels.** One leader initial (`L` or `P`) and one congregation initial (`J` or `K`), either order, in capitals. Joiners: `+` or `/` with optional spaces (`P+K`, `P + J`, `P/K`); a dot tight against the second initial (`P.J`); the two initials adjacent (`PJ`); a dot before the plus (`P.+K`, `L. + J`, `L.+J`). Optional spaces sit around the joiner. The mark is then closed by `:`, `.`, or a space, and the rest of the line is the words. The whole line is one joined voice. Capitals only, so `Lk 6:27` (Lukas) is not `L` + `K`.
- **Known congregation labels.** `J`, `K`, `Jemaat`, `Kuria`, `Bapa`, `Inang`, and `Namaposo`, case-insensitive, are the ordinary voice.
- **A period closes only a known label.** `P.`, `J.`, `Paragenda.`, `Bapa.` are marks. Any other word before a period ends a sentence (`Marolob-olob au mamuji Ham. …`, `Tuhan holong ma Ham. …`), so it is not a mark.
- **Other speakers need a colon.** Any other line-start label closed by `:` is an ordinary voice when it starts with a capital letter, has at most three words, holds no `. ` inside, and the words after the colon do not start with a digit. `Orang tua:`, `Pengkhotbah:`, `Ketua Sie Namaposo:`, `SM/Remaja:`, `O.T:` qualify. `Maka jiwaku pun memuji-Mu:` (four words) and `Lukas 6:27` (a reference) do not. The line sets the continuing voice to ordinary.
- **Cues.** A colon label whose first word is `Next`, `Lagu`, `Doding`, `Nyanyian`, `Mandoding`, `Mandodingkon`, `Refr`, `Reff`, `Puisi`, `Bacaan`, or `Prolog` (`Lagu Penutup:` included) is ordinary, keeps its words as written, and the lines that follow with no mark stay ordinary.
- **Line start only.** A colon inside a sentence stays in the sentence. `Pdt.` is a leader mark only when it is the label at the start of the line.
- **Continuation.** A line with no mark keeps the voice of the previous line in the same text body. A blank line does not reset that voice, so the next screen of the same item still carries it. Each item starts ordinary.
- **Precedence.** Joined mark, then a known label closed by a period, then a colon label (known label, cue, other speaker), then continuation.
- **Where it applies.** The classifier runs on text entries, single-screen text, and legacy text rows. Song, scripture, and section-break bodies are left unclassified.
- **Marks keep their separator.** On the page and in the preview, `P. …` shows the mark `P.` and `Paragenda: …` shows the mark `Paragenda:`. The projector shows the line as written and only changes its color.
- **The mark matches the line.** On a liturgy line, the speaker mark uses the line's color. An ordinary speaker's initials are the same ink as the words.

## UI details

Approved preview: [`preview.html`](./preview.html), accepted 2026-10-12. The Draft was accepted the same day. While building, a run over every liturgy text in the local database (4,458 lines) showed that a period after a short phrase is almost always the end of a sentence. The label rules above were tightened to match, and the owner was told.

- **Size / spacing:** unchanged. Projector type, the fit loop, line gaps, and the page's serif body stay as they are. The speaker mark keeps its current face: sans, weight 640, `0.82em`, tracking `0.02em`, `0.15em` after the mark.
- **Position / layout:** unchanged. Color does not move or resize a line.
- **Colors / typography:**
  - Ordinary text stays `--ink`: `#F5F3EE` on the dark canvas `#14130F` (16.76:1), `#1F1F1D` on the light canvas `#F7F5F1` (15.16:1).
  - Joined, `--speaker-join`: dark `#8EC2CC` (9.51:1 on `#14130F`), light `#2B5A64` (7.02:1 on `#F7F5F1`).
  - Leader, `--speaker-leader`: dark `#9C8463` (5.22:1 on `#14130F`), light `#866B50` (4.56:1 on `#F7F5F1`).
  - The projector header stays `#FFD166` (12.89:1 on `#14130F`).
  - In both themes the contrast order is ordinary, then joined, then leader. Each pair is at least 4.5:1.
  - Classes: `is-leader`, `is-join`, `is-assembly` on `.screen__line`, `.tatib__tx`, and `.preview__line`. Assembly sets no text color; it only makes the mark inherit.
- **States:** the colors stay put on hover, focus, and while a screen is entering or leaving.
- **Responsive behavior:** the same colors at every width. The projector still fits type to the screen.
- **Motion:** none added.

## Acceptance scenarios

### Scenario: A leader cue beside the congregation

- **Given** a text whose screen is `P: Marilah kita bangkit berdiri` and `J: Amin.`
- **When** it is shown on the projector
- **Then** the `P` line is `#9C8463` and the `J` line is `#F5F3EE`

### Scenario: The same screen on the page

- **Given** that text on the Tata Ibadah page
- **When** the theme is light
- **Then** the leader line is `#866B50` and the congregation line is `#1F1F1D`
- **When** the theme is dark
- **Then** the leader line is `#9C8463` and the congregation line is `#F5F3EE`
- **And** each speaker mark uses its line's color

### Scenario: A joined line

- **Given** a line `P+J: Marilah kita memuji TUHAN dan bersyukur bagi-Nya. Amin.`
- **When** it is shown on the projector
- **Then** the whole line is `#8EC2CC`
- **And** `P+K`, `P + K`, `P.+K`, `P/K`, `L+J`, `L.+J`, `L. + J`, `P.J`, and `PJ` are the same voice

### Scenario: Names that share the leader voice

- **Given** lines that start with `L.`, `Liturgis:`, `Litrugis:`, `Paragenda:`, `Pendeta:`, `Pandita:`, `Pdt:`, `Pelayan:`, `Pemimpin:`, or `Parambilan:`
- **Then** each line is the leader voice
- **And** `K`, `Kuria`, `Jemaat`, `Bapa`, `Inang`, and `Namaposo` are the ordinary voice

### Scenario: Continuation across a screen

- **Given** one text item whose first line is `P: …`, then a blank line, then a line with no speaker mark
- **When** the projector splits them into two screens
- **Then** the unmarked line is still the leader voice
- **And** the next item starts ordinary

### Scenario: Another speaker breaks the cue

- **Given** a leader line followed by `Bapa: …` and then a line with no mark
- **Then** the Bapa line and the line after it are the ordinary voice

### Scenario: A cue is not a speaker

- **Given** a leader line followed by `Nyanyian: Haleluya` and then `Haleluya, Haleluya`
- **Then** both of those lines are the ordinary voice
- **And** a colon inside `Maka jiwaku pun memuji-Mu:` does not start a voice

### Scenario: Preview follows the page

- **Given** a clipped text entry opened in the preview
- **Then** its leader, joined, and ordinary lines use the page's colors for the current theme

### Scenario: Songs and scripture

- **Given** a song line or a verse that begins with `P:`
- **When** it is shown on the projector, the page, or the preview
- **Then** the line is the ordinary text color

### Scenario: The header

- **Given** a projector screen with a section header
- **Then** the header is `#FFD166`

## Traceability

- Domain/app tests: `multimedia/web/test_speaker_voices.py` (`ReadMarkTests`, `VoiceLinesTests`, `RenderedVoicesTests`); `tests/test_design_tokens.py` (`--speaker-join` and `--speaker-leader` in `TEXT_PAIRS`, `test_speaker_voices_stay_quieter_than_the_ordinary_text`).
- E2E: `tests/e2e/test_speaker_voices.py` — `SpeakerVoicesE2ETests`.
- Implementation: `multimedia/web/reading/voices.py` (the classifier), `multimedia/web/reading/views.py` (`_paragraphs`, `_plain_paragraphs`, `_screen_lines`, `_line_pairs`), `multimedia/web/templates/reading/projector.html`, `multimedia/web/templates/reading/tatib.html`, `static/styles/design/tokens.css`, `static/styles/design/projector.css`, `static/styles/design/components.css`.
- Related: spec 004 (the `L.`/`P.`/`J.` speaker marks this extends), spec 006 (projector screens), spec 058 (built-in blanks, unchanged).
