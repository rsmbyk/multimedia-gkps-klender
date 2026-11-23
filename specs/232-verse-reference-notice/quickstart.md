# Quickstart: verse reference notice

Links: [`spec.md`](spec.md) · [`plan.md`](plan.md) · [`research.md`](research.md) ·
[`data-model.md`](data-model.md) · [`contracts/none.md`](contracts/none.md) ·
[`preview/README.md`](preview/README.md)

## Preview

```sh
python3 specs/232-verse-reference-notice/preview/build.py
```

Open `specs/232-verse-reference-notice/preview/index.html` directly or in the chat preview. The page
is self-contained; the product's tokens and editor CSS are inlined at build time.

## Targeted tests

From the worktree root, with the repo's venv:

```sh
../.venv/bin/python manage.py test tests.e2e.test_verse_reference_notice --keepdb
```

The E2E module uses `StaticLiveServerTestCase`; the repo's `repo:` test convention applies, so the
`STATICFILES_STORAGE` override is in the test class. Run Django tests while no sibling session holds the
shared test database, or point `DATABASE_URL` at a throwaway database.

The full browser suite is deferred to the push step.
