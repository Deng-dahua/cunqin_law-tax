#!/usr/bin/env python3
"""批量修复 </div></section> 合并成一行的问题"""
import os

src = r'C:\Users\26726\WorkBuddy\2026-05-20-21-20-24\source'
count = 0

for root, dirs, files in os.walk(src):
    for fn in files:
        if not fn.endswith('.html'):
            continue
        fpath = os.path.join(root, fn)
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        if '</div></section>' not in content:
            continue
        new_content = content.replace('</div></section>', '</div>\n</section>')
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        count += 1
        rel = os.path.relpath(fpath, src).replace('\\', '/')
        print(f'已修复: {rel}')

print(f'\n共修复 {count} 个文件')
