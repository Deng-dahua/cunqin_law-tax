"""Add 4 missing articles to the archives/法税洞察 page."""
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 4 missing articles metadata from source files
articles = [
    {
        'url': 'articles/qishui-zhengce-jiedu.html',
        'file': 'source/articles/qishui-zhengce-jiedu(source).html',
    },
    {
        'url': 'articles/qiye-fenli-shuiwu-chuli.html',
        'file': 'source/articles/qiye-fenli-shuiwu-chuli(source).html',
    },
    {
        'url': 'articles/xiaofeishui-shuiwu-guihua.html',
        'file': 'source/articles/xiaofeishui-shuiwu-guihua(source).html',
    },
    {
        'url': 'articles/ziyuanshui-huanbao-shuiwu.html',
        'file': 'source/articles/ziyuanshui-huanbao-shuiwu(source).html',
    },
]

# Extract metadata from each source file
for a in articles:
    with open(a['file'], 'r', encoding='utf-8') as f:
        content = f.read()
    
    # title
    tm = re.search(r'<title>(.+?)(?:\s*[-|]\s*存勤法税.*)?</title>', content)
    a['title'] = tm.group(1).strip() if tm else 'UNKNOWN'
    a['title'] = a['title'].replace('&quot;','"').replace('&amp;','&').replace('&lt;','<').replace('&gt;','>')
    
    # date
    dm = re.search(r'date:\s*(\d{4}-\d{2}-\d{2})', content)
    a['date'] = dm.group(1) if dm else '2026-05-01'
    
    # category
    cm = re.search(r'category:\s*(\S+)', content)
    a['category'] = cm.group(1).strip() if cm else '税务实务'
    
    # views
    vm = re.search(r'var base = (\d+)', content)
    a['views'] = int(vm.group(1)) if vm else 0
    
    # excerpt - try meta description first, then og:description
    em = re.search(r'<meta\s+name="description"\s+content="(.+?)"', content)
    if not em:
        em = re.search(r'<meta\s+property="og:description"\s+content="(.+?)"', content)
    excerpt = em.group(1).strip() if em else '暂无摘要'
    # Clean up excerpt - remove brand text that appears in meta
    excerpt = re.sub(r'，\s*适用于.+$', '。', excerpt)
    excerpt = re.sub(r'，\s*帮助.+$', '。', excerpt)
    if len(excerpt) > 120:
        excerpt = excerpt[:117] + '...'
    a['excerpt'] = excerpt
    
    # Slug for href
    a['slug'] = a['url'].replace('articles/', '').replace('.html', '')

# Sort by views descending
articles.sort(key=lambda x: x['views'], reverse=True)

print("=== 4 articles to add (sorted by views) ===")
for a in articles:
    print(f"  {a['slug']}: views={a['views']}, category={a['category']}, date={a['date']}")
    print(f"    Title: {a['title'][:60]}...")
    print()

# Generate article-item HTML blocks
def format_date(date_str):
    """2026-05-01 -> 2026.05.01"""
    return date_str.replace('-', '.')

def gen_article_item(a):
    date_formatted = format_date(a['date'])
    return f"""      <a href="../{a['url']}" class="article-item" data-date="{a['date']}" data-category="{a['category']}" data-views="{a['views']}">
        <div class="article-content">
          <h3>{a['title']}</h3>
          <p>{a['excerpt']}</p>
          <div class="article-meta-row">
            <span class="article-tag">{a['category']}</span>
            <span class="article-date-text"><i class="fas fa-calendar-alt"></i> {date_formatted}</span>
            <span class="article-views"><i class="fas fa-eye"></i> {a['views']}</span>
          </div>
        </div>
        <div class="article-arrow"><i class="fas fa-chevron-right"></i></div>
      </a>"""

# Read the archives page
with open('source/archives/法税洞察(source).html', 'r', encoding='utf-8') as f:
    page = f.read()

# Find insertion point: after the last article with views > these 4
# The 4 new articles have views 360-450. Find articles with views around 150.
# Insert before the first 150-view article.
# Anchor: the line before qianshui-guanli-jiuji (views=150)
anchor = '      <a href="../articles/qianshui-guanli-jiuji.html" class="article-item"'
if anchor not in page:
    print("ERROR: anchor not found!")
    sys.exit(1)

# Generate the 4 article-item blocks
new_blocks = '\n'.join(gen_article_item(a) for a in articles)

# Insert before the anchor
page = page.replace(anchor, new_blocks + '\n' + anchor)

# Write back
with open('source/archives/法税洞察(source).html', 'w', encoding='utf-8') as f:
    f.write(page)

# Verify
count = page.count('class="article-item"')
print(f"After update: {count} article-item entries")

# Verify each slug is present
for a in articles:
    if a['slug'] in page:
        print(f"  OK: {a['slug']}")
    else:
        print(f"  MISSING: {a['slug']}")

print("\nDone!")
