"""Screen boundaries for ordinary Tata Ibadah Text entries."""


def line_shape(text):
    return [bool(line.strip()) for line in (text or '').split('\n')]


def eligible_boundaries(text):
    shape = line_shape(text)
    return {index for index in range(1, len(shape))
            if shape[index - 1] and shape[index]}


def default_breaks(text):
    """Pair nonempty lines, restarting after each blank line."""
    boundaries = set()
    shape = line_shape(text)
    count = 0
    for index, present in enumerate(shape, 1):
        if not present:
            count = 0
            continue
        count += 1
        if count == 2:
            if index < len(shape) and shape[index]:
                boundaries.add(index)
            count = 0
    return sorted(boundaries)


def valid_breaks(text, breaks):
    allowed = eligible_boundaries(text)
    return (isinstance(breaks, list)
            and all(type(value) is int and value in allowed for value in breaks)
            and breaks == sorted(set(breaks)))
