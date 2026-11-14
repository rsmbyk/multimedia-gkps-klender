"""Screen boundaries for Tata Ibadah Text entries."""


def line_shape(text):
    return [bool(line.strip()) for line in (text or '').split('\n')]


def eligible_boundaries(text):
    shape = line_shape(text)
    return {index for index in range(1, len(shape))
            if shape[index - 1] and shape[index]}


def single_screen_boundaries(text):
    """Place a boundary after each content line except the last, across blank rows too."""
    positions = [index for index, present in enumerate(line_shape(text), 1) if present]
    return set(positions[:-1])


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


def valid_breaks(text, breaks, single_screen=False):
    allowed = single_screen_boundaries(text) if single_screen else eligible_boundaries(text)
    return (isinstance(breaks, list)
            and all(type(value) is int and value in allowed for value in breaks)
            and breaks == sorted(set(breaks)))
