/* The local lists' age buckets — one rule, so the Media Library, the transfer history and the Tata Ibadah
   panel cannot name the same age differently (spec 146, reading/R20, reading/R21). Nothing here is stored:
   a bucket is derived from a row and the present instant every time a list draws. */
(function () {
  'use strict';
  var DAY = 86400000;
  var HOUR = 3600000;
  var RECENT_DAYS = 30;
  var ZONE = 'Asia/Jakarta';

  var FILE_BUCKETS = [
    { key: 'last-30-days', label: 'Last 30 days' },
    { key: 'earlier-this-year', label: 'Earlier this year' },
    { key: 'older', label: 'Older' }
  ];
  var TRANSFER_BUCKETS = [
    { key: 'last-24-hours', label: 'Last 24 hours' },
    { key: 'last-7-days', label: 'Last 7 days' },
    { key: 'last-30-days', label: 'Last 30 days' },
    { key: 'earlier-this-year', label: 'Earlier this year' },
    { key: 'older', label: 'Older' }
  ];

  function dayParts(value) {
    var date = value instanceof Date ? value : new Date(value);
    if (isNaN(date.getTime())) return null;
    return new Intl.DateTimeFormat('en-US', { timeZone: ZONE, year: 'numeric', month: '2-digit', day: '2-digit' })
      .formatToParts(date);
  }
  function pick(parts, name) {
    for (var i = 0; i < parts.length; i += 1) if (parts[i].type === name) return Number(parts[i].value);
    return NaN;
  }
  /* The congregation's calendar day: a midnight-at-UTC number carrying that day's year, month and date, so
     two days subtract cleanly and a year comparison is the Jakarta year, never the server's (reading/R9). */
  function presentDay(nowMs) {
    var parts = dayParts(typeof nowMs === 'number' ? nowMs : Date.now());
    if (!parts) return NaN;
    return Date.UTC(pick(parts, 'year'), pick(parts, 'month') - 1, pick(parts, 'day'));
  }
  function todayIso(nowMs) {
    var day = presentDay(nowMs);
    if (isNaN(day)) return '';
    return new Date(day).toISOString().slice(0, 10);
  }
  function sameYear(day, today) {
    return new Date(day).getUTCFullYear() === new Date(today).getUTCFullYear();
  }

  /* A file is dated by its upload day, in the Tata Ibadah list's own windows: thirty days, then the year. */
  function fileKey(file, nowMs) {
    var parts = file && file.uploaded_at ? dayParts(file.uploaded_at) : null;
    if (!parts) return 'older';  // a row that cannot be dated is still drawn, never dropped
    var day = Date.UTC(pick(parts, 'year'), pick(parts, 'month') - 1, pick(parts, 'day'));
    var today = presentDay(nowMs);
    if (isNaN(today)) return 'older';
    if (Math.round((today - day) / DAY) <= RECENT_DAYS) return 'last-30-days';
    return sameYear(day, today) ? 'earlier-this-year' : 'older';
  }

  /* A transfer is dated by the instant it started — the only instant an active one has (FR-010) — and the
     first two rungs are rolling windows measured from this draw. */
  function transferKey(transfer, nowMs) {
    var started = Date.parse(transfer && transfer.started_at);
    if (isNaN(started)) return 'older';
    var now = typeof nowMs === 'number' ? nowMs : Date.now();
    var age = now - started;
    if (age < 24 * HOUR) return 'last-24-hours';
    if (age < 7 * DAY) return 'last-7-days';
    if (age < 30 * DAY) return 'last-30-days';
    var parts = dayParts(started);
    if (!parts) return 'older';
    var day = Date.UTC(pick(parts, 'year'), pick(parts, 'month') - 1, pick(parts, 'day'));
    return sameYear(day, presentDay(now)) ? 'earlier-this-year' : 'older';
  }

  /* The buckets a list draws: the ladder's own order, only the ones holding rows (FR-005, FR-009). */
  function group(rows, keyOf, ladder) {
    var byKey = {};
    var buckets = (ladder || FILE_BUCKETS).map(function (bucket) {
      var made = { key: bucket.key, label: bucket.label, rows: [] };
      byKey[bucket.key] = made;
      return made;
    });
    (rows || []).forEach(function (row) {
      var key = keyOf(row);
      (byKey[key] || byKey.older).rows.push(row);
    });
    return buckets.filter(function (bucket) { return bucket.rows.length; });
  }

  window.gkpsAgeBuckets = {
    FILE_BUCKETS: FILE_BUCKETS,
    TRANSFER_BUCKETS: TRANSFER_BUCKETS,
    presentDay: presentDay,
    todayIso: todayIso,
    fileKey: fileKey,
    transferKey: transferKey,
    group: group
  };
})();
