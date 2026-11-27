# Data model — spec 246

No change. No model, field, migration, manager, serializer or permission is added or altered.

The slice changes one server-rendered value: the template context key `section` passed by
`multimedia/web/reading/views.py::media_library`. The value `media-library` is a destination
identity carried on `<html data-section>`; it is not a database entity and is not one of the three
reading sections (`alkitab`, `kidung`, `tatib`).
