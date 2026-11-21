# Tasks: the runtime entrypoint survives the bind mount

**Slice**: `specs/217-entrypoint-shadowed` · **Created**: 2026-11-21 · Ordering per SDD-16; `[P]`
means order-independent, not concurrent.

## Setup

- No task — the branch and worktree were cut at the change request (C-SDD-GIT).

## US1 — A CRLF checkout starts both services

**Goal**: the container's entrypoint is a copy no mount can replace.

**Independent test**: the built image, run with a CRLF checkout mounted at `/app`, reaches its command.

- [x] T001 [US1] Write the failing test `RuntimeEntrypointPathTests.test_the_runtime_entrypoint_lives_outside_the_mounted_tree` in `tests/test_runtime_entrypoint.py`: the `Dockerfile` copies the entrypoint to a path that does not begin `/app/`, and the strip names the same path. Fails today — the only copy target is inside the context (C-SDD-TDD handoff for FR-001/FR-002).
- [x] T002 [US1] Make it pass: `COPY docker/entrypoint.sh /usr/local/bin/gkps-entrypoint.sh` and one `RUN sed -i 's/\r$//' … && chmod +x …` on that path in `Dockerfile`.
- [x] T003 [P] [US1] Write the failing test `test_the_image_starts_from_that_path_and_no_other`: `ENTRYPOINT` names exactly one absolute path besides `/bin/sh`, and it is the copied one (FR-003).
- [x] T004 [US1] Make it pass: `ENTRYPOINT ["/bin/sh", "/usr/local/bin/gkps-entrypoint.sh"]`.
- [x] T005 [P] [US1] Write the failing tests `RuntimeEntrypointStripTests.test_the_copied_entrypoint_fails_before_the_strip` and `…_runs_after_the_strip`: the strip command as written, applied to a CRLF fixture, makes `/bin/sh` run it (FR-002, SC-001).
- [x] T006 [P] [US1] Write `…::test_the_strip_leaves_an_lf_entrypoint_untouched` (US1/AC3).
- [x] T007 [US1] Narrow `tests/test_entrypoint_line_endings.py` to the `*.sh` pin and point its docstring at the new module; delete its `Dockerfile`-placement test, whose behaviour is gone (TDD-07).
- [x] T008 [US1] `manual` — FR-004/SC-001: build the image from a CRLF context and run it with that context at `/app`; `OK`, exit 0. Without the mount, `OK`. Inside: runtime copy 0 CR bytes, mounted file 19.
- [x] T009 [US1] `manual` — SC-003: on a Windows checkout, `docker compose build && docker compose up -d`; `web` and `media` `Up`. Not runnable here (the worktree's compose project would take the running stack's ports).
- [x] T010 [US1] `inspection` — the edge rows: `docker/entrypoint.sh` is byte-identical to the copy spec 216 verified, and `git check-attr eol` still answers `lf` for the shell scripts.

## Polish

- [x] T011 [Polish] Fold: rewrite `local-stack/R4` as a `modified` delta — the runtime copy lives
  outside the mounted tree — with `fold.md` (capabilities, operations, counts).
- [x] T012 [Polish] First commit at Fold: `Dockerfile`, both test modules, spec pack, card `ITEM-232`
  and its board row, `ITEM-233` filed in Backlog.
- [ ] T013 [Polish] Delivery: PR as a draft, then ready; card `In review` with `pr:` in a commit after
  the number exists; `VERSION` → `1.36.3` and the `CHANGELOG.md` Fixed line in the pre-merge commit;
  card `Done` and the board row with it, in the same PR.