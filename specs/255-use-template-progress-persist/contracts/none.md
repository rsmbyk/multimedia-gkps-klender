# Contracts

None. The slice changes where an existing client record lives and how one existing button paints a
mark. It introduces no URL, request, response, Django view, model field or event consumed outside
`static/web/generate.js` and `reading/tatib.html`.

`shell:page` is an existing event emitted by the reading shell (`static/web/reading.js:2221`); this
slice listens to it and does not change it.