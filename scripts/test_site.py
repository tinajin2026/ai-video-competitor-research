"""Acceptance checks for coverage, numerical provenance, links and bot boundaries."""
import copy,json,math,sys,tempfile,unittest
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
from datetime import datetime,timezone
from research import derive,keyword_type
from ingest_x import validate,merge,ingest
R=Path(__file__).resolve().parents[1];D=json.loads((R/'data/snapshot.json').read_text());O=R/'public'
class Links(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.ids=set()
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if a.get('id'):self.ids.add(a['id'])
  if tag in ['a','link','script','img']:
   v=a.get('href') or a.get('src')
   if v:self.links.append(v)
class ResearchTests(unittest.TestCase):
 def test_all_companies_and_sections(self):
  self.assertEqual(len(D['products']),37);self.assertEqual(len(list((O/'competitors').glob('*/index.html'))),37)
  for p in D['products']:
   h=(O/'competitors'/p['id']/'index.html').read_text()
   for section in ['portrait','acquisition','product','implications','social','sources']:self.assertIn(f'id="{section}"',h,p['id'])
   self.assertIn('THESIS:',h);self.assertNotIn('__REPORT_DATA__',h)
 def test_all_links_resolve(self):
  pages={f:f.read_text() for f in O.rglob('*.html')};parsed={}
  for f,html in pages.items():parser=Links();parser.feed(html);parsed[f]=parser
  count=0
  for f,parser in parsed.items():
   for ref in parser.links:
    u=urlsplit(ref)
    if u.scheme or u.netloc:continue
    dest=(f.parent/unquote(u.path)).resolve() if u.path else f
    if dest.is_dir():dest=dest/'index.html'
    self.assertTrue(dest.is_relative_to(O),ref);self.assertTrue(dest.exists(),str(f.relative_to(O))+' → '+ref);count+=1
    if u.fragment and dest in parsed and dest.name!='index.html':self.assertIn(u.fragment,parsed[dest].ids)
  self.assertGreater(count,1000)
 def test_metrics_recompute(self):
  for p in D['products']:
   t=p['domain_data']['traffic'];h={x['month']:x['visits'] for x in t['monthly_visits']};m=D['analysis']['metrics'][p['id']]
   self.assertEqual(m['visits'],h['2026-08']);self.assertAlmostEqual(m['mom'],h['2026-08']/h['2026-07']-1)
   self.assertAlmostEqual(m['rolling3'],sum(h[x] for x in ['2026-06','2026-07','2026-08'])/sum(h[x] for x in ['2026-03','2026-04','2026-05'])-1)
   r=derive(D,p)
   for c in r['channels']:
    if c['share'] is not None:self.assertAlmostEqual(c['visits'],m['visits']*c['share'])
 def test_fixed_cohort(self):
  ids=D['market']['summary']['ids'];self.assertEqual(len(ids),27)
  ps=[p for p in D['products'] if p['id'] in ids];self.assertEqual(len({p['traffic_domain'] for p in ps}),27)
  for p in ps:self.assertEqual(D['analysis']['metrics'][p['id']]['scope'],'site')
  self.assertEqual(sum(D['analysis']['metrics'][p['id']]['visits'] for p in ps),114357253)
 def test_peer_exclusion_and_scopes(self):
  for p in D['products']:
   r=derive(D,p);self.assertNotIn(p['id'],[q['id'] for q in r['peers']])
   for q in r['peers']:self.assertEqual(D['analysis']['metrics'][q['id']]['scope'],'site')
  self.assertEqual(D['analysis']['metrics']['flow']['scope'],'mixed')
  self.assertEqual(D['analysis']['metrics']['sora']['scope'],'discontinued')
 def test_keyword_truth(self):
  self.assertEqual(keyword_type('pollo','pixverse ai'),'第三方品牌 / 模型')
  self.assertEqual(keyword_type('vidu','image to video'),'通用任务')
  self.assertEqual(keyword_type('dreamina','capcut'),'第三方品牌 / 模型')
  self.assertEqual(keyword_type('magnific','80'),'其它 / 待核实')
 def test_evidence_and_dates(self):
  acts=D['market']['activities'];self.assertEqual(len(acts),60);self.assertEqual(len({a['product_id'] for a in acts}),35)
  for a in acts:
   self.assertIn(a['source'],D['public_sources']);self.assertEqual(a['observed_at'],'2026-10-02')
   self.assertTrue(a['source_url'].startswith('https://'))
  dream=next(a for a in acts if a['product_id']=='dreamina' and a['event_date']);self.assertEqual(dream['date_label'],'活动开始')
 def test_public_boundary(self):
  for f in O.rglob('*'):
   if f.is_file() and f.suffix in ['.html','.json','.js','.css','.csv']:
    text=f.read_text()
    for forbidden in ['Bearer ','/Users/tianjin/','tabapi.key','sk-proj-','<script>alert(']:self.assertNotIn(forbidden,text,str(f))
  self.assertFalse((O/'.git').exists());self.assertFalse((O/'.openai').exists())
 def test_source_file_sizes(self):
  for parent in [R/'scripts',R/'src']:
   for f in parent.rglob('*'):
    if f.suffix in ['.py','.js','.css','.html']:self.assertLessEqual(len(f.read_text().splitlines()),500,str(f))
class IngestTests(unittest.TestCase):
 def setUp(self):
  self.accounts={'topview':'TopviewAIhq'}
  self.post={'product_id':'topview','post_id':'123','author_handle':'TopviewAIhq','url':'https://x.com/TopviewAIhq/status/123','published_at':'2026-09-01T00:00:00Z','collected_at':'2026-09-02T00:00:00Z','text':'<script>alert("test")</script>','metrics':{'likes':2,'views':None},'relevance_evidence':'测试夹具；不是线上原帖。'}
 def test_valid_unknown_metrics(self):self.assertIsNone(validate(self.post,self.accounts)['metrics']['views'])
 def test_account_url_future_counts_rejected(self):
  variants=[{'product_id':'../topview'},{'author_handle':'wrong'},{'url':'javascript:alert(1)'},{'url':'https://x.com/wrong/status/123'},{'collected_at':'2099-01-01T00:00:00Z'},{'metrics':{'views':-1}},{'metrics':{'likes':True}},{'published_at':'2026-09-03T00:00:00Z'}]
  for change in variants:
   with self.assertRaises(ValueError):validate({**self.post,**change},self.accounts)
 def test_idempotency_order_history(self):
  post=validate(self.post,self.accounts);rows,n=merge([], [post,post]);self.assertEqual(n,1)
  newer={**post,'collected_at':'2026-09-03T00:00:00Z','metrics':{'likes':1}}
  rows,n=merge(rows,[newer,post]);self.assertEqual(n,1);self.assertEqual(rows[0]['metrics']['likes'],1);self.assertEqual(len(rows[0]['metric_snapshots']),2)
 def test_transaction_all_or_nothing(self):
  with tempfile.TemporaryDirectory() as tmp:
   path=Path(tmp)/'in.jsonl';dst=Path(tmp)/'posts.json'
   path.write_text(json.dumps(self.post)+'\n'+json.dumps({**self.post,'product_id':'unknown'})+'\n')
   with self.assertRaises(ValueError):ingest([path],dst,self.accounts)
   self.assertFalse(dst.exists())
 def test_escaping_social_text(self):
  from company_page import render_company
  p=next(x for x in D['products'] if x['id']=='topview');ed=json.loads((R/'data/editorial.json').read_text());html=render_company(D,p,ed,[self.post])
  self.assertIn('&lt;script&gt;',html);self.assertNotIn('<script>alert(',html)
if __name__=='__main__':unittest.main(verbosity=2)
