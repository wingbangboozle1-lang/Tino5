/* Small, dependency-free enhancements for the static dashboard. */
(function () {
  'use strict';

  // Row numbering for every data table.
  document.querySelectorAll('table.data tbody').forEach(function (tbody) {
    Array.prototype.forEach.call(tbody.rows, function (tr, i) {
      var cell = tr.querySelector('td.rownum');
      if (cell) cell.textContent = String(i + 1);
    });
  });

  // Per-table row filter.
  document.querySelectorAll('.tablesearch').forEach(function (input) {
    var card = input.closest('.tablecard');
    if (!card) return;
    var tbody = card.querySelector('table.data tbody');
    var foot = card.querySelector('.rowcount');
    var total = tbody.rows.length;
    input.addEventListener('input', function () {
      var q = input.value.trim().toLowerCase();
      var shown = 0;
      Array.prototype.forEach.call(tbody.rows, function (tr) {
        var match = !q || tr.textContent.toLowerCase().indexOf(q) !== -1;
        tr.style.display = match ? '' : 'none';
        if (match) shown++;
      });
      if (foot) foot.textContent = shown + ' of ' + total + ' rows shown · ' + total + ' official source links';
    });
  });

  // Keyboard shortcut: "/" focuses the first visible filter box.
  document.addEventListener('keydown', function (e) {
    if (e.key === '/' && !/input|textarea/i.test(document.activeElement.tagName)) {
      var first = document.querySelector('.tablesearch');
      if (first) { e.preventDefault(); first.focus(); }
    }
  });
})();
