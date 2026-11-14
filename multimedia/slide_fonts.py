"""The faces the decks ask for, and what this machine draws instead.

The image's answer is configuration, not code: `docker/slides-fonts.conf` names the mapping and
fontconfig applies it. This module exists so the same answer can be *read back* — by the build, which
refuses a monospaced fallback, and by the operator, who wants to see the mapping on their own image.

A monospaced fallback is not a cosmetic defect: every proportional glyph gets the same advance, so
every run re-wraps and the whole slide reflows. This deck's `Calibri` answered `Liberation Mono`
before spec 166.
"""

import subprocess

# The families the worship decks are set in. `Calibri Light` reaches a slide through the theme rather
# than through a run, which is why it is listed beside the run-level faces.
FAMILIES = (
    'Calibri',
    'Calibri Light',
    'Cambria',
    'Arial',
    'Arial Narrow',
    'Times New Roman',
    'Courier New',
    'Britannic Bold',
    'Berlin Sans FB Demi',
)

# Asked for a proportional face, drawn in a mono one: the failure this module exists to catch. Courier
# New is the one family that is *supposed* to reach a monospaced face.
MONOSPACED_BY_DESIGN = ('Courier New',)


def mapping():
    """Resolve each family through fontconfig. Returns {requested: drawn}."""
    resolved = {}
    for family in FAMILIES:
        try:
            output = subprocess.run(['fc-match', '-f', '%{family}', family], capture_output=True,
                                    text=True, timeout=10, check=True).stdout
        except (OSError, subprocess.SubprocessError):
            continue
        drawn = output.split(',')[0].strip()
        if drawn:
            resolved[family] = drawn
    return resolved


def violations(resolved):
    """The (requested, drawn) pairs where a proportional family landed on a mono face."""
    return [(asked, drawn) for asked, drawn in resolved.items()
            if asked not in MONOSPACED_BY_DESIGN and drawn.split(',')[0].strip().endswith('Mono')]


def main():
    resolved = mapping()
    if not resolved:
        print('slide fonts: fontconfig is unavailable; nothing to check.')
        return 0
    problems = violations(resolved)
    for asked, drawn in resolved.items():
        print(f'  {asked:<22} -> {drawn}')
    if problems:
        print('slide fonts: a proportional family resolves to a monospaced face:')
        for asked, drawn in problems:
            print(f'  {asked} -> {drawn}')
        return 1
    print(f'slide fonts: {len(resolved)} families resolve, none monospaced.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
