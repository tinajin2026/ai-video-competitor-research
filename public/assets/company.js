const $=id=>document.getElementById(id);const num=v=>Number.isFinite(v)?v.toLocaleString('en-US',{maximumFractionDigits:0}):'—';const compact=v=>v>=1e8?(v/1e8).toFixed(1)+'亿':v>=1e4?(v/1e4).toFixed(1)+'万':num(v);const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));const palette=['#a0ca92','#ee6018','#eee'];const patterns=['','5 4','2 4'];
function niceMax(value){const exponent=10**Math.floor(Math.log10(Math.max(1,value)));return Math.ceil(value/exponent)*exponent;}
function drawLines({id,series,months,indexed=false,legend,readout,table,unit='次'}){
 const host=$(id),W=Math.max(280,host.clientWidth),H=280,L=W<440?46:60,R=18,T=18,B=36;
 const valueLabel=v=>unit==='指数'?(Number.isFinite(v)?v.toFixed(1):'—'):num(v);
 const values=series.map(s=>{const base=s.history.find(x=>x.month===months[0])?.visits;return months.map(m=>{const raw=s.history.find(x=>x.month===m)?.visits;return {raw,value:indexed?(Number.isFinite(raw)&&base>0?raw/base*100:null):raw};});});
 const max=niceMax(Math.max(1,...values.flat().map(v=>v.value||0))*1.08);
 const x=i=>L+i*(W-L-R)/Math.max(1,months.length-1),y=v=>H-B-v/max*(H-B-T);
 let svg=`<svg viewBox="0 0 ${W} ${H}" role="group" aria-label="${indexed?'窗口首月归一为100的':unit==='指数'?'站点指数中位数':'月访问次数'}趋势；聚焦月份可读精确值">`;
 for(let i=0;i<=4;i++){const v=max*i/4;svg+=`<line class="grid-line" x1="${L}" x2="${W-R}" y1="${y(v)}" y2="${y(v)}"/><text x="${L-8}" y="${y(v)+4}" text-anchor="end">${indexed?num(v):compact(v)}</text>`;}
 const tickIds=W<440?[0,Math.floor((months.length-1)/2),months.length-1]:months.map((m,i)=>i).filter(i=>months.length<=6||i%3===0||i===months.length-1);
 tickIds.forEach(i=>svg+=`<text x="${x(i)}" y="${H-10}" text-anchor="middle">${months[i].slice(2)}</text>`);
 series.forEach((s,j)=>{let pen=false,path='';values[j].forEach((v,i)=>{if(!Number.isFinite(v.value)){pen=false;return;}path+=`${pen?'L':'M'}${x(i)},${y(v.value)} `;pen=true;});svg+=`<path d="${path}" stroke="${palette[j%8]}" stroke-dasharray="${patterns[j%8]}" stroke-width="2" fill="none"/>`;values[j].forEach((v,i)=>{if(Number.isFinite(v.value))svg+=`<circle cx="${x(i)}" cy="${y(v.value)}" r="2.5" fill="${palette[j%8]}"/>`;});});
 months.forEach((month,i)=>{const step=(W-L-R)/(months.length-1);const text=series.map((s,j)=>`${s.name} ${valueLabel(values[j][i].raw)}${unit}`).join('；');svg+=`<rect class="chart-hit" tabindex="0" x="${Math.max(L,x(i)-step/2)}" y="${T}" width="${i===0||i===months.length-1?step/2:step}" height="${H-B-T}" data-month-index="${i}" aria-label="${month}：${esc(text)}"><title>${esc(month+' '+text)}</title></rect>`;});
 host.innerHTML=svg+'</svg>';
 const show=i=>{$(readout).innerHTML=`<span>${months[i]}</span> · `+series.map((s,j)=>`<span style="color:${palette[j%8]}">${esc(s.name)} ${indexed&&Number.isFinite(values[j][i].value)?values[j][i].value.toFixed(1)+' / ':''}${valueLabel(values[j][i].raw)}${unit}</span>`).join(' · ');};
 host.querySelectorAll('[data-month-index]').forEach(el=>['pointerenter','pointerdown','focus'].forEach(event=>el.addEventListener(event,()=>show(Number(el.dataset.monthIndex)))));
 show(months.length-1);
 $(legend).innerHTML=series.map((s,j)=>`<span><i class="legend-line" style="border-color:${palette[j%8]};border-top-style:${patterns[j%8]?'dashed':'solid'}"></i>${esc(s.name)}</span>`).join('');
 if(table)$(table).innerHTML=`<table><thead><tr><th>月份 · 访问次数</th>${series.map(s=>`<th class="number">${esc(s.name)}</th>`).join('')}</tr></thead><tbody>${months.map((m,i)=>`<tr><td>${m}</td>${series.map((s,j)=>`<td class="number">${num(values[j][i].raw)}</td>`).join('')}</tr>`).join('')}</tbody></table>`;
}

const C=JSON.parse($('company-data').textContent);
function drawCompany(){const hist=C.history.slice(-Number($('trend-period').value));drawLines({id:'company-chart',series:[{name:C.domain,history:hist}],months:hist.map(x=>x.month),legend:'company-legend',readout:'company-readout'});if(C.migrations.length)drawLines({id:'migration-chart',series:C.migrations.map(s=>({name:s.domain,history:s.history})),months:hist.map(x=>x.month),legend:'migration-legend',readout:'migration-readout'});}
$('trend-period').addEventListener('change',drawCompany);$('company-switch').addEventListener('change',e=>location.href=e.target.value);
$('copy-link').addEventListener('click',async()=>{const button=$('copy-link');try{await navigator.clipboard.writeText(location.href);button.textContent='已复制';}catch{button.textContent='请复制地址栏链接';}setTimeout(()=>button.textContent='复制本页链接',4000);});
let timer;window.addEventListener('resize',()=>{clearTimeout(timer);timer=setTimeout(drawCompany,120);});drawCompany();
