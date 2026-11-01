# Analysis — the computer's own fonts reach the converter

**Date**: 2026-11-01
**Artifacts read**: `spec.md` `9de84903a8b9` · `plan.md` `8d7645657721` · `tasks.md` `9c34e4a797a6` ·
`research.md` `1dcabbcb2b0e` (pre-edit) · `checklists/requirements.md` `0f9f60ea4e9f`
**Metrics**: 9 requirements · 5 success criteria · 17 tasks · coverage 100% (FR 9/9, SC 5/5) ·
verification split **3 test · 11 inspection · 7 manual** · 0 CRITICAL · 1 HIGH

## Findings

| ID | Severity | Area | Finding | Disposition |
| --- | --- | --- | --- | --- |
| A1 | HIGH | Verification | FR-002, SC-002 and US2/AC1 — the Office faces actually being drawn — can only be verified by hand on a Windows computer with Office, which this machine is not. The highest-value outcome rests on the one row no command here can run. | Accepted and recorded: the steps are written in `quickstart.md` §6, and the operator's own laptop is the machine that runs them. The substitute path (US2/AC2) is verified here as the counter-case. |
| A2 | MEDIUM | Existing red test | `tests/test_docker_compose.py::DockerComposePortRulesTests::test_media_companion_uses_private_loopback_port_and_named_volume` is red on `develop`: it still expects `media.volumes` to hold only the named volume, and spec 166 added the operator's font mount. Reproduced on the untouched branch tip. | Fixed in the slice, by T005 — the assertion learns the second mount. The red predates this work and is noted in the closing report. |
| A3 | MEDIUM | Measurability | SC-005's "under 10 s on a 1,000-file directory" cannot be measured on this machine, which has no such directory; the closest is the container's own font tree. | Accepted: the number is measured on what is available and the shortfall named in the closing report rather than presented as a passed criterion. |
| A4 | LOW | Coverage shape | FR-008 (the renderer identity keeps covering the font inventory) has no code change — it is a guard that the change must not break. | Accepted; declared `inspection`, as the plan's table already does. |
| A5 | LOW | Research completeness | D003 did not say whether an empty generated override is legal, which the launcher will produce whenever a computer has no font directory. Measured afterwards: an override with an empty `volumes` list, or none at all, merges cleanly. | Mechanical fix applied — `research.md` D003 now records it; no requirement moved. |
| A6 | LOW | Terminology | The spec says "operator directory" and "host font source"; the existing documentation says "the operator's fonts" and "the mounted directory". | Fixed by T008 and T014, which rewrite the documentation in the spec's terms. |

## History

- 2026-11-01 — first pass, before gate 2: 6 findings (0 CRITICAL, 1 HIGH, 2 MEDIUM, 3 LOW); A5 fixed
  mechanically, A2 fixed by a task, A6 fixed by the documentation tasks; A1, A3 and A4 accepted.
