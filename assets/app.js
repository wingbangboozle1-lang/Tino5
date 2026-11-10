// Simple canvas line chart (no external dependencies)
function drawLineChart(canvasId, series, labels, yLabel){
  var c = document.getElementById(canvasId);
  if(!c) return;
  var dpr = window.devicePixelRatio || 1;
  var w = c.clientWidth || 800, h = c.clientHeight || 280;
  c.width = w*dpr; c.height = h*dpr;
  var ctx = c.getContext('2d'); ctx.scale(dpr,dpr);
  var padL=70, padR=16, padT=16, padB=36;
  var iw=w-padL-padR, ih=h-padT-padB;
  var all=[]; series.forEach(function(s){ s.data.forEach(function(v){ all.push(v); }); });
  var min=Math.min.apply(null,all), max=Math.max.apply(null,all);
  if(min===max){ min-=1; max+=1; }
  var range=max-min; min-=range*0.08; max+=range*0.08;
  function X(i){ return padL + (i/(labels.length-1))*iw; }
  function Y(v){ return padT + (1-(v-min)/(max-min))*ih; }
  ctx.strokeStyle='#d9e1ec'; ctx.fillStyle='#5b6b82'; ctx.font='11px sans-serif';
  for(var g=0; g<=4; g++){
    var v=min+(max-min)*g/4, y=Y(v);
    ctx.beginPath(); ctx.moveTo(padL,y); ctx.lineTo(padL+iw,y); ctx.stroke();
    ctx.fillText('$'+Math.round(v/1000)+'k', 8, y+4);
  }
  labels.forEach(function(l,i){ if(i%2===0||i===labels.length-1) ctx.fillText(String(l), X(i)-12, h-12); });
  var colors=['#0e7c7b','#0f2a44','#b45309','#2563eb'];
  series.forEach(function(s,si){
    ctx.strokeStyle=colors[si%colors.length]; ctx.lineWidth=2.5; ctx.beginPath();
    s.data.forEach(function(v,i){ if(i===0) ctx.moveTo(X(i),Y(v)); else ctx.lineTo(X(i),Y(v)); });
    ctx.stroke();
    ctx.fillStyle=colors[si%colors.length];
    s.data.forEach(function(v,i){ ctx.beginPath(); ctx.arc(X(i),Y(v),3,0,Math.PI*2); ctx.fill(); });
  });
  ctx.fillStyle='#5b6b82'; ctx.fillText(yLabel||'', padL, 12);
}
document.addEventListener('DOMContentLoaded', function(){
  // Projections chart data (modelled, $ rounded to $10 in tables; chart uses same values)
  var years=[2026,2030,2035,2040,2045,2050,2055];
  var cupMkt3=[3100000,3489080,4044800,4689030,5435870,6301660,7305350];
  var sfMkt3=[1800000,2025920,2348590,2722660,3156310,3659030,4241820];
  var cupAss=[550540,595920,657940,726420,802030,885500,977670];
  var sfAss=[114250,123670,136540,150750,166440,183760,202890];
  drawLineChart('chart-market',[ {data:cupMkt3},{data:sfMkt3} ], years, 'Market value (3% scenario)');
  drawLineChart('chart-assessed',[ {data:cupAss},{data:sfAss} ], years, 'Assessed value (2%/yr Prop 13)');
});
