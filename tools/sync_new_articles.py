#!/usr/bin/env python3
"""Sync new articles into sitemap.xml and search-index.json"""
import json
import os
import re
from datetime import datetime
from html.parser import HTMLParser

BASE_DIR = r'C:\Users\26726\WorkBuddy\2026-05-20-21-20-24'
SOURCE_DIR = os.path.join(BASE_DIR, 'source')
ARTICLES_DIR = os.path.join(SOURCE_DIR, 'articles')
SITE_URL = 'https://cunqin.tax'
TODAY = '2026-05-27'

class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []
        self.skip_tags = {'script', 'style', 'nav', 'header', 'footer'}
        self.current_skip = []
    def handle_starttag(self, tag, attrs):
        if tag in self.skip_tags:
            self.current_skip.append(tag)
    def handle_endtag(self, tag):
        if tag in self.skip_tags and self.current_skip and self.current_skip[-1] == tag:
            self.current_skip.pop()
    def handle_data(self, data):
        if not self.current_skip:
            self.text.append(data)
    def get_text(self):
        return ' '.join(self.text)

def get_article_info(filepath):
    """Extract permalink, title, description, and text from article HTML"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract frontmatter
    fm_match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if not fm_match:
        return None
    
    permalink = re.search(r'permalink:\s*(.+)', fm_match.group(1))
    permalink = permalink.group(1).strip() if permalink else None
    
    # Extract title
    title_match = re.search(r'<title>(.*?)</title>', content)
    title = title_match.group(1).strip() if title_match else None
    if title:
        title = title.split(' - ')[0].strip()
    
    # Extract description
    desc_match = re.search(r'<meta name="description" content="(.*?)"', content)
    description = desc_match.group(1).strip() if desc_match else ''
    
    # Extract article body text (from main article area)
    body_match = re.search(r'<article[^>]*>(.*?)</article>', content, re.DOTALL)
    if body_match:
        body_html = body_match.group(1)
    else:
        # Fallback: extract from body
        body_match = re.search(r'<body>(.*?)</body>', content, re.DOTALL)
        body_html = body_match.group(1) if body_match else ''
    
    extractor = TextExtractor()
    extractor.feed(body_html)
    body_text = extractor.get_text()
    body_text = re.sub(r'\s+', ' ', body_text).strip()[:500]
    
    return {
        'permalink': permalink,
        'title': title,
        'description': description,
        'body_text': body_text
    }

def main():
    # Get all article files
    articles = []
    for fname in os.listdir(ARTICLES_DIR):
        if fname.endswith('.html') and fname != 'index.html':
            filepath = os.path.join(ARTICLES_DIR, fname)
            info = get_article_info(filepath)
            if info:
                articles.append(info)
    
    print(f"Found {len(articles)} articles")
    
    # Read existing sitemap
    sitemap_path = os.path.join(SOURCE_DIR, 'sitemap.xml')
    with open(sitemap_path, 'r', encoding='utf-8') as f:
        sitemap_content = f.read()
    
    # Read existing search-index
    si_path = os.path.join(SOURCE_DIR, 'search-index.json')
    with open(si_path, 'r', encoding='utf-8') as f:
        search_index = json.load(f)
    
    existing_urls = set()
    for entry in search_index:
        existing_urls.add(entry.get('url', ''))
    
    # Also check sitemap URLs
    sitemap_urls = set(re.findall(r'<loc>https://cunqin\.tax(/[^<]*)</loc>', sitemap_content))
    existing_urls.update(sitemap_urls)
    
    # Find new articles
    new_count = 0
    for article in articles:
        permalink = article['permalink']
        # Construct URL from permalink
        url = permalink if permalink.startswith('/') else '/' + permalink
        
        if url in existing_urls:
            continue
        
        new_count += 1
        print(f"  NEW: {url} -> {article['title']}")
        
        # Add to search-index
        search_index.append({
            'title': article['title'],
            'url': url,
            'text': article.get('body_text', ''),
            'description': article.get('description', ''),
            'lastModified': TODAY
        })
        
        # Add to sitemap
        sitemap_entry = f"""
  <!-- Article -->
  <url>
    <loc>{SITE_URL}{url}</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
    <xhtml:link rel="alternate" hreflang="zh-CN" href="{SITE_URL}{url}"/>
  </url>"""
        
        # Insert before closing </urlset>
        sitemap_content = sitemap_content.replace('</urlset>', sitemap_entry + '\n</urlset>')
    
    if new_count > 0:
        # Write updated sitemap
        with open(sitemap_path, 'w', encoding='utf-8') as f:
            f.write(sitemap_content)
        print(f"\nUpdated sitemap.xml with {new_count} new entries")
        
        # Write updated search-index
        with open(si_path, 'w', encoding='utf-8') as f:
            json.dump(search_index, f, ensure_ascii=False, separators=(',', ':'))
        print(f"Updated search-index.json with {new_count} new entries")
    else:
        print("No new articles found (all already synced)")
    
    print(f"Total: {len(existing_urls) + new_count} entries")

if __name__ == '__main__':
    main()
