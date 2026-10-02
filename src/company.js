const C=JSON.parse($('company-data').textContent);
function drawCompany(){const hist=C.history.slice(-Number($('trend-period').value));drawLines({id:'company-chart',series:[{name:C.domain,history:hist}],months:hist.map(x=>x.month),legend:'company-legend',readout:'company-readout'});if(C.migrations.length)drawLines({id:'migration-chart',series:C.migrations.map(s=>({name:s.domain,history:s.history})),months:hist.map(x=>x.month),legend:'migration-legend',readout:'migration-readout'});}
$('trend-period').addEventListener('change',drawCompany);$('company-switch').addEventListener('change',e=>location.href=e.target.value);
$('copy-link').addEventListener('click',async()=>{const button=$('copy-link');try{await navigator.clipboard.writeText(location.href);button.textContent='已复制';}catch{button.textContent='请复制地址栏链接';}setTimeout(()=>button.textContent='复制本页链接',4000);});
let timer;window.addEventListener('resize',()=>{clearTimeout(timer);timer=setTimeout(drawCompany,120);});drawCompany();
