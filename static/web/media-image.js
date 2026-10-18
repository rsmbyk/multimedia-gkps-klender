/* Image bytes always come from the verified local Media Library identity. */
(function () {
  'use strict';
  var base = 'http://127.0.0.1:63174/v1/files/';
  function mime(bytes) {
    if (bytes.length >= 8 && bytes[0] === 137 && bytes[1] === 80 && bytes[2] === 78
        && bytes[3] === 71 && bytes[4] === 13 && bytes[5] === 10
        && bytes[6] === 26 && bytes[7] === 10) return 'image/png';
    if (bytes[0] === 255 && bytes[1] === 216 && bytes[2] === 255) return 'image/jpeg';
    var ascii = String.fromCharCode.apply(null, bytes.slice(0, 12));
    if (ascii.startsWith('GIF87a') || ascii.startsWith('GIF89a')) return 'image/gif';
    if (ascii.startsWith('RIFF') && ascii.slice(8, 12) === 'WEBP') return 'image/webp';
    return '';
  }
  function abortError() { return new DOMException('Image request cancelled', 'AbortError'); }
  async function load(sha, signal) {
    if (!/^[a-f0-9]{64}$/.test(sha)) throw new Error('Invalid image identity');
    var response = await fetch(base + sha, {mode: 'cors', cache: 'no-store', signal: signal});
    if (!response.ok) throw new Error('Image unavailable on this computer');
    var original = await response.blob();
    var type = mime(new Uint8Array(await original.slice(0, 16).arrayBuffer()));
    if (!type) throw new Error('Unsupported image bytes');
    var url = URL.createObjectURL(new Blob([original], {type: type}));
    try {
      var probe = new Image();
      probe.src = url;
      await probe.decode();
      if (signal && signal.aborted) throw abortError();
      return {url: url, width: probe.naturalWidth, height: probe.naturalHeight};
    } catch (error) {
      URL.revokeObjectURL(url);
      throw error;
    }
  }
  window.GKPSMediaImage = {load: load};
})();
