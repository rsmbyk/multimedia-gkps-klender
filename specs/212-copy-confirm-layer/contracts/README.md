# Contracts — spec 212

**none.**

The slice changes no external interface: no route, no request shape, no response shape, no template
variable, no script API. The markup the rules attach to is already emitted by
`multimedia/web/templates/reading/_copy_confirm.html`, and the copy endpoint it posts to
(`POST /tatib/<id>/copy-as-template/`) is unmodified.

The only contract this slice leans on is the class anatomy of that markup —
`.editor__confirm-layer > .editor__confirm > h3 + p + .editor__confirm-actions` — which the generate
page's twin dialog (`_generate_modal.html`) also uses. Changing that anatomy is out of scope; a rule
keyed to it is all this slice adds.
