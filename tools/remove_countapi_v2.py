#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全站删除 countapi.xyz 相关代码（77篇文章）
"""
import os, re, glob

source_dir = 'source/articles'
files = sorted(glob.glob(os.path.join(source_dir, '*(source).html')))
print(f'找到 {len(files)} 个文件')

# 要删除的块：
# 1. <script>...</script> 中包含 countapi.xyz 的整个 script 块
# 2. HTML 中的 <span id="articleViewCount">...</span> 或类似阅读量展示元素
# 3. JS 中获取/展示阅读量的代码

pattern_script = re.compile(
    r'<script>\s*\(function\(\)\{[^<]*var viewEl[^<]*countapi[^<]*\}?\);\s*</script>',
    re.DOTALL
)

count = 0
for fp in files:
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # 删除包含 countapi.xyz 的整个 script 块
    # 匹配从 <script> 到 </script>，中间包含 countapi
    # 使用非贪婪匹配，但要跨行
    def replacer(m):
        return ''
    
    # 方法：找到所有 <script>...</script> 块，检查是否含 countapi
    # 用正则把含 countapi 的 script 块删掉
    new_content = re.sub(
        r'<script>\s*\n?\s*\(function\(\)\{[^}]*countapi[^}]*\}\)\(\);\s*\n?\s*</script>\n?',
        '',
        content,
        flags=re.DOTALL
    )
    
    # 如果上面没匹配到，用更宽泛的方式
    if new_content == content:
        # 更宽泛：匹配任何包含 countapi 的 script 块
        new_content = re.sub(
            r'<script>[^<]*\(function\(\)\{.*?countapi.*?\}\)\(\);\s*</script>',
            '',
            content,
            flags=re.DOTALL
        )
    
    if new_content != original:
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(new_content)
        count += 1

print(f'成功处理 {count}/{len(files)} 个文件')
