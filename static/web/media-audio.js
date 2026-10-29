/* Fetch only the immutable, companion-verified local identity. */
(function () {
  'use strict';
  function mime(bytes) {
    var head = String.fromCharCode.apply(null, bytes.slice(0, 32));
    if (head.startsWith('ID3') || (bytes[0] === 255 && (bytes[1] & 224) === 224)) return 'audio/mpeg';
    if (head.startsWith('fLaC')) return 'audio/flac';
    if (head.startsWith('OggS') && !head.includes('theora')) return 'audio/ogg';
    if (head.startsWith('RIFF') && head.slice(8, 12) === 'WAVE') return 'audio/wav';
    if (head.slice(4, 8) === 'ftyp' && head.slice(8, 24).includes('M4A')) return 'audio/mp4';
    return '';
  }
  async function load(sha, signal) {
    if (!/^[a-f0-9]{64}$/.test(sha)) throw new Error('Invalid audio identity');
    var response = await fetch('http://127.0.0.1:63174/v1/files/' + sha,
      {mode: 'cors', cache: 'no-store', signal: signal});
    if (!response.ok) throw new Error('Audio unavailable on this computer');
    var original = await response.blob();
    var type = mime(new Uint8Array(await original.slice(0, 32).arrayBuffer()));
    if (!type) throw new Error('Unsupported audio bytes');
    if (signal && signal.aborted) throw new DOMException('Audio request cancelled', 'AbortError');
    return URL.createObjectURL(new Blob([original], {type: type}));
  }
  function clock(seconds) {
    if (!Number.isFinite(seconds)) return '0:00';
    return Math.floor(seconds / 60) + ':' + String(Math.floor(seconds % 60)).padStart(2, '0');
  }
  function attach(host, options) {
    var audio = new Audio();
    audio.preload = 'metadata';
    var play = host.querySelector('[data-audio-play]');
    var seek = host.querySelector('[data-audio-seek]');
    var elapsed = host.querySelector('[data-audio-elapsed]');
    var total = host.querySelector('[data-audio-total]');
    var ready = false;
    var lastPlaying = false;
    function update() {
      var duration = Number.isFinite(audio.duration) ? audio.duration : 0;
      elapsed.textContent = clock(audio.currentTime);
      total.textContent = clock(duration);
      seek.style.setProperty('--progress', duration ? (audio.currentTime / duration * 100) + '%' : '0%');
      if (seek.tagName === 'INPUT') { seek.max = String(duration || 1); seek.value = String(audio.currentTime); }
      play.dataset.playing = audio.paused ? 'false' : 'true';
      play.setAttribute('aria-label', audio.paused ? 'Play audio' : 'Pause audio');
      if (lastPlaying !== !audio.paused) {
        lastPlaying = !audio.paused;
        if (options && options.onPlayback) options.onPlayback(lastPlaying);
      }
    }
    function toggle() {
      if (!ready) return;
      if (audio.paused) {
        if (options && options.onPlayRequest) options.onPlayRequest();
        audio.play().catch(fail);
      }
      else audio.pause();
    }
    function fail() { if (options && options.onError) options.onError(); }
    function setPosition(event) {
      if (!ready || !Number.isFinite(audio.duration)) return;
      if (seek.tagName === 'INPUT') audio.currentTime = Math.min(audio.duration, Number(seek.value));
      else {
        var box = seek.getBoundingClientRect();
        audio.currentTime = Math.max(0, Math.min(audio.duration,
          (event.clientX - box.left) / box.width * audio.duration));
      }
      update();
    }
    play.addEventListener('click', toggle);
    if (seek.tagName === 'INPUT') seek.addEventListener('input', setPosition);
    else {
      seek.addEventListener('pointerdown', function (event) { seek.setPointerCapture(event.pointerId); setPosition(event); });
      seek.addEventListener('pointermove', function (event) { if (seek.hasPointerCapture(event.pointerId)) setPosition(event); });
    }
    audio.addEventListener('loadedmetadata', function () { ready = true; update(); if (options && options.onReady) options.onReady(); });
    audio.addEventListener('timeupdate', update);
    audio.addEventListener('play', update);
    audio.addEventListener('pause', update);
    audio.addEventListener('ended', update);
    audio.addEventListener('error', fail);
    update();
    return {
      audio: audio, toggle: toggle,
      pause: function () { audio.pause(); },
      setUrl: function (url) { audio.src = url; audio.load(); },
      stop: function () { audio.pause(); audio.removeAttribute('src'); audio.load(); ready = false; }
    };
  }
  window.GKPSMediaAudio = {load: load, attach: attach};
})();
