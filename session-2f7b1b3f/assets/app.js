/* Estate & Real Property Decision Dashboard — Client Engine
   All financial outputs strictly rounded to nearest $10 increments.
   Works cleanly offline and on GitHub Pages subpaths. */

(function () {
  "use strict";

  function r10(val) {
    if (val === null || val === undefined || isNaN(val)) return null;
    return Math.round(val / 10) * 10;
  }

  function fmt10(val, showSign) {
    if (val === null || val === undefined || isNaN(val)) return "—";
    const rounded = r10(val);
    const abs = Math.abs(rounded).toLocaleString("en-US");
    if (rounded < 0) return `-$${abs}`;
    if (showSign && rounded > 0) return `+$${abs}`;
    return `$${abs}`;
  }

  // Exact constants verified from official sources + user baseline
  const BASE = {
    cupFmv2026: 3100000,
    cupAv2026: 550540,
    cupParcel2026: 900,
    cupAdvalRate: 0.0118,
    cupWater2026: 1500,
    cupSolarCredit2026: -180,
    cupInsAvg2026: 1570,
    cupInsSens2026: 2800,
    cupMaint2026: 6200,

    sfFmv2026: 1800000,
    sfAv2026: Math.round(114250 * 1.02), // 116,530 statutory projection
    sfAdvalRate: 0.0118162182,
    sfParcel2026: 1100,
    sfRent2Units2026: 7150 * 12,
    sfRentUnit32026: 3580 * 12,
    sfWater2026: 365 * 12,
    sfElec2026: 50 * 12,
    sfInsAvg2026: 1570,
    sfInsSens2026: 3500,
    sfMaint2026: 12600,
    sfRentBoardFee: 59,

    prop19Cap2026: 1044586,
    fedExempt2026: 15000000,
  };

  function runProjection(opts) {
    const cupApp = opts.cupApprec ?? 0.0491;
    const sfApp = opts.sfApprec ?? 0.0476;
    const cpi = opts.cpi ?? 0.028;
    const p19Growth = opts.prop19CapGrowth ?? 0.042;
    const nemSunset = opts.nemSunsetYear ?? 2042;

    const rows = [];
    let cupFmv = BASE.cupFmv2026;
    let cupAv = BASE.cupAv2026;
    let sfFmv = BASE.sfFmv2026;
    let sfAv = BASE.sfAv2026;
    let p19Cap = BASE.prop19Cap2026;
    let fedExempt = BASE.fedExempt2026;

    for (let yr = 2026; yr <= 2050; yr++) {
      const t = yr - 2026;
      if (t > 0) {
        cupFmv *= 1 + cupApp;
        cupAv *= 1.02;
        sfFmv *= 1 + sfApp;
        sfAv *= 1.02;
        if (yr % 2 === 1) {
          p19Cap *= Math.pow(1 + p19Growth, 2);
        }
        fedExempt *= 1 + cpi;
      }

      const cupParcel = BASE.cupParcel2026 * Math.pow(1 + cpi, t);
      const sfParcel = BASE.sfParcel2026 * Math.pow(1 + cpi, t);

      const cupExcludedLimit = cupAv + p19Cap;
      const cupExcess = Math.max(0, cupFmv - cupExcludedLimit);
      const cupTaxableP19 = cupAv + cupExcess;
      const cupTaxProp19 = cupTaxableP19 * BASE.cupAdvalRate + cupParcel;
      const cupTaxNoP19 = cupFmv * BASE.cupAdvalRate + cupParcel;

      const sfTaxFull = sfFmv * BASE.sfAdvalRate + sfParcel;
      const sfUnitAv = sfAv / 3;
      const sfUnitFmv = sfFmv / 3;
      const sfUnitExcess = Math.max(0, sfUnitFmv - (sfUnitAv + p19Cap));
      const sfTaxable1UnitP19 = sfUnitAv + sfUnitExcess + 2 * sfUnitFmv;
      const sfTax1UnitP19 = sfTaxable1UnitP19 * BASE.sfAdvalRate + sfParcel;

      const cupWater = BASE.cupWater2026 * Math.pow(1.04, t);
      const cupElec = yr < nemSunset
        ? BASE.cupSolarCredit2026 * Math.pow(1.025, t)
        : 420 * Math.pow(1.03, t);
      const cupIns = BASE.cupInsAvg2026 * Math.pow(1.045, t);
      const cupInsSens = BASE.cupInsSens2026 * Math.pow(1.045, t);
      const cupMaint = BASE.cupMaint2026 * Math.pow(1 + cpi, t);

      let sfWaterFactor = 1;
      for (let k = 1; k <= t; k++) {
        sfWaterFactor *= 1 + (k <= 10 ? 0.085 : 0.045);
      }
      const sfWater = BASE.sfWater2026 * sfWaterFactor;
      const sfElec = BASE.sfElec2026 * Math.pow(1.035, t);
      const sfIns = BASE.sfInsAvg2026 * Math.pow(1.045, t);
      const sfInsSens = BASE.sfInsSens2026 * Math.pow(1.045, t);
      const sfMaint = BASE.sfMaint2026 * Math.pow(1 + cpi, t);
      const sfRent2uBlend = BASE.sfRent2Units2026 * Math.pow(1.03, t);

      rows.push({
        year: yr,
        t,
        cupFmv,
        cupAv,
        p19Cap,
        cupTaxableP19,
        cupTaxProp19,
        cupTaxNoP19,
        cupWater,
        cupElec,
        cupIns,
        cupInsSens,
        cupMaint,
        sfFmv,
        sfAv,
        sfTaxFull,
        sfTax1UnitP19,
        sfWater,
        sfElec,
        sfIns,
        sfInsSens,
        sfMaint,
        sfRent2uBlend,
        fedExempt,
      });
    }
    return rows;
  }

  function simulateStrategies(opts) {
    const inheritYear = opts.inheritYear ?? 2045;
    const holdYears = opts.holdYears ?? 10;
    const cupApp = opts.cupApprec ?? 0.0491;
    const sfApp = opts.sfApprec ?? 0.0476;
    const cpi = opts.cpi ?? 0.028;
    const eqRet = opts.equityReturn ?? 0.095;
    const treasRet = opts.treasuryReturn ?? 0.045;
    const cupRentYield = opts.cupRentYield ?? 0.028;
    const useSensIns = !!opts.useSensIns;
    const parentPrimaryCup = opts.parentPrimaryCup !== false;
    const marginalOrdTax = 0.35;
    const divYield = 0.015;
    const divTax = 0.30;
    const eqAfterDiv = eqRet - divYield * divTax;
    const treasAfterTax = treasRet * (1 - 0.24);
    const capGainTax = 0.30;
    const sellCostCup = 0.0511;

    function sfTransRate(v) {
      return v >= 5000000 ? 0.0225 : 0.0075;
    }

    const proj = runProjection({ cupApprec: cupApp, sfApprec: sfApp, cpi });
    const base = proj.find((r) => r.year === inheritYear);
    const insCup0 = useSensIns ? base.cupInsSens : base.cupIns;
    const insSf0 = useSensIns ? base.sfInsSens : base.sfIns;

    // A: Live SF Unit 3 + Sell Cupertino -> Equity or Treasury
    function simA(reinvestRate, label, key) {
      const cupProc = base.cupFmv * (1 - sellCostCup);
      let port = cupProc;
      let sfVal = base.sfFmv;
      let sfTaxable = parentPrimaryCup
        ? base.sfFmv
        : base.sfAv / 3 + Math.max(0, base.sfFmv / 3 - (base.sfAv / 3 + base.p19Cap)) + 2 * (base.sfFmv / 3);
      let sfRent = base.sfRent2uBlend;
      let sfWater = base.sfWater;
      let sfElec = base.sfElec;
      let sfIns = insSf0;
      let sfMaint = base.sfMaint;
      const sfDepr = (base.sfFmv * 0.6 * (2 / 3)) / 27.5;
      let yr1Cf = 0;
      let initSfTax = 0;

      for (let y = 0; y < holdYears; y++) {
        const tTot = base.t + y;
        if (y > 0) {
          sfVal *= 1 + sfApp;
          sfTaxable *= 1.02;
          sfRent *= 1.028;
          sfWater *= 1.045;
          sfElec *= 1.035;
          sfIns *= 1.045;
          sfMaint *= 1 + cpi;
        }
        const sfTax = sfTaxable * BASE.sfAdvalRate + BASE.sfParcel2026 * Math.pow(1 + cpi, tTot);
        if (y === 0) initSfTax = sfTax;
        const ded = (2 / 3) * (sfTax + sfWater + sfIns + sfMaint) + 2 * BASE.sfRentBoardFee;
        const incTax = Math.max(0, sfRent - ded - sfDepr) * marginalOrdTax;
        const cf = sfRent - (sfTax + sfWater + sfElec + sfIns + sfMaint + 2 * BASE.sfRentBoardFee) - incTax;
        if (y === 0) yr1Cf = cf;
        port = port * (1 + reinvestRate) + cf;
      }
      const sfAfterTax = sfVal * (1 - (0.05 + sfTransRate(sfVal))) - Math.max(0, sfVal - base.sfFmv) * capGainTax - sfDepr * holdYears * 0.25;
      const portAfterTax = port - Math.max(0, port - cupProc) * capGainTax;
      return {
        key, label,
        yr1Cf: r10(yr1Cf),
        initCupTax: 0,
        initSfTax: r10(initSfTax),
        endReGross: r10(sfVal),
        endLiqPortfolio: r10(port),
        endGross: r10(sfVal + port),
        endAfterTax: r10(sfAfterTax + portAfterTax),
      };
    }

    // B: Live SF Unit 3 + Rent Cupertino
    function simB() {
      let cupVal = base.cupFmv;
      let cupTaxable = base.cupFmv;
      let cupRent = base.cupFmv * cupRentYield;
      const cupDepr = (base.cupFmv * 0.45) / 27.5;
      let cupIns = insCup0 * 1.15;
      let cupMaint = base.cupMaint;

      let sfVal = base.sfFmv;
      let sfTaxable = parentPrimaryCup
        ? base.sfFmv
        : base.sfAv / 3 + Math.max(0, base.sfFmv / 3 - (base.sfAv / 3 + base.p19Cap)) + 2 * (base.sfFmv / 3);
      let sfRent = base.sfRent2uBlend;
      const sfDepr = (base.sfFmv * 0.6 * (2 / 3)) / 27.5;
      let sfWater = base.sfWater;
      let sfElec = base.sfElec;
      let sfIns = insSf0;
      let sfMaint = base.sfMaint;
      let side = 0;
      let yr1Cf = 0;
      let initCupTax = 0;
      let initSfTax = 0;

      for (let y = 0; y < holdYears; y++) {
        const tTot = base.t + y;
        if (y > 0) {
          cupVal *= 1 + cupApp;
          cupTaxable *= 1.02;
          cupRent *= 1 + cpi;
          cupIns *= 1.045;
          cupMaint *= 1 + cpi;
          sfVal *= 1 + sfApp;
          sfTaxable *= 1.02;
          sfRent *= 1.028;
          sfWater *= 1.045;
          sfElec *= 1.035;
          sfIns *= 1.045;
          sfMaint *= 1 + cpi;
        }
        const cupTax = cupTaxable * BASE.cupAdvalRate + BASE.cupParcel2026 * Math.pow(1 + cpi, tTot);
        const sfTax = sfTaxable * BASE.sfAdvalRate + BASE.sfParcel2026 * Math.pow(1 + cpi, tTot);
        if (y === 0) { initCupTax = cupTax; initSfTax = sfTax; }
        const cupEffRent = cupRent * 0.96;
        const cupIncTax = Math.max(0, cupEffRent - (cupTax + cupIns + cupMaint) - cupDepr) * marginalOrdTax;
        const cupCf = cupEffRent - (cupTax + cupIns + cupMaint) - cupIncTax;

        const sfDed = (2 / 3) * (sfTax + sfWater + sfIns + sfMaint) + 2 * BASE.sfRentBoardFee;
        const sfIncTax = Math.max(0, sfRent - sfDed - sfDepr) * marginalOrdTax;
        const sfCf = sfRent - (sfTax + sfWater + sfElec + sfIns + sfMaint + 2 * BASE.sfRentBoardFee) - sfIncTax;

        const cf = cupCf + sfCf;
        if (y === 0) yr1Cf = cf;
        side = side * (1 + eqAfterDiv) + cf;
      }
      const cupAfter = cupVal * (1 - sellCostCup) - Math.max(0, cupVal - base.cupFmv) * capGainTax - cupDepr * holdYears * 0.25;
      const sfAfter = sfVal * (1 - (0.05 + sfTransRate(sfVal))) - Math.max(0, sfVal - base.sfFmv) * capGainTax - sfDepr * holdYears * 0.25;
      return {
        key: "B",
        label: "B. Live in SF Unit 3 + Rent Out Cupertino",
        yr1Cf: r10(yr1Cf),
        initCupTax: r10(initCupTax),
        initSfTax: r10(initSfTax),
        endReGross: r10(cupVal + sfVal),
        endLiqPortfolio: r10(side),
        endGross: r10(cupVal + sfVal + side),
        endAfterTax: r10(cupAfter + sfAfter + side * 0.85),
      };
    }

    // C: Live in Cupertino (Prop 19 if parent primary) + Rent 3 Units in SF
    function simC() {
      let cupVal = base.cupFmv;
      let cupTaxable = parentPrimaryCup
        ? base.cupAv + Math.max(0, base.cupFmv - (base.cupAv + base.p19Cap))
        : base.cupFmv;
      let cupWater = base.cupWater;
      let cupElec = base.cupElec;
      let cupIns = insCup0;
      let cupMaint = base.cupMaint;

      let sfVal = base.sfFmv;
      let sfTaxable = base.sfFmv;
      let sfRent = base.sfRent2uBlend + BASE.sfRentUnit32026 * Math.pow(1 + cpi, base.t);
      const sfDepr = (base.sfFmv * 0.6) / 27.5;
      let sfWater = base.sfWater;
      let sfElec = base.sfElec;
      let sfIns = insSf0;
      let sfMaint = base.sfMaint;
      let side = 0;
      let yr1Cf = 0;
      let initCupTax = 0;
      let initSfTax = 0;

      for (let y = 0; y < holdYears; y++) {
        const tTot = base.t + y;
        if (y > 0) {
          cupVal *= 1 + cupApp;
          cupTaxable *= 1.02;
          cupWater *= 1.04;
          cupElec *= 1.03;
          cupIns *= 1.045;
          cupMaint *= 1 + cpi;
          sfVal *= 1 + sfApp;
          sfTaxable *= 1.02;
          sfRent *= 1.028;
          sfWater *= 1.045;
          sfElec *= 1.035;
          sfIns *= 1.045;
          sfMaint *= 1 + cpi;
        }
        const cupTax = cupTaxable * BASE.cupAdvalRate + BASE.cupParcel2026 * Math.pow(1 + cpi, tTot);
        const sfTax = sfTaxable * BASE.sfAdvalRate + BASE.sfParcel2026 * Math.pow(1 + cpi, tTot);
        if (y === 0) { initCupTax = cupTax; initSfTax = sfTax; }

        const cupCf = -(cupTax + cupWater + cupElec + cupIns + cupMaint);
        const sfExp = sfTax + sfWater + sfElec + sfIns + sfMaint + 3 * BASE.sfRentBoardFee;
        const sfIncTax = Math.max(0, sfRent - sfExp - sfDepr) * marginalOrdTax;
        const sfCf = sfRent - sfExp - sfIncTax;

        const cf = cupCf + sfCf;
        if (y === 0) yr1Cf = cf;
        side = side * (1 + eqAfterDiv) + cf;
      }
      const cupGain = Math.max(0, cupVal - base.cupFmv - 500000);
      const cupAfter = cupVal * (1 - sellCostCup) - cupGain * capGainTax;
      const sfAfter = sfVal * (1 - (0.05 + sfTransRate(sfVal))) - Math.max(0, sfVal - base.sfFmv) * capGainTax - sfDepr * holdYears * 0.25;
      return {
        key: "C",
        label: "C. Live in Cupertino (Prop 19) + Rent All 3 SF Units",
        yr1Cf: r10(yr1Cf),
        initCupTax: r10(initCupTax),
        initSfTax: r10(initSfTax),
        endReGross: r10(cupVal + sfVal),
        endLiqPortfolio: r10(side),
        endGross: r10(cupVal + sfVal + side),
        endAfterTax: r10(cupAfter + sfAfter + side * 0.85),
      };
    }

    // D: Live in Cupertino + Sell SF -> Equities
    function simD() {
      const sfProc = base.sfFmv * (1 - (0.05 + sfTransRate(base.sfFmv)));
      let port = sfProc;
      let cupVal = base.cupFmv;
      let cupTaxable = parentPrimaryCup
        ? base.cupAv + Math.max(0, base.cupFmv - (base.cupAv + base.p19Cap))
        : base.cupFmv;
      let cupWater = base.cupWater;
      let cupElec = base.cupElec;
      let cupIns = insCup0;
      let cupMaint = base.cupMaint;
      let yr1Cf = 0;
      let initCupTax = 0;

      for (let y = 0; y < holdYears; y++) {
        const tTot = base.t + y;
        if (y > 0) {
          cupVal *= 1 + cupApp;
          cupTaxable *= 1.02;
          cupWater *= 1.04;
          cupElec *= 1.03;
          cupIns *= 1.045;
          cupMaint *= 1 + cpi;
        }
        const cupTax = cupTaxable * BASE.cupAdvalRate + BASE.cupParcel2026 * Math.pow(1 + cpi, tTot);
        if (y === 0) initCupTax = cupTax;
        const cf = -(cupTax + cupWater + cupElec + cupIns + cupMaint);
        if (y === 0) yr1Cf = cf;
        port = port * (1 + eqAfterDiv) + cf;
      }
      const cupAfter = cupVal * (1 - sellCostCup) - Math.max(0, cupVal - base.cupFmv - 500000) * capGainTax;
      const portAfter = port - Math.max(0, port - sfProc) * capGainTax;
      return {
        key: "D",
        label: "D. Live in Cupertino (Prop 19) + Sell SF -> Equities",
        yr1Cf: r10(yr1Cf),
        initCupTax: r10(initCupTax),
        initSfTax: 0,
        endReGross: r10(cupVal),
        endLiqPortfolio: r10(port),
        endGross: r10(cupVal + port),
        endAfterTax: r10(cupAfter + portAfter),
      };
    }

    // E: Sell Both -> Equities (rent outside housing)
    function simE() {
      const cupProc = base.cupFmv * (1 - sellCostCup);
      const sfProc = base.sfFmv * (1 - (0.05 + sfTransRate(base.sfFmv)));
      let port = cupProc + sfProc;
      let rentCost = 4500 * 12 * Math.pow(1 + cpi, base.t);
      let yr1Cf = 0;
      for (let y = 0; y < holdYears; y++) {
        if (y > 0) rentCost *= 1 + cpi;
        if (y === 0) yr1Cf = -rentCost;
        port = port * (1 + eqAfterDiv) - rentCost;
      }
      const portAfter = port - Math.max(0, port - (cupProc + sfProc)) * capGainTax;
      return {
        key: "E",
        label: "E. Sell Both at Inheritance -> 100% Equities (Rent Home)",
        yr1Cf: r10(yr1Cf),
        initCupTax: 0,
        initSfTax: 0,
        endReGross: 0,
        endLiqPortfolio: r10(port),
        endGross: r10(port),
        endAfterTax: r10(portAfter),
      };
    }

    return {
      inheritYear,
      holdYears,
      cupFmv: r10(base.cupFmv),
      sfFmv: r10(base.sfFmv),
      prop19Cap: r10(base.p19Cap),
      results: [
        simA(eqAfterDiv, "A. Live in SF Unit 3 + Sell Cupertino -> S&P 500 Equities (Recommended)", "A"),
        simE(),
        simB(),
        simD(),
        simC(),
        simA(treasAfterTax, "A2. Live in SF Unit 3 + Sell Cupertino -> 4.5% U.S. Treasuries", "A2"),
      ],
    };
  }

  // Generic table search filter helper
  function attachTableFilter(inputId, tableId) {
    const inp = document.getElementById(inputId);
    const tbl = document.getElementById(tableId);
    if (!inp || !tbl) return;
    inp.addEventListener("input", function () {
      const q = inp.value.trim().toLowerCase();
      const rows = tbl.querySelectorAll("tbody tr");
      rows.forEach((tr) => {
        const txt = tr.textContent.toLowerCase();
        tr.style.display = txt.includes(q) ? "" : "none";
      });
    });
  }

  // Render Executive Summary dynamic scenario on index.html
  function initExecutivePage() {
    const container = document.getElementById("exec-strategy-table");
    if (!container || !window.INHERITANCE_MODEL_DATA) return;

    const regimeSel = document.getElementById("exec-regime");
    const yearSel = document.getElementById("exec-year");

    function render() {
      const reg = regimeSel ? regimeSel.value : "hist";
      const yr = yearSel ? parseInt(yearSel.value, 10) : 2045;
      const sim = simulateStrategies(
        reg === "cons"
          ? { inheritYear: yr, cupApprec: 0.0375, sfApprec: 0.035, equityReturn: 0.08 }
          : { inheritYear: yr, cupApprec: 0.0491, sfApprec: 0.0476, equityReturn: 0.095 }
      );

      document.getElementById("exec-cup-val").textContent = fmt10(sim.cupFmv);
      document.getElementById("exec-sf-val").textContent = fmt10(sim.sfFmv);
      const bestA = sim.results.find((r) => r.key === "A");
      const rentB = sim.results.find((r) => r.key === "B");
      document.getElementById("exec-adv-val").textContent = fmt10(bestA.endGross - rentB.endGross, true);
      document.getElementById("exec-yr1-cf").textContent = fmt10(bestA.yr1Cf, true);

      const tbody = container.querySelector("tbody");
      tbody.innerHTML = "";
      const maxGross = Math.max(...sim.results.map((r) => r.endGross));
      const barsEl = document.getElementById("exec-bars");
      if (barsEl) barsEl.innerHTML = "";

      sim.results.forEach((r) => {
        const tr = document.createElement("tr");
        if (r.key === "A") tr.className = "row-highlight";
        if (r.key === "A2") tr.className = "row-warn";
        tr.innerHTML = `
          <td><strong>${r.label}</strong></td>
          <td class="num">${fmt10(r.yr1Cf, true)}</td>
          <td class="num">${fmt10(r.initCupTax)} / ${fmt10(r.initSfTax)}</td>
          <td class="num">${fmt10(r.endReGross)}</td>
          <td class="num">${fmt10(r.endLiqPortfolio)}</td>
          <td class="num"><strong>${fmt10(r.endGross)}</strong></td>
          <td class="num">${fmt10(r.endAfterTax)}</td>
        `;
        tbody.appendChild(tr);

        if (barsEl) {
          const pct = Math.max(4, Math.round((r.endGross / maxGross) * 100));
          const cls = r.key === "A" ? "best" : r.key === "E" ? "alt" : r.key === "A2" ? "warn" : "";
          const rowDiv = document.createElement("div");
          rowDiv.className = "bar-row";
          rowDiv.innerHTML = `
            <div class="bar-label">${r.label.split(" (")[0]}</div>
            <div class="bar-track"><div class="bar-fill ${cls}" style="width:${pct}%"></div></div>
            <div class="bar-val">${fmt10(r.endGross)}</div>
          `;
          barsEl.appendChild(rowDiv);
        }
      });
    }

    if (regimeSel) regimeSel.addEventListener("change", render);
    if (yearSel) yearSel.addEventListener("change", render);
    render();
  }

  // Render Interactive Simulator on pages/decision-analysis.html
  function initDecisionSimulator() {
    const simRoot = document.getElementById("decision-simulator");
    if (!simRoot) return;

    const els = {
      preset: document.getElementById("sim-preset"),
      year: document.getElementById("sim-year"),
      hold: document.getElementById("sim-hold"),
      cupApp: document.getElementById("sim-cup-app"),
      sfApp: document.getElementById("sim-sf-app"),
      eqRet: document.getElementById("sim-eq-ret"),
      cupYield: document.getElementById("sim-cup-yield"),
      parentRes: document.getElementById("sim-parent-res"),
      insMode: document.getElementById("sim-ins-mode"),
    };

    function syncLabels() {
      document.getElementById("lbl-year").textContent = els.year.value;
      document.getElementById("lbl-hold").textContent = `${els.hold.value} yrs`;
      document.getElementById("lbl-cup-app").textContent = `${parseFloat(els.cupApp.value).toFixed(2)}%`;
      document.getElementById("lbl-sf-app").textContent = `${parseFloat(els.sfApp.value).toFixed(2)}%`;
      document.getElementById("lbl-eq-ret").textContent = `${parseFloat(els.eqRet.value).toFixed(2)}%`;
      document.getElementById("lbl-cup-yield").textContent = `${parseFloat(els.cupYield.value).toFixed(2)}%`;
    }

    function applyPreset() {
      if (els.preset.value === "hist") {
        els.cupApp.value = "4.91";
        els.sfApp.value = "4.76";
        els.eqRet.value = "9.50";
      } else if (els.preset.value === "cons") {
        els.cupApp.value = "3.75";
        els.sfApp.value = "3.50";
        els.eqRet.value = "8.00";
      } else if (els.preset.value === "tsp") {
        els.cupApp.value = "4.91";
        els.sfApp.value = "4.76";
        els.eqRet.value = "11.34";
      }
      render();
    }

    function render() {
      syncLabels();
      const sim = simulateStrategies({
        inheritYear: parseInt(els.year.value, 10),
        holdYears: parseInt(els.hold.value, 10),
        cupApprec: parseFloat(els.cupApp.value) / 100,
        sfApprec: parseFloat(els.sfApp.value) / 100,
        equityReturn: parseFloat(els.eqRet.value) / 100,
        cupRentYield: parseFloat(els.cupYield.value) / 100,
        parentPrimaryCup: els.parentRes.value === "cup",
        useSensIns: els.insMode.value === "sens",
      });

      document.getElementById("sim-cup-fmv").textContent = fmt10(sim.cupFmv);
      document.getElementById("sim-sf-fmv").textContent = fmt10(sim.sfFmv);
      document.getElementById("sim-p19-cap").textContent = fmt10(sim.prop19Cap);

      const best = [...sim.results].sort((a, b) => b.endAfterTax - a.endAfterTax)[0];
      const stratA = sim.results.find((r) => r.key === "A");
      const stratB = sim.results.find((r) => r.key === "B");
      document.getElementById("sim-winner-note").innerHTML =
        `Top After-Tax Wealth Strategy: <strong>${best.label}</strong> (${fmt10(best.endAfterTax)} after-tax; Strategy A vs Renting Cupertino B advantage: <strong>${fmt10(stratA.endGross - stratB.endGross, true)}</strong> gross / <strong>${fmt10(stratA.endAfterTax - stratB.endAfterTax, true)}</strong> after-tax).`;

      const tbody = document.querySelector("#sim-table tbody");
      tbody.innerHTML = "";
      const maxGross = Math.max(...sim.results.map((r) => r.endGross));
      const bars = document.getElementById("sim-bars");
      bars.innerHTML = "";

      sim.results.forEach((r) => {
        const tr = document.createElement("tr");
        if (r.key === "A") tr.className = "row-highlight";
        if (r.key === "A2") tr.className = "row-warn";
        tr.innerHTML = `
          <td><strong>${r.label}</strong></td>
          <td class="num">${fmt10(r.yr1Cf, true)}</td>
          <td class="num">${fmt10(r.initCupTax)}</td>
          <td class="num">${fmt10(r.initSfTax)}</td>
          <td class="num">${fmt10(r.endReGross)}</td>
          <td class="num">${fmt10(r.endLiqPortfolio)}</td>
          <td class="num"><strong>${fmt10(r.endGross)}</strong></td>
          <td class="num"><strong>${fmt10(r.endAfterTax)}</strong></td>
        `;
        tbody.appendChild(tr);

        const pct = Math.max(4, Math.round((r.endGross / maxGross) * 100));
        const cls = r.key === "A" ? "best" : r.key === "E" ? "alt" : r.key === "A2" ? "warn" : "";
        const d = document.createElement("div");
        d.className = "bar-row";
        d.innerHTML = `
          <div class="bar-label">${r.label.split(" (")[0]}</div>
          <div class="bar-track"><div class="bar-fill ${cls}" style="width:${pct}%"></div></div>
          <div class="bar-val">${fmt10(r.endGross)}</div>
        `;
        bars.appendChild(d);
      });
    }

    els.preset.addEventListener("change", applyPreset);
    [els.year, els.hold, els.cupApp, els.sfApp, els.eqRet, els.cupYield].forEach((el) => {
      el.addEventListener("input", function () {
        if (el !== els.year && el !== els.hold) els.preset.value = "custom";
        render();
      });
    });
    els.parentRes.addEventListener("change", render);
    els.insMode.addEventListener("change", render);
    render();
  }

  // Render Year-by-Year Projections on pages/projections.html
  function initProjectionsPage() {
    const cupTbl = document.getElementById("proj-cup-table");
    const sfTbl = document.getElementById("proj-sf-table");
    if (!cupTbl || !sfTbl || !window.INHERITANCE_MODEL_DATA) return;

    const btnHist = document.getElementById("btn-proj-hist");
    const btnCons = document.getElementById("btn-proj-cons");

    function render(regime) {
      const rows = window.INHERITANCE_MODEL_DATA.projections[regime];
      const cupBody = cupTbl.querySelector("tbody");
      const sfBody = sfTbl.querySelector("tbody");
      cupBody.innerHTML = "";
      sfBody.innerHTML = "";

      rows.forEach((r) => {
        const highlight = r.year === 2040 || r.year === 2045 || r.year === 2050 ? "row-highlight" : "";
        const cTr = document.createElement("tr");
        if (highlight) cTr.className = highlight;
        cTr.innerHTML = `
          <td><strong>${r.year}</strong></td>
          <td class="num">${fmt10(r.cup_fmv)}</td>
          <td class="num">${fmt10(r.cup_av_prop13)}</td>
          <td class="num">${fmt10(r.cup_tax_pre)}</td>
          <td class="num">${fmt10(r.prop19_cap)}</td>
          <td class="num">${fmt10(r.cup_taxable_prop19)}</td>
          <td class="num">${fmt10(r.cup_tax_prop19)}</td>
          <td class="num">${fmt10(r.cup_tax_no_prop19)}</td>
          <td class="num"><strong>${fmt10(r.cup_prop19_savings)}</strong></td>
          <td class="num">${fmt10(r.cup_water)}</td>
          <td class="num">${fmt10(r.cup_elec, true)}</td>
          <td class="num">${fmt10(r.cup_ins_base)} / ${fmt10(r.cup_ins_sens)}</td>
          <td class="num">${fmt10(r.cup_maint)}</td>
        `;
        cupBody.appendChild(cTr);

        const sTr = document.createElement("tr");
        if (highlight) sTr.className = highlight;
        sTr.innerHTML = `
          <td><strong>${r.year}</strong></td>
          <td class="num">${fmt10(r.sf_fmv)}</td>
          <td class="num">${fmt10(r.sf_av_prop13)}</td>
          <td class="num">${fmt10(r.sf_tax_pre)}</td>
          <td class="num">${fmt10(r.sf_tax_full_reassess)}</td>
          <td class="num">${fmt10(r.sf_tax_1unit_prop19)}</td>
          <td class="num">${fmt10(r.sf_rent_2u_rc)}</td>
          <td class="num">${fmt10(r.sf_rent_2u_blend)}</td>
          <td class="num">${fmt10(r.sf_water)}</td>
          <td class="num">${fmt10(r.sf_elec)}</td>
          <td class="num">${fmt10(r.sf_ins_base)} / ${fmt10(r.sf_ins_sens)}</td>
          <td class="num">${fmt10(r.sf_maint)}</td>
        `;
        sfBody.appendChild(sTr);
      });
    }

    if (btnHist && btnCons) {
      btnHist.addEventListener("click", function () {
        btnHist.classList.add("active");
        btnCons.classList.remove("active");
        render("historical_baseline");
      });
      btnCons.addEventListener("click", function () {
        btnCons.classList.add("active");
        btnHist.classList.remove("active");
        render("conservative");
      });
    }
    render("historical_baseline");
  }

  // Render Estate Thresholds & Liquid Headroom on pages/estate-thresholds.html
  function initEstateThresholdsPage() {
    const tbl = document.getElementById("estate-headroom-table");
    if (!tbl || !window.INHERITANCE_MODEL_DATA) return;

    const liqInput = document.getElementById("est-liquid-2026");
    const liqGrowth = document.getElementById("est-liquid-growth");
    const tbody = tbl.querySelector("tbody");

    function render() {
      const liq0 = liqInput ? parseFloat(liqInput.value) || 0 : 4000000;
      const g = liqGrowth ? (parseFloat(liqGrowth.value) || 0) / 100 : 0.06;
      const rows = window.INHERITANCE_MODEL_DATA.projections.historical_baseline;
      tbody.innerHTML = "";

      rows.forEach((r) => {
        if (r.year !== 2026 && r.year < 2030 && r.year % 2 !== 0) return;
        const t = r.year - 2026;
        const projLiq = r10(liq0 * Math.pow(1 + g, t));
        const totalGross = r10(r.combined_re + projLiq);
        const taxSingle = r10(Math.max(0, totalGross - r.fed_exempt_single) * 0.40);
        const taxMarried = r10(Math.max(0, totalGross - r.fed_exempt_married) * 0.40);
        const taxRisk75 = r10(Math.max(0, totalGross - (r.combined_re + r.headroom_7_5m_risk)) * 0.40);

        const tr = document.createElement("tr");
        if (r.year === 2040 || r.year === 2045 || r.year === 2050) tr.className = "row-highlight";
        if (taxSingle > 0) tr.className = "row-warn";
        tr.innerHTML = `
          <td><strong>${r.year}</strong></td>
          <td class="num">${fmt10(r.combined_re)}</td>
          <td class="num">${fmt10(r.fed_exempt_single)}</td>
          <td class="num">${fmt10(r.headroom_single)}</td>
          <td class="num">${fmt10(r.fed_exempt_married)}</td>
          <td class="num">${fmt10(r.headroom_married)}</td>
          <td class="num">${fmt10(projLiq)}</td>
          <td class="num"><strong>${fmt10(totalGross)}</strong></td>
          <td class="num">${taxSingle > 0 ? `<span class="badge badge-danger">${fmt10(taxSingle)}</span>` : "$0"}</td>
          <td class="num">${taxMarried > 0 ? `<span class="badge badge-danger">${fmt10(taxMarried)}</span>` : "$0"}</td>
          <td class="num">${taxRisk75 > 0 ? `<span class="badge badge-flagged">${fmt10(taxRisk75)}</span>` : "$0"}</td>
        `;
        tbody.appendChild(tr);
      });
    }

    if (liqInput) liqInput.addEventListener("input", render);
    if (liqGrowth) liqGrowth.addEventListener("input", render);
    render();
  }

  // Render Historical Audit Tables on pages/verification-review.html
  function initAuditTables() {
    const cupTbl = document.getElementById("audit-cup-table");
    const sfTbl = document.getElementById("audit-sf-table");
    if (!cupTbl || !sfTbl || !window.INHERITANCE_MODEL_DATA) return;

    function fillAudit(tbl, rows, officialUrl) {
      const tbody = tbl.querySelector("tbody");
      tbody.innerHTML = "";
      rows.forEach((r) => {
        const hasFlag = r.flags && r.flags.length > 0;
        const tr = document.createElement("tr");
        if (hasFlag) tr.className = "row-warn";
        tr.innerHTML = `
          <td><strong>${r.year}</strong> (${r.boe_fy})</td>
          <td class="num">${r.tax !== null ? fmt10(r.tax_r10) + ` <span class="text-muted">($${r.tax.toLocaleString()})</span>` : '<span class="blank-cell">Blank / Unverified</span>'}</td>
          <td class="num">${r.actual_tax_chg_pct !== null ? `${r.actual_tax_chg_pct >= 0 ? "+" : ""}${r.actual_tax_chg_pct}%` : "—"}</td>
          <td class="num">${r.assessed !== null ? fmt10(r.assessed_r10) + ` <span class="text-muted">($${r.assessed.toLocaleString()})</span>` : '<span class="blank-cell">Blank / Unverified</span>'}</td>
          <td class="num">${r.actual_av_chg_pct !== null ? `${r.actual_av_chg_pct >= 0 ? "+" : ""}${r.actual_av_chg_pct}%` : "—"}</td>
          <td class="num">${r.boe_factor.toFixed(5)} (${r.boe_ccpi_pct}%)</td>
          <td class="num">${r.effective_tax_pct !== null ? r.effective_tax_pct.toFixed(3) + "%" : "—"}</td>
          <td>${hasFlag ? `<span class="badge badge-flagged">Flagged</span> ${r.flags.join("; ")}` : '<span class="badge badge-verified">Verified Match</span>'}</td>
          <td><a class="source-link" href="${officialUrl}" target="_blank" rel="noopener">BOE LTA 2026/002</a></td>
        `;
        tbody.appendChild(tr);
      });
    }

    fillAudit(cupTbl, window.INHERITANCE_MODEL_DATA.history_audit.cupertino, "https://boe.ca.gov/proptaxes/pdf/lta26002.pdf");
    fillAudit(sfTbl, window.INHERITANCE_MODEL_DATA.history_audit.san_francisco, "https://boe.ca.gov/proptaxes/pdf/lta26002.pdf");
  }

  document.addEventListener("DOMContentLoaded", function () {
    initExecutivePage();
    initDecisionSimulator();
    initProjectionsPage();
    initEstateThresholdsPage();
    initAuditTables();
    attachTableFilter("law-filter", "law-table-fed");
    attachTableFilter("law-filter", "law-table-ca");
    attachTableFilter("law-filter", "law-table-local");
  });
})();
