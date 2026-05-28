"""Article inventory check - why 59 vs 62?"""
import json, sys, re, glob, os
sys.stdout.reconfigure(encoding='utf-8')

BASE = r'C:\Users\26726\WorkBuddy\2026-05-20-21-20-24'

# 1. All article files
all_files = sorted(glob.glob(os.path.join(BASE, 'source', 'articles', '*.html')))
all_slugs = set()
for f in all_files:
    bn = os.path.basename(f)
    # Remove (source).html -> .html
    slug = bn.replace('(source).html', '.html')
    all_slugs.add(slug)

# 2. Articles in 法税洞察 page
with open(os.path.join(BASE, 'source', 'archives', '法税洞察(source).html'), 'r', encoding='utf-8') as f:
    html = f.read()
page_urls = set()
for m in re.finditer(r'href="\.\./articles/([^"]+)" class="article-item"', html):
    page_urls.add(m.group(1))

# 3. home-insights.json
with open(os.path.join(BASE, 'source', 'home-insights.json'), 'r', encoding='utf-8') as f:
    data = json.load(f)
json_urls = set(a['url'].replace('articles/', '') for a in data['articles'])

# 4. search-index.json
with open(os.path.join(BASE, 'source', 'search-index.json'), 'r', encoding='utf-8') as f:
    si_data = json.load(f)
si_urls = set()
for item in si_data:
    if item.get('category') not in ('案例', '服务'):
        si_urls.add(item['url'].replace('articles/', ''))

print(f"=== 文章库存对比 ===")
print(f"source/articles/ 文件数: {len(all_slugs)}")
print(f"法税洞察页 文章数:   {len(page_urls)}")
print(f"home-insights.json:  {len(json_urls)}")
print(f"search-index.json:   {len(si_urls)}")
print()

# Find which 3 articles are NOT in 法税洞察
# Need to map Chinese filenames to pinyin slugs
# Read the articles to find their permalink
article_slug_map = {}
for f in all_files:
    with open(f, 'r', encoding='utf-8') as fh:
        content = fh.read(2000)
    m = re.search(r'permalink:\s*articles/([^\s]+)', content)
    if m:
        article_slug_map[m.group(1)] = os.path.basename(f).replace('(source).html', '.html')

# In page but slug not mapping to any source file
print("=== 在法税洞察页但无对应source文件(可能正常,因为source用中文名) ===")
# The page uses pinyin slugs for URLs

# Find articles in source that have NO corresponding entry in 法税洞察
# This requires reading permalink from each source file
source_permalinks = {}
for f in all_files:
    with open(f, 'r', encoding='utf-8') as fh:
        content = fh.read(3000)
    m = re.search(r'permalink:\s*articles/([^\s]+)', content)
    bn = os.path.basename(f)
    chinese_name = bn.replace('(source).html', '')
    if m:
        source_permalinks[m.group(1)] = chinese_name
    else:
        source_permalinks[bn] = chinese_name  # Use filename as slug

# Compare
missing_from_page = set(source_permalinks.keys()) - page_urls
extra_in_page = page_urls - set(source_permalinks.keys())

print(f"\n=== 在source/articles但不在法税洞察页 ({len(missing_from_page)}) ===")
for slug in sorted(missing_from_page):
    chinese = source_permalinks.get(slug, slug)
    print(f"  [{slug}] → {chinese}")

if extra_in_page:
    print(f"\n=== 在法税洞察页但不在source/articles ({len(extra_in_page)}) ===")
    for slug in sorted(extra_in_page):
        print(f"  {slug}")
