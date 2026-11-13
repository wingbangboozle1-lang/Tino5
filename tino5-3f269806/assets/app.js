// Minimal, dependency-free helpers: filter tables and sort by clicking a header.
(function () {
  document.querySelectorAll('input.filter').forEach(function (box) {
    var table = document.getElementById(box.getAttribute('data-target'));
    if (!table) return;
    box.addEventListener('input', function () {
      var q = box.value.toLowerCase();
      table.querySelectorAll('tbody tr').forEach(function (tr) {
        tr.style.display = tr.textContent.toLowerCase().indexOf(q) > -1 ? '' : 'none';
      });
    });
  });
  document.querySelectorAll('table.data thead th').forEach(function (th, idx) {
    th.style.cursor = 'pointer';
    th.title = 'Click to sort';
    th.addEventListener('click', function () {
      var table = th.closest('table');
      var tbody = table.querySelector('tbody');
      var rows = Array.prototype.slice.call(tbody.querySelectorAll('tr'));
      var asc = th.getAttribute('data-asc') !== '1';
      th.setAttribute('data-asc', asc ? '1' : '0');
      rows.sort(function (a, b) {
        var x = a.children[idx] ? a.children[idx].textContent.trim() : '';
        var y = b.children[idx] ? b.children[idx].textContent.trim() : '';
        var nx = parseFloat(x.replace(/[^0-9.\-]/g, '')), ny = parseFloat(y.replace(/[^0-9.\-]/g, ''));
        var cmp = (!isNaN(nx) && !isNaN(ny)) ? nx - ny : x.localeCompare(y);
        return asc ? cmp : -cmp;
      });
      rows.forEach(function (r) { tbody.appendChild(r); });
    });
  });
})();
