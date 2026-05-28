"""Find the 3 articles missing from 法税洞察 page vs source/articles"""
import sys, re, glob, os, json
sys.stdout.reconfigure(encoding='utf-8')

BASE = r'C:\Users\26726\WorkBuddy\2026-05-20-21-20-24'
articles_dir = os.path.join(BASE, 'source', 'articles')

# 1. Get all permalinks from source articles
files = sorted(glob.glob(os.path.join(articles_dir, '*.html')))
source_slugs = {}
for fp in files:
    bn = os.path.basename(fp)
    chinese = bn.replace('(source).html', '')
    with open(fp, 'r', encoding='utf-8') as f:
        text = f.read(800)
    pm = re.search(r'permalink:\s*/articles/(\S+)', text)
    if pm:
        slug = pm.group(1).strip()
        source_slugs[slug] = chinese
    else:
        print(f'WARN: No permalink in {bn}')

# 2. Get slugs from home-insights.json
with open(os.path.join(BASE, 'source', 'home-insights.json'), 'r', encoding='utf-8') as f:
    data = json.load(f)
indexed = set(a['url'].replace('articles/', '') for a in data['articles'])

# 3. Get slugs from 法税洞察 page
with open(os.path.join(BASE, 'source', 'archives', '法税洞察(source).html'), 'r', encoding='utf-8') as f:
    html = f.read()
page_set = set(re.findall(
    r'href="\.\./articles/([^"]+)" class="article-item"',
    html
))

# 4. Compare
print(f"=== 文章库存总览 ===")
print(f"source/articles/ 文件数:    {len(files)}")
print(f"source permalink 提取:     {len(source_slugs)}")
print(f"home-insights.json 文章数: {len(indexed)}")
print(f"法税洞察页 article-item:    {len(page_set)}")
print()

# Missing from page
missing_page = set(source_slugs.keys()) - page_set
print(f"=== 在 source 但不在法税洞察页 ({len(missing_page)}) ===")
for s in sorted(missing_page):
    print(f"  {s}  →  {source_slugs.get(s, '???')}")

# Missing from home-insights.json
missing_json = set(source_slugs.keys()) - indexed
print(f"\n=== 在 source 但不在 home-insights.json ({len(missing_json)}) ===")
for s in sorted(missing_json):
    print(f"  {s}  →  {source_slugs.get(s, '???')}")

# In page but not in source
extra_page = page_set - set(source_slugs.keys())
if extra_page:
    print(f"\n=== 在法税洞察页但不在 source ({len(extra_page)}) ===")
    for s in sorted(extra_page):
        print(f"  {s}")

# In JSON but not in source
extra_json = indexed - set(source_slugs.keys())
if extra_json:
    print(f"\n=== 在 home-insights.json 但不在 source ({len(extra_json)}) ===")
    for s in sorted(extra_json):
        print(f"  {s}")
