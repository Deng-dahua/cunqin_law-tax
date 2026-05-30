#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全站删除 countapi.xyz 相关代码（77篇文章）
精确删除：包含 countapi.xyz 的整段 <script>...</script>
"""
import os, re, glob

source_dir = 'source/articles'
files = sorted(glob.glob(os.path.join(source_dir, '*(source).html')))
print(f'找到 {len(files)} 个文件')

count = 0
for fp in files:
    with open(fp, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # 找到包含 countapi.xyz 的行范围（从 <script> 到 </script>）
    new_lines = []
    skip = False
    i = 0
    while i < len(lines):
        line = lines[i]
        # 检测是否进入含 countapi 的 script 块
        if '<script>' in line and 'countapi' in line:
            skip = True
            i += 1
            continue
        # 如果在 skip 模式，检查是否到了 </script>
        if skip:
            if '</script>' in line:
                skip = False
                i += 1
                continue
            i += 1
            continue
        # 也检查单行 script（<script>...</script> 在同一行）
        if '<script>' in line and '</script>' in line and 'countapi' in line:
            i += 1
            continue
        new_lines.append(line)
        i += 1

    if len(new_lines) < len(lines):
        with open(fp, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        count += 1

print(f'成功处理 {count}/{len(files)} 个文件')
