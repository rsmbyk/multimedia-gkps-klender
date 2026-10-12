# Plan 059: Color liturgy speakers as a congregation cue

- **Status:** Accepted
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-061
- **Bump:** minor

## Why

A Tata Ibadah text is a liturgy. Several voices share one projection screen, and today every line is the same off-white, so the congregation cannot tell a leader's line from their own. The screen faces them. A leader line is only a cue that the leader is speaking, so they know when their turn starts. Their own lines, and a joined line they also say, are what they read. The cue has to sit behind the off-white. The joined line has to stay readable, and its color is what tells them the line is theirs to say.

The owner approved this look on `preview.html` (2026-10-12, "nice").

## Scope / edges

**In:**

- A fixed voice for each liturgy line: leader, joined, or the ordinary text color.
- The same mapping on the projector, on the Tata Ibadah page in both themes, and in the entry preview.
- Text entries, single-screen text entries, and legacy text rows.
- Continuation of a voice across unmarked lines of the same item, including the next two-line screen.

**Out:**

- Songs, scripture, and section breaks.
- Sidebar labels, search snippets, and `_first_line`.
- A separate color for Bapa, Inang, Namaposo, or any other named group.
- Rewriting the operator's line breaks. Two congregation voices on one screen both stay the ordinary color; operators split them with a blank line when they want two screens.
- The gold section header on the projector.

## Approach

1. Classify each line of a liturgy body in order, before the projector pairs lines into screens. One pure function owns the rules, so the page, the preview, and the projector share it.
2. Recognition, first match wins:
   - A joined mark, capitals only: one leader initial (`L` or `P`) and one congregation initial (`J` or `K`), either order, written with `+`, `/`, a dot and no space (`P.J`), the two initials adjacent (`PJ`), or a dot before the plus (`P.+K`, `L. + J`). Optional spaces around the joiner. Then `:` or `.` or a space, and the words.
   - A known label closed by a period: the leader labels `L`, `Liturgis`, `Litrugis`, `P`, `Paragenda`, `Pendeta`, `Pandita`, `Pdt`, `Pelayan`, `Pemimpin`, `Parambilan`, or the congregation labels `J`, `K`, `Jemaat`, `Kuria`, `Bapa`, `Inang`, `Namaposo`. No other word before a period is a mark. In the real data, a period after a short phrase ends a sentence.
   - A colon label. A known label takes its voice. A label whose first word is a cue (`Next`, `Lagu`, `Doding`, `Nyanyian`, `Mandoding`, `Mandodingkon`, `Refr`, `Reff`, `Puisi`, `Bacaan`, `Prolog`) is ordinary and not lifted. Any other capitalised label of up to three words, not followed by a digit, is an ordinary speaker, and that voice continues.
   - No mark: keep the voice from earlier in the same body. A blank line does not reset it. A new item starts ordinary.
3. Known labels match case-insensitively, at the start of the line only. A colon later in the sentence stays part of the sentence. `Pdt. August Theis` counts only when `Pdt` is the line-start label.
4. Bare `P` is the leader voice. Spelled names are their own labels, so `Pendeta:` is leader because the word is leader, and the letters are never read as a bare `P`.
5. Colors are two tokens, `--speaker-leader` and `--speaker-join`, light and dark. The ordinary voice is `--ink`. The projector already pins `data-theme="dark"`, so it uses the dark pair. Classes `is-leader`, `is-join`, and `is-assembly` carry the voice. Assembly has no color of its own; its speaker mark inherits the line so the initials match the words. Projector screen lines become `{text, voice}` pairs for every kind; songs and passages pass an empty voice.
6. The projector keeps the line text as written. The page and the preview keep lifting the mark into `.tatib__sp`, and they keep the separator that was written (`P.` stays `P.`; `Paragenda:` stays `Paragenda:`).
7. Leave `_first_line` on today's initial pattern so sidebar labels do not change.

## TDD

- Domain/app tests: `multimedia/web/test_speaker_voices.py` (classifier, continuation, cues, and the rendered classes on a text, a song, and a passage). `tests/test_design_tokens.py` gains the two pairs and a hierarchy check: ink contrast above join, join above leader, every pair at least 4.5:1.
- E2E: `tests/e2e/test_speaker_voices.py`, one class. Stage in light, then the projector: computed colors for a leader line, a congregation line, and a joined line.
- Targeted local runs only. Full suite and full browser E2E stay on push/CI.

## Risks

- **The cue is easy to over-brighten.** Leader on the dark canvas is 5.22:1 and on the page 4.56:1, just above the 4.5 floor, on purpose. The hierarchy test keeps a later palette edit from making the cue louder than the off-white.
- **A long leader line still has presence from its length.** The color is the quiet part. The spec does not shrink the type.
- **Short labels can over-match.** The real data has 4,458 liturgy lines. A few sentence starts still read as an ordinary speaker: `Martonggo ma hita:` (twice), `Sebab:`, and `Jikalau mereka berkata:`. The only effect is the ordinary color, plus a lifted mark on the page. Tightening further would drop real speakers such as `Orang tua:`.
- **Separate branch.** The work is on `feat/059-speaker-colors` from `develop`, in its own worktree, apart from the in-progress highlight branch.
