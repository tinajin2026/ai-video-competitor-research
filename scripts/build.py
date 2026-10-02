"""Deterministic static build. No network, dependencies or credentials required."""
import json,re,shutil,csv,io
from pathlib import Path
from html_parts import E,num,pct,change,tone,link,table,section,shell
from research import derive,SCOPES
from company_page import render_company
R=Path(__file__).resolve().parents[1];O=R/'public';S=R/'src'
def write(path,text):
 f=O/path;f.parent.mkdir(parents=True,exist_ok=True);f.write_text(text)
def js(data):return json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')
def directory(d,ed):
 rows=''
 for p in d['products']:
  pid=p['id'];m=d['analysis']['metrics'][pid];r=derive(d,p);group=d['market']['products'][pid]['group']
  rows+=f'<tr data-company="{pid}" data-group="{group}" data-scope="{m["scope"]}" data-visits="{m["visits"]}" data-mom="{m["mom"]}"><td><a class="company-name" href="../competitors/{pid}/index.html">{E(p["name"])}</a><span class="meta">{E(p["traffic_domain"])}</span><span class="scope-badge">{SCOPES[m["scope"]]}</span></td><td><span class="thesis">{E(ed[pid]["thesis"])}</span><span class="meta">{E(r["stage"])}</span></td><td class="number">{num(m["visits"])}<span class="meta {tone(m["mom"])}">月环比 {change(m["mom"])}</span></td><td><a href="../competitors/{pid}/index.html#acquisition">获客分析</a><br><a href="../competitors/{pid}/index.html#product">动作与价格</a><br><a href="../competitors/{pid}/index.html#implications">实践与跟踪</a></td></tr>'
 groups=''.join(f'<option value="{k}">{v["name"]}</option>' for k,v in d['market']['groups'].items())
 body=f'<h1>37 家竞品，37 份独立研究</h1><p class="directory-intro">从行业总览发现变化，再进入公司研究页：看增长是否持续、访问来自哪里、产品如何承接需求，以及哪些做法值得用自己的数据验证。每家公司都有可收藏和分享的独立地址。</p><div class="directory-toolbar"><label>搜索<input id="directory-search" type="search" placeholder="竞品、域名或研究主题"></label><label>赛道<select id="directory-group"><option value="all">全部赛道</option>{groups}</select></label><label>排序<select id="directory-sort"><option value="original">清单顺序</option><option value="visits">访问量</option><option value="mom">月环比</option></select></label><span id="directory-count" role="status">37 家</span></div><div class="table-scroll"><table class="directory-table"><thead><tr><th>竞品</th><th>本公司研究重点</th><th class="number">8 月域名访问估算</th><th>直接进入章节</th></tr></thead><tbody id="directory-rows">{rows}</tbody></table></div><p id="directory-empty" class="empty" hidden>没有符合条件的公司。请清空搜索或切换赛道。</p><p class="source-note">排序时特殊口径置于表尾；母域数字不代表单一产品。所有公司保留完整研究入口。</p>'
 return shell('竞品研究',body,1,'<script src="../assets/directory.js"></script>')

