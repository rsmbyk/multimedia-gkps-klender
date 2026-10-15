/* Spec 092: public rail status, separate from the shared library store. */
(function () {
  'use strict';
  var library = window.GKPSOffline;
  var button = document.getElementById('offlineSyncButton');
  var panel = document.getElementById('offlineSyncPanel');
  if (!library || !button || !panel) return;
  var dot = document.getElementById('offlineSyncDot');
  var mark = document.getElementById('offlineSyncMark');
  var title = document.getElementById('offlineSyncTitle');
  var detail = document.getElementById('offlineSyncDetail');
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
      synced.textContent = date(status.generation && status.generation.syncedAt, 'Never');
      checked.textContent = date(status.lastCheckedAt, 'Not checked');
      if (status.syncing) {
        title.textContent = 'Syncing library';
        detail.textContent = 'Checking for changes and saving updated content…';
      } else if (status.ready && status.offline) {
        title.textContent = 'Ready · offline';
        detail.textContent = 'Public reading and the service projector can use saved data. Editing needs a connection.';
      } else if (status.ready && status.error) {
        title.textContent = 'Update failed · saved copy ready';
        detail.textContent = 'The previous complete library is still available.';
      } else if (status.ready) {
        title.textContent = 'Ready for offline use';
        detail.textContent = 'Public reading and the service projector are ready offline. Bible, songs, and Tata Ibadah are saved.';
      } else {
        title.textContent = 'Not ready offline';
        detail.textContent = 'The two page shells and complete Bible, song, and Tata Ibadah data have not finished saving.';
      }
      action.textContent = status.syncing ? 'Syncing…' : status.offline ? 'Sync when online'
        : status.error ? 'Retry sync' : status.ready ? 'Sync now' : 'Start sync';
      action.disabled = status.syncing || status.offline;
      progress.hidden = !status.syncing;
    }).catch(function () {
      title.textContent = 'Not ready offline';
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
  refresh();
})();
