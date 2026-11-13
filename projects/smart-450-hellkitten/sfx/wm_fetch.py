import json, urllib.request, urllib.parse, time, re, os, html, datetime
names=["Maullido de gata hembra joven.ogg","Maullido de gata hembra.ogg","Meow of a Siamese cat - freemaster2.wav","Black cat sound begging the foods.flac","Meow of a pleading cat.oga","GettingOutImpatient.ogg"]
def get(url):
    for t in range(12):
        try: return urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'curl/8.0'})).read()
        except urllib.error.HTTPError as e:
            if e.code!=429: raise
            time.sleep(60)
    return None
q=urllib.parse.urlencode(dict(action='query',prop='imageinfo',iiprop='url|extmetadata',titles='|'.join('File:'+n for n in names),format='json'))
r=json.loads(get("https://commons.wikimedia.org/w/api.php?"+q))
strip=lambda s: html.unescape(re.sub('<[^>]+>','',s or '')).strip()
meta=[]
for pg in r['query']['pages'].values():
    ii=pg['imageinfo'][0]; m=ii['extmetadata']
    fn='src/wm__'+re.sub(r'[^A-Za-z0-9._-]','_',pg['title'][5:])
    d=dict(title=pg['title'],url=ii['url'],lic=m['LicenseShortName']['value'],licurl=m.get('LicenseUrl',{}).get('value'),artist=strip(m.get('Artist',{}).get('value')),page="https://commons.wikimedia.org/wiki/"+urllib.parse.quote(pg['title'].replace(' ','_')),file=fn,fetched=datetime.date.today().isoformat())
    if d['lic'] not in ('CC0','Public domain'): continue
    data=get(d['url'])
    if data: open(fn,'wb').write(data); meta.append(d); print('ok',fn,flush=True)
    time.sleep(30)
json.dump(meta,open('wm_meta.json','w'),indent=1,ensure_ascii=False)
