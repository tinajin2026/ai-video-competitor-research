"""Bounded, atomic, product-scoped ingestion of untrusted X observations."""
import argparse,copy,fcntl,json,os,re,tempfile
from datetime import datetime,timezone,timedelta
from pathlib import Path
from urllib.parse import urlsplit
R=Path(__file__).resolve().parents[1]
FIELDS={'product_id','post_id','author_handle','url','published_at','collected_at','text','metrics','relevance_evidence'}
METRICS={'likes','reposts','replies','quotes','views','bookmarks'}

def timestamp(value):
 if not isinstance(value,str) or not re.fullmatch(r'\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?Z',value):raise ValueError('timestamp must be UTC ISO-8601 ending Z')
 return datetime.fromisoformat(value.replace('Z','+00:00'))

def validate(record,accounts,now=None):
 if not isinstance(record,dict) or set(record)!=FIELDS:raise ValueError('unexpected or missing fields')
 p=record['product_id'];author=record['author_handle'];post=record['post_id']
 if not isinstance(p,str) or p not in accounts:raise ValueError('unknown product_id')
 if not isinstance(author,str) or not re.fullmatch(r'[A-Za-z0-9_]{1,15}',author):raise ValueError('invalid author_handle')
 if not accounts[p] or author.lower()!=accounts[p].lower():raise ValueError('author does not match this product registry')
 if not isinstance(post,str) or not re.fullmatch(r'[0-9]{1,25}',post):raise ValueError('invalid post_id')
 u=urlsplit(record['url'])
 if u.scheme!='https' or u.netloc.lower() not in ['x.com','twitter.com'] or u.query or u.fragment or u.path.lower()!=f'/{author}/status/{post}'.lower():raise ValueError('source URL must match X author and post_id')
 pub=timestamp(record['published_at']);col=timestamp(record['collected_at']);now=now or datetime.now(timezone.utc)
 if pub>col or col>now+timedelta(minutes=5):raise ValueError('observation dates are inconsistent or in future')
 for k,limit in [('text',30000),('relevance_evidence',1000)]:
  if not isinstance(record[k],str) or not 1<=len(record[k].strip())<=limit:raise ValueError(k+' must be nonempty and bounded')
 metrics=record['metrics']
 if not isinstance(metrics,dict) or set(metrics)-METRICS:raise ValueError('unknown metric name')
 for key,val in metrics.items():
  if val is not None and (type(val)!=int or not 0<=val<=10**15):raise ValueError('metrics must be nonnegative integers or null')
 result=copy.deepcopy(record);result['author_handle']=accounts[p];result['url']=f'https://x.com/{author}/status/{post}'
 return result

def merge(existing,records):
 by={(x['product_id'],x['post_id']):copy.deepcopy(x) for x in existing};changed=0
 for rec in sorted(records,key=lambda x:timestamp(x['collected_at'])):
  key=(rec['product_id'],rec['post_id']);old=by.get(key)
  if old and timestamp(old['collected_at'])>=timestamp(rec['collected_at']):continue
  snapshots=copy.deepcopy(old.get('metric_snapshots',[])) if old else []
  snapshots.append({'collected_at':rec['collected_at'],'metrics':copy.deepcopy(rec['metrics'])})
  by[key]={**rec,'metric_snapshots':snapshots[-100:]};changed+=1
 return sorted(by.values(),key=lambda x:(x['product_id'],x['post_id'])),changed

def ingest(files,destination,accounts):
 records=[]
 for file in files:
  if file.stat().st_size>10*1024*1024:raise ValueError('input file exceeds 10 MiB')
  for line_no,line in enumerate(file.read_text().splitlines(),1):
   if line.strip():
    try:records.append(validate(json.loads(line),accounts))
    except (ValueError,TypeError,KeyError) as exc:raise ValueError(f'{file.name}:{line_no}: {exc}') from None
   if len(records)>10000:raise ValueError('batch exceeds 10,000 observations')
 destination.parent.mkdir(parents=True,exist_ok=True)
 with (destination.parent/(destination.name+'.lock')).open('a') as lock:
  fcntl.flock(lock,fcntl.LOCK_EX)
  state=json.loads(destination.read_text()) if destination.exists() else {'schema_version':1,'posts':[]}
  if state.get('schema_version')!=1 or not isinstance(state.get('posts'),list):raise ValueError('unsupported stored state')
  posts,changed=merge(state['posts'],records)
  if changed:
   fd,tmp=tempfile.mkstemp(dir=destination.parent,prefix='.x-posts-',suffix='.tmp')
   try:
    with os.fdopen(fd,'w') as out:json.dump({'schema_version':1,'posts':posts},out,ensure_ascii=False,indent=2);out.write('\n');out.flush();os.fsync(out.fileno())
    os.replace(tmp,destination)
   finally:
    if os.path.exists(tmp):os.unlink(tmp)
 return {'accepted_observations':len(records),'updated_records':changed,'total_posts':len(posts)}

def main():
 parser=argparse.ArgumentParser();parser.add_argument('files',nargs='*',type=Path);args=parser.parse_args()
 files=args.files or sorted((R/'data/inbox').glob('*.jsonl'))
 registry=json.loads((R/'data/accounts.json').read_text());accounts={k:v['handle'] for k,v in registry.items()}
 try:print(json.dumps(ingest(files,R/'data/x-posts.json',accounts)))
 except (ValueError,OSError) as exc:raise SystemExit(str(exc)) from None
if __name__=='__main__':main()
