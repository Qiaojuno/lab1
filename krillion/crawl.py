"""Download every saved Krillion dive from krilliongame.com into one JSON file per date.

Usage: python3 crawl.py <out_dir>
"""
import re, json, sys, time, urllib.request, os

BASE = 'https://krilliongame.com/krillion-answers/'
UA = {'User-Agent': 'Mozilla/5.0 (personal study archive)'}

def get(url):
    for attempt in range(4):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read().decode('utf-8')
        except Exception as ex:
            print('retry', url, ex, flush=True); time.sleep(2 ** (attempt + 1))
    raise RuntimeError('failed: ' + url)

def practice_data(html):
    m = re.search(r'id="krilling-practice-data">(.*?)</script>', html, re.S)
    return json.loads(m.group(1))

out = sys.argv[1]; os.makedirs(out, exist_ok=True)
index = re.findall(r'href="/krillion-answers/(\d{4}-\d{2}-\d{2})/"', get(BASE))
for d in sorted(set(index), reverse=True):
    fn = os.path.join(out, d + '.json')
    if os.path.exists(fn): continue
    data = practice_data(get(f'{BASE}{d}/')); data.pop('dates', None)
    json.dump(data, open(fn, 'w'), ensure_ascii=False)
    print(d, sum(len(p['answers']) for p in data['prompts']), flush=True)
    time.sleep(1)  # be polite
