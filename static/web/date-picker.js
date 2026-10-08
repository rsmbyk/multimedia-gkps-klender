/* Optional Tata Ibadah dates (spec 016).
 *
 * The form keeps Django's date field as a hidden ISO value. The visible calendar
 * is dependency-free and is initialized each time editors.js replaces a form
 * fragment, including a server-rendered validation response.
 */
(function () {
  'use strict';

  var MONTHS = new Intl.DateTimeFormat('id-ID', { month: 'long', year: 'numeric' });
  var LABEL = new Intl.DateTimeFormat('id-ID', {
    day: 'numeric', month: 'long', year: 'numeric'
  });
  var FULL_DATE = new Intl.DateTimeFormat('id-ID', {
    weekday: 'long', day: 'numeric', month: 'long', year: 'numeric'
  });
  var activePicker = null;

  function localDate(year, month, day) {
    return new Date(year, month, day);
  }

  function fromIso(value) {
    var match = /^(\d{4})-(\d{2})-(\d{2})$/.exec(value || '');
    if (!match) return null;
    var parsed = localDate(Number(match[1]), Number(match[2]) - 1, Number(match[3]));
    return parsed.getFullYear() === Number(match[1])
      && parsed.getMonth() === Number(match[2]) - 1
      && parsed.getDate() === Number(match[3]) ? parsed : null;
  }

  function iso(date) {
    return [date.getFullYear(), String(date.getMonth() + 1).padStart(2, '0'),
      String(date.getDate()).padStart(2, '0')].join('-');
  }

  function sameDay(left, right) {
    return !!left && !!right && left.getFullYear() === right.getFullYear()
      && left.getMonth() === right.getMonth() && left.getDate() === right.getDate();
  }

  function addDays(date, amount) {
    return localDate(date.getFullYear(), date.getMonth(), date.getDate() + amount);
  }

  function shiftMonth(date, amount) {
    var day = date.getDate();
    var target = localDate(date.getFullYear(), date.getMonth() + amount, 1);
    var lastDay = new Date(target.getFullYear(), target.getMonth() + 1, 0).getDate();
    target.setDate(Math.min(day, lastDay));
    return target;
  }

  function initialize(scope) {
    scope.querySelectorAll('[data-date-picker]').forEach(function (picker) {
      if (picker.dataset.datePickerReady === 'true') return;
      var field = picker.closest('.editor__field');
      var value = field && field.querySelector('[data-date-picker-value]');
      var trigger = picker.querySelector('[data-date-picker-trigger]');
      var label = picker.querySelector('[data-date-picker-label]');
      var clear = picker.querySelector('[data-date-picker-clear]');
      var calendar = picker.querySelector('[data-date-picker-calendar]');
      var monthLabel = picker.querySelector('[data-date-picker-month]');
      var grid = picker.querySelector('[data-date-picker-grid]');
      var previous = picker.querySelector('[data-date-picker-prev]');
      var next = picker.querySelector('[data-date-picker-next]');
      if (!value || !trigger || !label || !calendar || !monthLabel || !grid) return;

      picker.dataset.datePickerReady = 'true';
      var selected = fromIso(value.value);
      var today = localDate(new Date().getFullYear(), new Date().getMonth(), new Date().getDate());
      if (!selected && picker.dataset.datePickerDefaultSunday === 'true') {
        selected = addDays(today, (7 - today.getDay()) % 7);
      }
      var view = selected || today;
      var focusDate = selected || today;
      var calendarOpen = false;

      function positionCalendar() {
        if (!calendarOpen) return;
        calendar.style.maxHeight = 'calc(100vh - 16px)';
        var triggerBounds = trigger.getBoundingClientRect();
        var viewportWidth = document.documentElement.clientWidth;
        var viewportHeight = document.documentElement.clientHeight;
        var margin = 8;
        var gap = 8;
        var width = calendar.getBoundingClientRect().width;
        var height = calendar.getBoundingClientRect().height;
        var left = Math.max(margin, Math.min(triggerBounds.left,
          viewportWidth - width - margin));
        var belowTop = triggerBounds.bottom + gap;
        var spaceBelow = viewportHeight - margin - belowTop;
        var spaceAbove = triggerBounds.top - gap - margin;
        var top;

        if (height <= spaceBelow) {
          top = belowTop;
        } else if (height <= spaceAbove) {
          top = triggerBounds.top - gap - height;
        } else if (spaceBelow >= spaceAbove) {
          calendar.style.maxHeight = Math.max(0, spaceBelow) + 'px';
          top = belowTop;
        } else {
          calendar.style.maxHeight = Math.max(0, spaceAbove) + 'px';
          height = calendar.getBoundingClientRect().height;
          top = triggerBounds.top - gap - height;
        }
        calendar.style.left = left + 'px';
        calendar.style.top = Math.max(margin, top) + 'px';
      }

      function syncValue() {
        value.value = selected ? iso(selected) : '';
        label.textContent = selected ? LABEL.format(selected) : 'Choose a date';
        value.dispatchEvent(new Event('input', { bubbles: true }));
        value.dispatchEvent(new Event('change', { bubbles: true }));
      }

      function setOpen(open, restoreFocus) {
        if (open) {
          if (activePicker && activePicker.root !== picker) activePicker.close(false);
          calendar.removeAttribute('hidden');
          if (typeof calendar.showPopover === 'function') calendar.showPopover();
          calendarOpen = true;
          trigger.setAttribute('aria-expanded', 'true');
          activePicker = {root: picker, close: function (restore) {
            setOpen(false, restore);
          }, position: positionCalendar};
          focusDate = selected || today;
          view = focusDate;
          render(true);
          positionCalendar();
        } else {
          calendarOpen = false;
          if (typeof calendar.hidePopover === 'function' && calendar.matches(':popover-open')) {
            calendar.hidePopover();
          }
          calendar.hidden = true;
          trigger.setAttribute('aria-expanded', 'false');
          if (activePicker && activePicker.root === picker) activePicker = null;
          if (restoreFocus) trigger.focus();
        }
      }

      function focusVisibleDate() {
        var button = grid.querySelector('[data-date="' + iso(focusDate) + '"]');
        if (button) button.focus();
      }

      function render(shouldFocus) {
        monthLabel.textContent = MONTHS.format(view);
        grid.replaceChildren();
        grid.setAttribute('aria-label', 'Choose a date in ' + MONTHS.format(view));
        var first = localDate(view.getFullYear(), view.getMonth(), 1);
        var mondayOffset = (first.getDay() + 6) % 7;
        var daysInMonth = new Date(view.getFullYear(), view.getMonth() + 1, 0).getDate();
        var row = createWeekRow();
        for (var blank = 0; blank < mondayOffset; blank += 1) appendEmptyCell(row);
        for (var day = 1; day <= daysInMonth; day += 1) {
          if (row.children.length === 7) row = createWeekRow();
          var date = localDate(view.getFullYear(), view.getMonth(), day);
          var button = document.createElement('button');
          button.type = 'button';
          button.className = 'editor__date-day';
          button.setAttribute('role', 'gridcell');
          button.setAttribute('aria-label', FULL_DATE.format(date));
          button.setAttribute('aria-selected', String(sameDay(selected, date)));
          button.setAttribute('data-date', iso(date));
          if (date.getDay() === 0) button.setAttribute('data-date-sunday', '');
          button.tabIndex = sameDay(focusDate, date) ? 0 : -1;
          if (sameDay(today, date)) {
            button.setAttribute('aria-current', 'date');
            button.setAttribute('data-date-today', '');
          }
          button.textContent = String(day);
          button.addEventListener('click', function (event) {
            var chosen = fromIso(event.currentTarget.dataset.date);
            selected = chosen;
            focusDate = chosen;
            view = chosen;
            syncValue();
            setOpen(false, true);
          });
          button.addEventListener('keydown', onDayKeydown);
          row.appendChild(button);
        }
        while (row.children.length > 0 && row.children.length < 7) appendEmptyCell(row);
        if (shouldFocus) focusVisibleDate();
        positionCalendar();
      }

      function createWeekRow() {
        var row = document.createElement('div');
        row.className = 'editor__date-row';
        row.setAttribute('role', 'row');
        grid.appendChild(row);
        return row;
      }

      function appendEmptyCell(row) {
        var empty = document.createElement('span');
        empty.className = 'editor__date-empty';
        empty.setAttribute('role', 'presentation');
        empty.setAttribute('aria-hidden', 'true');
        row.appendChild(empty);
      }

      function moveFocus(nextDate) {
        focusDate = nextDate;
        view = nextDate;
        render(true);
      }

      function onDayKeydown(event) {
        var day = fromIso(event.currentTarget.dataset.date);
        var destination = null;
        if (event.key === 'ArrowLeft') destination = addDays(day, -1);
        else if (event.key === 'ArrowRight') destination = addDays(day, 1);
        else if (event.key === 'ArrowUp') destination = addDays(day, -7);
        else if (event.key === 'ArrowDown') destination = addDays(day, 7);
        else if (event.key === 'Home') destination = addDays(day, -((day.getDay() + 6) % 7));
        else if (event.key === 'End') destination = addDays(day, 6 - ((day.getDay() + 6) % 7));
        else if (event.key === 'PageUp') destination = shiftMonth(day, event.shiftKey ? -12 : -1);
        else if (event.key === 'PageDown') destination = shiftMonth(day, event.shiftKey ? 12 : 1);
        else if (event.key === 'Escape') {
          event.preventDefault();
          event.stopPropagation();
          setOpen(false, true);
          return;
        }
        if (!destination) return;
        event.preventDefault();
        moveFocus(destination);
      }

      trigger.setAttribute('aria-controls', calendar.id || 'id_date_calendar');
      calendar.id = calendar.id || 'id_date_calendar';
      trigger.addEventListener('click', function () {
        setOpen(!calendarOpen, false);
      });
      if (previous) previous.addEventListener('click', function () {
        view = shiftMonth(view, -1);
        focusDate = localDate(view.getFullYear(), view.getMonth(),
          Math.min(focusDate.getDate(), new Date(view.getFullYear(), view.getMonth() + 1, 0).getDate()));
        render(true);
      });
      if (next) next.addEventListener('click', function () {
        view = shiftMonth(view, 1);
        focusDate = localDate(view.getFullYear(), view.getMonth(),
          Math.min(focusDate.getDate(), new Date(view.getFullYear(), view.getMonth() + 1, 0).getDate()));
        render(true);
      });
      if (clear) clear.addEventListener('click', function () {
        selected = null;
        syncValue();
        setOpen(false, true);
        render(false);
      });
      syncValue();
      render(false);
    });
  }

  function repositionActivePicker() {
    if (activePicker) activePicker.position();
  }

  document.addEventListener('scroll', repositionActivePicker, true);
  window.addEventListener('resize', repositionActivePicker);
  document.addEventListener('click', function (event) {
    if (activePicker && !activePicker.root.contains(event.target)) activePicker.close(false);
  });
  document.addEventListener('keydown', function (event) {
    if (event.key !== 'Escape' || !activePicker) return;
    event.preventDefault();
    event.stopPropagation();
    activePicker.close(true);
  }, true);
  document.addEventListener('date-picker:cleanup', function () {
    if (activePicker) activePicker.close(false);
  });
  document.addEventListener('date-picker:initialize', function () {
    initialize(document.getElementById('editorContent') || document);
  });
  initialize(document);
})();
