/* Tino5 — data-driven renderer. No build step, no external dependencies. */
(function () {
  "use strict";

  var SOURCES = null;
  var MODEL = null;

  function root() {
    // pages live in /pages/, index at /
    return document.body.dataset.root || "";
  }

  function money(n, opts) {
    if (n === null || n === undefined || n === "") return "";
    var v = Number(n);
    if (!isFinite(v)) return "";
    var s = Math.round(v).toLocaleString("en-US");
    return (v < 0 ? "-$" + Math.abs(Math.round(v)).toLocaleString("en-US") : "$" + s);
  }

  function pct(n, d) {
    if (n === null || n === undefined) return "";
    return (Number(n) * 100).toFixed(d === undefined ? 1 : d) + "%";
  }

  var STATUS_LABEL = {
    verified: "verified",
    secondary: "secondary",
    owner: "owner-provided",
    derived: "derived",
    assumption: "assumption",
    unverified: "unverified"
  };

  function badge(status) {
    var s = status || "unverified";
    return '<span class="badge b-' + s + '">' + (STATUS_LABEL[s] || s) + "</span>";
  }

  function sourceLinks(ids) {
    if (!ids || !ids.length) return '<span class="none">—</span>';
    return ids
      .map(function (id) {
        var s = (SOURCES.sources || []).filter(function (x) { return x.id === id; })[0];
        if (!s) return '<span class="none">' + id + " (missing)</span>";
        if (!s.url || s.url === "#")
          return '<span class="none" title="internal working note">owner data</span>';
        return '<a href="' + s.url + '" target="_blank" rel="noopener" title="' +
          escapeAttr(s.org + " — " + s.title) + '">' + escapeHtml(shortOrg(s.org)) + " ↗</a>";
      })
      .join(" ");
  }

  function shortOrg(org) {
    var map = {
      "California State Board of Equalization (BOE)": "BOE",
      "California Legislative Information (leginfo)": "leginfo",
      "Internal Revenue Service": "IRS",
      "California Courts (Judicial Branch)": "CA Courts",
      "SF Office of the Treasurer & Tax Collector": "SF Treasurer",
      "Santa Clara County Assessor": "SCC Assessor",
      "San Jose Water Company / CPUC": "SJWC tariff",
      "Pacific Gas and Electric Company": "PG&E",
      "California Public Utilities Commission": "CPUC",
      "San Francisco Public Utilities Commission": "SFPUC",
      "Congressional Budget Office": "CBO",
      "Federal Housing Finance Agency": "FHFA",
      "U.S. Department of Housing and Urban Development": "HUD",
      "California Secretary of State": "CA SOS",
      "California Department of Insurance": "CDI",
      "California Earthquake Authority": "CEA",
      "City of Cupertino (Municipal Code)": "Cupertino code",
      "California Franchise Tax Board": "FTB",
      "Internal working note (this project)": "owner"
    };
    return map[org] || org;
  }

  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }
  function escapeAttr(s) { return escapeHtml(s); }

  function cell(row, key, colLabel) {
    var v = row[key];
    if (key === "status") return badge(row.status);
    if (key === "sources") return '<span class="src">' + sourceLinks(row.sources) + "</span>";
    if (key === "note") return '<span class="' + (row[key] ? "" : "") + '">' + escapeHtml(v || "") + "</span>";
    if (v === undefined || v === null || v === "") {
      if (row.value_display && key === "value")
        return '<span class="small">' + escapeHtml(row.value_display) + "</span>";
      if (row.status === "unverified" && (key === "value" || key === "value2" || key === "value3"))
        return '<span class="small" style="color:#a02222">— blank (unverified)</span>';
      return "";
    }
    if (key === "value" && row.value_display) return escapeHtml(row.value_display);
    return escapeHtml(v);
  }

  function renderTable(section, rows) {
    var cols = section.columns || ["item", "value", "status", "sources", "note"];
    var labels = section.column_labels || cols.map(function (c) {
      return {
        item: "Item", value: "Value", value2: "Value", value3: "Value",
        status: "Status", sources: "Source", note: "Note"
      }[c] || c;
    });
    var html = ['<div class="tbl-wrap"><table><thead><tr>'];
    cols.forEach(function (c, i) {
      var align = c === "value2" || c === "value3" ? ' style="text-align:right"' : "";
      html.push("<th" + align + ">" + escapeHtml(labels[i]) + "</th>");
    });
    html.push("</tr></thead><tbody>");
    rows.forEach(function (row) {
      html.push('<tr data-status="' + (row.status || "") + '">');
      cols.forEach(function (c) {
        var cls = c === "item" ? "item" : c === "note" ? "note" :
          (c === "value2" || c === "value3") ? "numv" : "";
        html.push('<td class="' + cls + '">' + cell(row, c) + "</td>");
      });
      html.push("</tr>");
    });
    html.push("</tbody></table></div>");
    return html.join("");
  }

  function sectionBlock(section) {
    var out = ['<section id="' + (section.id || "") + '" class="section-head">'];
    out.push("<h2>" + escapeHtml(section.title) + "</h2>");
    if (section.intro) out.push("<p>" + escapeHtml(section.intro) + "</p>");
    out.push("</section>");
    if (section.table_html) out.push(section.table_html);
    else out.push(renderTable(section, section.rows || []));
    return out.join("");
  }

  /* ---------------- data page ---------------- */
  function renderDataPage(data, mount) {
    var html = "";
    if (data.title) document.title = data.title + " · Inheritance decision dashboard";
    if (data.intro) html += '<p class="lead">' + escapeHtml(data.intro) + "</p>";
    (data.sections || []).forEach(function (s) {
      if (s.source === "model" && s.id === "exposure") {
        s.table_html = estateTableHtml();
      }
      if (s.source === "model" && s.id === "sensitivity") {
        s.table_html = sensitivityTableHtml();
      }
      html += sectionBlock(s);
    });
    mount.innerHTML = html;
  }

  /* ---------------- model-driven tables ---------------- */
  function estateTableHtml() {
    var rows = MODEL.estate.examples.map(function (e) {
      return "<tr><td class=\"numv\">" + money(e.estate) + '</td><td class="numv">' +
        (e.tax_2026 ? money(e.tax_2026) : "$0") + '</td><td class="numv">' +
        (e.tax_at_death ? money(e.tax_at_death) : "$0") + "</td></tr>";
    });
    return '<div class="tbl-wrap"><table><thead><tr><th style="text-align:right">Gross estate at death</th>' +
      '<th style="text-align:right">Federal estate tax, death in 2026</th>' +
      '<th style="text-align:right">Federal estate tax, death in 2045</th></tr></thead><tbody>' +
      rows.join("") + "</tbody></table></div>" +
      '<p class="small">Model output, rounded to the nearest $10. Exemption for a 2045 death = $15,000,000 indexed at 2.3%/yr ≈ ' +
      money(MODEL.estate.exemption_path.filter(function (x) { return x.year === 2045; })[0].exemption) +
      ". California adds nothing. A married couple with portability doubles every figure. Source: IRS basic exclusion amounts; indexation is assumption A2.</p>";
  }

  function qualityLabel(q) { return { low: "Low case", mid: "Base case", high: "High case" }[q] || q; }

  function sensitivityTableHtml() {
    var rows = MODEL.sensitivity.map(function (g) {
      return "<tr><td>" + qualityLabel(g.case) + "</td><td class=\"numv\">" + g.inherit_year +
        '</td><td>' + g.scenario + '</td><td class="numv">' + money(g.terminal) +
        '</td><td class="numv">' + money(g.economic_value) + '</td><td class="numv">' +
        money(g.npv) + "</td></tr>";
    });
    return '<div class="tbl-wrap"><table><thead><tr><th>Assumption case</th><th style="text-align:right">Transfer year</th>' +
      "<th>Option</th><th style=\"text-align:right\">Wealth in year+20</th>" +
      "<th style=\"text-align:right\">Incl. housing consumed</th><th style=\"text-align:right\">Present value</th>" +
      "</tr></thead><tbody>" + rows.join("") + "</tbody></table></div>" +
      '<p class="small">Low = 3% appreciation + 5% investment return. Base = 4% + 6%. High = 5% + 7%. ' +
      "Present value discounts all after-tax cash flows, sale proceeds and net liquidation value at 5%.</p>";
  }

  function scenarioCards() {
    var order = [
      { k: "sell", t: "Sell at inheritance", d: "Take the stepped-up basis, pay ≈6.1% of value in selling costs, invest the rest." },
      { k: "rent", t: "Keep and rent it out", d: "Full reassessment to market value; rent covers the tax but not the risk." },
      { k: "live", t: "Live in it", d: "The only route that keeps the Prop 19 exclusion — and the only route that consumes the house." }
    ];
    return order.map(function (o) {
      var s = MODEL.scenarios[o.k];
      return '<div class="card kpi"><div class="lab">' + o.t + "</div><div class=\"val\">" +
        money(s.terminal) + '</div><div class="sub">wealth in 2065 after all taxes · ' +
        money(s.economic_value) + " including housing consumed</div><p class=\"small\" style=\"margin:8px 0 0\">" +
        o.d + "</p></div>";
    }).join("");
  }

  function projectionTableHtml() {
    var rows = MODEL.projection.map(function (p) {
      return "<tr><td class=\"numv\">" + p.year + '</td><td class="numv">' + money(p.cu_market_value) +
        '</td><td class="numv">' + money(p.cu_assessed_no_transfer) + '</td><td class="numv">' + money(p.cu_tax_no_transfer) +
        '</td><td class="numv">' + money(p.cu_assessed_live) + '</td><td class="numv">' + money(p.cu_tax_live) +
        '</td><td class="numv">' + money(p.cu_assessed_rent) + '</td><td class="numv">' + money(p.cu_tax_rent) +
        '</td><td class="numv">' + money(p.sf_market_value) + '</td><td class="numv">' + money(p.sf_tax) + "</td></tr>";
    });
    return '<div class="tbl-wrap"><table><thead><tr>' +
      '<th style="text-align:right">Year</th>' +
      '<th style="text-align:right">A market value</th><th style="text-align:right">A assessed (no transfer)</th>' +
      '<th style="text-align:right">A tax (no transfer)</th><th style="text-align:right">A assessed (live in)</th>' +
      '<th style="text-align:right">A tax (live in)</th><th style="text-align:right">A assessed (rent out)</th>' +
      '<th style="text-align:right">A tax (rent out)</th><th style="text-align:right">B market value</th>' +
      '<th style="text-align:right">B tax</th></tr></thead><tbody>' + rows.join("") + "</tbody></table></div>" +
      '<p class="small">Model output, nearest $10. Transfer assumed in 2045 — the "no transfer" columns show what the current assessment would have grown to if nothing happened. ' +
      "B assessed value and tax are unaffected by the Property A decision.</p>";
  }

  function cashflowTableHtml() {
    var rows = MODEL.timeline.sell.concat([]).filter(function (r) {
      return r.year % 5 === 0 || r.year === MODEL.meta.inherit_year;
    });
    var out = ['<div class="tbl-wrap"><table><thead><tr><th style="text-align:right">Year</th>' +
      '<th style="text-align:right">A value</th><th style="text-align:right">A property tax</th>' +
      '<th style="text-align:right">Rent received</th><th style="text-align:right">Insurance</th>' +
      '<th style="text-align:right">Other running costs</th><th style="text-align:right">Income tax</th>' +
      '<th style="text-align:right">Net cash</th><th style="text-align:right">Sale proceeds</th></tr></thead><tbody>'];
    rows.forEach(function (r) {
      out.push("<tr><td class=\"numv\">" + r.year + "</td><td class=\"numv\">" + money(r.cu_value) +
        '</td><td class="numv">' + money(r.cu_property_tax) + '</td><td class="numv">' + money(r.rent) +
        '</td><td class="numv">' + money(r.insurance) + '</td><td class="numv">' + money(r.other_costs) +
        '</td><td class="numv">' + money(r.income_tax) + '</td><td class="numv">' + money(r.net_cash) +
        '</td><td class="numv">' + (r.sale_proceeds ? money(r.sale_proceeds) : "—") + "</td></tr>");
    });
    out.push("</tbody></table></div>");
    out.push('<p class="small">Sell-at-inheritance case, every fifth year plus the transfer year. Negative net cash in the ' +
      "transfer year reflects the one-off costs of the sale.</p>");
    return out.join("");
  }

  function snapshotTableHtml() {
    var labels = { live: "Live in it", rent: "Rent it out", sell: "Sell at inheritance" };
    var keys = [
      ["cu_property_tax", "Property A property tax"],
      ["sf_property_tax", "Property B property tax"],
      ["insurance", "Insurance, both properties"],
      ["other_costs", "Water, electricity, maintenance, management"],
      ["rent", "Rent received"],
      ["income_tax", "Income tax on rent"],
      ["net_cash", "Net cash"],
      ["sale_proceeds", "Sale proceeds"]
    ];
    var head = '<tr><th>Annual line, transfer year 2045</th>' +
      ["live", "rent", "sell"].map(function (k) { return '<th style="text-align:right">' + labels[k] + "</th>"; }).join("") +
      "</tr>";
    var rows = keys.map(function (p) {
      return "<tr><td class=\"item\">" + p[1] + "</td>" +
        ["live", "rent", "sell"].map(function (k) {
          return '<td class="numv">' + money(MODEL.derived.snapshot_at_inheritance[k][p[0]]) + "</td>";
        }).join("") + "</tr>";
    });
    return '<div class="tbl-wrap"><table><thead>' + head + "</thead><tbody>" + rows.join("") + "</tbody></table></div>" +
      '<p class="small">First year after the transfer, nominal dollars, nearest $10. These are the operating lines; the ' +
      "capital decision is in the comparison table above.</p>";
  }

  function prop19RowsHtml() {
    var rows = MODEL.derived.prop19_rows.filter(function (r) { return r.year % 5 === 0 || r.year === 2045; });
    return rows.map(function (r) {
      return "<tr><td class=\"numv\">" + r.year + '</td><td class="numv">' + money(r.tax_live) +
        '</td><td class="numv">' + money(r.tax_rent) + '</td><td class="numv">' + money(r.saving) + "</td></tr>";
    }).join("");
  }

  function hydrateKpis() {
    var el;
    function set(sel, val) { el = document.querySelectorAll(sel); for (var i = 0; i < el.length; i++) el[i].textContent = val; }
    set("[data-bind=sell]", money(MODEL.scenarios.sell.terminal));
    set("[data-bind=rent]", money(MODEL.scenarios.rent.terminal));
    set("[data-bind=live]", money(MODEL.scenarios.live.terminal));
    set("[data-bind=prop19pv]", money(MODEL.derived.prop19_pv_2045_2065));
    set("[data-bind=breakeven]", pct(MODEL.derived.breakeven_appreciation_vs_sell.rent, 1));
    set("[data-bind=breakeven-live]", pct(MODEL.derived.breakeven_appreciation_vs_sell.live, 1));
    set("[data-bind=tax-live]", money(MODEL.derived.snapshot_at_inheritance.live.cu_property_tax));
    set("[data-bind=tax-rent]", money(MODEL.derived.snapshot_at_inheritance.rent.cu_property_tax));
    set("[data-bind=tax-taxdiff]", money(
      MODEL.derived.snapshot_at_inheritance.rent.cu_property_tax -
      MODEL.derived.snapshot_at_inheritance.live.cu_property_tax));
    set("[data-bind=sell-net]", money(MODEL.derived.snapshot_at_inheritance.sell.sale_proceeds));
  }

  /* ---------------- boot ---------------- */
  function loadJSON(path) {
    return fetch(path, { cache: "no-cache" }).then(function (r) {
      if (!r.ok) throw new Error(path + ": " + r.status);
      return r.json();
    });
  }

  function init() {
    var r = root();
    var mount = document.getElementById("content");
    var page = document.body.dataset.page;

    loadJSON(r + "data/sources.json")
      .then(function (s) {
        SOURCES = s;
        return loadJSON(r + "data/model.json");
      })
      .then(function (m) {
        MODEL = m;
        hydrateKpis();
        if (document.getElementById("scenario-cards")) document.getElementById("scenario-cards").innerHTML = scenarioCards();
        if (document.getElementById("scenario-table")) document.getElementById("scenario-table").innerHTML = scenarioTableHtml();
        if (document.getElementById("snapshot")) document.getElementById("snapshot").innerHTML = snapshotTableHtml();
        if (document.getElementById("projection")) document.getElementById("projection").innerHTML = projectionTableHtml();
        if (document.getElementById("cashflow")) document.getElementById("cashflow").innerHTML = cashflowTableHtml();
        if (document.getElementById("sensitivity")) document.getElementById("sensitivity").innerHTML = sensitivityTableHtml();
        if (document.getElementById("prop19rows")) document.getElementById("prop19rows").innerHTML = prop19RowsHtml();
        if (document.getElementById("estate-table")) document.getElementById("estate-table").innerHTML = estateTableHtml();
        if (page === "sources" && mount) { renderSources(mount); try { wireFilters(); } catch (e) {} }
        else if (mount && document.body.dataset.json) {
          loadJSON(r + document.body.dataset.json).then(function (data) {
            renderDataPage(data, mount);
            try { wireFilters(); } catch (e) { /* filters are non-essential */ }
          }).catch(function (e) {
            mount.innerHTML = '<div class="callout bad"><h4>Data unavailable</h4><p>' + e.message + "</p></div>";
          });
        } else {
          wireFilters();
        }
      })
      .catch(function (e) {
        if (mount) mount.innerHTML = '<div class="callout bad"><h4>Data unavailable</h4><p>' + e.message + "</p></div>";
      });
  }

  function scenarioTableHtml() {
    var rows = [
      ["Property A property tax in 2045", "live", "rent", "sell", "cu_property_tax"],
      ["Property B property tax in 2045", "live", "rent", "sell", "sf_property_tax"],
      ["Insurance (both), 2045", null, null, null, "insurance"],
      ["Water / electricity / maintenance / management, 2045", null, null, null, "other_costs"],
      ["Rent received in 2045", null, null, null, "rent"],
      ["Income tax on rent, 2045", null, null, null, "income_tax"],
      ["Net operating cash, 2045", null, null, null, "net_cash"],
      ["Sale proceeds at transfer", null, null, null, "sale_proceeds"]
    ];
    var out = ['<div class="tbl-wrap"><table><thead><tr><th>Line</th>' +
      '<th style="text-align:right">Live in it</th><th style="text-align:right">Rent it out</th>' +
      '<th style="text-align:right">Sell at inheritance</th></tr></thead><tbody>'];
    rows.forEach(function (row) {
      out.push('<tr><td class="item">' + row[0] + "</td>");
      ["live", "rent", "sell"].forEach(function (k) {
        out.push('<td class="numv">' + money(MODEL.derived.snapshot_at_inheritance[k][row[4]]) + "</td>");
      });
      out.push("</tr>");
    });
    ["portfolio", "housing_asset", "cap_gains_tax", "terminal", "economic_value"].forEach(function (key) {
      var label = {
        portfolio: "Invested portfolio in 2065",
        housing_asset: "Property A value in 2065 (after selling costs)",
        cap_gains_tax: "Capital gains + recapture tax on a 2065 sale",
        terminal: "Net wealth in 2065",
        economic_value: "Plus housing consumed (imputed rent)"
      }[key];
      out.push('<tr><td class="item">' + label + "</td>");
      ["live", "rent", "sell"].forEach(function (k) {
        out.push('<td class="numv">' + money(MODEL.scenarios[k][key]) + "</td>");
      });
      out.push("</tr>");
    });
    out.push("</tbody></table></div>");
    return out.join("");
  }

  function renderSources(mount) {
    var rows = (SOURCES.sources || []).map(function (s) {
      var link = (s.url && s.url !== "#")
        ? '<a href="' + s.url + '" target="_blank" rel="noopener">' + escapeHtml(s.url) + "</a>"
        : '<span class="small">internal owner-supplied data</span>';
      return '<tr data-status="' + s.type + '"><td class="item">' + escapeHtml(s.org) + "</td><td>" +
        escapeHtml(s.title) + '</td><td style="max-width:38ch;word-break:break-all">' + link +
        '</td><td>' + escapeHtml(s.type) + '</td><td>' + escapeHtml(s.checked) + "</td></tr>";
    });
    mount.innerHTML = '<div class="tbl-wrap"><table><thead><tr><th>Publisher</th><th>Document</th>' +
      "<th>Link</th><th>Type</th><th>How verified here</th></tr></thead><tbody>" + rows.join("") + "</tbody></table></div>" +
      '<p class="small">Registry dated ' + escapeHtml(SOURCES.generated || "") + ". Links open in a new tab; official pages " +
      "are maintained by the publishing agency and may change without notice, which is why the access date is recorded on every page.</p>";
  }

  /* ---------------- search / filter ---------------- */
  function wireFilters() {
    var input = document.getElementById("q");
    var btns = document.querySelectorAll("[data-filter]");
    function apply() {
      var q = (input && input.value || "").toLowerCase();
      var active = document.querySelector("[data-filter].on");
      var st = active ? active.dataset.filter : "all";
      var rows = document.querySelectorAll("#content tbody tr");
      for (var i = 0; i < rows.length; i++) {
        var t = rows[i].textContent.toLowerCase();
        var ok = (!q || t.indexOf(q) > -1) && (st === "all" || rows[i].dataset.status === st);
        rows[i].style.display = ok ? "" : "none";
      }
    }
    if (input && typeof input.addEventListener === "function") input.addEventListener("input", apply);
    for (var i = 0; i < btns.length; i++) {
      if (typeof btns[i].addEventListener !== "function") continue;
      btns[i].addEventListener("click", function () {
        for (var j = 0; j < btns.length; j++) btns[j].classList.remove("on");
        this.classList.add("on");
        apply();
      });
    }
  }

  document.addEventListener("DOMContentLoaded", init);
})();
