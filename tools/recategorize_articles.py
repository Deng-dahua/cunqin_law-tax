#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将 11 篇"跨境税务"文章分配到其他 4 个分类。
更新：source 文章 frontmatter、home-insights.json、search-index.json、法税洞察页。
"""
import re, json, os, sys
sys.stdout = sys.stderr = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)

BASE = os.path.dirname(os.path.abspath(__file__)) or '.'

# URL -> 新分类
NEW_CATS = {
    "articles/beps-2.0-qiye-yingdui.html": "政策解读",
    "articles/kuajing-fuwu-maoyi-shuiwu.html": "税务实务",
    "articles/zhuanrang-dingjia-tongqi-ziliao.html": "税务实务",
    "articles/tan-guan-shui-cbam-chukou.html": "政策解读",
    "articles/jingwai-suode-dijiang-zhinan.html": "税务实务",
    "articles/zhuanrang-dingjia-guanlian-jiaoyi.html": "税务实务",
    "articles/chukou-tuishui-hegui-fengkong.html": "税务实务",
    "articles/CRS-kuajing-zichan-shenbao.html": "税务实务",
    "articles/shuishou-xieding-daiyu-shenqing.html": "税务实务",
    "articles/odi-beian-quanliucheng.html": "税务实务",
    "articles/kuajing-dianshang-shuiwu.html": "行业洞察",
}

ARTICLES_DIR = os.path.normpath(os.path.join(BASE, '..', 'source', 'articles'))

# 建立 slug -> 源文件路径映射
SLUG_TO_FILE = {}
for fn in os.listdir(ARTICLES_DIR):
    if not fn.endswith('(source).html'):
        continue
    fp = os.path.join(ARTICLES_DIR, fn)
    with open(fp, 'r', encoding='utf-8') as f:
        head = f.read(3000)
    m = re.search(r'^permalink:\s*/(.+?)\s*$', head, re.MULTILINE)
    if m:
        permalink = m.group(1).strip('/')
        slug = permalink.split('/')[-1]
        url = 'articles/' + slug
        SLUG_TO_FILE[url] = fp

print(f"源文件映射: {len(SLUG_TO_FILE)} 篇")

# ─── 1. 更新源文章 frontmatter ───────────────────────────
updated_src = 0
for url, new_cat in NEW_CATS.items():
    fp = SLUG_TO_FILE.get(url)
    if not fp or not os.path.exists(fp):
        print(f"  ✗ 未找到源文件: {url}")
        continue
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()
    old = content
    content = re.sub(
        r'^(category:\s*)\S+',
        r'\g<1>' + new_cat,
        content, count=1, flags=re.MULTILINE
    )
    if content == old:
        print(f"  ⚠  category 未替换: {os.path.basename(fp)}")
    else:
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(content)
        updated_src += 1
        print(f"  ✓ {os.path.basename(fp)} → {new_cat}")

print(f"源文件已更新: {updated_src}/{len(NEW_CATS)}")

# ─── 2. 更新 home-insights.json ─────────────────────────────
HI_PATH = os.path.normpath(os.path.join(BASE, '..', 'source', 'home-insights.json'))
with open(HI_PATH, 'r', encoding='utf-8') as f:
    hi = json.load(f)

hi_updated = 0
for art in hi['articles']:
    url = art['url']
    if url in NEW_CATS and art.get('category') != NEW_CATS[url]:
        old_cat = art.get('category', '')
        art['category'] = NEW_CATS[url]
        hi_updated += 1
        print(f"  home-insights: {art['title'][:28]}  {old_cat}→{NEW_CATS[url]}")

if hi_updated:
    with open(HI_PATH, 'w', encoding='utf-8') as f:
        json.dump(hi, f, ensure_ascii=False, indent=2)
        f.write('\n')
print(f"home-insights.json 已更新: {hi_updated}")

# ─── 3. 更新 search-index.json ─────────────────────────────
SI_PATH = os.path.normpath(os.path.join(BASE, '..', 'source', 'search-index.json'))
with open(SI_PATH, 'r', encoding='utf-8') as f:
    si = json.load(f)

si_updated = 0
for entry in si:
    url = entry.get('url', '')
    if url in NEW_CATS:
        if entry.get('category') != NEW_CATS[url]:
            entry['category'] = NEW_CATS[url]
            si_updated += 1

if si_updated:
    with open(SI_PATH, 'w', encoding='utf-8') as f:
        json.dump(si, f, ensure_ascii=False, indent=2)
        f.write('\n')
print(f"search-index.json 已更新: {si_updated}")

# ─── 4. 更新法税洞察页 ───────────────────────────────────
ARCHIVES_PATH = os.path.normpath(
    os.path.join(BASE, '..', 'source', 'archives', '法税洞察(source).html')
)
with open(ARCHIVES_PATH, 'r', encoding='utf-8') as f:
    archives = f.read()

archives_updated = 0
for url, new_cat in NEW_CATS.items():
    # 找到包含 data-url="url" 的 article-item 块
    # 然后替换其中的 <span class="article-tag" data-category="OLD">OLD</span>
    idx = archives.find(f'data-url="{url}"')
    if idx == -1:
        print(f"  ✗ 法税洞察页未找到: {url}")
        continue

    # 从 idx 开始找后续的 </div> 结束该 article-item
    # 简单方法：找最近的 article-tag span 并替换
    end_idx = archives.find('</div>', idx)
    block = archives[idx:end_idx + 6]

    old_span = re.search(r'<span class="article-tag" data-category="[^"]+">[^<]+</span>', block)
    if not old_span:
        print(f"  ⚠  未找到 article-tag: {url}")
        continue

    old_text = old_span.group(0)
    new_span = f'<span class="article-tag" data-category="{new_cat}">{new_cat}</span>'
    if old_text == new_span:
        continue

    archives = archives[:idx] + archives[idx:end_idx + 6].replace(old_text, new_span) + archives[idx + len(block):]
    archives_updated += 1
    print(f"  法税洞察页: {url} → {new_cat}")

if archives_updated:
    with open(ARCHIVES_PATH, 'w', encoding='utf-8') as f:
        f.write(archives)
print(f"法税洞察页已更新: {archives_updated}")

# ─── 5. 验证新分布 ─────────────────────────────────────────
from collections import Counter
new_dist = Counter(a['category'] for a in hi['articles'])
print(f"\n=== 新分类分布 ===")
for cat, cnt in new_dist.most_common():
    print(f"  {cat}: {cnt} 篇")
print(f"  合计: {sum(new_dist.values())} 篇")
