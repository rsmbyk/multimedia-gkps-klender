/* One size label for every media surface: the largest unit that still reads a number, never a rounded zero. */
(function () {
  'use strict';
  var units = ['KB', 'MB', 'GB'];
  function label(number) {
    var rounded = Math.round(number * 10) / 10;
    return (rounded % 1 === 0 ? String(rounded) : rounded.toFixed(1));
  }
  function formatSize(bytes) {
    var size = Math.max(0, Number(bytes) || 0);
    if (size < 1000) return Math.round(size) + ' B';
    var unit = 0;
    var value = size / 1000;
    while (unit < units.length - 1 && Math.round(value * 10) / 10 >= 1000) {
      unit += 1;
      value = size / Math.pow(1000, unit + 1);
    }
    return label(value) + ' ' + units[unit];
  }
  window.gkpsFormatSize = formatSize;
})();
