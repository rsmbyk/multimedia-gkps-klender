"""Analyze checks for spec 212 (SDD-17): coverage, split, assignment, paths, digests.

Written for this pack because the `check_pack_consistency.py` that spec 209's analysis
names is not present in this repository or anywhere on this machine.

    .venv/bin/python specs/212-copy-confirm-layer/preview/analyze.py
"""
import hashlib
import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parents[3]
PACK = REPO / 'specs' / '212-copy-confirm-layer'


def text(name):
    return (PACK / name).read_text()


def main():
    spec, plan, tasks = text('spec.md'), text('plan.md'), text('tasks.md')
    failures = []

    # 1. Coverage — every FR / SC id in the spec is in the plan's traceability table
    spec_ids = sorted(set(re.findall(r'^\| (FR-\d{3}|SC-\d{3}) \|', spec, re.M)))
    plan_ids = set(re.findall(r'^\| (FR-\d{3}|SC-\d{3}) \|', plan, re.M))
    missing = [i for i in spec_ids if i not in plan_ids]
    if missing:
        failures.append(f'COVERAGE: {missing} in spec, not in plan')
    print(f'COVERAGE {len(spec_ids) - len(missing)}/{len(spec_ids)} ids traced'
          f'{" — PASS" if not missing else " — FAIL " + str(missing)}')

    # 2. Split — declared numbers equal the rows counted in the table
    rows = [ln for ln in plan.splitlines() if ln.startswith('| ') and '→' in ln or
            (ln.startswith('| ') and '`inspection`' in ln)]
    counted = {'test': 0, 'inspection': 0, 'manual': 0}
    for ln in plan.splitlines():
        if not ln.startswith('| ') or ln.startswith('| Requirement') or ln.startswith('| ---'):
            continue
        cells = ln.split('|')
        if len(cells) < 4:
            continue
        method = cells[3]
        for key in counted:
            if f'`{key}`' in method:
                counted[key] += 1
    declared = re.search(r'\*\*Verification split\*\*: (\d+) test · (\d+) inspection · (\d+) manual',
                         plan)
    want = tuple(int(x) for x in declared.groups()) if declared else None
    got = (counted['test'], counted['inspection'], counted['manual'])
    ok = want == got
    if not ok:
        failures.append(f'SPLIT: declared {want}, counted {got}')
    print(f'SPLIT declared {want} = counted {got}{" — PASS" if ok else " — FAIL"}')

    # 3. Assignment — every FR / SC id in the plan is named by at least one task
    unnamed = [i for i in spec_ids if i not in tasks]
    if unnamed:
        failures.append(f'ASSIGNMENT: {unnamed} traced in plan, named by no task')
    print(f'ASSIGNMENT {len(spec_ids) - len(unnamed)}/{len(spec_ids)} ids named in tasks'
          f'{" — PASS" if not unnamed else " — FAIL " + str(unnamed)}')

    # 4. Paths — every repo-relative path the pack names exists
    named = set()
    for body in (spec, plan, tasks, text('quickstart.md'), text('research.md')):
        named |= set(re.findall(r'`((?:specs|static|tests|multimedia|docs|backlog)/[^`\s]+)`', body))
    missing_paths = sorted(p for p in named
                           if '*' not in p and not (REPO / p.split(':')[0]).exists())
    if missing_paths:
        failures.append(f'PATHS: {missing_paths}')
    print(f'PATHS {len(named) - len(missing_paths)}/{len(named)} exist'
          f'{" — PASS" if not missing_paths else " — FAIL " + str(missing_paths)}')

    # 5. Digests
    print('\nDIGESTS')
    for name in ('spec.md', 'plan.md', 'research.md', 'data-model.md', 'quickstart.md',
                 'tasks.md', 'checklists/requirements.md', 'contracts/README.md'):
        digest = hashlib.sha256((PACK / name).read_bytes()).hexdigest()[:12]
        print(f'  {name:32s} {digest}')

    return 1 if failures else 0


if __name__ == '__main__':
    sys.exit(main())
