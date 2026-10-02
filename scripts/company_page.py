"""One complete HTML dossier per product, including explicit evidence boundaries."""
import statistics
from html_parts import E,num,pct,change,tone,link,table,section,shell,json_script
from research import derive,SCOPES

def render_company(d,p,editorial,posts):
 pid=p['id'];m=d['analysis']['metrics'][pid];mp=d['market']['products'][pid];t=p['domain_data']['traffic'];o=t['overview'];r=derive(d,p);ed=editorial[pid]
 activities=[a for a in d['market']['activities'] if a['product_id']==pid];root='../../'
 def source(path,label='数据文件'):
  return f'<a href="{root}{E(path)}">{E(label)}</a>' if path else ''
 def company(x):return f'<a href="../{x["id"]}/index.html">{E(x["name"])}</a>'
 options=''.join(f'<option value="../{x["id"]}/index.html" {"selected" if x["id"]==pid else ""}>{E(x["name"])}</option>' for x in d['products'])
 body=f'<div class="breadcrumbs"><a href="{root}companies/index.html">全部竞品</a><span>/ {E(r["group"]["name"])}</span><label class="switch-company">切换竞品 <select id="company-switch">{options}</select></label></div>'
 body+=f'<div class="dossier-heading"><div><h1>{E(p["name"])}</h1><p>{E(m["profile"])}</p></div><div class="source-links">{link(p["homepage"],"官网")}{link("https://x.com/"+p["x_handle"],"@"+p["x_handle"]) if p["x_handle"] else ""}<button id="copy-link">复制本页链接</button><a class="button" href="{root}data/companies/{pid}.json" download>下载本公司数据</a></div></div>'
 body+=f'<p class="scope-line"><span class="scope-badge">{SCOPES[m["scope"]]}</span> {E(p["traffic_domain"])} · {E(p["scope_note"])}</p>'
 nav=[('portrait','增长画像'),('acquisition','获客与搜索'),('product','产品与动作'),('implications','实践与跟踪'),('social','X 动态'),('sources','来源')]
 body+='<nav class="chapter-nav" aria-label="本页章节">'+''.join(f'<a href="#{id}">{label}</a>' for id,label in nav)+'</nav>'
 label='母域背景访问' if m['scope']=='mixed' else '当前域访问'
 body+='<div class="stats-strip">'+''.join(f'<div><span>{E(k)}</span><strong class="{tone(val) if fmt=="change" else ""}">{change(val) if fmt=="change" else num(val)}</strong><small>{E(note)}</small></div>' for k,val,fmt,note in [(label,m['visits'],'num','2026-08 · 访问次数估算'),('月环比',m['mom'],'change','8 月 / 7 月 − 1'),('近三月均值变化',m['rolling3'],'change','6—8 月 / 3—5 月 − 1'),('月访问增减',mp['delta'],'num','8 月减 7 月')])+'</div>'
 hist=t['monthly_visits'];first=min(hist,key=lambda x:x['month']);peak=r['peak']
 reading=f'观测窗口从 {first["month"]} 的 {num(first["visits"])} 次到 2026-08 的 {num(m["visits"])} 次，变化 {change(r["period_change"])}。窗口最高点为 {peak["month"]} 的 {num(peak["visits"])} 次，当前相对最高点 {change(r["drawdown"])}。'
 thesis=f'<div class="research-thesis"><h2>{E(ed["thesis"])}</h2><span class="status-label">{E(r["stage"])}</span><p>{E(reading)}</p><p>{E(ed["focus"])}</p></div>'
 chart='<div class="surface"><div class="section-title"><h2>访问轨迹</h2><select id="trend-period" aria-label="趋势时间范围"><option value="12">近 12 个月</option><option value="6">近 6 个月</option></select></div><div id="company-chart" class="chart"></div><div id="company-readout" class="readout"></div><div id="company-legend" class="chart-legend"></div></div>'
 body+=f'<section id="portrait" class="portrait-grid">{thesis}{chart}</section>'
 rows=[[E(x['month']),num(x['visits']),change(next((c['change'] for c in r['changes'] if c['month']==x['month']),None))] for x in hist]
 body+='<details class="inline-details"><summary>逐月访问与环比精确值 · '+source(p['domain_data']['traffic_evidence'],'下载来源')+'</summary>'+table(['月份','访问估算','月环比'],rows)+'</details>'
 if m['scope']=='migration':
  body+=section('migration','新旧域分别观察','<div id="migration-chart" class="chart"></div><div id="migration-readout" class="readout"></div><div id="migration-legend" class="chart-legend"></div>','迁移期不相加、不计算跨域净用户；新域增长可能包含迁移。')
 peers=r['peers'];peerlist=[p,*sorted(peers,key=lambda q:-d['analysis']['metrics'][q['id']]['visits'])]
 if m['scope']=='site' and peers:
  med=statistics.median(d['analysis']['metrics'][q['id']]['mom'] for q in peers)
  rank=1+sum(d['analysis']['metrics'][q['id']]['visits']>m['visits'] for q in peers)
  peer_read=f'<p class="section-lead">在同赛道 {len(peers)+1} 个可比主域中，当前访问规模第 {rank}；本公司环比 {change(m["mom"])}，其余同行中位数 {change(med)}，相差 {(m["mom"]-med)*100:+.2f} 个百分点。当前连续上升 {m["up_streak"]} 个月（0 表示本月未延续上升）。</p>'
  pr=[]
  for x in peerlist:
   xm=d['analysis']['metrics'][x['id']];xo=x['domain_data']['traffic']['overview'];pr.append([company(x),num(xm['visits']),change(xm['mom']),pct(xo['bounce_rate']),f'{xo["pages_per_visit"]:.2f}',num(xo['time_on_site_seconds'])+' 秒'])
  body+=section('peers','在同类站点中的位置',peer_read+table(['竞品','8 月访问','月环比','跳出率','页 / 次','时长 / 次'],pr)+f'<p class="source-note">本组除自身外有 {len(peers)} 家固定主域。不同产品使用路径仍有差异，时长与跳出率不作留存或付费代理。</p><a href="{root}index.html?compare={pid},{",".join(x["id"] for x in peers[:5])}#competitors">在工作台比较这些公司</a>')
 else:
  reason='当前对象属于特殊统计口径，不参与同行效率排名。' if m['scope']!='site' else '同赛道暂无其他符合固定主域口径的对象，不计算单家公司组成的同行基准。'
  body+=f'<p class="context-line">{reason}</p>'
 # Channels preserve raw shares and show calculated volume beside each component.
 maxshare=max(c['share'] or 0 for c in r['channels']) or 1
 channels=table(['渠道','占全站','折算访问'],[[E(c['name']),f'<div class="channel-cell"><span class="bar-track"><span class="bar-fill primary" style="display:block;width:{(c["share"] or 0)/maxshare*100:.1f}%"></span></span><span>{pct(c["share"])}</span></div>',num(c['visits'])] for c in r['channels']])
 paid=t['traffic_sources'].get('social_paid');organic=t['traffic_sources'].get('search_organic');top=r['channels'][0]
 channel_read=f'最大的归类来源为{top["name"]}（{pct(top["share"])}，约 {num(top["visits"])} 次）；自然搜索 {pct(organic)}，付费社交 {pct(paid)}。'
 keywords=table(['关键词样本','需求类型','月搜索量','CPC / USD'],[[E(k['name']),E(k['type']),num(k['volume']),f'{k["cpc"]:.2f}' if k.get('cpc') is not None else '—'] for k in r['keywords']])
 body+=section('acquisition','获客与搜索',f'<p class="section-lead">{channel_read}</p><div class="two-columns"><div>{channels}<p class="source-note">折算访问 = 当月全站估算 × 渠道份额；子项与 Search / Social 合计不重复相加。Direct 不等于留存，付费社交不等于预算。</p></div><div>{keywords}<p class="source-note">{len(r["keywords"])} 个词的样本中，{r["brand_count"]} 个含自有品牌/变体、{r["task_count"]} 个为通用任务。只统计词数，不推算品牌流量份额；月搜索量不是本站导流量。类型按词面归类，词面歧义和母域跨业务需结合原词判断。</p></div></div>')
 regions=t['top_regions'];covered=sum(x['share'] for x in regions)
 body+=section('audience','访问质量与地区',table(['地区样本','访问份额','折算访问'],[[E(x['name'])+' · '+E(x['country']),pct(x['share']),num(x['share']*m['visits'])] for x in regions])+f'<p class="source-note">列示地区覆盖 {pct(covered)}，其余地区未逐项返回。地域数据用于决定语言与地区实验，不推算购买力或收入。</p><div class="engagement-strip"><span>跳出率 <b>{pct(o["bounce_rate"])}</b></span><span>页 / 次 <b>{o["pages_per_visit"]:.2f}</b></span><span>时长 / 次 <b>{num(o["time_on_site_seconds"])} 秒</b></span></div><p>这些指标描述当前统计域。'+('官网正文可见的独立产品入口：'+' · '.join(link(u,u) for u in p['product_entry_links']) if p['product_entry_links'] else '当前公开快照未提取到足够明确的独立应用入口，不能据此认定主站与应用同域。')+'</p><p class="source-note">若营销页面与实际创作应用分域，较短会话可能包含正常跳转；目前没有跨域会话串联、注册、生成、D7 留存或付费转化数据。</p>')
 pr=r['price'];pg=next((x for x in p['pages'] if x['path']==pr.get('source')),None)
 pricing=f'<div class="pricing-readout"><div><span>{E(pr["plan"])}</span><strong>{E(pr["price"])}</strong></div><p>{E(pr["terms"])}</p>{link(pg["source"].get("resolved_url") or pg["source"].get("requested_url"),"官网价格依据") if pg else ""}</div>'
 acts=''
 for a in sorted(activities,key=lambda x:x.get('event_date') or '',reverse=True):
  date=(a.get('date_label') or '官方公布日期')+' '+a['event_date'] if a.get('event_date') else '2026-10-02 观察 · 发生日期未标注'
  acts+=f'<article class="action-record"><div><span class="mono">{E(date)}</span><span class="scope-badge">{E(d["market"]["activity_types"][a["type"]])}</span></div><h3>{E(a["title"])}</h3><p>{E(a["detail"])}</p><div class="source-links">{link(a["source_url"],"官方来源")}{source(a["source"],"研究摘记")}</div></article>'
 if not acts:acts='<p class="empty">'+('官网主页采集失败；不等于产品停服。' if pid=='haiper' else '官网正文不足，尚无足够依据提炼增长动作。')+'</p>'
 body+=section('product','产品、价格与增长动作',pricing+acts,'套餐条件来自 10 月 2 日采集；当前展示不等于最近新增。9—10 月动作不能解释 8 月流量。')
 experiment=f'<div class="experiment"><h3>值得测试的做法</h3><p>{E(ed["experiment"])}</p><h3>怎样判断是否有效</h3><p>{E(ed["measure"])}</p><h3>接下来跟踪</h3><p>{E(ed["watch"])}</p></div><p class="source-note">以上是基于已列证据提出的自身实验建议，不是竞品已实现效果。先采集同一任务、同一渠道的自身基线，再设成功门槛。</p>'
 body+=section('implications','把观察转成可验证的行动',experiment)
 if posts:
  social=''.join(f'<article class="action-record"><p class="source-note">{E(x["published_at"])} · 指标采集 {E(x["collected_at"])}</p><p>{E(x["text"])}</p>{link(x["url"],"查看 X 原帖")}<p class="source-note">'+ ' · '.join(E(k)+' '+num(v) for k,v in x['metrics'].items())+'</p></article>' for x in sorted(posts,key=lambda x:x['published_at'],reverse=True)[:50])
 else:social='<p class="empty">尚未接入 X 动态。这里将展示原帖、发布时间和各次采集的互动指标；当前不生成虚构动态或增长曲线。</p>'
 body+=section('social','X 动态',social+f'<p class="source-note">跟踪账号：{E("@"+p["x_handle"] if p["x_handle"] else "未确认独立账号；由后续账号映射维护")}</p><a href="{root}methodology/index.html#updates">数据更新格式</a>')
 sources=table(['已采集页面','状态','官网来源'],[[E(x['label']),E(x['status']),link(x['source'].get('resolved_url') or x['source'].get('requested_url'),'打开来源')] for x in p['pages']])
 body+=section('sources','来源与研究边界',sources+f'<p>{source(p["domain_data"]["traffic_evidence"],"流量来源数据")} · {source(p["domain_data"]["backlinks_evidence"],"外链样本")} · <a href="{root}data/companies/{pid}.json">全部公开数据</a></p><p class="source-note">流量来自 TabAPI 域名级第三方估算，未经竞品后台验证；官网陈述是产品方自报。公开版保留数据、来源及研究摘记，本地采集包保留原始响应。10 月 2 日重新请求全部 41 个根域，最新仍为 8 月。没有广告花费、独立用户、付费率和留存，因而不计算 ROAS、ARR 推估或综合健康分。</p>')
 payload={'product_id':pid,'domain':p['traffic_domain'],'history':hist,'migrations':d['analysis']['migrations'].get(pid,[])}
 extra=json_script('company-data',payload)+f'<script src="{root}assets/company.js"></script>'
 return shell(p['name']+' · 独立研究',body,2,extra)
