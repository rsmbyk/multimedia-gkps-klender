# Quickstart — spec 246

Links: [data model](../data-model.md) · [contracts](../contracts/none.md) ·
[plan](../plan.md) · [preview](preview/README.md).

## Reproduce on the unmodified app

```sh
# from any checkout on origin/develop, e.g. http://127.0.0.1:63404/
# open /, click Media Library, then click Alkitab.
# Expected before the fix: data-section=alkitab, 0 /bible/ requests, "No books yet."
```

## Live preview (approved at gate 1)

```sh
# preview server already running from this worktree
xdg-open http://127.0.0.1:8769/
python specs/246-media-library-bible-rail/preview/probe.py
```

The probe prints the base and preview sections, request counts, row counts and empty-state
visibility side by side.

## Targeted E2E lane

```sh
# from the slice worktree; the helper reads the compose database URL at runtime
./.venv/bin/python specs/246-media-library-bible-rail/preview/run_tests.py   test tests.e2e.test_media_library_bible_rail --noinput
```

Red on the base view: `0 != 1` requests and `'alkitab' != 'media-library'`. Green with the fix.