def methodology():
 body='''<article class="method-body"><h1>数据、证据与更新方式</h1><p>本研究站覆盖 37 个产品对象、41 个根域。网站访问来自 TabAPI 的第三方估算；官网动作与价格来自官方页面。流量月份为 2026-08，官网采集日期为 2026-10-02。两个时间窗口分别呈现。</p>

<h2>如何使用</h2><p>行业总览看固定样本和赛道分化；竞品研究进入每家公司独立 HTML；公司页依次拆解增长、渠道、关键词、地区、产品动作和可验证实验。对比页可自由选 2—6 家，导出当前筛选。证据链接可返回官网或下载公开研究数据。</p>

<h2>为什么最新仍是 8 月</h2><p>10 月 2 日重新请求了全部 41 个根域，41 个 HTTP 200，overview.month 全部为 2026-08；最近三个月返回 6、7、8 月。尚未取得 9 月和 10 月，不能把重新请求日期当作统计月份。TabAPI 官方接口只暴露 trailing months（3—12），没有指定月份或实时查询参数。<a href="../data/freshness.json">逐域重新请求记录</a> · <a href="https://tabapi.com/docs#traffic">官方文档</a></p>
<h2>我们实际测量什么</h2><p>访问次数是会话级域名估算，不是用户、付费人数或收入。跳出率、时长、访问页数不等于留存。Direct 可能包含品牌访问、书签、未归因分享等，不能据此断言品牌忠诚。渠道折算访问 = 全站访问估算 × 同月份额，不是投放花费。</p>
<p>关键词字段 volume 是词的月搜索量，不是给本站带来的访问。品牌、第三方品牌与通用任务按词面标注，样本词数不是流量份额。地区只返回前列样本，不代表完整市场分布。单个地区份额不推算 ARPU。</p>

<h2>固定样本与计算</h2><p>宏观使用 3—8 月持续有数据的 27 个主域，按域名去重。排除共享母域、迁移域和停服对象；这些公司仍有独立研究页。样本含综合创作与开发者业务，因此不是整个 AI 视频市场规模。</p>
<ul><li>月环比 = 8 月访问 / 7 月访问 − 1。</li><li>近三月均值变化 = 6—8 月平均访问 / 3—5 月平均访问 − 1。</li><li>指数首月 = 100；缺月不插值。Runway、Kling 新旧域分别展示。</li><li>同行基准使用同赛道合格主域，且移除当前公司；不跨赛道生成健康分。</li></ul>
<h2>已知缺口</h2><p>Happy Horse 官网正文不足；Haiper 主页抓取失败。均保留流量和身份信息，但不补造增长动作。没有完整广告素材库、广告花费、竞品转化、留存或付费数据。Higgsfield 与 Topview 重点投放研究仍需广告主体与素材原帖证据，不能将同名 TikTok TopView 广告位算入 Topview。</p>
<p>60 条官网动作覆盖 35 家；没有日期的记录只标为“10 月 2 日观察”。官网自报营收与客户效果不属于独立验证。9—10 月动作不能归因为 8 月增长。具体分析将观察事实与我们建议的实验分开。</p>

<h2 id="updates">接入 Grok BOT 与 GitHub</h2><p>站点已拆为数据、分析规则和页面三个层次。每家公司有稳定 product_id、独立 URL 与 JSON。Grok BOT 将 X 原帖写为 JSONL，经校验脚本处理后，重新构建即可更新页面；无需改 HTML。当前尚未连接 Grok、X API 或定时任务。</p>
<p>公开站点没有上传写入接口。机器人在受控 GitHub 仓库内提交 data/inbox/*.jsonl，由工作流校验、构建并发布 GitHub Pages。当前 Sites 链接是本次发布快照，与 GitHub Pages 是两个独立部署目标；建库后若采用 Pages，以 Pages 链接作为持续更新地址。</p>
<p>数据格式、幂等规则、运行命令和最小权限建议随源码包提供。X 账号初始映射来自用户清单；接入前应核对官方身份，复用 OpenAI 等公司账号时必须提供产品相关性依据。</p>

<h2>可下载数据</h2><p><a href="../data/snapshot.json">公开研究快照 JSON</a> · <a href="../data/companies.csv">公司指标 CSV</a> · <a href="../data/monthly-visits.csv">逐月访问 CSV</a> · <a href="../data/growth-actions.csv">增长动作 CSV</a></p>
<p>原始采集响应、付费 API key、共享对话正文与本地绝对路径不发布。公开数据保留来源地址、观察时间和计算口径。完整原始采集包保存在本地。</p>
</article>'''
 return shell('数据与方法',body,1,active='method')

