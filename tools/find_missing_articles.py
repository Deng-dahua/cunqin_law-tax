#!/usr/bin/env python3
"""Find articles missing from home-insights.json by comparing source file permalinks."""
import json, os, re

SRC_DIR = 'source/articles'
JSON_PATH = 'source/home-insights.json'

# 1. URLs from home-insights.json
with open(JSON_PATH, 'r', encoding='utf-8') as f:
    jdata = json.load(f)
json_urls = {}  # url -> title
for a in jdata['articles']:
    json_urls[a['url']] = a['title']
print(f'home-insights.json: {len(json_urls)} articles')

# 2. Read each source file's permalink from frontmatter
src_files = sorted(
    f for f in os.listdir(SRC_DIR) if f.endswith('(source).html')
)

src_info = {}  # url (e.g. 'articles/xxx.html') -> (filename, title, date, category)
for fname in src_files:
    fpath = os.path.join(SRC_DIR, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read(3000)

    # Extract permalink
    m = re.search(r'permalink:\s*(/\S+)', content)
    if not m:
        # Try reading more of the file
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read(10000)
        m = re.search(r'permalink:\s*(/\S+)', content)
        if not m:
            print(f'  SKIP: {fname} - no permalink even with 10k read')
            continue

    permalink = m.group(1)
    url = permalink.lstrip('/')

    # Extract title
    tm = re.search(r'<title>(.+?)</title>', content)
    title = tm.group(1).strip() if tm else 'UNKNOWN'
    # Remove site suffix
    title = re.sub(r'\s*[-|–—]\s*存勤法税.*$', '', title)
    title = title.replace('&quot;', '"').replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')

    # Extract date from meta or filename
    dm = re.search(r'<meta\s+name="date"\s+content="([^"]+)"', content)
    date = dm.group(1)[:10] if dm else '2026-05-28'

    # Extract category
    cm = re.search(r'<meta\s+name="category"\s+content="([^"]+)"', content)
    category = cm.group(1) if cm else '税务实务'

    # Extract description
    desc_m = re.search(r'<meta\s+name="description"\s+content="([^"]+)"', content)
    excerpt = desc_m.group(1)[:150] if desc_m else ''

    src_info[url] = {
        'filename': fname,
        'title': title,
        'date': date,
        'category': category,
        'excerpt': excerpt
    }

print(f'Source with permalink: {len(src_info)}')

# 3. Find missing: source URLs NOT in json
missing = {}
for url, info in sorted(src_info.items()):
    if url not in json_urls:
        missing[url] = info

print(f'\n=== Missing from home-insights.json: {len(missing)} ===')
for i, (url, info) in enumerate(missing.items(), 1):
    print(f'  [{i}] {info["title"]}')
    print(f'      URL:      {url}')
    print(f'      FILE:     {info["filename"]}')
    print(f'      Date:     {info["date"]}')
    print(f'      Category: {info["category"]}')
    print()

# 4. Find stale: JSON URLs NOT in source
stale = {}
for url, title in sorted(json_urls.items()):
    if url not in src_info:
        stale[url] = title

print(f'=== In JSON but NOT in source (stale): {len(stale)} ===')
if stale:
    for url, title in sorted(stale.items()):
        print(f'  {title}')
        print(f'  URL: {url}')
        print()
else:
    print('  None!')

# Summary
print(f'\n=== Summary ===')
print(f'Source files: {len(src_files)}')
print(f'In JSON:      {len(json_urls)}')
print(f'Missing:      {len(missing)}')
print(f'Stale:        {len(stale)}')
print(f'Expected:     {len(src_files)} source = {len(json_urls) - len(stale) + len(missing)} JSON')
