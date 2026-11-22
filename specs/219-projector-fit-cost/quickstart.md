# Quickstart

Every command below runs from the slice's worktree
(`~/Projects/multimedia-gkps-klender-219`), with the project's own interpreter
(`~/Projects/multimedia-gkps-klender/.venv/bin/python`) and `DATABASE_URL` pointing at the local
compose database.

## Serve the preview

```
manage.py collectstatic --noinput
manage.py runserver 0.0.0.0:8791 --noreload
```

Then open `http://127.0.0.1:8791/projector?service=144` — the service `Ibadah Minggu` (171 screens,
126 carrying words). Advance with ArrowRight; the arrival of a screen of words is the thing this slice
changes.

## Reproduce the numbers

```
python specs/219-projector-fit-cost/preview/probe.py \
    --develop http://127.0.0.1:63404 --slice http://127.0.0.1:8791 --service 144
python specs/219-projector-fit-cost/preview/verify_sizes.py \
    --develop http://127.0.0.1:63404 --slice http://127.0.0.1:8791 --service 144
```

`--develop` is any build without the change (here the main checkout's compose stack on port 63404).
The first prints the advance cost and the layout reads at both cadences; the second prints how many
screens are fitted to a different size on arrival than on a resize.

## Run the tests

```
manage.py test tests.e2e.test_projector --keepdb
```

The fitting tests are `test_a_body_too_long_for_the_screen_comes_down_to_fit`,
`test_a_gap_opens_between_the_words_own_lines`,
`test_a_single_screen_text_fits_its_whole_body_on_one_screen` and the new
`test_a_text_screen_arrives_without_being_fitted`.

The contracts and the data model are in `contracts/none.md` and `data-model.md`: both are explicitly
none.