def main():
 d=json.loads((R/'data/snapshot.json').read_text());ed=json.loads((R/'data/editorial.json').read_text());x=json.loads((R/'data/x-posts.json').read_text())
 assert set(ed)=={p['id'] for p in d['products']}
 O.mkdir(exist_ok=True);(O/'assets').mkdir(exist_ok=True)
 fonts=''.join("@font-face{font-family:'"+family+"';src:url('"+filename+"') format('woff2');font-weight:400;font-display:swap;}" for family,filename in [('Geist','Geist-Regular.woff2'),('Geist Mono','GeistMono-Regular.woff2')])
 write('assets/dashboard.css',(S/'dashboard.css').read_text().replace('__FONT_FACES__',fonts))
 for f in (S/'assets').glob('*.woff2'):shutil.copyfile(f,O/'assets'/f.name)
 for name in ['research.css','directory.js']:shutil.copyfile(S/name,O/'assets'/name)
 chart=(S/'charts.js').read_text();chartfn=chart[chart.index('function niceMax'):]
 shared="const $=id=>document.getElementById(id);const num=v=>Number.isFinite(v)?v.toLocaleString('en-US',{maximumFractionDigits:0}):'—';const compact=v=>v>=1e8?(v/1e8).toFixed(1)+'亿':v>=1e4?(v/1e4).toFixed(1)+'万':num(v);const esc=v=>String(v??'').replace(/[&<>\"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;',\"'\":'&#39;'}[c]));const palette=['#a0ca92','#ee6018','#eee'];const patterns=['','5 4','2 4'];\n"
 write('assets/company.js',shared+chartfn+'\n'+(S/'company.js').read_text())
 macro=(S/'report-template.html').read_text().replace('<style>__DASHBOARD_CSS__</style>','<link rel="stylesheet" href="assets/dashboard.css"><link rel="stylesheet" href="assets/research.css">')
 macro=macro.replace('<div class="global-filters">','<div class="macro-navigation"><p>行业变化 → 同行对比 → 公司独立研究 → 具体动作与实验。每家公司的增长、获客与商业化在独立页面展开。</p><div class="source-links"><a class="jump-link" href="companies/index.html">进入 37 家独立研究</a><a href="signals/index.html">X 动态</a></div></div><div class="global-filters">')
 for mark,file in [('__CHARTS_JS__','charts.js'),('__MARKET_UI_JS__','market-ui.js'),('__DASHBOARD_JS__','dashboard.js'),('__DETAILS_JS__','details.js')]:
  code=(S/file).read_text()
  if file=='charts.js':code=code.replace('`<button class="name-link" data-detail="${id}">${esc(product(id).name)}</button>`','`<a class="name-link" href="competitors/${id}/index.html">${esc(product(id).name)}</a>`')
  if file=='details.js':
   a=code.index('function renderDetail(');b=code.index('function renderActivity(',a)
   code=code[:a]+"function renderDetail(id){if(product(id))location.href='competitors/'+id+'/index.html';}\n"+code[b:]
   code=code.replace('原始响应','公开数据').replace('官网正文','研究摘记').replace('页面原文','研究摘记').replace('静态 HTML 不会自动更新','X 数据接入后须重新构建发布')
  if file=='dashboard.js':code=code.replace("syncProductOptions();showView(location.hash.slice(1));","syncProductOptions();(new URLSearchParams(location.search).get('compare')||'').split(',').filter(id=>product(id)).slice(0,6).forEach(id=>selected.add(id));showView(location.hash.slice(1));")
  macro=macro.replace(mark,code)
 macro=macro.replace('__REPORT_DATA__',js(d)).replace('查看原文','查看依据').replace('价格原文','价格依据')
 # Data links in the inherited dashboard now resolve to explicit public projections.
 for old in ['research-access-log.json','research-notes.json','README.md','VALIDATION.md','issues.csv','market-research.json','data-audit.json']:
  macro=macro.replace('href="'+old+'"','href="methodology/index.html"').replace("evidenceLink('"+old+"'","evidenceLink('methodology/index.html'")
 fresh=json.loads((R/'data/freshness.json').read_text())
 macro=macro.replace('<div class="global-filters">',f'<p class="source-note">10 月 2 日已重新请求全部 {fresh["domains_checked"]} 个根域：最新返回仍为 8 月，暂未取得 9 / 10 月。<a href="data/freshness.json">查看逐域核验记录</a></p><div class="global-filters">')
 write('data/freshness.json',json.dumps(fresh,ensure_ascii=False,indent=2))
 write('index.html',macro)
 write('companies/index.html',directory(d,ed));write('methodology/index.html',methodology())
 for p in d['products']:
  posts=[v for v in x['posts'] if v['product_id']==p['id']]
  write(f'competitors/{p["id"]}/index.html',render_company(d,p,ed,posts))
  public={'schema_version':1,'product':p,'metrics':d['analysis']['metrics'][p['id']],'editorial':ed[p['id']],'activities':[a for a in d['market']['activities'] if a['product_id']==p['id']],'x_posts':posts}
  write(f'data/companies/{p["id"]}.json',json.dumps(public,ensure_ascii=False,indent=2))
 for path,record in d['public_sources'].items():write(path,json.dumps(record,ensure_ascii=False,indent=2))
 write('data/snapshot.json',json.dumps(d,ensure_ascii=False,indent=2));write('market-data.json',json.dumps(d['market'],ensure_ascii=False));write('data/x-posts.json',json.dumps(x,ensure_ascii=False))
 for filename,rows in [('companies',[{'product_id':p['id'],'name':p['name'],'domain':p['traffic_domain'],**{k:d['analysis']['metrics'][p['id']][k] for k in ['visits','mom','rolling3','scope']}} for p in d['products']]),('monthly-visits',[{'domain':domain,**h} for domain,v in d['domains'].items() for h in v['traffic']['monthly_visits']]),('growth-actions',d['market']['activities'])]:
  fields=list(dict.fromkeys(k for row in rows for k in row));buf=io.StringIO();w=csv.DictWriter(buf,fieldnames=fields);w.writeheader();w.writerows(rows);write('data/'+filename+'.csv','\ufeff'+buf.getvalue())
 shutil.copyfile(O/'data/monthly-visits.csv',O/'monthly-visits.csv')
 body='<h1>X 动态追踪</h1><p class="directory-intro">按产品聚合官方原帖、发布时间和采集时的互动指标。网站流量、官网观察、社交动态分别保存时间，不混成一个“实时增长”数字。</p>'
 if not x['posts']:body+='<div class="notice">尚未接入 X 数据源。37 家公司研究页已准备好动态章节与稳定产品 ID。接入 Grok BOT 后，经过数据校验和重新发布，原帖会出现在对应公司页面。</div><p><a href="../methodology/index.html#updates">查看更新方式</a> · <a href="../companies/index.html">打开竞品研究</a></p>'
 else:
  for post in sorted(x['posts'],key=lambda z:z['published_at'],reverse=True)[:200]:
   body+=f'<article class="action-record"><h2><a href="../competitors/{post["product_id"]}/index.html#social">{E(next(p["name"] for p in d["products"] if p["id"]==post["product_id"]))}</a></h2><p class="source-note">{E(post["published_at"])} · 采集 {E(post["collected_at"])}</p><p>{E(post["text"])}</p>{link(post["url"],"X 原帖")}</article>'
 write('signals/index.html',shell('X 动态',body,1,active='signals'))
 write('404.html',shell('页面未找到','<h1>页面未找到</h1><p>请从竞品目录重新选择。</p><a href="companies/index.html">打开 37 家竞品目录</a>'))
 print(f'Built {len(d["products"])} company dossiers, macro dashboard, directory, methodology and X stream.')
if __name__=='__main__':main()
