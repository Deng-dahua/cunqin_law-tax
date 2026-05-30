#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全站删除 77 篇文章中的 countapi.xyz 代码块
将日志写入文件，避免终端编码问题
"""
import os, glob, re

source_dir = 'source/articles'
log_path = 'tools/remove_countapi_log.txt'

files = sorted(glob.glob(os.path.join(source_dir, '*(source).html')))
print(f'找到 {len(files)} 个文件')

count = 0
failed = []

for fp in files:
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # 方法1：删除包含 countapi.xyz 的整个 <script>...</script> 块
    # 精确匹配从 <script> 开始到 </script> 结束，中间含 countapi
    # 使用非贪婪匹配，跨行
    new_content = re.sub(
        r'<script>\s*\n?\s*\(function\(\)\{[^}]*?countapi[^}]*?\}\)\(\);\s*\n?\s*</script>\n?',
        '',
        content,
        flags=re.DOTALL
    )
    
    # 如果没匹配到，用更宽泛的方式：按行处理
    if new_content == content:
        lines = content.split('\n')
        new_lines = []
        skip_block = False
        script_tag_line = -1
        
        i = 0
        while i < len(lines):
            line = lines[i]
            
            # 检测进入含 countapi 的 script 块（单行）
            if '<script>' in line and 'countapi' in line and '</script>' in line:
                i += 1
                continue
            
            # 检测进入含 countapi 的 script 块（多行）
            if '<script>' in line and 'countapi' in line:
                skip_block = True
                script_tag_line = i
                i += 1
                continue
            
            if skip_block:
                if '</script>' in line:
                    skip_block = False
                    script_tag_line = -1
                    i += 1
                    continue
                i += 1
                continue
            
            new_lines.append(line)
            i += 1
        
        new_content = '\n'.join(new_lines)
    
    if new_content != original:
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(new_content)
        count += 1

# 写日志文件
with open(log_path, 'w', encoding='utf-8') as f:
    f.write(f'处理完成：{count}/{len(files)} 个文件\n')
    if failed:
        f.write(f'失败：{len(failed)} 个\n')
        for fp in failed:
            f.write(f'  {fp}\n')

print(f'成功处理 {count}/{len(files)} 个文件')
print(f'日志已写入 {log_path}')
