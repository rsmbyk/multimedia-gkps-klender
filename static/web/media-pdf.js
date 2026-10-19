/* Render verified local PDF bytes, never a filename or remote URL. */
(function () {
  'use strict';
  var base = 'http://127.0.0.1:63174/v1/files/';
  var library = null;
  var source = document.currentScript && document.currentScript.dataset.pdfjsSource;
  var worker = document.currentScript && document.currentScript.dataset.pdfjsWorker;
  function engine() {
    if (!library) library = import(source).then(function (pdfjs) {
      pdfjs.GlobalWorkerOptions.workerSrc = worker;
      return pdfjs;
    });
    return library;
  }
  function aborted() { return new DOMException('PDF request cancelled', 'AbortError'); }
  async function load(sha, signal) {
    if (!/^[a-f0-9]{64}$/.test(sha)) throw new Error('Invalid PDF identity');
    var response = await fetch(base + sha, {mode: 'cors', cache: 'no-store', signal: signal});
    if (!response.ok) throw new Error('PDF unavailable on this computer');
    var bytes = new Uint8Array(await response.arrayBuffer());
    if (signal && signal.aborted) throw aborted();
    if (bytes.length < 5 || String.fromCharCode.apply(null, bytes.slice(0, 5)) !== '%PDF-') {
      throw new Error('Unsupported PDF bytes');
    }
    var pdfjs = await engine();
    if (signal && signal.aborted) throw aborted();
    var task = pdfjs.getDocument({data: bytes, isEvalSupported: false, enableScripting: false});
    try {
      var document = await task.promise;
      if (signal && signal.aborted) { await document.destroy(); throw aborted(); }
      if (!document.numPages) { await document.destroy(); throw new Error('Empty PDF'); }
      return document;
    } catch (error) {
      await task.destroy();
      throw error;
    }
  }
  async function paint(document, number, canvas, availableWidth, availableHeight, signal) {
    if (signal && signal.aborted) throw aborted();
    var page = await document.getPage(number);
    try {
      if (signal && signal.aborted) throw aborted();
      var source = page.getViewport({scale: 1});
      var scale = Math.min(1, availableWidth / source.width, availableHeight / source.height);
      var viewport = page.getViewport({scale: scale});
      var pixelRatio = Math.min(window.devicePixelRatio || 1, 2,
        Math.sqrt(6000000 / (viewport.width * viewport.height)));
      canvas.width = Math.max(1, Math.floor(viewport.width * pixelRatio));
      canvas.height = Math.max(1, Math.floor(viewport.height * pixelRatio));
      canvas.style.width = Math.floor(viewport.width) + 'px';
      canvas.style.height = Math.floor(viewport.height) + 'px';
      var render = page.render({canvasContext: canvas.getContext('2d'), viewport: viewport,
        transform: pixelRatio === 1 ? null : [pixelRatio, 0, 0, pixelRatio, 0, 0]});
      if (signal) signal.addEventListener('abort', function () { render.cancel(); }, {once: true});
      await render.promise;
      if (signal && signal.aborted) throw aborted();
      return {width: viewport.width, height: viewport.height};
    } finally {
      page.cleanup();
    }
  }
  window.GKPSMediaPDF = {load: load, paint: paint};
})();
