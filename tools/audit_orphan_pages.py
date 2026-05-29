#!/usr/bin/env python3
"""Audit: find all source files not in sitemap, sitemap duplicates, and orphan pages."""
import json, os, re, sys, io
from collections import Counter

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(BASE, 'source')
SITEMAP = os.path.join(SRC, 'sitemap.xml')

# ============================================================
# 1. Parse sitemap.xml
# ============================================================
with open(SITEMAP, 'r', encoding='utf-8') as f:
    sm = f.read()

sitemap_urls_raw = re.findall(r'<loc>https://cunqin\.tax/(.+?)</loc>', sm)
print(f'=== SITEMAP ANALYSIS ===')
print(f'Total <loc> entries: {len(sitemap_urls_raw)}')

url_counts = Counter(sitemap_urls_raw)
dups = {u: c for u, c in url_counts.items() if c > 1}
if dups:
    print(f'\n*** DUPLICATED URLs in sitemap: ***')
    for u, c in sorted(dups.items()):
        print(f'  [{c}x] {u}')
else:
    print('  No duplicates')

unique_sitemap = set(sitemap_urls_raw)
print(f'  Unique URLs: {len(unique_sitemap)}')

# ============================================================
# 2. Collect all source HTML files
# ============================================================
TEMPLATE_FILES = {'_article_list_generated.html', '_article_list_new.html'}
all_src = []
for root, dirs, files in os.walk(SRC):
    dirs[:] = [d for d in dirs if d not in ('.git', 'node_modules', '.workbuddy')]
    for fn in files:
        if fn.endswith('.html') and fn not in TEMPLATE_FILES:
            rel = os.path.relpath(os.path.join(root, fn), BASE).replace('\\', '/')
            all_src.append(rel)

print(f'\n=== SOURCE FILES ===')
print(f'Total source HTML: {len(all_src)}')
articles_only = [s for s in all_src if s.startswith('source/articles/')]
services_only = [s for s in all_src if s.startswith('source/services/')]
other_pages = [s for s in all_src if not s.startswith('source/articles/') and not s.startswith('source/services/')]
print(f'  Articles: {len(articles_only)}')
print(f'  Services: {len(services_only)}')
print(f'  Other:    {len(other_pages)}')

# ============================================================
# 3. Extract permalink from each source file
# ============================================================
source_permalinks = {}  # normalized_url -> file_path
for rel in all_src:
    fp = os.path.join(BASE, rel)
    with open(fp, 'r', encoding='utf-8') as f:
        head = f.read(3000)
    m = re.search(r'permalink:\s*(/\S+)', head)
    if m:
        url = m.group(1).lstrip('/').rstrip('/')
        if url:
            source_permalinks[url] = rel

print(f'Files with permalink: {len(source_permalinks)}')

# ============================================================
# 4. Find source pages NOT in sitemap
# ============================================================
print(f'\n=== SOURCE PAGES MISSING FROM SITEMAP ===')
missing = []
for url, fp in sorted(source_permalinks.items()):
    # Try matching with and without trailing slash
    variants = {url, url + '/', url.rstrip('/')}
    if not variants & unique_sitemap:
        # Also check: sitemap might have URL without .html or with .html
        alt_url = url + '/' if not url.endswith('.html') else url.rstrip('/')
        if alt_url not in unique_sitemap and alt_url + '/' not in unique_sitemap:
            missing.append((url, fp))
            print(f'  {url}')
            print(f'    -> {fp}')
            print()

if not missing:
    print('  None!')

# ============================================================
# 5. Check about/deng-dahua specifically
# ============================================================
print(f'=== ABOUT/DENG-DAHUA ===')
dh_path = os.path.join(SRC, 'about', 'deng-dahua.html')
in_sm = 'about/deng-dahua' in unique_sitemap or 'about/deng-dahua/' in unique_sitemap
print(f'  Source file: {os.path.exists(dh_path)}')
print(f'  In sitemap:  {in_sm}')

# Check if linked from key pages
key_pages = [
    'source/about/关于我们(source).html',
    'source/首页(source).html',
    'source/services/十大核心服务(source).html',
    'source/archives/法税洞察(source).html',
    'source/cases/客户案例(source).html',
    'source/contact/联系我们(source).html',
]
for kp in key_pages:
    fp = os.path.join(BASE, kp)
    if os.path.exists(fp):
        with open(fp, 'r', encoding='utf-8') as f:
            content = f.read()
        linked = 'deng-dahua' in content
        print(f'  Linked from {kp.split("/")[-1]}: {linked}')

# ============================================================
# 6. Check home-insights.json for article completeness
# ============================================================
hi_path = os.path.join(SRC, 'home-insights.json')
with open(hi_path, 'r', encoding='utf-8') as f:
    hi = json.load(f)
hi_urls = set(a['url'] for a in hi['articles'])
print(f'\n=== HOME-INSIGHTS.JSON ===')
print(f'  Articles: {len(hi["articles"])}')

# Find articles in source NOT in home-insights.json
article_source_urls = {u: f for u, f in source_permalinks.items()
                       if f.startswith('source/articles/')}
missing_from_hi = []
for url, fp in sorted(article_source_urls.items()):
    if url not in hi_urls:
        missing_from_hi.append((url, fp))
        print(f'  MISSING: {url} -> {fp}')

if not missing_from_hi:
    print('  All source articles in home-insights.json')

# Find articles in hi NOT in source
hi_not_in_src = []
for url in sorted(hi_urls):
    if url not in article_source_urls:
        hi_not_in_src.append(url)

if hi_not_in_src:
    print(f'\n  ORPHAN in home-insights.json ({len(hi_not_in_src)}):')
    for u in hi_not_in_src:
        print(f'    {u}')

# ============================================================
# 7. Summary
# ============================================================
print(f'\n{"="*50}')
print(f'SUMMARY')
print(f'{"="*50}')
print(f'Source pages not in sitemap: {len(missing)}')
if missing:
    for u, f in missing:
        print(f'  - {u} ({f})')
print(f'Sitemap duplicate groups: {len(dups)} ({sum(c-1 for c in dups.values())} excess entries)')
print(f'Source articles: {len(article_source_urls)}')
print(f'home-insights.json: {len(hi["articles"])}')
print(f'Articles missing from hi: {len(missing_from_hi)}')
print(f'Articles in hi but not source: {len(hi_not_in_src)}')
print(f'Sitemap unique: {len(unique_sitemap)}')
print(f'Source files total: {len(all_src)}')
