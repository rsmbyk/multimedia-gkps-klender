/* Spec 092: navigation fallback for the two explicitly supported page shells. */
var CACHE = 'gkps-public-shell-__VERSION__';
var ASSETS = [
  '/home/', '/offline/projector-shell/',
  '/static/assets/gkps.png',
  '/static/styles/design/tokens.css',
  '/static/styles/design/components.css',
  '/static/styles/design/offline.css',
  '/static/styles/design/projector.css',
  '/static/web/offline-library.js', '/static/web/offline-status.js',
  '/static/web/offline-render.js', '/static/web/reading.js',
  '/static/web/projector.js', '/static/web/projector-library.js',
  '/static/web/display.js', '/static/web/focus.js',
  '/static/web/editors.js', '/static/web/date-picker.js', '/static/web/entries.js',
  '/static/web/reorder.js', '/static/web/preview.js',
  '/static/web/media-pdf.js', '/static/vendor/pdfjs/pdf.min.mjs',
  '/static/vendor/pdfjs/pdf.worker.min.mjs'
];
self.addEventListener('install', function (event) {
  event.waitUntil(caches.open(CACHE).then(function (cache) { return cache.addAll(ASSETS); }));
});
self.addEventListener('activate', function (event) {
  event.waitUntil(caches.keys().then(function (keys) {
    return Promise.all(keys.filter(function (key) {
      return key.indexOf('gkps-public-shell-') === 0 && key !== CACHE;
    }).map(function (key) { return caches.delete(key); }));
  }).then(function () { return self.clients.claim(); }));
});
function supported(path) {
  return path === '/' || path === '/home/' || path === '/search' || path === '/search/'
    || /^\/bible\/(?:\d+\/){0,2}$/.test(path)
    || /^\/songs\/(?:book\/\d+\/|\d+\/)?$/.test(path)
    || /^\/tatib\/(?:\d+\/)?$/.test(path)
    || /^\/obs\/service\/\d+\/$/.test(path);
}
self.addEventListener('fetch', function (event) {
  var request = event.request;
  if (request.method !== 'GET') return;
  var url = new URL(request.url);
  if (url.origin !== self.location.origin) return;
  if (request.mode === 'navigate' && supported(url.pathname)) {
    event.respondWith(fetch(request, {cache: 'no-store'}).catch(function () {
      var shell = /^\/obs\/service\/\d+\/$/.test(url.pathname)
        ? '/offline/projector-shell/' : '/home/';
      return caches.match(shell).then(function (response) {
        return response || Response.error();
      });
    }));
  } else if (ASSETS.indexOf(url.pathname) !== -1) {
    event.respondWith(caches.match(request).then(function (response) {
      return response || fetch(request);
    }));
  }
});
