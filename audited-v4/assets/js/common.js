/* Shared utilities, data loader, and formatting (nearest $10 for model values) */

window.AppUtils = (function () {
  function fmtUSD(val, round10 = false) {
    if (val === null || val === undefined || Number.isNaN(val)) return "—";
    const num = round10 ? Math.round(val / 10) * 10 : Math.round(val);
    const sign = num < 0 ? "-" : "";
    return sign + "$" + Math.abs(num).toLocaleString("en-US");
  }

  function fmtSignedUSD(val) {
    if (val === null || val === undefined || Number.isNaN(val)) return "—";
    const num = Math.round(val / 10) * 10;
    const sign = num > 0 ? "+" : num < 0 ? "-" : "";
    return sign + "$" + Math.abs(num).toLocaleString("en-US");
  }

  function fmtCompactUSD(val) {
    if (val === null || val === undefined || Number.isNaN(val)) return "—";
    const abs = Math.abs(val);
    const sign = val < 0 ? "-" : "";
    if (abs >= 1e6) return sign + "$" + (abs / 1e6).toFixed(2) + "M";
    if (abs >= 1e3) return sign + "$" + Math.round(abs / 1e3) + "k";
    return sign + "$" + Math.round(abs);
  }

  async function loadProjections(prefix = "") {
    const res = await fetch(prefix + "data/projections.json");
    if (!res.ok) throw new Error("Failed to load projections.json");
    return res.json();
  }

  function sourceAnchor(url, label) {
    return `<a class="source-link" href="${url}" target="_blank" rel="noopener noreferrer">${label} &#8599;</a>`;
  }

  return {
    fmtUSD,
    fmtSignedUSD,
    fmtCompactUSD,
    loadProjections,
    sourceAnchor,
  };
})();
