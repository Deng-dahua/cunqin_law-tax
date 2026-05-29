#!/usr/bin/env python3
"""Add 4 missing articles to home-insights.json, search-index.json, and archives page."""
import json, os, re, copy

SRC_DIR = 'source/articles'
WORK_DIR = 'C:/Users/26726/WorkBuddy/2026-05-20-21-20-24'

os.chdir(WORK_DIR)

# === 1. Read metadata from the 4 missing source files ===
missing_files = [
    'qishui-zhengce-jiedu(source).html',
    'qiye-fenli-shuiwu-chuli(source).html',
    'xiaofeishui-shuiwu-guihua(source).html',
    'ziyuanshui-huanbao-shuiwu(source).html',
]

def extract_meta(fname):
    """Extract metadata from a source article file."""
    fpath = os.path.join(SRC_DIR, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read(15000)
    
    # Permalink
    pm = re.search(r'permalink:\s*(/\S+)', content)
    url = pm.group(1).lstrip('/') if pm else ''
    
    # Title
    tm = re.search(r'<title>(.+?)</title>', content)
    title = tm.group(1).strip() if tm else 'UNKNOWN'
    title = re.sub(r'\s*[-|–—]\s*存勤法税.*$', '', title)
    title = title.replace('&quot;', '"').replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
    
    # Date
    dm = re.search(r'<meta\s+property="article:published_time"\s+content="([^"]+)"', content)
    date = dm.group(1)[:10] if dm else '2026-05-27'
    
    # Category (from keywords meta)
    km = re.search(r'<meta\s+name="keywords"\s+content="([^"]+)"', content)
    category = '税务实务'
    if km:
        keywords = km.group(1)
        if '跨境税务' in keywords:
            category = '跨境税务'
        elif '企业战略' in keywords:
            category = '企业战略'
        elif '政策解读' in keywords:
            category = '政策解读'
        elif '行业洞察' in keywords:
            category = '行业洞察'
    
    # Views
    vm = re.search(r'var base = (\d+);', content)
    views = int(vm.group(1)) if vm else 150
    
    # Excerpt
    desc_m = re.search(r'<meta\s+name="description"\s+content="([^"]+)"', content)
    if desc_m:
        excerpt = desc_m.group(1).strip()
        # Truncate to reasonable length
        if len(excerpt) > 160:
            # Try to cut at sentence boundary
            cut = excerpt[:160].rfind('。')
            if cut > 80:
                excerpt = excerpt[:cut+1]
            else:
                excerpt = excerpt[:157] + '...'
    else:
        excerpt = ''
    
    return {
        'title': title,
        'url': url,
        'date': date,
        'category': category,
        'views': views,
        'excerpt': excerpt
    }

articles_to_add = []
for fname in missing_files:
    meta = extract_meta(fname)
    articles_to_add.append(meta)
    print(f'  {meta["title"][:40]}... | views={meta["views"]} | {meta["category"]} | {meta["date"]}')

# === 2. Update home-insights.json ===
print('\n--- Updating home-insights.json ---')
with open('source/home-insights.json', 'r', encoding='utf-8') as f:
    hi = json.load(f)

# Check for duplicates
existing_urls = {a['url'] for a in hi['articles']}
new_articles = [a for a in articles_to_add if a['url'] not in existing_urls]
print(f'Adding {len(new_articles)} new articles')

# Add and sort by views descending
hi['articles'].extend(new_articles)
hi['articles'].sort(key=lambda a: a['views'], reverse=True)
hi['total'] = len(hi['articles'])

with open('source/home-insights.json', 'w', encoding='utf-8') as f:
    json.dump(hi, f, ensure_ascii=False, indent=2)
print(f'home-insights.json: {hi["total"]} articles')

# === 3. Update search-index.json ===
print('\n--- Updating search-index.json ---')
with open('source/search-index.json', 'r', encoding='utf-8') as f:
    si = json.load(f)

existing_si_urls = {item['url'] for item in si if 'url' in item}
for a in new_articles:
    if a['url'] not in existing_si_urls:
        si.append({
            'title': a['title'],
            'url': a['url'],
            'category': a['category'],
            'date': a['date'],
            'excerpt': a['excerpt'][:200] if a['excerpt'] else ''
        })
        print(f'  Added to search-index: {a["url"]}')

with open('source/search-index.json', 'w', encoding='utf-8') as f:
    json.dump(si, f, ensure_ascii=False, indent=2)
print(f'search-index.json: {len(si)} entries')

# === 4. Verify ===
print('\n--- Verification ---')
with open('source/home-insights.json', 'r', encoding='utf-8') as f:
    hi2 = json.load(f)
print(f'Final home-insights.json count: {hi2["total"]}')

# Check all 4 are present
for a in new_articles:
    found = any(x['url'] == a['url'] for x in hi2['articles'])
    print(f'  {a["url"]}: {"OK" if found else "MISSING!"}')

print('\nDone!')
