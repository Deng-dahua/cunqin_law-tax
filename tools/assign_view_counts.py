"""为法税洞察页11篇新文章分配随机基础阅读量"""
import re, random

path = 'C:/Users/26726/WorkBuddy/2026-05-20-21-20-24/source/archives/法税洞察(source).html'
with open(path, encoding='utf-8') as f:
    lines = f.readlines()

# 按日期分档的基础阅读量范围
ranges = {
    '2026-05-22': (300, 600),
    '2026-05-21': (200, 500),
    '2026-05-20': (150, 400),
}

changed = 0
for i, line in enumerate(lines):
    if 'data-views="100"' not in line:
        continue
    m_date = re.search(r'data-date="([^"]+)"', line)
    if not m_date:
        continue
    date = m_date.group(1)
    lo, hi = ranges.get(date, (150, 300))
    new_val = random.randint(lo, hi)
    lines[i] = line.replace('data-views="100"', f'data-views="{new_val}"')
    changed += 1
    print(f'  Line {i+1}: {date} → views={new_val}')

print(f'\nChanged {changed} lines')

if changed > 0:
    with open(path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print('File updated successfully')
else:
    print('No changes made')
