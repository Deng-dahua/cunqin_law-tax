import re, os

files = sorted([f for f in os.listdir('source/articles') if f.endswith('.html')])
print('=== 现有19篇文章 ===')
for i, f in enumerate(files, 1):
    path = os.path.join('source/articles', f)
    with open(path, 'r', encoding='utf-8') as fh:
        content = fh.read()
    title = re.search(r'<h1>([^<]+)</h1>', content)
    permalink = re.search(r'permalink:\s*(\S+)', content)
    slug = permalink.group(1) if permalink else 'N/A'
    print(f'{i:02d}. {title.group(1) if title else f}')
    print(f'    slug: {slug}')
