# Quickstart — the Tata Ibadah list groups by age

**Spec** `spec.md` · **Plan** `plan.md` · **Rule** `data-model.md` · **Interfaces** `contracts/README.md` (none)

Everything below is runnable in this worktree, with the shared virtualenv
(`/home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python`) and the compose database
(`postgres://…:59075/multimedia` — the password is in `docker-compose.yml`).

## The rule and the markup

```
manage.py test multimedia.web.test_date_buckets          # the six boundary tests
manage.py test multimedia.web.test_obs_dock              # the dock's four buckets and its badge
manage.py test multimedia.web.tests.ReadingViewTests     # the panel's groups, ordering, badge
```

## The running branch

```
manage.py runserver 0.0.0.0:8766 --noreload             # the project's own data
specs/132-tatib-sidebar-date-buckets/preview/probe_date_buckets.py \
    http://127.0.0.1:8766/tatib/ /tmp/panel.png
```

## The demo instance (a throwaway SQLite, never the project's database)

`preview/README.md` carries the four commands, and `preview/seed_demo_data.py` the dataset: today ×2,
+6, +60, −8, −30 (the edge), −45, −100, a January date, −320 and −400 days. It deletes every service in
**that** database before seeding — never point it at the compose database.

## The browser suites (run at the push step)

```
manage.py test tests.e2e.test_reading
manage.py test tests.e2e.test_saved_render_parity
```

`test_reading.py` reads the four headings, the today-first order and the single badge; the parity suite
compares the saved page's headings, bucket keys, rows and badges with the server's for every route,
`/tatib/` included.
