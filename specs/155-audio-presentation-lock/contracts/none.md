# Contracts: none

No endpoint, no payload, no route and no template interface changes. The one seam this slice touches is
`GKPSMediaAudio.attach(host, options)` in `static/web/media-audio.js`, and both changes are additive:

| Addition | Shape | Consumers |
| --- | --- | --- |
| `options.onPlayRequest` | optional callback, called in `toggle()` before `audio.play()` | `projector.js` passes it; `preview.js` does not, so the preview dialog is unchanged |
| `handle.pause()` | method, no arguments, no return | `projector.js` calls it when the browser leaves fullscreen |

Nothing existing is renamed, removed or given new semantics: `load`, `attach`, `setUrl`, `stop`,
`toggle` and the `onReady`/`onError`/`onPlayback` callbacks keep their signatures, and the projector page's
markup, data islands and CSS class names are unchanged.
