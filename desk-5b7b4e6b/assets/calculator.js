(function(){
  function fmt(v){
    var n = Math.round(v/10)*10;
    return '$' + n.toFixed(0).replace(/\B(?=(\d{3})+(?!\d))/g, ',');
  }
  function run(){
    var eq  = parseFloat(document.getElementById('eq').value)/100;
    var hp  = parseFloat(document.getElementById('hp').value)/100;
    var inf = parseFloat(document.getElementById('inf').value)/100;
    var yr  = parseFloat(document.getElementById('yr').value);
    var out = document.getElementById('calc-out');
    if(!isFinite(eq)||!isFinite(hp)||!isFinite(inf)||!isFinite(yr)||yr<=0){
      out.textContent='Check the inputs.'; return;
    }
    var keep = 3100000*Math.pow(1+hp, yr);
    var sell = 3100000*0.935*Math.pow(1+eq, yr);
    var d = keep - sell;
    out.textContent =
      'Live in it: ' + fmt(keep) + '  |  Sell it: ' + fmt(sell) +
      '  |  Difference: ' + fmt(Math.abs(d)) + ' (' + (d>0?'keeping ahead':'selling ahead') +
      ').  In today's money: ' + fmt(keep/Math.pow(1+inf,yr)) + ' against ' +
      fmt(sell/Math.pow(1+inf,yr)) + '.  Tax, rent and running costs are not included.';
  }
  [].forEach.call(document.querySelectorAll('.calc input'), function(el){
    el.addEventListener('input', run);
  });
  run();
})();
