# Analysis: the runtime entrypoint survives the bind mount

**Slice**: `specs/217-entrypoint-shadowed` · **Run**: 2026-11-21 · **Gate 2 pre-read**

## Artifacts read

| Artifact | SHA (git hash-object) |
| --- | --- |
| `spec.md` | `280fb71b4f41467e820fe962b958f56e80c6263e` |
| `plan.md` | `ca0ab408c518b7484bb1587350af335c8eb6aeb8` |
| `research.md` | `712205703c5dc5f08d82315e269a20d4c09f5b16` |
| `data-model.md` | `c71ed896fe85ad166fe91ef635cf3d6625259f8d` |
| `contracts/none.md` | `9e2732fb8dd2a00bbe262206daedc3f6f5cfc3a3` |
| `quickstart.md` | `ef2c67358a20713d084a5bd440a8a3ff7e0b4660` |
| `tasks.md` | `a7159c99137bbf09ac243ca128a0a03cb0b833cd` |
| `checklists/requirements.md` | `730fc5949173ce88ef57f4efbfef564f5e66d0ef` |

## Metrics

`FR: 4/4 with tasks · scenarios: 7/7 with a verification row · coverage (traceability): 100% ·
markers: 0 · findings: 0 CRITICAL, 1 HIGH, 1 MEDIUM, 0 LOW`

Coverage is read from Plan's traceability table (SDD-17): FR-001 → T001 (`test`), FR-002 → T005
(`test`), FR-003 → T003 (`test`), FR-004 → T008/T009 (`manual`). SC-001 → T008 (`manual`), SC-002 →
T001/T003 (`test`), SC-003 → T009 (`manual`). US1's three scenarios → T005, T008, T006. The four edge
cases → T008 (no mount), T010 (Linux checkout, contents unchanged), T008 (path inside the container).

## Findings

| ID | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| A-01 | HIGH | SC-003 — both services `Up` from a CRLF checkout — is marked `manual` and **cannot be run on this machine**: a `docker compose` project started from the worktree takes the same host ports (63404, 59075, 63174) as the running stack. The end-to-end claim therefore rests on the bind-mount shape, which reproduces what compose does to `web` (`- .:/app`) but not what it does to `media`. | **Accepted, with its cost stated.** `media`'s half is already evidenced: it has no mount and started on the operator's machine with `--build` (their own report). The bind-mount row is the shape that was broken. The row stays `manual` and names the operator's machine. |
| A-02 | MEDIUM | The `Dockerfile`'s `COPY . .` still puts the checkout's `docker/entrypoint.sh` at `/app/docker/entrypoint.sh`, so two copies of the file exist in the image and only one runs. A reader can reasonably edit the wrong one. | **Accepted.** The comment above the `COPY` names the mount and the reason; keeping the context copy is what lets `COPY . .` stay a single statement, and every other file in the tree already has the same shadowed-but-present status under the mount. |

No mechanical fixes were applied. The checklist's nine items map to the spec's sections — CHK001/CHK002
→ §US1 and §Edge Cases, CHK003 → §FR-003, CHK004 → §SC-002, CHK005 → §Assumptions, CHK006/CHK007 →
§FR-002 and §Assumptions, CHK008/CHK009 → §Success Criteria.

## History

- 2026-11-21 — first run: 0 CRITICAL, 100% coverage → gate 2 opens.