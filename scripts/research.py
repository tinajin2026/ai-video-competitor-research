"""Pure derived research metrics. Input is the public snapshot, never API responses."""
import statistics,re
ALIASES={
 'higgsfield':['higgsfield','higsfield','힉스필드'],'pollo':['pollo'], 'dreamina':['dreamina'],
 'seedance':['seedance'],'minimax':['minimax'],'hailuo':['hailuo','hailou'], 'happyhorse':['happy horse','happyhorse'],
 'yoroll':['yoroll'],'runway':['runway'],'kling':['kling','king ai'],'pika':['pika'],
 'luma':['luma'],'sora':['sora'],'veo':['veo'],'flow':['google flow'], 'wan':['wan'], 'vidu':['vidu'],
 'haiper':['haiper','hyper ai'],'krea':['krea'],'openart':['openart','open art'], 'fal':['fal'],
 'leonardo':['leonardo'],'heygen':['heygen','hey gen','hygen'],'synthesia':['synthesia'],
 'invideo':['invideo'],'capcut':['capcut','cap cut'],'topview':['topview','top view'],
 'creatify':['creatify'],'arcads':['arcads','arc ads','arcards'],'makeugc':['makeugc','make ugc'],
 'jogg':['jogg'],'pixverse':['pixverse','pix verse'],'imagineart':['imagineart'],'skyreels':['skyreel','sky reels'],
 'hedra':['hedra'],'magnific':['magnific','freepik','freepick'],'grok':['grok','grock','그록','грок']}
THIRD=['google','gemini','gimini','chatgpt','midjourney','elevenlabs','opus clip','instagram','bytedance','字节跳动','eromify','flow ai']
SCOPES={'site':'独立主域','mixed':'母域 / 多业务','migration':'新旧域并存','discontinued':'停服 / 历史'}
def ratio(a,b):return a/b-1 if a is not None and b is not None and b>0 else None

def keyword_type(pid,word):
 w=word.lower()
 if any(a in w for a in ALIASES[pid]):return '自有品牌 / 变体'
 if any(a in w for key,words in ALIASES.items() if key!=pid for a in words) or any(a in w for a in THIRD):return '第三方品牌 / 模型'
 if any(a in w for a in ['generator','image to video','image enhancer','face swap','ai ugc']):return '通用任务'
 return '其它 / 待核实'

def price(d,p):
 fresh=next((x for x in d['market']['price_observations'] if x['product_id']==p['id']),None)
 if fresh:return fresh
 old=next((x for x in d['analysis']['prices'] if x['id']==p['id']),None)
 if old:return {'plan':old['plan'],'price':old['price'],'terms':old['billing']+'；'+old['caveat'],'source':next((x['path'] for x in d['analysis']['evidence'] if x['id']==old['evidence']),None)}
 return {'plan':'停服 / 历史' if p['id']=='sora' else '未确认','price':'不适用' if p['id']=='sora' else '—','terms':'当前未取得可确认的独立套餐条件。','source':None}

def derive(d,p):
 pid=p['id'];m=d['analysis']['metrics'][pid];t=p['domain_data']['traffic'];hist=sorted(t['monthly_visits'],key=lambda x:x['month']);h={x['month']:x['visits'] for x in hist}
 group=d['market']['groups'][d['market']['products'][pid]['group']]
 peers=[x for x in d['products'] if x['id'] in group['summary']['ids'] and x['id']!=pid]
 changes=[{'month':b['month'],'delta':b['visits']-a['visits'],'change':ratio(b['visits'],a['visits'])} for a,b in zip(hist,hist[1:])]
 peak=max(hist,key=lambda x:x['visits']);keywords=[{**k,'type':keyword_type(pid,k['name'])} for k in t['top_keywords']]
 if m['scope']!='site':stage={'mixed':'仅作母域背景','migration':'迁移期，分域观察','discontinued':'历史流量'}[m['scope']]
 elif m['mom']>0 and m['rolling3']>0:stage='单月与三月均上行'
 elif m['mom']>0:stage='单月回升，三月仍偏弱'
 elif m['rolling3']>0:stage='单月回落，三月仍较高'
 else:stage='单月与三月均下行'
 channels=[{'key':k,'name':name,'share':t['traffic_sources'].get(k),'visits':m['visits']*t['traffic_sources'][k] if t['traffic_sources'].get(k) is not None else None} for k,name in d['market']['channels'].items()]
 return {'stage':stage,'peak':peak,'drawdown':ratio(hist[-1]['visits'],peak['visits']),
 'period_change':ratio(hist[-1]['visits'],hist[0]['visits']),'changes':changes,'best_month':max(changes,key=lambda x:x['delta']),
 'keywords':keywords,'brand_count':sum(x['type']=='自有品牌 / 变体' for x in keywords),
 'task_count':sum(x['type']=='通用任务' for x in keywords),'channels':sorted(channels,key=lambda x:-(x['share'] or 0)),
 'peers':peers,'group':group,'price':price(d,p)}
