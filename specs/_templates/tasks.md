# Tasks: \<CODE\> — \<Feature name\>

Spec: [`spec.md`](spec.md) (`<CODE>`) · Plan: [`plan.md`](plan.md)

Work top to bottom. Check a box when the task and its verification are done.
Task IDs: `<CODE>-T<n>`.

## Checklist

- [ ] **\<CODE\>-T1 — \<objective\>**
  - Touch: \<files / areas\>
  - Verify: \<failing test first if behavior; commands; manual check\>
  - Covers: \<e.g. CODE-AC1, CODE-AC2\>

- [ ] **\<CODE\>-T2 — \<objective\>**
  - Touch:
  - Verify:
  - Covers:

- [ ] **\<CODE\>-T3 — \<objective\>**
  - Touch:
  - Verify:
  - Covers:

## Done when

- All acceptance criteria in `spec.md` are met (or verified as as-built).
- Relevant test suites pass (`pytest` / `npm test` as applicable).
- Changelog `## Unreleased` bullet added if the change warrants one.
