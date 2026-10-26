# Quickstart: a Tata Ibadah sidebar row is three lines, ellipsized

**Slice**: `specs/135-tatib-sidebar-row-clamp`
Contracts: [`contracts/toc-item.md`](./contracts/toc-item.md) · Data: [`data-model.md`](./data-model.md)

Everything runs from the slice's worktree, against the compose database.

```sh
export DATABASE_URL="postgres://multimedia:<password>@127.0.0.1:59075/multimedia"
PY=/home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python
```

## Payload rules — Django tests

```sh
$PY manage.py test multimedia.web --keepdb
```

Named rows of the traceability table:

```sh
$PY manage.py test \
  multimedia.web.tests.TatibServiceViewTests.test_a_row_label_is_no_longer_cut_at_sixty_characters \
  multimedia.web.tests.TatibServiceViewTests.test_an_untitled_text_row_carries_three_body_lines \
  --keepdb
```

*Not yet runnable: the tests above are written in Implement (`tasks.md` T003–T010), so they do not
exist at gate 2.*

## Rendered geometry — Playwright E2E

```sh
$PY manage.py test tests.e2e.test_reading tests.e2e.test_saved_render_parity --keepdb
```

*Not yet runnable for the same reason (`T011–T013`); the suite needs a browser and the compose
database, and the repository's E2E modules run through `LiveServerTestCase`.*

## The preview, rebuilt from the unchanged app

```sh
$PY manage.py collectstatic --noinput
$PY manage.py runserver 0.0.0.0:8769 --noreload &
$PY specs/135-tatib-sidebar-row-clamp/preview/build_preview.py     # the real /tatib/144/ page, re-marked
$PY specs/135-tatib-sidebar-row-clamp/preview/build_cases.py       # every case, two widths
$PY specs/135-tatib-sidebar-row-clamp/preview/probe_rows.py        # heights, clamp, overflow
```

These three ran at Preview and produced `after.html`, `cases.html` and the numbers in the spec's
`## UI/UX`. After Implement, the same pages can be rebuilt from the live route — the change will be
in the app, so `build_preview.py`'s mutation step becomes a no-op and the page is the real thing.

## What to look at

| Surface | Path | Expectation |
| --- | --- | --- |
| Every case | `preview/cases.html` | no row taller than three lines; `…` where text is hidden; no ellipsis where it is not |
| A real service | `preview/after.html` | rows 1, 2, 8, 16, 17 as specified |
| The unchanged app | `http://127.0.0.1:8769/tatib/143/` | row 1's Drive link overflows its pane and its `…` is clipped away — the fault this slice removes |
