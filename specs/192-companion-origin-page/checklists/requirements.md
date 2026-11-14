# Media Library Checklist: The companion's page manages this computer's origins

**Spec**: `specs/192-companion-origin-page/spec.md` · **Created**: 2026-11-14 · **Depth**: Lite

- [x] CHK001 Is the page reachable in every start mode and with an empty recorded set — its own origin never needing the allowlist? [Completeness, Spec §Functional FR-001]
- [x] CHK002 Is the empty recorded state said outright on the page? [Coverage, Spec §US1]
- [x] CHK003 Is the exact-origin grammar complete — every rule, the first break named — for the page's form? [Clarity, Spec §Functional FR-002]
- [x] CHK004 Is a duplicate refused, both as an add and as an edit? [Coverage, Spec §US2]
- [x] CHK005 Does a deletion renumber the list? [Coverage, Spec §US2]
- [x] CHK006 Is persistence defined — where the set lives, restart and reboot survival, volume removal documented? [Clarity, Spec §Functional FR-002]
- [x] CHK007 Is enforcement per request over the union of the local seeds and the recorded set? [Completeness, Spec §Functional FR-003]
- [x] CHK008 Does a refusal name the configuration page, and carry no CORS headers? [Coverage, Spec §Functional FR-003]
- [x] CHK009 Are the page's endpoints bound to the loopback Host and same-origin, with no media token required? [Completeness, Spec §Functional FR-004]
- [x] CHK010 Are the local seeds read-only on the page? [Coverage, Spec §US1]
- [x] CHK011 Does the fonts section name directories with family counts and say outright when none is found? [Coverage, Spec §Functional FR-005]
- [x] CHK012 Is the launcher free of origin logic, and does plain compose start without `.env`? [Completeness, Spec §Functional FR-006]
- [x] CHK013 Is the operator variable removed everywhere — compose, `.env.example`, README, docs, tests — no occurrence left? [Completeness, Spec §Functional FR-006]
- [x] CHK014 Does the launcher still name its mounted font directories — count and paths agreeing, zero said outright? [Coverage, Spec §Functional FR-007]
- [x] CHK015 Does the web app surface the companion's refusal message when present? [Coverage, Spec §Functional FR-008]
- [x] CHK016 Is a dead origin line in an existing `.env` documented as ignored? [Completeness, Spec §US4]
- [x] CHK017 Does every functional requirement trace to at least one acceptance scenario that observes it? [Traceability, Gap]
- [x] CHK018 Is the documentation update (README first-time section, `docs/local-media-companion.md`) part of the slice's scope? [Completeness, Gap]
