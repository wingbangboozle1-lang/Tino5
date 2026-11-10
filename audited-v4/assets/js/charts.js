/* Lightweight vector SVG chart helpers with interactive tooltips */

window.AppCharts = (function () {
  function ensureTooltip(container) {
    let tip = container.querySelector(".tooltip");
    if (!tip) {
      tip = document.createElement("div");
      tip.className = "tooltip";
      container.appendChild(tip);
    }
    return tip;
  }

  function renderHorizontalBars(containerId, items, opts = {}) {
    const el = document.getElementById(containerId);
    if (!el) return;
    const width = Math.max(el.clientWidth || 640, 360);
    const barH = 30;
    const gap = 14;
    const padL = opts.padL || 230;
    const padR = 95;
    const padT = 16;
    const padB = 26;
    const height = padT + padB + items.length * (barH + gap);

    const maxVal = Math.max(...items.map((d) => Math.max(0, d.value)), 1);
    const chartW = width - padL - padR;

    const svgNS = "http://www.w3.org/2000/svg";
    el.innerHTML = "";
    const tip = ensureTooltip(el);

    const svg = document.createElementNS(svgNS, "svg");
    svg.setAttribute("viewBox", `0 0 ${width} ${height}`);
    svg.setAttribute("width", "100%");
    svg.setAttribute("height", String(height));

    items.forEach((item, idx) => {
      const y = padT + idx * (barH + gap);
      const w = Math.max(4, (Math.max(0, item.value) / maxVal) * chartW);

      const label = document.createElementNS(svgNS, "text");
      label.setAttribute("x", String(padL - 10));
      label.setAttribute("y", String(y + barH / 2 + 4));
      label.setAttribute("text-anchor", "end");
      label.setAttribute("font-size", "12");
      label.setAttribute("fill", "#17212b");
      label.textContent = item.label;
      svg.appendChild(label);

      const bgRect = document.createElementNS(svgNS, "rect");
      bgRect.setAttribute("x", String(padL));
      bgRect.setAttribute("y", String(y));
      bgRect.setAttribute("width", String(chartW));
      bgRect.setAttribute("height", String(barH));
      bgRect.setAttribute("rx", "5");
      bgRect.setAttribute("fill", "#f2efe9");
      svg.appendChild(bgRect);

      const rect = document.createElementNS(svgNS, "rect");
      rect.setAttribute("x", String(padL));
      rect.setAttribute("y", String(y));
      rect.setAttribute("width", String(w));
      rect.setAttribute("height", String(barH));
      rect.setAttribute("rx", "5");
      rect.setAttribute("fill", item.color || "#0f4c5c");
      rect.style.cursor = "pointer";

      rect.addEventListener("mousemove", (e) => {
        const box = el.getBoundingClientRect();
        tip.style.display = "block";
        tip.style.left = Math.min(e.clientX - box.left + 12, box.width - 210) + "px";
        tip.style.top = (e.clientY - box.top - 36) + "px";
        tip.innerHTML = `<strong>${item.fullLabel || item.label}</strong><br>${AppUtils.fmtUSD(item.value, true)}`;
      });
      rect.addEventListener("mouseleave", () => {
        tip.style.display = "none";
      });
      svg.appendChild(rect);

      const valText = document.createElementNS(svgNS, "text");
      valText.setAttribute("x", String(padL + w + 8));
      valText.setAttribute("y", String(y + barH / 2 + 4));
      valText.setAttribute("font-size", "12");
      valText.setAttribute("font-weight", "700");
      valText.setAttribute("fill", "#17212b");
      valText.textContent = AppUtils.fmtCompactUSD(item.value);
      svg.appendChild(valText);
    });

    el.appendChild(svg);
  }

  function renderMultiLineChart(containerId, xLabels, seriesList) {
    const el = document.getElementById(containerId);
    if (!el) return;
    const width = Math.max(el.clientWidth || 640, 360);
    const height = 290;
    const padL = 70;
    const padR = 24;
    const padT = 20;
    const padB = 34;
    const plotW = width - padL - padR;
    const plotH = height - padT - padB;

    const allVals = seriesList.flatMap((s) => s.values);
    const maxY = Math.max(...allVals, 1) * 1.06;
    const minY = Math.min(0, ...allVals);
    const spanY = maxY - minY || 1;

    const xPos = (i) => padL + (i / Math.max(xLabels.length - 1, 1)) * plotW;
    const yPos = (v) => padT + plotH - ((v - minY) / spanY) * plotH;

    const svgNS = "http://www.w3.org/2000/svg";
    el.innerHTML = "";
    const tip = ensureTooltip(el);

    const svg = document.createElementNS(svgNS, "svg");
    svg.setAttribute("viewBox", `0 0 ${width} ${height}`);
    svg.setAttribute("width", "100%");
    svg.setAttribute("height", String(height));

    // Horizontal gridlines
    const ticks = 4;
    for (let t = 0; t <= ticks; t++) {
      const val = minY + (spanY * t) / ticks;
      const y = yPos(val);
      const line = document.createElementNS(svgNS, "line");
      line.setAttribute("x1", String(padL));
      line.setAttribute("x2", String(width - padR));
      line.setAttribute("y1", String(y));
      line.setAttribute("y2", String(y));
      line.setAttribute("stroke", "#e8e4dc");
      line.setAttribute("stroke-dasharray", t === 0 ? "none" : "3,3");
      svg.appendChild(line);

      const lbl = document.createElementNS(svgNS, "text");
      lbl.setAttribute("x", String(padL - 8));
      lbl.setAttribute("y", String(y + 4));
      lbl.setAttribute("text-anchor", "end");
      lbl.setAttribute("font-size", "11");
      lbl.setAttribute("fill", "#52606d");
      lbl.textContent = AppUtils.fmtCompactUSD(val);
      svg.appendChild(lbl);
    }

    // X axis labels every ~4 years
    xLabels.forEach((lbl, idx) => {
      if (idx === 0 || idx === xLabels.length - 1 || idx % 4 === 0) {
        const txt = document.createElementNS(svgNS, "text");
        txt.setAttribute("x", String(xPos(idx)));
        txt.setAttribute("y", String(height - 10));
        txt.setAttribute("text-anchor", "middle");
        txt.setAttribute("font-size", "11");
        txt.setAttribute("fill", "#52606d");
        txt.textContent = String(lbl);
        svg.appendChild(txt);
      }
    });

    // Series polylines
    seriesList.forEach((s) => {
      const pts = s.values.map((v, i) => `${xPos(i).toFixed(1)},${yPos(v).toFixed(1)}`).join(" ");
      const poly = document.createElementNS(svgNS, "polyline");
      poly.setAttribute("fill", "none");
      poly.setAttribute("stroke", s.color);
      poly.setAttribute("stroke-width", s.dashed ? "2" : "2.6");
      if (s.dashed) poly.setAttribute("stroke-dasharray", "6,4");
      poly.setAttribute("points", pts);
      svg.appendChild(poly);

      s.values.forEach((v, i) => {
        if (i === 0 || i === xLabels.length - 1 || i % 5 === 0) {
          const c = document.createElementNS(svgNS, "circle");
          c.setAttribute("cx", String(xPos(i)));
          c.setAttribute("cy", String(yPos(v)));
          c.setAttribute("r", "3.6");
          c.setAttribute("fill", s.color);
          c.style.cursor = "pointer";
          c.addEventListener("mousemove", (e) => {
            const box = el.getBoundingClientRect();
            tip.style.display = "block";
            tip.style.left = Math.min(e.clientX - box.left + 12, box.width - 190) + "px";
            tip.style.top = (e.clientY - box.top - 36) + "px";
            tip.innerHTML = `<strong>${s.name} (${xLabels[i]})</strong><br>${AppUtils.fmtUSD(v, true)}`;
          });
          c.addEventListener("mouseleave", () => {
            tip.style.display = "none";
          });
          svg.appendChild(c);
        }
      });
    });

    el.appendChild(svg);

    let leg = el.parentElement.querySelector(".chart-legend");
    if (leg) {
      leg.innerHTML = seriesList
        .map(
          (s) =>
            `<span class="legend-item"><span class="legend-swatch" style="background:${s.color}"></span>${s.name}</span>`
        )
        .join("");
    }
  }

  return {
    renderHorizontalBars,
    renderMultiLineChart,
  };
})();
