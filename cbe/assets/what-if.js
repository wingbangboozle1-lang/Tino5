/* Local-only what-if calculators. No network, browser storage, cookies, or analytics. */
(function () {
  "use strict";

  var ids = [
    "phase-principal", "phase-treasury", "phase-treasury-roll", "phase-equity", "phase-wait",
    "phase-length", "phase-horizon", "phase-s1-drop", "phase-s1-month",
    "phase-s2-drop", "phase-s2-month"
  ];

  function value(id) {
    var el = document.getElementById(id);
    if (!el || el.value.trim() === "") return null;
    var n = Number(el.value);
    return Number.isFinite(n) ? n : null;
  }

  function dollars(n) {
    var rounded = Math.round(n / 10) * 10;
    return "$" + rounded.toLocaleString("en-US", { maximumFractionDigits: 0 });
  }

  function run(principal, treasuryRate, reinvestmentRate, equityRate, waitMonths, phaseMonths, horizonYears, dropPct, shockMonth) {
    var months = Math.round(horizonYears * 12);
    if (months < 1 || months > 1200 || waitMonths < 0 || phaseMonths < 1 || dropPct < 0 || dropPct > 100 || (shockMonth !== null && shockMonth > months)) return null;
    var tFactor = Math.pow(1 + treasuryRate, 1 / 12);
    var rollFactor = Math.pow(1 + reinvestmentRate, 1 / 12);
    var eFactor = Math.pow(1 + equityRate, 1 / 12);
    if (!Number.isFinite(tFactor) || !Number.isFinite(rollFactor) || !Number.isFinite(eFactor)) return null;

    var lump = { cash: 0, stock: principal, peak: principal, maxDraw: 0 };
    var phased = { cash: principal, stock: 0, peak: principal, maxDraw: 0 };
    var phasedAtStart = null;
    var crashApplied = false;
    var crashAt = shockMonth === null ? -1 : Math.round(shockMonth);

    for (var month = 1; month <= months; month += 1) {
      lump.stock *= eFactor;
      phased.cash *= month <= 12 ? tFactor : rollFactor;
      phased.stock *= eFactor;

      if (!crashApplied && crashAt === month) {
        lump.stock *= 1 - dropPct / 100;
        phased.stock *= 1 - dropPct / 100;
        crashApplied = true;
      }

      if (month === waitMonths) phasedAtStart = phased.cash;
      if (month > waitMonths && month <= waitMonths + phaseMonths) {
        var monthsLeft = waitMonths + phaseMonths - month + 1;
        var buy = monthsLeft === 1 ? phased.cash : phased.cash / monthsLeft;
        phased.cash -= buy;
        phased.stock += buy;
      }

      [lump, phased].forEach(function (portfolio) {
        var total = portfolio.cash + portfolio.stock;
        if (total > portfolio.peak) portfolio.peak = total;
        if (portfolio.peak > 0) portfolio.maxDraw = Math.max(portfolio.maxDraw, (portfolio.peak - total) / portfolio.peak);
      });
    }

    return {
      lumpEnd: lump.cash + lump.stock,
      phasedEnd: phased.cash + phased.stock,
      lumpDraw: lump.maxDraw,
      phasedDraw: phased.maxDraw,
      phaseStart: phasedAtStart
    };
  }

  function render() {
    var output = document.getElementById("phase-result");
    if (!output) return;
    var p = value("phase-principal");
    var t = value("phase-treasury");
    var roll = value("phase-treasury-roll");
    var e = value("phase-equity");
    var wait = value("phase-wait");
    var phase = value("phase-length");
    var horizon = value("phase-horizon");
    var s1Drop = value("phase-s1-drop");
    var s1Month = value("phase-s1-month");
    var s2Drop = value("phase-s2-drop");
    var s2Month = value("phase-s2-month");
    var required = [p, t, e, wait, phase, horizon];
    if (required.some(function (x) { return x === null; })) {
      output.textContent = "Enter proceeds, Treasury yield, equity total return, and a horizon to calculate. Optional stress outputs require both a chosen loss and month.";
      return;
    }
    if (p <= 0 || wait < 0 || phase < 1 || horizon <= 0 || wait + phase > horizon * 12) {
      output.textContent = "Check the entries: proceeds and horizon must be positive, phase-in must be at least one month, and parking plus phase-in must fit within the comparison horizon.";
      return;
    }
    if (roll === null) roll = t;
    var noCrash = run(p, t / 100, roll / 100, e / 100, wait, phase, horizon, 0, null);
    if (!noCrash) {
      output.textContent = "The inputs are outside the supported calculation range. Check rates, percentages, and horizon.";
      return;
    }
    var lines = ["No crash: immediate equity " + dollars(noCrash.lumpEnd) + " (max drawdown " + (noCrash.lumpDraw * 100).toFixed(1) + "%); Treasury parking then phase-in " + dollars(noCrash.phasedEnd) + " (max drawdown " + (noCrash.phasedDraw * 100).toFixed(1) + "%)."];

    [["Depression-era stress (assumed shock)", s1Drop, s1Month], ["2008-style stress (assumed shock)", s2Drop, s2Month]].forEach(function (scenario) {
      if (scenario[1] === null && scenario[2] === null) return;
      if (scenario[1] === null || scenario[2] === null) {
        lines.push(scenario[0] + ": enter both the shock loss and month; neither is pre-filled or inferred from recession dates.");
        return;
      }
      var outcome = run(p, t / 100, roll / 100, e / 100, wait, phase, horizon, scenario[1], scenario[2]);
      if (!outcome) {
        lines.push(scenario[0] + ": invalid loss, month, or horizon.");
        return;
      }
      lines.push(scenario[0] + ": immediate " + dollars(outcome.lumpEnd) + " (max drawdown " + (outcome.lumpDraw * 100).toFixed(1) + "%); phased " + dollars(outcome.phasedEnd) + " (max drawdown " + (outcome.phasedDraw * 100).toFixed(1) + "%). Inputs are stress assumptions, not historical returns.");
    });
    output.textContent = lines.join(" ");
  }

  function init() {
    ids.forEach(function (id) {
      var el = document.getElementById(id);
      if (el) el.addEventListener("input", render);
    });
    render();
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
}());
