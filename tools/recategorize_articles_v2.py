#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将法税洞察页和 home-insights.json 中的 11 篇文章从"跨境税务"改为新分类。
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

# ─── 1. 更新 home-insights.json ─────────────────────────────
HI_PATH = os.path.normpath(os.path.join(BASE, '..', 'source', 'home-insights.json'))
with open(HI_PATH, 'r', encoding='utf-8') as f:
    hi = json.load(f)

hi_updated = 0
for art in hi['articles']:
    url = art['url']
    if url in NEW_CATS and art.get('category') != NEW_CATS[url]:
        old = art.get('category', '')
        art['category'] = NEW_CATS[url]
        hi_updated += 1
        print(f"  home-insights: {art['title'][:30]}  {old}→{NEW_CATS[url]}")

if hi_updated:
    with open(HI_PATH, 'w', encoding='utf-8') as f:
        json.dump(hi, f, ensure_ascii=False, indent=2)
        f.write('\n')
print(f"home-insights.json 已更新: {hi_updated}")

# ─── 2. 更新法税洞察页 ─────────────────────────────────────
ARCHIVES_PATH = os.path.normpath(
    os.path.join(BASE, '..', 'source', 'archives', '法税洞察(source).html')
)
with open(ARCHIVES_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

archives_updated = 0
for url, new_cat in NEW_CATS.items():
    # 找到包含 data-url="url" 的 article-item 块
    # 替换其中的 <span class="article-tag" data-category="OLD">OLD</span>
    old_pattern = re.compile(
        r'(<div class="article-item"[^>]*data-url="' + re.escape(url) +
        r'"[^>]*>.*?<span class="article-tag" data-category=")[^"]+(">)[^<]+(</span>)',
        re.DOTALL
    )
    m = old_pattern.search(content)
    if m:
        old_cat = content[m.start(3):m.end(3)].strip('</span>')
        new_span = f'{m.group(1)}{new_cat}{m.group(2)}{new_cat}{m.group(3)}'
        content = content[:m.start()] + new_span + content[m.end():]
        archives_updated += 1
        print(f"  法税洞察页: {url}  {old_cat}→{new_cat}")
    else:
        print(f"  ✗ 未找到: {url}")

if archives_updated:
    with open(ARCHIVES_PATH, 'w', encoding='utf-8') as f:
        f.write(content)
print(f"法税洞察页已更新: {archives_updated}")

# ─── 3. 更新 search-index.json ──────────────────────────────
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

# ─── 4. 验证新分布 ─────────────────────────────────────────
from collections import Counter
new_dist = Counter(a['category'] for a in hi['articles'])
print(f"\n=== 新分类分布 ===")
for cat, cnt in new_dist.most_common():
    print(f"  {cat}: {cnt} 篇")
print(f"  合计: {sum(new_dist.values())} 篇")
