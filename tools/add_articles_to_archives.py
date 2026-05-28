#!/usr/bin/env python3
"""Add 8 new GEO articles to the archives page (法税洞察)"""
import re, os, sys
sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r'C:\Users\26726\WorkBuddy\2026-05-20-21-20-24'
SOURCE_DIR = os.path.join(BASE_DIR, 'source')
ARTICLES_DIR = os.path.join(SOURCE_DIR, 'articles')
ARCHIVES_PATH = os.path.join(SOURCE_DIR, 'archives', '法税洞察(source).html')

slugs_to_add = [
    'beps-2.0-qiye-yingdui',
    'jinrong-qiye-shuiwu-hegui',
    'jizheng-jitui-zhengce',
    'keji-chengguo-zhuanhua-shuiwu',
    'kuajing-fuwu-maoyi-shuiwu',
    'qianshui-guanli-jiuji',
    'zhizaoye-shuiwu-chouhua',
    'zhuanrang-dingjia-tongqi-ziliao'
]

# Step 1: Extract article info
articles = []
for slug in slugs_to_add:
    found = False
    for fname in os.listdir(ARTICLES_DIR):
        if '(source).html' not in fname:
            continue
        path = os.path.join(ARTICLES_DIR, fname)
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            if f'permalink: /articles/{slug}.html' not in content:
                continue
            
            # Title from <title>
            title_m = re.search(r'<title>(.*?)</title>', content)
            title = title_m.group(1).strip() if title_m else slug
            title = title.split(' - 存勤')[0].strip()
            
            # Description excerpt (80 chars from meta description)
            desc_m = re.search(r'<meta name="description" content="([^"]+)"', content)
            desc = desc_m.group(1).strip()[:100] if desc_m else title[:80]
            
            # Date
            date_m = re.search(r'property="article:published_time" content="(\d{4}-\d{2}-\d{2})"', content)
            date = date_m.group(1) if date_m else '2026-05-27'
            
            # Category from keywords
            kw_m = re.search(r'<meta name="keywords" content="([^"]+)"', content)
            keywords = kw_m.group(1) if kw_m else ''
            if '稽查' in keywords:
                cat = '税务稽查'
            elif '个税' in keywords or '个人所得税' in keywords:
                cat = '个税合规'
            elif '跨境' in keywords or '国际税' in keywords or 'BEPS' in keywords:
                cat = '国际税收'
            elif '增值税' in keywords:
                cat = '增值税'
            else:
                cat = '税务实务'
            
            articles.append({
                'slug': slug, 'title': title, 'date': date,
                'category': cat, 'views': 150, 'excerpt': desc
            })
            found = True
            break
    
    if not found:
        print(f'[WARN] Not found: {slug}')

print(f'Extracted {len(articles)} articles')

# Step 2: Sort by date descending
articles.sort(key=lambda x: x['date'], reverse=True)

# Step 3: Generate article-item HTML
cards = []
for a in articles:
    date_parts = a['date'].split('-')
    date_display = f'{date_parts[0]}.{date_parts[1]}.{date_parts[2]}'
    card = f'''      <a href="../articles/{a['slug']}.html" class="article-item" data-date="{a['date']}" data-category="{a['category']}" data-views="{a['views']}">
        <div class="article-content">
          <h3>{a['title']}</h3>
          <p>{a['excerpt']}</p>
          <div class="article-meta-row">
            <span class="article-tag">{a['category']}</span>
            <span class="article-date-text"><i class="fas fa-calendar-alt"></i> {date_display}</span>
            <span class="article-views"><i class="fas fa-eye"></i> {a['views']}</span>
          </div>
        </div>
        <div class="article-arrow"><i class="fas fa-chevron-right"></i></div>
      </a>'''
    cards.append(card)

# Step 4: Read archives page
with open(ARCHIVES_PATH, 'r', encoding='utf-8') as f:
    archives_content = f.read()

# Step 5: Find insertion point - right after article-list div opening
article_list_marker = '<div class="article-list" id="articleList">'
insert_pos = archives_content.find(article_list_marker)
if insert_pos < 0:
    print('ERROR: Could not find article-list div!')
    sys.exit(1)

# Insert right after the div opening tag + newline
insert_pos += len(article_list_marker) + 1

# Join all cards
cards_html = '\n'.join(cards) + '\n\n'

# Insert
new_content = archives_content[:insert_pos] + cards_html + archives_content[insert_pos:]

# Step 6: Write back
with open(ARCHIVES_PATH, 'w', encoding='utf-8') as f:
    f.write(new_content)

# Verify
article_count = new_content.count('class="article-item"')
print(f'Updated archives page: {article_count} article-item entries (was {archives_content.count("class=\"article-item\"")})')
print(f'Added {len(articles)} new articles:')
for a in articles:
    print(f'  [{a["date"]}] {a["slug"]} → {a["title"][:60]}')
