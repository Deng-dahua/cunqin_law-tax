#!/usr/bin/env python3
"""
更新法税洞察页、search-index.json、sitemap.xml，加入11篇新文章。
"""
import json
import os
import re
import html as html_mod
from datetime import datetime

BASE_DIR = r'C:\Users\26726\WorkBuddy\2026-05-20-21-20-24'
SOURCE_DIR = os.path.join(BASE_DIR, 'source')
JSON_DIR = os.path.join(BASE_DIR, 'tools')
ARTICLES_DIR = os.path.join(SOURCE_DIR, 'articles')
SITE_URL = 'https://cunqin.tax'
TODAY = '2026-05-27'


def load_articles():
    """Load all new articles from JSON batch files"""
    articles = []
    batch_files = ['articles_batch1.json', 'articles_batch2.json', 'articles_batch3.json', 'geo_articles_batch1.json']
    for batch in batch_files:
        path = os.path.join(JSON_DIR, batch)
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                articles.extend(json.load(f))
    return articles


def extract_summary(body_html, max_chars=300):
    """Extract plain text summary from HTML body"""
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', body_html)
    # Remove extra whitespace
    text = re.sub(r'\s+', '', text)
    return text[:max_chars]


def generate_article_card(article):
    """Generate one article-item card HTML for the archives page"""
    slug = article['slug']
    title = article['title']
    category = article.get('category', '实操指南')
    date = article.get('date', '2026-05-20')
    base_views = article.get('base_views', 100)
    
    # Parse date
    parts = date.split('-')
    year_month = f'{parts[0]}.{parts[1]}'
    day = parts[2]
    
    # Generate a short description from body
    body = article.get('body', '')
    text = re.sub(r'<[^>]+>', '', body)
    text = re.sub(r'\s+', '', text)
    desc = text[:80]
    
    # Escape title for HTML
    title_escaped = title.replace('"', '&quot;')
    
    card = f'''      <a href="../articles/{slug}.html" class="article-item" data-date="{date}" data-category="{category}" data-views="{base_views}">
        <div class="article-date">
          <div class="day">{day}</div>
          <div class="month">{year_month}</div>
        </div>
        <div class="article-content">
          <h3>{title_escaped}</h3>
          <p>{desc}</p>
          <span class="article-tag">{category}</span>
</div>
        <div class="article-arrow"><i class="fas fa-chevron-right"></i></div>
      </a>'''
    return card


def update_archives_page(articles):
    """Insert 11 new article cards into the archives page"""
    page_path = os.path.join(SOURCE_DIR, 'archives', '法税洞察(source).html')
    with open(page_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the first article item (after article-list div)
    first_item_marker = '<a href="../articles/yecai-fasui-ronghe.html" class="article-item"'
    insert_pos = content.find(first_item_marker)
    
    if insert_pos < 0:
        print('ERROR: Could not find first article item in archives page!')
        return False
    
    # Generate all 11 new article cards
    cards = []
    for article in articles:
        cards.append(generate_article_card(article))
    
    cards_html = '\n\n'.join(cards) + '\n\n'
    
    # Insert before the first existing article item
    new_content = content[:insert_pos] + cards_html + content[insert_pos:]
    
    with open(page_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f'  [OK] 法税洞察页：插入 {len(cards)} 个新文章卡片')
    return True


def update_search_index(articles):
    """Add 11 new entries to search-index.json"""
    index_path = os.path.join(SOURCE_DIR, 'search-index.json')
    with open(index_path, 'r', encoding='utf-8') as f:
        index = json.load(f)
    
    for article in articles:
        slug = article['slug']
        title = article['title']
        body = article.get('body', '')
        summary = extract_summary(body, 300)
        
        entry = {
            "title": f"{title} - 存勤法税",
            "url": f"/articles/{slug}.html",
            "text": summary
        }
        index.append(entry)
    
    with open(index_path, 'w', encoding='utf-8') as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
    
    print(f'  [OK] search-index.json：新增 {len(articles)} 条，共 {len(index)} 条')


def update_sitemap(articles):
    """Add 11 new URLs to sitemap.xml"""
    sitemap_path = os.path.join(SOURCE_DIR, 'sitemap.xml')
    with open(sitemap_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Generate new URL entries
    url_entries = []
    for article in articles:
        slug = article['slug']
        entry = f'''  <url>
    <loc>{SITE_URL}/articles/{slug}.html</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>'''
        url_entries.append(entry)
    
    # Insert before </urlset>
    insert_marker = '</urlset>'
    insert_pos = content.rfind(insert_marker)
    
    if insert_pos < 0:
        print('ERROR: Could not find </urlset> in sitemap!')
        return False
    
    urls_html = '\n' + '\n'.join(url_entries) + '\n'
    new_content = content[:insert_pos] + urls_html + content[insert_pos:]
    
    with open(sitemap_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    # Count total URLs
    url_count = new_content.count('<loc>')
    print(f'  [OK] sitemap.xml：新增 {len(articles)} 条，共 {url_count} 条')


def apply_skip_render():
    """Update _config.yml skip_render to include new article HTML files"""
    config_path = os.path.join(BASE_DIR, '_config.yml')
    with open(config_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if articles/ is already in skip_render
    if 'articles/' in content:
        # Already covers all articles in the directory
        print('  [OK] skip_render：articles/ 已配置，无需修改')
        return
    
    # Need to add articles/ to skip_render
    # Find the skip_render section
    skip_match = re.search(r'skip_render:.*?(?=\n\w|\Z)', content, re.DOTALL)
    if skip_match:
        print('  [WARN]  skip_render 需要手动检查（articles目录可能未列入）')
    else:
        print('  [WARN]  未找到 skip_render 配置')


def main():
    print('Loading article data...')
    articles = load_articles()
    print(f'Loaded {len(articles)} new articles\n')
    
    # 1. Update archives page
    print('1. Updating 法税洞察页...')
    update_archives_page(articles)
    
    # 2. Update search-index.json
    print('\n2. Updating search-index.json...')
    update_search_index(articles)
    
    # 3. Update sitemap.xml
    print('\n3. Updating sitemap.xml...')
    update_sitemap(articles)
    
    # 4. Check skip_render
    print('\n4. Checking skip_render...')
    apply_skip_render()
    
    print('\n[OK] All indexes updated!')


if __name__ == '__main__':
    main()
