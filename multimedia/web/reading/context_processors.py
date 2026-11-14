"""Template context for the reading shell (spec 005).

The sidebar editor controls are rendered only when editing is allowed, which is
one setting away from staff-only -- see ``reading.editors.editors_allowed``.
"""

from multimedia.web.reading import editors


def sidebar_editors(request):
    return {'editor_enabled': editors.editors_allowed(request)}
