#!/usr/bin/env python3
"""
全站索引更新工具：扫描 source/articles/ 下所有 HTML 文章，
自动更新 sitemap.xml、search-index.json、法税洞察页。
"""
import os
import re
import json
import html as html_mod
from datetime import datetime

BASE_DIR = r'C:\Users\26726\WorkBuddy\2026-05-20-21-20-24'
SOURCE_DIR = os.path.join(BASE_DIR, 'source')
ARTICLES_DIR = os.path.join(SOURCE_DIR, 'articles')
SITE_URL = 'https://cunqin.tax'
TODAY = '2026-05-24'


def extract_meta_from_html(filepath):
    """从文章HTML中提取元数据"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    result = {}
    
    # permalink
    m = re.search(r'permalink:\s*/articles/([^\s]+)', content)
    if m:
        result['slug'] = m.group(1).replace('.html', '')
    
    # title from <title> tag
    m = re.search(r'<title>([^<]+)</title>', content)
    if m:
        title = m.group(1).strip()
        # Remove site suffix
        title = re.sub(r'\s*[-–|]\s*存勤法税.*$', '', title)
        result['title'] = title
    
    # description
    m = re.search(r'<meta\s+name="description"\s+content="([^"]+)"', content)
    if not m:
        m = re.search(r'<meta\s+name="description"\s+content=\'([^\']+)\'', content)
    if m:
        result['description'] = m.group(1)
    
    # og:title
    m = re.search(r'<meta\s+property="og:title"\s+content="([^"]+)"', content)
    if m:
        result['og_title'] = m.group(1)
    
    # og:description
    m = re.search(r'<meta\s+property="og:description"\s+content="([^"]+)"', content)
    if m:
        result['og_description'] = m.group(1)
    
    # keywords
    m = re.search(r'<meta\s+name="keywords"\s+content="([^"]+)"', content)
    if m:
        result['keywords'] = m.group(1)
    
    # published_time
    m = re.search(r'<meta\s+property="article:published_time"\s+content="([^"]+)"', content)
    if m:
        result['date'] = m.group(1)
    
    # modified_time
    m = re.search(r'<meta\s+property="article:modified_time"\s+content="([^"]+)"', content)
    if m:
        result['modified'] = m.group(1)
    
    # category from cat-tag
    m = re.search(r'<span class="cat-tag">([^<]+)</span>', content)
    if m:
        result['category'] = m.group(1).strip()
    
    # base views from view counter slug
    m = re.search(r"var\s+slug\s*=\s*'([^']+)'", content)
    if m:
        result['view_slug'] = m.group(1)
    m = re.search(r'var\s+base\s*=\s*(\d+)', content)
    if m:
        result['base_views'] = int(m.group(1))
    
    # Extract article body text for search-index summary
    body_match = re.search(r'<!-- ===== 正文 ===== -->.*?<article class="article-body">(.*?)</article>', content, re.DOTALL)
    if not body_match:
        body_match = re.search(r'<article class="article-body">(.*?)</article>', content, re.DOTALL)
    if body_match:
        body_html = body_match.group(1)
        # Remove HTML tags for plain text
        body_text = re.sub(r'<[^>]+>', '', body_html)
        body_text = re.sub(r'\s+', '', body_text)
        result['body_text'] = body_text[:300]
    
    return result


def scan_articles():
    """扫描所有文章并提取元数据"""
    articles = []
    for fname in os.listdir(ARTICLES_DIR):
        if fname.endswith('(source).html'):
            fpath = os.path.join(ARTICLES_DIR, fname)
            meta = extract_meta_from_html(fpath)
            if meta.get('slug'):
                articles.append(meta)
                print(f"  ✓ {meta.get('slug')} - {meta.get('title', 'N/A')[:50]}...")
            else:
                print(f"  ✗ {fname}: no slug found")
    return articles


def generate_sitemap_entries(articles):
    """生成sitemap中文章部分的XML"""
    entries = []
    for a in sorted(articles, key=lambda x: x.get('date', ''), reverse=True):
        slug = a['slug']
        date = a.get('date', TODAY)
        entries.append(f"""  <url>
    <loc>https://cunqin.tax/articles/{slug}.html</loc>
    <lastmod>{date}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
    <xhtml:link rel="alternate" hreflang="zh-CN" href="https://cunqin.tax/articles/{slug}.html"/>
  </url>""")
    return entries


def generate_search_index_entries(articles):
    """生成search-index.json的文章条目"""
    entries = []
    for a in sorted(articles, key=lambda x: x.get('date', ''), reverse=True):
        entry = {
            'title': a.get('title', ''),
            'url': f"/articles/{a['slug']}.html",
            'text': a.get('body_text', ''),
            'date': a.get('date', ''),
            'category': a.get('category', '')
        }
        entries.append(entry)
    return entries


def generate_article_cards(articles):
    """为法税洞察页生成文章卡片HTML - 匹配现有格式"""
    cards = []
    for a in sorted(articles, key=lambda x: x.get('date', ''), reverse=True):
        slug = a['slug']
        title = a.get('title', '')
        category = a.get('category', '税务实务')
        date = a.get('date', '2026-05-24')
        base_views = a.get('base_views', 100)
        
        body = a.get('body_text', '')
        desc = body[:80]
        
        card = f'''      <a href="../articles/{slug}.html" class="article-item" data-date="{date}" data-category="{category}" data-views="{base_views}">
        <div class="article-content">
          <h3>{title}</h3>
          <p>{desc}</p>
          <span class="article-tag">{category}</span>
</div>
        <div class="article-arrow"><i class="fas fa-chevron-right"></i></div>
      </a>'''
        cards.append(card)
    return cards


def update_sitemap(articles):
    """更新sitemap.xml"""
    sitemap_path = os.path.join(SOURCE_DIR, 'sitemap.xml')
    with open(sitemap_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 找到文章部分（从第一篇文章URL开始到文件末尾）
    # 替换所有文章条目
    article_start = content.find('<!-- 8 篇文章 -->')
    if article_start == -1:
        article_start = content.find('<!-- 19 篇文章 -->')
    
    if article_start == -1:
        print("ERROR: Cannot find article section in sitemap.xml")
        return
    
    # 找到文章部分在urlset结束前的位置
    urlset_end = content.rfind('</urlset>')
    
    new_entries = generate_sitemap_entries(articles)
    new_article_section = f'<!-- {len(articles)} 篇文章 -->\n' + '\n'.join(new_entries) + '\n'
    
    new_content = content[:article_start] + new_article_section + content[urlset_end:]
    
    with open(sitemap_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"  ✓ sitemap.xml updated: {len(articles)} articles")


def update_search_index(articles):
    """更新search-index.json"""
    index_path = os.path.join(SOURCE_DIR, 'search-index.json')
    with open(index_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 找到并移除旧的文章条目（URL包含/articles/的条目）
    non_article_entries = [e for e in data if '/articles/' not in e.get('url', '')]
    
    # 添加新文章条目
    article_entries = generate_search_index_entries(articles)
    new_data = non_article_entries + article_entries
    
    with open(index_path, 'w', encoding='utf-8') as f:
        json.dump(new_data, f, ensure_ascii=False, indent=2)
    
    print(f"  ✓ search-index.json updated: {len(article_entries)} articles, {len(new_data)} total entries")


def update_archives_page(articles):
    """更新法税洞察页面的文章列表"""
    archives_path = os.path.join(SOURCE_DIR, 'archives', '法税洞察(source).html')
    
    with open(archives_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 文章列表在 <div class="article-list" id="articleList"> 和对应的 </div> 之间
    list_start_tag = '<div class="article-list" id="articleList">'
    list_start = content.find(list_start_tag)
    if list_start == -1:
        print("ERROR: Cannot find article list div")
        return
    
    # 文章内容从 div 开始标签之后开始
    content_start = list_start + len(list_start_tag)
    
    # 找到这个div的结束标签（文章列表容器结束）
    # 策略：从 list_start 往后找，匹配 div 的层级
    # 在 list_start_tag 之后，先找到第一个 </div> 作为 article-list 的闭合
    # 但 article-list 内部有很多 <div> → 需要逐层匹配
    depth = 1
    pos = content_start
    list_end = -1
    while pos < len(content) and depth > 0:
        next_open = content.find('<div', pos)
        next_close = content.find('</div>', pos)
        
        if next_close == -1:
            break
        
        # 如果下一个是 </div> 且它在 <div 之前
        if next_open == -1 or next_close < next_open:
            depth -= 1
            pos = next_close + len('</div>')
            if depth == 0:
                list_end = next_close
                break
        else:
            depth += 1
            pos = next_open + 1
    
    if list_end == -1:
        print("ERROR: Cannot find end of article list")
        return
    
    cards = generate_article_cards(articles)
    cards_html = '\n'.join(cards) + '\n'
    
    new_content = content[:content_start] + '\n' + cards_html + content[list_end:]
    
    with open(archives_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"  ✓ 法税洞察页 updated: {len(articles)} articles")


def main():
    print("扫描文章...")
    articles = scan_articles()
    print(f"\n共找到 {len(articles)} 篇文章\n")
    
    if not articles:
        print("ERROR: No articles found!")
        return
    
    print("更新 sitemap.xml...")
    update_sitemap(articles)
    
    print("更新 search-index.json...")
    update_search_index(articles)
    
    print("更新 法税洞察页...")
    update_archives_page(articles)
    
    print("\n全部更新完成！")


if __name__ == '__main__':
    main()
