#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把搜索页中的 goToArchives() 替换为 applyFilters()（onchange 属性值）"""
import os

path = r'C:\Users\26726\WorkBuddy\2026-05-20-21-20-24\source\search.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old = 'onchange="goToArchives()"'
new = 'onchange="applyFilters()"'
count = content.count(old)
print(f'找到 {count} 处 goToArchives()，替换为 applyFilters()')

content = content.replace(old, new)

with open(path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(content)

print('✅ 替换完成')
