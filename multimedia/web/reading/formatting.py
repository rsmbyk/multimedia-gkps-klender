"""Display helpers for the reading pages (spec 057)."""


def format_verses(numbers):
    """A song's verse numbers as runs: ``[1, 2, 4, 5]`` -> ``1–2, 4–5``.

    Input is sorted and de-duplicated first. Any run of two or more consecutive
    numbers becomes ``a–b`` with an en dash, so a pair collapses too — the same
    reading the song entry's own summary gives (spec 210), which keeps every verse
    reference on the page in one shape.
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
        parts.append(f'{start}–{end}' if end > start else str(start))
    return ', '.join(parts)
