function activityRows(){
 const ids=new Set(current().map(p=>p.id)),pid=$('action-product').value,q=$('action-search').value.trim().toLowerCase(),time=$('action-time').value;
 return M.activities.filter(a=>ids.has(a.product_id)&&(pid==='all'||a.product_id===pid)&&(actionType==='all'||a.type===actionType)&&(time==='all'||time==='dated'&&a.event_date||time==='snapshot'&&!a.event_date)&&[a.title,a.detail,product(a.product_id).name].join(' ').toLowerCase().includes(q)).sort((a,b)=>(b.event_date||'').localeCompare(a.event_date||'')||product(a.product_id).name.localeCompare(product(b.product_id).name));
}
function activityTable(rows,compactMode=false){return `<table class="activity-table ${compactMode?'compact-activity':''}"><thead><tr><th>时间</th>${compactMode?'':'<th>竞品</th>'}<th>动作类型</th><th>具体动作</th><th>来源</th></tr></thead><tbody>${rows.map(a=>`<tr><td class="date-col">${a.event_date||'10/02 观察'}<span class="table-note">${a.event_date?esc(a.date_label||'官方公布日期'):'未标注发生日期'}</span></td>${compactMode?'':`<td>${nameButton(a.product_id)}<span class="table-note">8 月环比 ${change(metric(a.product_id).mom)}</span></td>`}<td>${esc(M.activity_types[a.type])}</td><td><button class="action-title" data-activity="${a.id}">${esc(a.title)}</button><p>${esc(a.detail)}</p></td><td><button class="plain" data-activity="${a.id}">查看原文</button></td></tr>`).join('')||emptyRow(compactMode?4:5)}</tbody></table>`;}
function renderActions(){
 const ps=current(),ids=new Set(ps.map(p=>p.id)),available=M.activities.filter(a=>ids.has(a.product_id)),rows=activityRows();
 $('action-type-bar').innerHTML=[['all','全部'],...Object.entries(M.activity_types)].map(([key,name])=>`<button data-action-type="${key}" aria-pressed="${key===actionType}">${esc(name)} <span>${key==='all'?available.length:available.filter(a=>a.type===key).length}</span></button>`).join('');
 $('action-count').textContent=`${rows.length} 条记录 · ${new Set(rows.map(a=>a.product_id)).size} 家`;
 const gaps=ps.filter(p=>!M.coverage[p.id]&&($('action-product').value==='all'||$('action-product').value===p.id));
 $('action-table').innerHTML=activityTable(rows)+(gaps.length?`<div class="gap-row">${gaps.map(p=>`${esc(p.name)}：${p.id==='haiper'?'官网正文抓取失败':'官网正文不足'}，暂无可核实的增长动作。`).join(' ')} ${gaps.map(p=>nameButton(p.id)).join(' · ')}</div>`:'');
 $('action-matrix').innerHTML=`<table><thead><tr><th>竞品</th>${Object.values(M.activity_types).map(n=>`<th>${esc(n)}</th>`).join('')}</tr></thead><tbody>${ps.map(p=>`<tr><td>${nameButton(p.id)}</td>${Object.keys(M.activity_types).map(type=>{const count=M.activities.filter(a=>a.product_id===p.id&&a.type===type).length;return `<td class="number">${count?`<button class="plain" data-action-cell="${p.id}" data-type="${type}">${count}</button>`:'—'}</td>`;}).join('')}</tr>`).join('')||emptyRow(11)}</tbody></table>`;
}
function channelRows(){const key=$('channel-key').value,volume=$('channel-measure').value==='volume';return current().sort((a,b)=>Number(metric(a.id).scope!=='site')-Number(metric(b.id).scope!=='site')||(chValue(b,key,volume)??-1)-(chValue(a,key,volume)??-1));}
function renderChannels(){
 const key=$('channel-key').value,volume=$('channel-measure').value==='volume',rows=channelRows(),max=Math.max(.001,...eligible(rows).map(p=>chValue(p,key,volume)||0));
 const peers=['direct','search_organic','search_paid','social_organic','social_paid'];
 $('channel-ranking').innerHTML=`<table><thead><tr><th>竞品</th><th>${esc(M.channels[key])} · ${volume?'折算访问量':'占全站'}</th>${peers.filter(k=>k!==key).map(k=>`<th class="number">${esc(M.channels[k])}</th>`).join('')}<th>主要地区</th><th>动作</th></tr></thead><tbody>${rows.map(p=>{const val=chValue(p,key,volume),region=traffic(p).top_regions[0];return `<tr><td>${nameButton(p.id)} ${scopeBadge(p)}</td><td><div class="channel-cell"><span class="bar-track"><span class="bar-fill primary" style="display:block;width:${Math.min(100,(val||0)/max*100)}%"></span></span><span>${volume?compact(val):pct(val)}</span></div></td>${peers.filter(k=>k!==key).map(k=>`<td class="number">${volume?compact(chValue(p,k,true)):pct(chValue(p,k,false))}</td>`).join('')}<td>${region?esc(region.country)+' '+pct(region.share):'—'}</td><td><button class="plain" data-channel-product="${p.id}">搜索 / 地区</button></td></tr>`;}).join('')||emptyRow(8)}</tbody></table>`;
 renderSearchRegions();
}
function renderSearchRegions(){
 const p=product($('channel-detail-product').value);if(!p){$('keyword-table').innerHTML='<p class="empty">当前范围没有竞品。</p>';$('region-table').innerHTML='';return;}
 const t=traffic(p);
 $('keyword-table').innerHTML=`<table><thead><tr><th>关键词样本</th><th class="number">月搜索量</th><th class="number">CPC / USD</th></tr></thead><tbody>${t.top_keywords.map(k=>`<tr><td>${esc(k.name)}</td><td class="number">${num(k.volume)}</td><td class="number">${Number.isFinite(k.cpc)?k.cpc.toFixed(2):'—'}</td></tr>`).join('')}</tbody></table><p class="source-note">上游关键词样本，不是关键词带来的站点访问量。</p>`;
 $('region-table').innerHTML=`<table><thead><tr><th>地区</th><th class="number">访问份额</th></tr></thead><tbody>${t.top_regions.map(r=>`<tr><td>${esc(r.name)} · ${esc(r.country)}</td><td class="number">${pct(r.share)}</td></tr>`).join('')}</tbody></table><p class="source-note">前列地区样本，非完整分布。${evidenceLink(p.domain_data.traffic_evidence,'原始流量数据')}</p>`;
}
function priceFor(p){
 const fresh=M.price_observations.find(x=>x.product_id===p.id);if(fresh)return fresh;
 const old=A.prices.find(x=>x.id===p.id);if(old)return {product_id:p.id,plan:old.plan,price:old.price,terms:old.billing+'；'+old.caveat,source:A.evidence.find(e=>e.id===old.evidence)?.path};
 const pg=p.pages.find(x=>x.kind==='pricing');return {product_id:p.id,plan:p.id==='sora'?'停服':pg?'计价资料':'未取得独立价目页',price:p.id==='sora'?'不适用':'未确认',terms:pg?.status==='limited'?'资料受限，未提取可靠价格。':p.id==='capcut'?'已取得价格说明文章，未取得统一套餐价。':p.id==='veo'?'模型介绍页未返回可确认的报价。':pg?'当前页面不足以形成可靠报价。':'保留为空。',source:pg?.path};
}
function renderProducts(){
 $('product-table').innerHTML=`<table class="product-table"><thead><tr><th>竞品</th><th>定位 / 主要任务</th><th>已观察到的增长方式</th><th>套餐与价格</th><th>购买条件</th><th>来源</th></tr></thead><tbody>${current().map(p=>{const pr=priceFor(p),types=[...new Set(M.activities.filter(a=>a.product_id===p.id).map(a=>M.activity_types[a.type]))];return `<tr><td>${nameButton(p.id)}<span class="table-note">${esc(groupName(p.id))}</span></td><td>${esc(metric(p.id).profile)}</td><td>${esc(types.join(' / ')||'暂无可核实记录')}<br><button class="plain" data-company-actions="${p.id}">查看动作</button></td><td><strong>${esc(pr.price)}</strong><span class="table-note">${esc(pr.plan)}</span></td><td>${esc(pr.terms)}</td><td>${pr.source?`<button class="plain" data-page="${esc(pr.source)}">价格原文</button>`:'—'}</td></tr>`;}).join('')||emptyRow(6)}</tbody></table>`;
}
function syncProductOptions(){
 ['action-product','channel-detail-product'].forEach(id=>{const el=$(id),old=el.value,all=id==='action-product';el.innerHTML=(all?'<option value="all">全部竞品</option>':'')+current().map(p=>`<option value="${p.id}">${esc(p.name)}</option>`).join('');if([...el.options].some(o=>o.value===old))el.value=old;});
}
function renderCurrent(){
 const ps=current();$('scope-count').textContent=`${ps.length} 家 · ${eligible(ps).length} 个可比主域`;
 if(activeView==='overview')renderOverview();if(activeView==='competitors')renderCompetitors();if(activeView==='actions')renderActions();if(activeView==='channels')renderChannels();if(activeView==='products')renderProducts();
}
function showView(name,focus=false){
 if(!['overview','competitors','actions','channels','products'].includes(name))name='overview';activeView=name;
 document.querySelectorAll('.view').forEach(el=>el.hidden=el.id!=='view-'+name);document.querySelectorAll('nav [role=tab]').forEach(el=>{const yes=el.dataset.view===name;el.setAttribute('aria-selected',String(yes));el.tabIndex=yes?0:-1;});
 history.replaceState(null,'','#'+name);renderCurrent();if(focus){$('main').focus({preventScroll:true});window.scrollTo({top:0,behavior:'instant'});}
}
function exportRows(){
 if(activeView==='actions')return activityRows().map(a=>({product:product(a.product_id).name,type:M.activity_types[a.type],event_date:a.event_date||'',date_type:a.event_date?(a.date_label||'官方公布日期'):'当前观察',observed:a.observed_at,title:a.title,detail:a.detail,source_url:a.source_url,source_file:a.source}));
 if(activeView==='products')return current().map(p=>({product:p.name,group:groupName(p.id),profile:metric(p.id).profile,...priceFor(p)}));
 const rows=activeView==='competitors'?competitorRows():activeView==='channels'?channelRows():current();
 return rows.map(p=>({product:p.name,domain:p.traffic_domain,group:groupName(p.id),scope:scopeText[metric(p.id).scope],month:'2026-08',visits:metric(p.id).visits,mom:metric(p.id).mom,delta:ma(p.id).delta,rolling3:metric(p.id).rolling3,...Object.fromEntries(Object.keys(M.channels).map(k=>[k,traffic(p).traffic_sources[k]])),...Object.fromEntries(traffic(p).monthly_visits.map(x=>[x.month,x.visits])),activity_count:ma(p.id).activity_count,traffic_source:p.domain_data.traffic_evidence}));
}
function downloadCSV(){
 const rows=exportRows();if(!rows.length){toast('当前筛选没有可导出的记录。');return;}
 const fields=[...new Set(rows.flatMap(Object.keys))],cell=v=>{let s=v==null?'':typeof v==='object'?JSON.stringify(v):String(v);if(typeof v==='string'&&/^[=+@\-\t\r]/.test(s))s="'"+s;return '"'+s.replace(/"/g,'""')+'"';};
 const csv='\uFEFF'+[fields,...rows.map(r=>fields.map(k=>r[k]))].map(row=>row.map(cell).join(',')).join('\r\n');const url=URL.createObjectURL(new Blob([csv],{type:'text/csv;charset=utf-8'}));const a=document.createElement('a');a.href=url;a.download=`竞品分析-${activeView}-2026-10-02.csv`;a.click();setTimeout(()=>URL.revokeObjectURL(url),10000);toast(`已导出 ${rows.length} 行，保留当前筛选及来源。`);
}
// Explicit assignment keeps global filters deterministic after reload.
$('segment').insertAdjacentHTML('beforeend',Object.entries(M.groups).map(([id,g])=>`<option value="${id}">${g.name} · ${g.ids.length} 家</option>`).join(''));
$('channel-key').innerHTML=Object.entries(M.channels).map(([k,n])=>`<option value="${k}">${n}</option>`).join('');$('channel-key').value='search_organic';syncProductOptions();showView(location.hash.slice(1));
function resetFilters(){$('segment').value='all';$('universe').value='all';$('competitor-search').value='';$('competitor-scope').value='all';$('growth-filter').value='all';$('action-product').value='all';$('action-time').value='all';$('action-search').value='';actionType='all';syncProductOptions();renderCurrent();}
$('reset-filters').addEventListener('click',resetFilters);$('export-current').addEventListener('click',downloadCSV);
['segment','universe'].forEach(id=>$(id).addEventListener('change',()=>{syncProductOptions();renderCurrent();}));
['macro-mode','heat-metric','mover-metric'].forEach(id=>$(id).addEventListener('change',renderOverview));
['competitor-scope','growth-filter'].forEach(id=>$(id).addEventListener('change',renderCompetitors));$('competitor-search').addEventListener('input',renderCompetitors);
['compare-period','compare-mode'].forEach(id=>$(id).addEventListener('change',renderCompare));$('clear-compare').addEventListener('click',()=>{selected.clear();renderCompetitors();});
['action-product','action-time'].forEach(id=>$(id).addEventListener('change',renderActions));$('action-search').addEventListener('input',renderActions);
['channel-key','channel-measure'].forEach(id=>$(id).addEventListener('change',renderChannels));$('channel-detail-product').addEventListener('change',renderSearchRegions);$('channel-open-detail').addEventListener('click',()=>renderDetail($('channel-detail-product').value));
$('migration-product').addEventListener('change',renderMigration);$('migration-chart').closest('details').addEventListener('toggle',e=>{if(e.target.open)renderMigration();});
document.addEventListener('click',e=>{
 const target=e.target.closest('button,[data-view]');if(!target)return;const d=target.dataset;
 if(d.view)showView(d.view,!target.closest('nav'));
 if(d.segment){$('segment').value=d.segment;syncProductOptions();renderCurrent();}
 if(d.watch){if(watched.has(d.watch))watched.delete(d.watch);else watched.add(d.watch);saveWatch();syncProductOptions();renderCurrent();}
 if(d.sort){if(sortKey===d.sort)sortDirection*=-1;else{sortKey=d.sort;sortDirection=d.sort==='name'?1:-1;}renderCompetitors();}
 if(d.removeCompare){selected.delete(d.removeCompare);renderCompetitors();}
 if(d.companyActions||d.actionCell){$('action-product').value=d.companyActions||d.actionCell;actionType=d.type||'all';$('action-time').value='all';$('action-search').value='';showView('actions',true);}
 if(d.actionType){actionType=d.actionType;renderActions();}
 if(d.channelProduct){$('channel-detail-product').value=d.channelProduct;renderSearchRegions();$('channel-detail-product').scrollIntoView({block:'center',behavior:'instant'});}
});
document.addEventListener('change',e=>{if(!e.target.matches('[data-compare]'))return;const id=e.target.dataset.compare;if(e.target.checked&&selected.size>=6){e.target.checked=false;toast('最多对比 6 家。请先移除一个已选对象。');return;}if(e.target.checked)selected.add(id);else selected.delete(id);renderCompare();$('compare-feedback').textContent=`已选 ${selected.size} 家；趋势与指标在表格下方。`;});
document.querySelector('nav').addEventListener('keydown',e=>{if(!['ArrowLeft','ArrowRight','Home','End'].includes(e.key))return;const tabs=[...document.querySelectorAll('nav button')],i=tabs.indexOf(document.activeElement);if(i<0)return;e.preventDefault();const n=e.key==='Home'?0:e.key==='End'?tabs.length-1:(i+(e.key==='ArrowRight'?1:-1)+tabs.length)%tabs.length;tabs[n].focus();showView(tabs[n].dataset.view);});
window.addEventListener('hashchange',()=>showView(location.hash.slice(1)));let resizeTimer;window.addEventListener('resize',()=>{clearTimeout(resizeTimer);resizeTimer=setTimeout(()=>{if(activeView==='overview')renderOverview();if(activeView==='competitors'){renderCompare();if($('migration-chart').closest('details').open)renderMigration();}if($('detail-dialog').open&&window.currentDetailId)drawDetailTrend(window.currentDetailId);},120);});
