# Contracts

None. The slice adds only browser-local state to an existing modal; it introduces no URL, request,
response shape, Django view, model field or event consumed outside `static/web/generate.js`.

The `editor:saved` event and the generate POST payload are existing contracts and are consumed
unchanged. The new leave-confirmation layer is markup inside `_generate_modal.html`, not an interface.
