
function num(id,d){var v=parseFloat(document.getElementById(id).value);return isNaN(v)?d:v;}
function fmt(x){return '$'+(Math.round(x/10)*10).toLocaleString();}
function calcBreak(){
 var pav=num('pav',3100000), g=num('g',4.5)/100, yrs=num('yrs',19);
 var rent=num('rent',0), cost=num('cost',250), pret=num('pret',6)/100;
 var fut=pav*Math.pow(1+g,yrs);
 var annualRent=rent*12, annualCost=cost*12, netRent=annualRent-annualCost;
 var keepNet=netRent/pret; // perpetuity-ish of net rent vs portfolio
 var sellInv=fut; // proceeds invested
 var el=document.getElementById('res');
 el.innerHTML='Property A in '+yrs+' yrs ≈ '+fmt(fut)+'. Net annual rent ≈ '+fmt(netRent)+'. Break-even: keep beats sell when net rent after carrying cost exceeds after-tax portfolio return on the sale proceeds. Test your own inputs.';
}
function calcPhase(){
 var proceeds=num('proceeds',3000000), ty=num('ty',3.7)/100, hold=num('hold',30);
 var treasury=proceeds*Math.pow(1+ty/12,hold);
 var el=document.getElementById('pres');
 el.innerHTML='After '+hold+' months at '+Math.round(ty*100)/100+'%: ≈ '+fmt(treasury)+' (Treasury hold). Then phase into equities over ~12 months (e.g. 25% per quarter).';
}
