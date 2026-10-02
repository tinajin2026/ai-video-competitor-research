"""One-way whitelist export. Raw API metadata and full scraped text stay private."""
import copy,json,re,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
source=Path(sys.argv[1]) if len(sys.argv)>1 else R.parent/'outputs/competitor-data-2026-10-02/report-data.json'
d=json.loads(source.read_text()); out={k:copy.deepcopy(d[k]) for k in ['summary','analysis','market','audit']}
out['summary'].pop('estimated_credits',None);out['summary'].pop('generated_at_utc',None)
out['analysis'].pop('serp_review',None);out['analysis'].pop('cleaned_search',None)
out['products']=[];out['domains']={};sources={}
for domain,x in d['domains'].items():
 y={k:copy.deepcopy(x[k]) for k in ['domain','traffic','traffic_evidence','traffic_status','registration_date','backlinks','backlinks_evidence']}
 y['traffic']={k:v for k,v in y['traffic'].items() if k in ['domain','overview','monthly_visits','traffic_sources','top_keywords','top_regions']}
 out['domains'][domain]=y
 for kind in ['traffic','backlinks']:
  sources[x[kind+'_evidence']]={'provider':'TabAPI','observed_at':'2026-10-02','domain':domain,'measurement':'第三方域名级估算' if kind=='traffic' else '第三方外链样本','data':y[kind]}
for p in d['products']:
 q={k:copy.deepcopy(p.get(k)) for k in ['id','name','x_handle','homepage','ads_priority','traffic_domain','additional_domains','scope_note','shared_scope']}
 q['domain_data']=out['domains'][p['traffic_domain']];q['pages']=[];q['searches']=[];q['issues']=[];q['screenshot']=None
 for page in p['pages']:
  related=[a for a in out['market']['activities'] if a['source']==page['path']]
  evidence=[a for a in out['analysis']['evidence'] if a['path']==page['path']]
  note='\n'.join(dict.fromkeys([a['detail'] for a in related]+[a['summary'] for a in evidence])) or '已保存官网来源；本公开版不转载页面全文。'
  y={k:copy.deepcopy(page[k]) for k in ['kind','label','path','status','reason']}
  y['source']={k:v for k,v in page['source'].items() if k in ['requested_url','resolved_url','http_status']}
  y['page']={'title':page['page'].get('title')};y['content']=note
  q['pages'].append(y)
  sources[y['path']]={'product_id':p['id'],'observed_at':'2026-10-02','source_url':y['source'].get('resolved_url') or y['source'].get('requested_url'),'status':y['status'],'research_note':note,'notice':'公开研究摘记；原始抓取保留在本地。'}
 # Only links visibly present in the captured homepage, not guessed app addresses.
 home=next((x for x in p['pages'] if x['kind']=='home'),{})
 urls=re.findall(r'https?://[^\s<>\)\]"]+',home.get('content',''))
 q['product_entry_links']=list(dict.fromkeys(u for u in urls if re.search(r'https://(?:app\.|platform\.|create\.|studio\.|flow\.)',u)))[:8]
 out['products'].append(q)
out['public_sources']=sources
out['dataset_version']='2026-10-02';out['schema_version']=1
(R/'data/snapshot.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
for f in ['report-template.html','dashboard.css','charts.js','market-ui.js','dashboard.js','details.js']:
 (R/'src'/f).write_text((source.parent/f).read_text())
(R/'src/assets').mkdir(exist_ok=True)
for f in (source.parent/'assets').glob('*.woff2'):(R/'src/assets'/f.name).write_bytes(f.read_bytes())
print('Exported',len(out['products']),'products;',len(sources),'public source records; no raw page text.')
