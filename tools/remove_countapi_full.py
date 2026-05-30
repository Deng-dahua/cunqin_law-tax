#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全站删除 countapi.xyz 相关代码
- 77篇文章：删除 countapi.xyz fetch/hit JS + art-meta 中的阅读量 span
- 不打印中文到 stdout（避免 Windows 终端乱码）
"""
import os
import re
import glob

SOURCE_DIR = os.path.join(os.path.dirname(__file__), '..', 'source', 'articles')
pattern = os.path.join(SOURCE_DIR, '*(source).html')

files = sorted(glob.glob(pattern))
print(f'Found {len(files)} article files, removing countapi.xyz...')

modified = 0
errors = []

for fp in files:
    try:
        with open(fp, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        
        # 1. 删除 </body> 前或 </html> 前的 countapi.xyz JS 区块
        #    匹配  fetch('https://api.countapi.xyz 到 </script> 的完整块
        content = re.sub(
            r'\s*<script>\s*fetch\([\'"]https://api\.countapi\.xyz.*?</script>\s*',
            '',
            content,
            flags=re.DOTALL
        )
        
        # 2. 删除 window.addEventListener('DOMContentLoaded'...) 中的 countapi hit JS
        content = re.sub(
            r'\s*<script>\s*window\.addEventListener\([\'"]DOMContentLoaded[\'"].*?</script>\s*',
            '',
            content,
            flags=re.DOTALL
        )
        
        # 3. 删除文章 meta 行中的阅读量 <span class="art-view-count">...</span>
        content = re.sub(
            r'\s*<span class="art-view-count"[^>]*>.*?</span>',
            '',
            content
        )
        
        # 4. 删除文章底部阅读量显示区块（如有）
        content = re.sub(
            r'\s*<div class="article-views"[^>]*>.*?</div>',
            '',
            content,
            flags=re.DOTALL
        )
        
        if content != original:
            with open(fp, 'w', encoding='utf-8') as f:
                f.write(content)
            modified += 1
    except Exception as e:
        errors.append((os.path.basename(fp), str(e)))

print(f'Done: {modified}/{len(files)} articles modified')
if errors:
    print('Errors:')
    for name, err in errors:
        print(f'  {name}: {err}')

# Verify: random sample check (no Chinese chars)
import random
sample = random.sample(files, min(5, len(files)))
print('\nSample verification (expect False/False):')
for fp in sample:
    with open(fp, 'r', encoding='utf-8') as f:
        c = f.read()
    has_countapi = 'countapi.xyz' in c
    has_view_span = 'art-view-count' in c
    print(f'  {os.path.basename(fp)[:45]}: countapi={has_countapi}, span={has_view_span}')
