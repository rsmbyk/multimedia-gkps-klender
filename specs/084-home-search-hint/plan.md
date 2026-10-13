# Plan 084: Refresh the home search helper line

- **Status:** Accepted
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-087
- **Bump:** patch

## Why

The search-first home carries one helper line under the field:

```html
<p class="search-home__hint">Try Matius 5:13, KJ 152, or pengampunan dosa</p>
```

The owner wants the two examples that match what the congregation actually reaches for: a New Testament
verse and a Simalungun hymn. `Yoh 3:16` and `HAL 411` replace the current three examples.

## Scope / edges

**In:**

- `multimedia/web/templates/reading/base.html`: the `search-home__hint` copy.

**Out:**

- The field's placeholder, its accessible label, the search behaviour, ranking, and the results page.
- The team's other surfaces, which carry no helper line.

## Approach

Swap the copy in place. The element, its class, its 13px `--head-ink` styling, and its existing
"hidden on the results page" rule stay exactly as they are, so nothing but the sentence changes.

## Verification of the new examples

Both queries were run against the local stack (`/search/?q=…`, the database copied from production) and
return real matches, so the line is not advertising a dead query:

- `Yoh 3:16` → *Yohanes 3:16 · Alkitab reference · TB* (`/bible/43/3/?v=16&to=16`), among 18 rows.
- `HAL 411` → *HAL 411 · Diatei Tupa ma Bamu Ham Naibata* (`/songs/412/`), among 9 rows.

## TDD

- Domain/app tests: `multimedia/web/tests.py::HomeTests` asserts the hint text; update the expected
  string.
- E2E (Playwright): `tests/e2e/test_reading.py` asserts the hint in four places (the landing home, the
  return-to-home paths); update the expected string.

## Risks

- The old copy is asserted in five places across two suites; a partial update leaves a red suite that
  looks unrelated to the change.
- `Yoh` must stay a recognised Bible abbreviation. The reference parser resolves it as a full book name
  today (verified above); a future alias change would make the hint stale, which is why the spec's
  scenario pins the resolution rather than only the string.
