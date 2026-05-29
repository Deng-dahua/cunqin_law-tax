#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将法税洞察页中所有"跨境税务"相关标记，改为新的分类。
同时删除筛选下拉框中的"跨境税务"选项。
"""
import re, os, sys
sys.stdout = sys.stderr = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)

BASE = os.path.dirname(os.path.abspath(__file__)) or '.'

# URL（相对于 archives 页的路径）-> 新分类
NEW_CATS = {
    "../articles/beps-2.0-qiye-yingdui.html":           "政策解读",
    "../articles/kuajing-fuwu-maoyi-shuiwu.html":       "税务实务",
    "../articles/zhuanrang-dingjia-tongqi-ziliao.html":  "税务实务",
    "../articles/tan-guan-shui-cbam-chukou.html":        "政策解读",
    "../articles/jingwai-suode-dijiang-zhinan.html":      "税务实务",
    "../articles/zhuanrang-dingjia-guanlian-jiaoyi.html": "税务实务",
    "../articles/chukou-tuishui-hegui-fengkong.html":     "税务实务",
    "../articles/CRS-kuajing-zichan-shenbao.html":       "税务实务",
    "../articles/shuishou-xieding-daiyu-shenqing.html":   "税务实务",
    "../articles/odi-beian-quanliucheng.html":            "税务实务",
    "../articles/kuajing-dianshang-shuiwu.html":           "行业洞察",
}

ARCHIVES_PATH = os.path.normpath(
    os.path.join(BASE, '..', 'source', 'archives', '法税洞察(source).html')
)

with open(ARCHIVES_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

updated = 0

# ── 1. 替换每篇 article-item 中的 data-category 和 article-tag ─────
for url, new_cat in NEW_CATS.items():
    # 1a. 替换 data-category="跨境税务"
    old_dc = f'data-category="跨境税务"'
    new_dc = f'data-category="{new_cat}"'
    if old_dc in content:
        content = content.replace(old_dc, new_dc, 1)
        updated += 1
        print(f"  ✓ data-category: {url.split('/')[-1][:30]} → {new_cat}")

    # 1b. 替换 <span class="article-tag">跨境税务</span>
    old_span = f'<span class="article-tag">跨境税务</span>'
    new_span = f'<span class="article-tag">{new_cat}</span>'
    if old_span in content:
        content = content.replace(old_span, new_span, 1)
        # 不重复计数
    elif f'<span class="article-tag">{new_cat}</span>' in content:
        pass  # 已经是对的
    else:
        print(f"  ✗ 未找到 tag span: {url.split('/')[-1]}")

# ── 2. 删除筛选下拉框中的"跨境税务"选项 ─────────────────────
old_option = '<option value="跨境税务">跨境税务</option>'
if old_option in content:
    content = content.replace(old_option, '', 1)
    print("  ✓ 已删除筛选下拉框中的「跨境税务」选项")
else:
    print("  (下拉框中已无「跨境税务」选项，跳过)")

# ── 3. 检查筛选下拉框的选项数量（应为 5 个：全部 + 4 类）──
options = re.findall(r'<option[^>]*>[^<]+</option>', content)
filter_options = [o for o in options if 'value=' in o and ('全部' in o or '税务实务' in o or '企业战略' in o or '政策解读' in o or '行业洞察' in o)]
print(f"\n  筛选下拉框剩余选项: {len(filter_options)} 个")
for o in filter_options:
    print(f"    {o}")

# ── 4. 写回 ────────────────────────────────────────────────────────
with open(ARCHIVES_PATH, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n法税洞察页已更新，共修改 {updated} 处 data-category。")
