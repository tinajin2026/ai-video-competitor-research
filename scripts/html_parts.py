"""Escaped HTML primitives and the shared public shell."""
from html import escape
from urllib.parse import urlsplit
import json
E=lambda x:escape(str(x if x is not None else ''),quote=True)
def num(x):return f'{x:,.0f}' if isinstance(x,(float,int)) else '—'
def pct(x):return f'{x*100:.2f}%' if isinstance(x,(float,int)) else '—'
def change(x):return ('+' if x>0 else '')+pct(x) if isinstance(x,(float,int)) else '—'
def tone(x):return 'up' if x is not None and x>0 else 'down' if x is not None and x<0 else ''
def link(url,label):
 u=urlsplit(url or '')
 return f'<a href="{E(url)}" target="_blank" rel="noopener noreferrer">{E(label)}</a>' if u.scheme in ['https','http'] and not u.username else E(label)
def table(headers,rows):
 return '<div class="table-scroll"><table><thead><tr>'+''.join('<th>'+E(x)+'</th>' for x in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+v+'</td>' for v in row)+'</tr>' for row in rows)+'</tbody></table></div>'
def section(id,title,body,subtitle=''):
 return f'<section id="{id}" class="research-section"><div class="section-title"><h2>{E(title)}</h2></div>'+ (f'<p class="source-note">{E(subtitle)}</p>' if subtitle else '')+body+'</section>'
def json_script(id,data):return '<script type="application/json" id="'+id+'">'+json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')+'</script>'
def shell(title,body,depth=0,extra='',active='research'):
 root='../'*depth
 nav=''.join(f'<a href="{root}{url}" '+('aria-current="page"' if name==active else '')+'>'+label+'</a>' for name,url,label in [('macro','index.html','行业总览'),('research','companies/index.html','竞品研究'),('signals','signals/index.html','X 动态'),('method','methodology/index.html','数据与方法')])
 return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="AI 视频竞品研究：行业趋势、独立竞品分析与可追溯增长动作。"><title>{E(title)} · AI VIDEO</title><link rel="stylesheet" href="{root}assets/dashboard.css"><link rel="stylesheet" href="{root}assets/research.css"></head><body>
<!-- THESIS: Connect market movement to a separate, evidence-led dossier for every competitor.
OWN-WORLD: User-pinned Factory; Geist, dark graphite, measured green/orange and precise tables.
STORY: Inspect a company, compare its trajectory and acquisition, trace actions to sources, define a measurable experiment.
FIRST VIEWPORT: Company identity and scope, growth thesis beside twelve-month chart, precise metric strip, chapter navigation.
FORM: Read and Operate extension; user-pinned Factory and explicit independent dossier scope. Fixed-world extension, no concept roll or seed.
FINISH: unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, and DESIGN.md -->
<a class="skip" href="#main">跳到内容</a><header><div class="nav-wrap"><a class="brand" href="{root}index.html">AI VIDEO <span>/ INTELLIGENCE</span></a><nav aria-label="主要导航" class="site-nav">{nav}</nav></div></header><main id="main" class="research-main">{body}<footer><span>流量估算 2026.08 · 10.02 已重新请求，暂无 9 / 10 月</span><a href="{root}methodology/index.html">来源、口径与更新</a></footer></main>{extra}</body></html>'''
