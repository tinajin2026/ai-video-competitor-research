const M=D.market;
const own=(obj,k)=>Object.prototype.hasOwnProperty.call(obj,k);
const positive=v=>Number.isFinite(v)?v>0?'up':v<0?'down':'':'';
const median=xs=>{const a=xs.filter(Number.isFinite).sort((a,b)=>a-b);return a.length?a.length%2?a[(a.length-1)/2]:(a[a.length/2-1]+a[a.length/2])/2:null;};
const ma=id=>M.products[id];
const segments=Object.entries(M.groups);
const groupName=id=>M.groups[ma(id).group].name;
let watched=new Set(),storageWorks=true;
try{const saved=JSON.parse(localStorage.getItem('competitor-watch-v1')||'[]');if(Array.isArray(saved))watched=new Set(saved.filter(id=>product(id)));}catch{storageWorks=false;}
const selected=new Set();let sortKey='visits',sortDirection=-1,actionType='all',activeView='overview';
const current=()=>D.products.filter(p=>($('segment').value==='all'||ma(p.id).group===$('segment').value)&&($('universe').value!=='watch'||watched.has(p.id)));
const eligible=rows=>rows.filter(p=>M.summary.ids.includes(p.id));
const chValue=(p,k,volume)=>{const share=traffic(p).traffic_sources[k];return Number.isFinite(share)?volume?share*metric(p.id).visits:share:null;};
const signed=v=>Number.isFinite(v)?(v>0?'+':'')+compact(v):'—';
const scopeBadge=p=>metric(p.id).scope==='site'?'':`<span class="scope-badge">${esc(scopeText[metric(p.id).scope])}</span>`;
const watchButton=p=>`<button class="watch-button" data-watch="${p.id}" aria-pressed="${watched.has(p.id)}" aria-label="${watched.has(p.id)?'取消关注':'关注'} ${esc(p.name)}">${watched.has(p.id)?'已关注':'关注'}</button>`;
const cmpCheck=p=>`<input type="checkbox" data-compare="${p.id}" aria-label="对比 ${esc(p.name)}" ${selected.has(p.id)?'checked':''}>`;
const emptyRow=n=>`<tr><td colspan="${n}" class="empty">当前筛选没有结果。请更换赛道、关注范围或清空搜索。</td></tr>`;
function toast(message){$('toast').textContent=message;$('toast').hidden=false;clearTimeout(toast.timer);toast.timer=setTimeout(()=>$('toast').hidden=true,3500);}
function saveWatch(){try{localStorage.setItem('competitor-watch-v1',JSON.stringify([...watched]));}catch{storageWorks=false;}if(!storageWorks)toast('浏览器未允许本地保存，关注列表仅在本次打开期间有效。');}
function matchProduct(p,q){return [p.name,p.traffic_domain,p.x_handle,p.homepage,...p.additional_domains].join(' ').toLowerCase().includes(q.toLowerCase());}
function currentSummary(){
 const rows=eligible(current()),history=M.months.map(month=>({month,visits:rows.reduce((sum,p)=>sum+(traffic(p).monthly_visits.find(x=>x.month===month)?.visits||0),0)}));
 const ms=rows.map(p=>metric(p.id).mom),last=history.at(-1)?.visits,prev=history.at(-2)?.visits;
 return {rows,history,visits:rows.length?last:null,mom:prev>0?last/prev-1:null,median:median(ms),up:ms.filter(v=>v>0).length,down:ms.filter(v=>v<0).length};
}
function renderOverview(){
 const s=currentSummary(),rows=current();
 $('market-stats').innerHTML=[['样本站点月访问',compact(s.visits),`${s.rows.length} 个固定主域`],['样本总量环比',change(s.mom),'按访问量加总'],['站点环比中位数',change(s.median),'每个站点等权'],['上升 / 下降',`${s.up} / ${s.down}`,'8 月相对 7 月']].map(([l,v,n])=>`<div><span>${l}</span><strong class="${l.includes('环比')?positive(l.includes('中位数')?s.median:s.mom):''}">${v}</strong><small>${n}</small></div>`).join('');
 const indexed=$('macro-mode').value==='median';
 const series=indexed?M.months.map(month=>({month,visits:median(s.rows.map(p=>{const hist=traffic(p).monthly_visits,base=hist.find(x=>x.month===M.months[0])?.visits,val=hist.find(x=>x.month===month)?.visits;return base>0?val/base*100:null;}))})):s.history;
 if(s.rows.length)drawLines({id:'macro-chart',series:[{name:indexed?'站点指数中位数':'固定样本总访问',history:series}],months:M.months,legend:'macro-legend',readout:'macro-readout',unit:indexed?'指数':'次'});else{$('macro-chart').innerHTML='<div class="empty">暂无可比站点。可在竞品对比中关注公司，或切回全部竞品。</div>';$('macro-readout').textContent='';$('macro-legend').textContent='';}
 $('sample-note').innerHTML=`${s.rows.length} 个固定站点，${rows.length-s.rows.length} 个母域、迁移或停服对象不计入总量。<button class="plain" data-method="sample">查看样本</button>`;
 const gs=segments.filter(([key])=>$('segment').value==='all'||key===$('segment').value).map(([key,g])=>{const ps=s.rows.filter(p=>ma(p.id).group===key);return {key,name:g.name,n:ps.length,total:rows.filter(p=>ma(p.id).group===key).length,value:median(ps.map(p=>metric(p.id).mom))};});
 $('segment-table').innerHTML=`<table><thead><tr><th>赛道</th><th class="number">可比 / 全部</th><th class="number">中位数</th></tr></thead><tbody>${gs.map(g=>`<tr><td><button class="name-link" data-segment="${g.key}">${g.name}</button></td><td class="number">${g.n} / ${g.total}</td><td class="number ${positive(g.value)}">${change(g.value)}</td></tr>`).join('')}</tbody></table>`;
 $('market-readout').textContent=s.rows.length?`${s.rows.length} 个站点中，${s.up} 个环比增长、${s.down} 个下降。样本总访问${s.mom>=0?'上升':'下降'} ${pct(Math.abs(s.mom))}，站点中位数为 ${change(s.median)}。`:'当前范围没有可比站点；其产品和动作资料仍可在其他视图查看。';
 renderHeatmap();renderMovers();
}
function renderHeatmap(){
 const mode=$('heat-metric').value,rows=current().sort((a,b)=>Number(metric(a.id).scope!=='site')-Number(metric(b.id).scope!=='site')||metric(b.id).visits-metric(a.id).visits);
 $('market-heatmap').innerHTML=`<table><thead><tr><th>竞品 / 统计口径</th><th>赛道</th>${M.months.map(m=>`<th class="number">${m.slice(2)}</th>`).join('')}<th class="number">近 3 月均值变化</th><th>动作</th></tr></thead><tbody>${rows.map(p=>{const h=traffic(p).monthly_visits;return `<tr><td>${nameButton(p.id)} ${scopeBadge(p)}</td><td class="muted">${esc(groupName(p.id))}</td>${M.months.map(month=>{const v=h.find(x=>x.month===month)?.visits;const i=h.findIndex(x=>x.month===month),prev=h[i-1];const date=new Date(month+'-01T00:00:00Z');date.setUTCMonth(date.getUTCMonth()-1);const growth=prev?.month===date.toISOString().slice(0,7)&&prev.visits>0?v/prev.visits-1:null;return `<td class="number heat-cell ${mode==='growth'?positive(growth):''}" style="${mode==='growth'&&Number.isFinite(growth)?`background:rgba(${growth>0?'160,202,146':'238,96,24'},${Math.min(.25,Math.abs(growth)*.7)})`:''}">${mode==='visits'?compact(v):change(growth)}</td>`;}).join('')}<td class="number ${positive(metric(p.id).rolling3)}">${change(metric(p.id).rolling3)}</td><td><button class="plain" data-company-actions="${p.id}">${ma(p.id).activity_count?ma(p.id).activity_count+' 条':'待补充'}</button></td></tr>`;}).join('')||emptyRow(10)}</tbody></table>`;
}
function renderMovers(){
 const key=$('mover-metric').value,rows=eligible(current()),value=p=>key==='delta'?ma(p.id).delta:metric(p.id).mom;
 ['up','down'].forEach(dir=>{const list=rows.filter(p=>dir==='up'?value(p)>0:value(p)<0).sort((a,b)=>dir==='up'?value(b)-value(a):value(a)-value(b)).slice(0,5),max=Math.max(1,...list.map(p=>Math.abs(value(p))));
 $('movers-'+dir).innerHTML=list.map(p=>`<button class="rank-row" data-detail="${p.id}"><span>${esc(p.name)}</span><span class="bar-track"><span class="bar-fill ${dir}" style="display:block;width:${Math.abs(value(p))/max*100}%"></span></span><span class="rank-value ${dir}">${key==='delta'?signed(value(p)):change(value(p))}</span></button>`).join('')||'<p class="empty">该方向暂无站点。</p>';});
}
function competitorRows(){
 const q=$('competitor-search').value.trim(),scope=$('competitor-scope').value,growth=$('growth-filter').value;
 return current().filter(p=>matchProduct(p,q)&&(scope==='all'||metric(p.id).scope===scope)&&(growth==='all'||growth==='up'&&metric(p.id).mom>0||growth==='down'&&metric(p.id).mom<0||growth==='both'&&metric(p.id).mom>0&&metric(p.id).rolling3>0||growth==='rebound'&&metric(p.id).mom>0&&metric(p.id).rolling3<0)).sort((a,b)=>{
 const scopeOrder=Number(metric(a.id).scope!=='site')-Number(metric(b.id).scope!=='site');if(scopeOrder)return scopeOrder;
 const value=p=>sortKey==='delta'?ma(p.id).delta:sortKey==='paid'?traffic(p).traffic_sources.social_paid:sortKey==='name'?p.name:metric(p.id)[sortKey];const av=value(a),bv=value(b);return typeof av==='string'?sortDirection*av.localeCompare(bv):av==null?1:bv==null?-1:sortDirection*(av-bv);});
}
function renderCompetitors(){
 const cols=[['name','竞品 / 主域'],['visits','8 月访问'],['mom','环比'],['delta','访问增减'],['rolling3','近 3 月均值'],['paid','付费社交占比']];
 $('competitor-head').innerHTML=`<tr><th>对比</th><th>关注</th>${cols.map(([key,name])=>`<th aria-sort="${sortKey===key?sortDirection===-1?'descending':'ascending':'none'}"><button data-sort="${key}" class="sort-button">${name}${sortKey===key?sortDirection===-1?' ↓':' ↑':''}</button></th>`).join('')}<th>增长动作</th></tr>`;
 const rows=competitorRows();$('competitor-count').textContent=rows.length+' 家 · 特殊口径列于表尾';
 $('competitor-rows').innerHTML=rows.map(p=>{const m=metric(p.id);return `<tr><td>${cmpCheck(p)}</td><td>${watchButton(p)}</td><td>${nameButton(p.id)} ${scopeBadge(p)}<span class="domain">${esc(p.traffic_domain)}${ma(p.id).small_base?' · 小基数':''}</span></td><td class="number">${num(m.visits)}</td><td class="number ${positive(m.mom)}">${change(m.mom)}</td><td class="number ${positive(ma(p.id).delta)}">${signed(ma(p.id).delta)}</td><td class="number ${positive(m.rolling3)}">${change(m.rolling3)}</td><td class="number">${pct(traffic(p).traffic_sources.social_paid)}</td><td><button class="plain" data-company-actions="${p.id}">${ma(p.id).activity_count} 条</button></td></tr>`;}).join('')||emptyRow(9);
 renderCompare();
}
function renderCompare(){
 const ids=[...selected];$('compare-selection').innerHTML=ids.map(id=>`<button data-remove-compare="${id}">${esc(product(id).name)} · 移除</button>`).join('');$('compare-empty').hidden=!!ids.length;$('compare-visual').hidden=!ids.length;if(!ids.length)return;
 const months=[...new Set(ids.flatMap(id=>traffic(product(id)).monthly_visits.map(x=>x.month)))].sort().slice(-Number($('compare-period').value));
 drawLines({id:'compare-chart',series:ids.map(id=>({name:product(id).name,history:traffic(product(id)).monthly_visits})),months,indexed:$('compare-mode').value==='index',legend:'compare-legend',readout:'compare-readout',table:'compare-data'});
 const rows=[['8 月访问',id=>num(metric(id).visits)],['8 月环比',id=>change(metric(id).mom)],['近 3 月均值变化',id=>change(metric(id).rolling3)],['自然搜索占比',id=>pct(traffic(product(id)).traffic_sources.search_organic)],['付费搜索占比',id=>pct(traffic(product(id)).traffic_sources.search_paid)],['付费社交占比',id=>pct(traffic(product(id)).traffic_sources.social_paid)],['当前动作记录',id=>`${ma(id).activity_count} 条`],['口径',id=>scopeText[metric(id).scope]]];
 $('compare-metrics').innerHTML=`<table><thead><tr><th>指标</th>${ids.map(id=>`<th>${esc(product(id).name)}</th>`).join('')}</tr></thead><tbody>${rows.map(([label,fn])=>`<tr><td>${label}</td>${ids.map(id=>`<td class="number">${fn(id)}</td>`).join('')}</tr>`).join('')}</tbody></table>`;
}
function renderMigration(){const id=$('migration-product').value,rows=A.migrations[id];drawLines({id:'migration-chart',series:rows.map(x=>({name:x.domain,history:x.history})),months:M.months,legend:'migration-legend',readout:'migration-readout'});$('migration-note').innerHTML='新旧域分别统计，不相加。'+rows.map(x=>evidenceLink(x.source,x.domain)).join(' · ');}
