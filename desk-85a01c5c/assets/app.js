/* desk-85a01c5c what-if calculator (client-side).
   The same formulas as _src/model.py; both must stay in sync. */
(function () {
  "use strict";
  var A_VALUE = 3100000, A_BASE_YEAR = 2026;
  var ALLOWANCE = 1044586, GROWTH = 0.045, CAP = 0.02;
  var RATE = 0.0112, BROKERAGE = 0.05, EQ_RETURN = 0.07;
  var PARK_YIELD = 4.32 / 100 / 12; // 3-month Treasury, 13 Nov 2026

  function m10(x) { return Math.round(x / 10) * 10; }
  function money(x) { return "$" + m10(x).toLocaleString("en-US"); }

  function compute() {
    var ty = parseInt(document.getElementById("wf-year").value, 10);
    var g = parseFloat(document.getElementById("wf-growth").value) / 100;
    var r = parseFloat(document.getElementById("wf-return").value) / 100;
    var mv = A_VALUE * Math.pow(1 + g, ty - A_BASE_YEAR);
    var fbv = 550000 * Math.pow(1 + CAP, ty - A_BASE_YEAR);
    var assessed = Math.max(0, mv - ALLOWANCE); // Prop 19: FBV + excess
    var brokerage = mv * BROKERAGE;
    var ttax = Math.round(mv / 500) * 0.55;
    var proceeds = mv - brokerage - ttax - 100;
    var yrs = 2076 - ty;
    var sell = proceeds * Math.pow(1 + r, yrs);
    // phased: park 36 months, then phase in over 24 months (monthly, equal)
    var park = 36, phase = 24;
    var cash = proceeds, units = 0, tranche = proceeds / phase;
    var mr = Math.pow(1 + r, 1 / 12);
    var level = 1; // flat market path (no crash): price index held at peak
    for (var k = 0; k < yrs * 12; k++) {
      if (k >= park && cash > 0) {
        var buy = Math.min(tranche, cash);
        units += buy * Math.pow(mr, yrs * 12 - k);
        cash -= buy;
      }
      if (cash > 0) { cash *= (1 + PARK_YIELD); }
    }
    var phased = cash + units; // flat path: buying at level 1 = holding cash until end
    var out = document.getElementById("wf-out");
    out.innerHTML =
      "<tr><td>Market value at " + ty + " transfer</td><td class='num'>" + money(mv) + "</td></tr>" +
      "<tr><td>Prop 19 assessed after transfer (heir occupies)</td><td class='num'>" + money(assessed) + "</td></tr>" +
      "<tr><td>Annual property tax at " + (RATE * 100).toFixed(2) + "% (band midpoint)</td><td class='num'>" + money(assessed * RATE) + "</td></tr>" +
      "<tr><td>Sale proceeds after costs (assumption: 5% brokerage, $0.55/$500 transfer tax, $100 fees)</td><td class='num'>" + money(proceeds) + "</td></tr>" +
      "<tr><td>Sell-and-reinvest value at 2076 (at " + (r * 100).toFixed(1) + "%/yr)</td><td class='num'>" + money(sell) + "</td></tr>" +
      "<tr><td>Phased variant: park 36 months, phase 24 months, flat market (no crash)</td><td class='num'>" + money(phased) + "</td></tr>" +
      "<tr><td>Cost of the cushion on a flat market</td><td class='num'>" + money(sell - phased) + "</td></tr>";
  }
  var btn = document.getElementById("wf-go");
  if (btn) {
    btn.addEventListener("click", compute);
    compute();
  }
})();
