# Plan 056: Give the stage entry links a theme-aware colour

- **Status:** Accepted
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-058
- **Bump:** patch

## Why

On the Tata Ibadah stage the entry titles — `.entry__jump`, the song and passage links the owner
clicks — are raw anchors with no author colour, so they render in the browser's default blue
`#0000EE` in both themes. Measured on the dark canvas that is **1.98:1** contrast while the
theme's own body text sits at 16.8:1; nothing else in the surface is off-palette. The owner
asked for a colour that does not clash with the other texts. Live previews rendered four options
in both themes; the owner chose the accent combo: forest green in light, lifted royal blue in
dark.

## Scope / edges

**In:**

- A `--link` token in `tokens.css` (both theme blocks): light `#1C5C3C`, dark `#7C9CF0`.
- One rule colouring `.entry__jump` from the token.
- The tokens contrast test gains the pair; one E2E theme check.

**Out:**

- Every other anchor (the rail logo is an `<img>`; sidebar/TOC rows are already styled).
- Visited styling, hover/focus decoration, and the underline (it stays).

## Approach

- `tokens.css`: `--link: #1C5C3C;` in `:root`; `--link: #7C9CF0;` in `:root[data-theme="dark"]`.
- `components.css`: `.entry__jump { color: var(--link); }` next to the Tata Ibadah stage rules.
  The rule sets colour only — the UA underline (the non-colour cue) is untouched, and hover,
  focus and visited keep the colour.
- Tests: `tests/test_design_tokens.py` adds `('--link', '--canvas')` to `TEXT_PAIRS` (red
  first — the token does not exist yet); `tests/e2e/test_reading.py` gains one test that toggles
  `#themeBtn` and reads the link's computed colour.

## TDD

- Domain/app tests: `tests/test_design_tokens.py` (token + contrast pair, 7.29:1 and 6.97:1).
- E2E: `tests/e2e/test_reading.py` — `test_tatib_stage_entry_links_follow_the_theme`.

## Risks

- **Contrast floor.** Both pairs clear the 4.5:1 AA floor (7.29 / 6.97) — the light pair also
  clears 7:1, the dark pair sits a hair under it by design (accent colour, quieter than body
  ink). The tokens test guards the floor against later palette edits.
- **Scope creep.** The rule is deliberately `--link` on `.entry__jump`, not a global anchor
  colour; other links keep today's rendering.
