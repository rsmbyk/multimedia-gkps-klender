"""Display helpers for the reading pages (spec 057)."""


def format_verses(numbers):
    """A song's verse numbers as runs: ``[1, 2, 3, 5, 6, 8, 9, 10]`` -> ``1-3, 5, 6, 8-10``.

    Input is sorted and de-duplicated first. A run of three or more consecutive numbers
    becomes ``a-b``; a run of one or two stays as separate numbers.
    """
    values = sorted({int(number) for number in numbers or []})
    runs = []
    for number in values:
        if runs and number == runs[-1][1] + 1:
            runs[-1][1] = number
        else:
            runs.append([number, number])
    parts = []
    for start, end in runs:
        if end - start >= 2:
            parts.append(f'{start}-{end}')
        else:
            parts.extend(str(n) for n in range(start, end + 1))
    return ', '.join(parts)
