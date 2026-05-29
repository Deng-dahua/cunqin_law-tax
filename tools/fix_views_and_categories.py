#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix article view counts and categories across all pages.
1. Sync view counts from home-insights.json to article detail pages
2. Sync categories from home-insights.json to article detail pages
3. Update 法税洞察 page with new categories
"""
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARTICLES_DIR = os.path.join(BASE_DIR, 'source', 'articles')
ARCHIVES_FILE = os.path.join(BASE_DIR, 'source', 'archives', '法税洞察(source).html')
INSIGHTS_FILE = os.path.join(BASE_DIR, 'source', 'home-insights.json')


def get_file_permalink(filepath):
    """Extract permalink from article source file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    m = re.search(r'permalink:\s*(.+?)\s*\n', content)
    if m:
        return m.group(1).strip().lstrip('/')
    return None


def build_url_mapping():
    """Build mapping from permalink URL to source filename."""
    mapping = {}
    for fname in os.listdir(ARTICLES_DIR):
        if fname.endswith('.html') and '(source)' in fname:
            filepath = os.path.join(ARTICLES_DIR, fname)
            permalink = get_file_permalink(filepath)
            if permalink:
                mapping[permalink] = fname
            else:
                print(f'  Warning: no permalink in {fname}')
    return mapping


def update_article_file(filepath, new_category, new_views):
    """Update category tag and view count in article file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Update cat-tag
    content = re.sub(
        r'(<span class="cat-tag">)[^<]+(</span>)',
        rf'\g<1>{new_category}\g<2>',
        content
    )

    # Update view-num (format: 1,234 or 1234)
    content = re.sub(
        r'(<span class="view-num" id="view-[^"]+">)[\d,]+(</span>)',
        lambda m: f'{m.group(1)}{new_views:,}{m.group(2)}',
        content
    )

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


def update_archives_page(articles_data):
    """Update 法税洞察 page with correct categories and views."""
    with open(ARCHIVES_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Build slug -> (category, views) mapping
    slug_map = {}
    for a in articles_data:
        slug = a['url'].replace('articles/', '').replace('.html', '')
        slug_map[slug] = (a['category'], a['views'])

    # Update each article-item's data-category and data-views
    def replace_article_item(match):
        full = match.group(0)
        href = re.search(r'href="([^"]+)"', full)
        if not href:
            return full
        slug = href.group(1).replace('../articles/', '').replace('.html', '')
        if slug not in slug_map:
            return full
        cat, views = slug_map[slug]
        # Replace data-category
        full = re.sub(r'data-category="[^"]*"', f'data-category="{cat}"', full, count=1)
        # Replace data-views
        full = re.sub(r'data-views="\d+"', f'data-views="{views}"', full, count=1)
        # Replace views display text
        full = re.sub(r'(<span class="article-views"><i class="fas fa-eye"></i> )\d+(</span>)',
                      rf'\g<1>{views}\g<2>', full, count=1)
        return full

    content = re.sub(
        r'<a href="[^"]+" class="article-item"[^>]*>[\s\S]*?</a>',
        replace_article_item,
        content
    )

    # Update filter dropdown options
    # Find all unique categories
    all_cats = sorted(set(a['category'] for a in articles_data))
    cat_options = '        <option value="">全部分类</option>\n'
    for cat in all_cats:
        cat_options += f'        <option value="{cat}">{cat}</option>\n'

    # Replace the category select options
    content = re.sub(
        r'(<select id="filterCategory"[^>]*>[\s\S]*?</select>)',
        lambda m: f'<select id="filterCategory" onchange="applyFilters()" style="padding:0.35rem 0.5rem;border:1px solid #e8e8e8;border-radius:4px;font-size:0.85rem;font-family:inherit;color:#333;background:#fff;">\n{cat_options}      </select>',
        content
    )

    if content != original:
        with open(ARCHIVES_FILE, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


def main():
    print('Building URL mapping...')
    url_map = build_url_mapping()
    print(f'  Mapped {len(url_map)} source files')

    print('Loading home-insights.json...')
    with open(INSIGHTS_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    articles = data['articles']
    print(f'  Loaded {len(articles)} articles')

    # Update article detail pages
    updated = 0
    skipped = 0
    missing = []
    for a in articles:
        permalink = a['url']  # e.g., articles/xxx.html
        fname = url_map.get(permalink)
        if not fname:
            missing.append(permalink)
            continue
        filepath = os.path.join(ARTICLES_DIR, fname)
        if update_article_file(filepath, a['category'], a['views']):
            updated += 1
        else:
            skipped += 1

    print(f'\nArticle pages:')
    print(f'  Updated: {updated}')
    print(f'  No changes needed: {skipped}')
    if missing:
        print(f'  Missing source files: {len(missing)}')
        for m in missing[:5]:
            print(f'    - {m}')

    # Update archives page
    print('\nUpdating 法税洞察 page...')
    if update_archives_page(articles):
        print('  Updated successfully')
    else:
        print('  No changes needed')

    print('\nDone!')


if __name__ == '__main__':
    main()
