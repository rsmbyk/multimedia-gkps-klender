/* Spec 092: public rail status, separate from the shared library store. */
(function () {
  'use strict';
  var library = window.GKPSOffline;
  var button = document.getElementById('offlineSyncButton');
  var panel = document.getElementById('offlineSyncPanel');
  if (!library || !button || !panel) return;
  var dot = document.getElementById('offlineSyncDot');
  var mark = document.getElementById('offlineSyncMark');
  var availability = document.getElementById('offlineSyncAvailability');
  var detail = document.getElementById('offlineSyncDetail');
  var connectionValue = document.getElementById('offlineConnectionValue');
  var connectionLabel = document.getElementById('offlineConnectionLabel');
  var synced = document.getElementById('offlineLastSynced');
  var checked = document.getElementById('offlineLastChecked');
  var action = document.getElementById('offlineSyncNow');
  var progress = document.getElementById('offlineSyncProgress');
  function date(value, empty) {
    return value ? new Date(value).toLocaleString() : empty;
  }
  function refresh() {
    library.status().then(function (status) {
      var state = status.syncing ? 'syncing' : status.ready
        ? (status.error ? 'stale' : 'ready') : 'empty';
      dot.dataset.state = mark.dataset.state = state;
      connectionValue.dataset.offline = String(status.offline);
      connectionLabel.textContent = status.offline ? 'Offline' : 'Online';
      synced.textContent = date(status.generation && status.generation.syncedAt, 'Never');
      checked.textContent = date(status.lastCheckedAt, 'Not checked');
      if (status.syncing) {
        availability.textContent = 'Syncing library…';
        detail.textContent = 'Checking for changes and saving updated content…';
      } else if (status.ready && status.error) {
        availability.textContent = 'Ready for offline use';
        detail.textContent = 'The latest update failed. The previously saved library is still available.';
      } else if (status.ready) {
        availability.textContent = 'Ready for offline use';
        detail.textContent = 'Bible, songs, and Tata Ibadah are saved and available offline.';
      } else {
        availability.textContent = 'Not ready for offline use';
        detail.textContent = 'The page shells and complete Bible, song, and Tata Ibadah library have not finished saving.';
      }
      action.textContent = status.syncing ? 'Syncing…' : status.offline ? 'Sync when online'
        : status.error ? 'Retry sync' : status.ready ? 'Sync now' : 'Start sync';
      action.disabled = status.syncing || status.offline;
      progress.hidden = !status.syncing;
    }).catch(function () {
      connectionValue.dataset.offline = String(!navigator.onLine);
      connectionLabel.textContent = navigator.onLine ? 'Online' : 'Offline';
      availability.textContent = 'Not ready for offline use';
      detail.textContent = 'Browser storage is unavailable.';
    });
  }
  button.addEventListener('click', function () {
    panel.hidden = !panel.hidden;
    button.setAttribute('aria-expanded', String(!panel.hidden));
    if (!panel.hidden) refresh();
  });
  document.addEventListener('pointerdown', function (event) {
    if (panel.hidden || panel.contains(event.target) || button.contains(event.target)) return;
    panel.hidden = true;
    button.setAttribute('aria-expanded', 'false');
  });
  action.addEventListener('click', function () { library.sync().catch(function () {}); });
  library.subscribe(refresh);
  window.addEventListener('online', refresh);
  window.addEventListener('offline', refresh);
  refresh();
})();
