#!/usr/bin/env python3
"""Check all article related-reading titles match actual article titles - v2."""
import re, os, sys
sys.stdout.reconfigure(encoding='utf-8')

BASE = os.path.dirname(os.path.abspath(__file__))
ARTICLES_DIR = os.path.join(BASE, '..', 'source', 'articles')

# Build slug -> actual title map
slug_to_title = {}
for f in sorted(os.listdir(ARTICLES_DIR)):
    if not f.endswith('.html'):
        continue
    fpath = os.path.join(ARTICLES_DIR, f)
    with open(fpath, encoding='utf-8') as fh:
        content = fh.read()
    m = re.search(r'permalink:\s*/articles/([\w-]+)\.html', content)
    if not m:
        continue
    slug = m.group(1)
    # Extract title: find <title>...</title> then strip trailing site name
    mt = re.search(r'<title>(.*?)</title>', content, re.DOTALL)
    if mt:
        raw = mt.group(1).strip()
        # Remove trailing " | 存勤法税" or "｜存勤法税"
        raw = re.sub(r'\s*[|｜]\s*存勤法税.*$', '', raw)
        raw = re.sub(r'\s*-\s*存勤法税.*$', '', raw)
        slug_to_title[slug] = raw.strip()

print(f'共扫描 {len(slug_to_title)} 篇文章的标题')
# Show a few examples
for s, t in list(slug_to_title.items())[:3]:
    print(f'  {s} -> "{t}"')

# Scan each article's related-reading h4
mismatches = 0
for fname in sorted(os.listdir(ARTICLES_DIR)):
    if not fname.endswith('.html'):
        continue
    fpath = os.path.join(ARTICLES_DIR, fname)
    with open(fpath, encoding='utf-8') as fh:
        content = fh.read()
    
    my_slug_m = re.search(r'permalink:\s*/articles/([\w-]+)\.html', content)
    my_slug = my_slug_m.group(1) if my_slug_m else fname
    
    related = re.findall(
        r'<a href="([\w-]+\.html)"[^>]*>.*?<h4>(.*?)</h4>',
        content, re.DOTALL
    )
    for href, h4_text in related:
        target_slug = href.replace('.html', '')
        actual_title = slug_to_title.get(target_slug, '')
        h4_clean = h4_text.strip()
        if not actual_title:
            status = '(文章不存在)'
            mismatches += 1
            print(f'  [MISSING] {fname} -> {href}')
        elif h4_clean != actual_title:
            mismatches += 1
            print(f'  [MISMATCH] {fname}')
            print(f'    显示: "{h4_clean}"')
            print(f'    实际: "{actual_title}"')
            print()

if mismatches == 0:
    print('\n所有延伸阅读标题与实际文章标题一致')
else:
    print(f'\n共 {mismatches} 处需处理')
