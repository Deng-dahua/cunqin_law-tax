import os, json

src = r'C:\Users\26726\WorkBuddy\2026-05-20-21-20-24\source'
old1 = 'https://deng-dahua.github.io/cunqin_law-tax/'
old2 = 'https://deng-dahua.github.io/cunqin_law-tax'
new = 'https://cunqin.tax/'

count = 0
files = []
for root, dirs, fnames in os.walk(src):
    for f in fnames:
        if f.endswith('.html') or f in ('CNAME','sitemap.xml','robots.txt'):
            files.append(os.path.join(root, f))

for fpath in files:
    with open(fpath, 'r', encoding='utf-8') as fh:
        content = fh.read()
    changed = False
    if old1 in content:
        content = content.replace(old1, new)
        changed = True
    if old2 in content:
        content = content.replace(old2, new.rstrip('/'))
        changed = True
    if changed:
        with open(fpath, 'w', encoding='utf-8') as fh:
            fh.write(content)
        count += 1
        print('  [已替换]', os.path.relpath(fpath, src))

# search-index.json
sij = os.path.join(src, 'search-index.json')
with open(sij, 'r', encoding='utf-8') as fh:
    data = json.load(fh)
sij_count = 0
for item in data:
    u = item.get('url', '')
    if u.startswith('/cunqin_law-tax/'):
        item['url'] = '/' + u[len('/cunqin_law-tax/'):]
        sij_count += 1
if sij_count:
    with open(sij, 'w', encoding='utf-8') as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
    print('  [已更新] search-index.json (' + str(sij_count) + ' 条)')

print()
print('共替换', count, '个文件')
