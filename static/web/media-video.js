/* Video bytes are fetched by immutable Media Library identity and typed from signatures. */
(function () {
  'use strict';

  var base = 'http://127.0.0.1:63174/v1/files/';

  function mime(bytes) {
    var head = String.fromCharCode.apply(null, bytes.slice(0, 256));
    if (bytes[0] === 0x1a && bytes[1] === 0x45 && bytes[2] === 0xdf && bytes[3] === 0xa3)
      return 'video/webm';
    if (head.startsWith('OggS') && head.toLowerCase().includes('theora')) return 'video/ogg';
    if (head.startsWith('RIFF') && head.slice(8, 12) === 'AVI ') return 'video/x-msvideo';
    if (head.slice(4, 8) === 'ftyp') return head.slice(8, 12) === 'qt  ' ? 'video/quicktime' : 'video/mp4';
    if (bytes[0] === 0 && bytes[1] === 0 && bytes[2] === 1
        && (bytes[3] === 0xba || bytes[3] === 0xb3)) return 'video/mpeg';
    return '';
  }

  async function load(sha, signal) {
    if (!/^[a-f0-9]{64}$/.test(sha)) throw new Error('Invalid video identity');
    var response = await fetch(base + sha, {mode: 'cors', cache: 'no-store', signal: signal});
    if (!response.ok) throw new Error('Video unavailable on this computer');
    var original = await response.blob();
    var type = mime(new Uint8Array(await original.slice(0, 256).arrayBuffer()));
    if (!type) throw new Error('Unsupported video bytes');
    if (signal && signal.aborted) throw new DOMException('Video request cancelled', 'AbortError');
    return URL.createObjectURL(new Blob([original], {type: type}));
  }

  function clock(seconds) {
    if (!Number.isFinite(seconds)) return '0:00';
    return Math.floor(seconds / 60) + ':' + String(Math.floor(seconds % 60)).padStart(2, '0');
  }

  function attach(host, options) {
    options = options || {};
    var video = host.querySelector('video');
    var plays = [].slice.call(host.querySelectorAll('[data-video-play]'));
    var seek = host.querySelector('[data-video-seek]');
    var elapsed = host.querySelector('[data-video-elapsed]');
    var total = host.querySelector('[data-video-total]');
    var ready = false;
    var lastPlaying = false;
    var destroyed = false;
    var listeners = [];

    function listen(target, name, callback) {
      target.addEventListener(name, callback);
      listeners.push([target, name, callback]);
    }

    function update() {
      if (destroyed) return;
      var duration = Number.isFinite(video.duration) ? video.duration : 0;
      var playing = !video.paused && !video.ended;
      host.classList.toggle('is-playing', playing);
      if (elapsed) elapsed.textContent = clock(video.currentTime);
      if (total) total.textContent = clock(duration);
      if (seek) {
        seek.style.setProperty('--progress', duration ? (video.currentTime / duration * 100) + '%' : '0%');
        if (seek.tagName === 'INPUT') {
          seek.max = String(duration || 1);
          seek.value = String(video.currentTime || 0);
        }
      }
      plays.forEach(function (play) {
        play.dataset.playing = playing ? 'true' : 'false';
        play.setAttribute('aria-label', playing ? 'Pause video' : 'Play video');
      });
      if (lastPlaying !== playing) {
        lastPlaying = playing;
        if (options.onPlayback) options.onPlayback(playing);
      }
    }

    function fail() {
      if (!destroyed && options.onError) options.onError();
    }

    function toggle() {
      if (destroyed || !ready) return;
      if (video.paused || video.ended) {
        if (options.onPlayRequest) options.onPlayRequest();
        video.play().catch(fail);
      } else video.pause();
    }

    function setPosition(event) {
      if (!ready || !Number.isFinite(video.duration)) return;
      if (seek.tagName === 'INPUT') video.currentTime = Math.max(0, Math.min(video.duration, Number(seek.value)));
      else {
        var box = seek.getBoundingClientRect();
        if (!box.width) return;
        video.currentTime = Math.max(0, Math.min(video.duration,
          (event.clientX - box.left) / box.width * video.duration));
      }
      update();
    }

    plays.forEach(function (play) { listen(play, 'click', toggle); });
    if (seek) {
      if (seek.tagName === 'INPUT') listen(seek, 'input', setPosition);
      else {
        listen(seek, 'pointerdown', function (event) {
          seek.setPointerCapture(event.pointerId);
          setPosition(event);
        });
        listen(seek, 'pointermove', function (event) {
          if (seek.hasPointerCapture(event.pointerId)) setPosition(event);
        });
      }
    }
    listen(video, 'loadedmetadata', function () {
      ready = true;
      update();
      if (options.onReady) options.onReady();
    });
    listen(video, 'timeupdate', update);
    listen(video, 'play', update);
    listen(video, 'pause', update);
    listen(video, 'ended', function () {
      update();
      if (options.onEnded) options.onEnded();
    });
    listen(video, 'error', fail);
    update();

    return {
      video: video,
      toggle: toggle,
      pause: function () { if (!destroyed) video.pause(); },
      setUrl: function (url) { video.src = url; video.load(); },
      stop: function () {
        if (destroyed) return;
        video.pause();
        try { video.currentTime = 0; } catch (error) { /* no metadata yet */ }
        update();
        destroyed = true;
        listeners.forEach(function (listener) {
          listener[0].removeEventListener(listener[1], listener[2]);
        });
        listeners = [];
        video.removeAttribute('src');
        video.load();
        ready = false;
      }
    };
  }

  window.GKPSMediaVideo = {load: load, attach: attach};
})();
