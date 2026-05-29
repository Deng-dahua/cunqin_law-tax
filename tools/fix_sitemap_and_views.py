#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""修复 sitemap.xml：补缺失URL + 删重复条目；清零法税洞察页 data-views"""

import re, json, os
from collections import Counter

# ============================================================
#  Part 1: 修复 sitemap.xml
# ============================================================
SITEMAP = 'source/sitemap.xml'
with open(SITEMAP, 'r', encoding='utf-8') as f:
    sm_content = f.read()

# 用正则提取所有 <url>...</url> 块（DOTALL 模式匹配多行）
url_pattern = re.compile(r'(<url>\s*<loc>https://cunqin\.tax/(.+?)</loc>.*?</url>)', re.DOTALL)
url_blocks = url_pattern.findall(sm_content)

print(f'[sitemap] 总 <url> 条目: {len(url_blocks)}')

# 找出重复的 URL（去重：每个 URL 只保留第一次出现）
url_list = [m[1].rstrip('/') for m in url_blocks]
counter = Counter(url_list)
dups = {u: c for u, c in counter.items() if c > 1}
print(f'[sitemap] 重复 URL: {len(dups)} 个')
for u, c in sorted(dups.items()):
    print(f'  [x{c}] {u}')

# 构建新内容：按原始顺序，每个 URL 只保留第一次出现
seen = set()
keep_blocks = []
for block, url_raw in url_blocks:
    url = url_raw.rstrip('/')
    if url in seen:
        continue
    seen.add(url)
    keep_blocks.append(block)

print(f'[sitemap] 去重后保留: {len(keep_blocks)} 条')

# 检查并添加缺失 URL
expected_missing = ['about/deng-dahua', 'search']
new_entries = ''
now = '2026-05-30'

def make_entry(url, priority='0.6'):
    if not url.endswith('/'):
        url_disp = url + '/'
    else:
        url_disp = url
    return f'''  <url>
    <loc>https://cunqin.tax/{url_disp}</loc>
    <lastmod>{now}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>{priority}</priority>
    <xhtml:link rel="alternate" hreflang="zh-CN" href="https://cunqin.tax/{url_disp}"/>
  </url>\n'''

for url in expected_missing:
    key = url.rstrip('/')
    if key not in seen:
        entry = make_entry(key)
        new_entries += entry
        seen.add(key)
        print(f'[sitemap] 将添加: {key}/')

# 重新组装 sitemap
# 提取 XML 声明和 <urlset> 开头
xml_decl_match = re.match(r'<\?xml[^?]*\?>', sm_content)
urlset_open_match = re.search(r'(<urlset[^>]*>)', sm_content)
assert xml_decl_match and urlset_open_match, 'sitemap 格式异常'

new_sitemap = xml_decl_match.group(0) + '\n' + urlset_open_match.group(1) + '\n'
for block in keep_blocks:
    new_sitemap += block + '\n'
new_sitemap += new_entries
new_sitemap += '</urlset>\n'

with open(SITEMAP, 'w', encoding='utf-8') as f:
    f.write(new_sitemap)

# 验证
with open(SITEMAP, 'r', encoding='utf-8') as f:
    v = f.read()
v_urls = re.findall(r'<loc>https://cunqin\.tax/(.+?)</loc>', v)
v_counter = Counter(v_urls)
v_dups = {u: c for u, c in v_counter.items() if c > 1}
print(f'[sitemap] 验证: {len(v_urls)} 条, 重复: {len(v_dups)} 个')
assert len(v_dups) == 0, f'还有重复: {v_dups}'
for em in expected_missing:
    key = em.rstrip('/') + '/'
    full = 'https://cunqin.tax/' + key
    assert full in v, f'缺失: {em}'
print('[sitemap] ✓ 验证通过')

# ============================================================
#  Part 2: 清零法税洞察页 data-views
# ============================================================
ARCHIVES = 'source/archives/法税洞察(source).html'
with open(ARCHIVES, 'r', encoding='utf-8') as f:
    content = f.read()

pattern = r'data-views="\d+"'
matches = re.findall(pattern, content)
print(f'\n[archives] 找到 {len(matches)} 处 data-views')
if matches:
    vals = Counter(matches)
    print(f'[archives] 当前值分布: {dict(vals)}')
    new_content = re.sub(pattern, 'data-views="0"', content)
    with open(ARCHIVES, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print('[archives] ✓ 全部清零为 data-views="0"')
else:
    print('[archives] 未找到 data-views，无需修改')

# ============================================================
#  Part 3: 确认 home-insights.json 已清零
# ============================================================
HI = 'source/home-insights.json'
if os.path.exists(HI):
    with open(HI, 'r', encoding='utf-8') as f:
        hi = json.load(f)
    non_zero = sum(1 for a in hi['articles'] if a.get('views', 0) > 0)
    print(f'\n[home-insights.json] 非零 views: {non_zero}/{len(hi["articles"])}')
    if non_zero > 0:
        print('[home-insights.json] 警告: 还有非零值！')
    else:
        print('[home-insights.json] ✓ 全部为零')

print('\n全部完成！')
