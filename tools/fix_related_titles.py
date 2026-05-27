#!/usr/bin/env python3
"""Batch fix all related-reading h4 titles to match actual article titles."""
import re, os, sys
sys.stdout.reconfigure(encoding='utf-8')

BASE = os.path.dirname(os.path.abspath(__file__))
ARTICLES_DIR = os.path.join(BASE, '..', 'source', 'articles')

# Build slug -> actual title map
slug_to_title = {}
for f in sorted(os.listdir(ARTICLES_DIR)):
    if not f.endswith('.html'):
        continue
    fpath = os.path.join(ARTICLES_DIR, f)
    with open(fpath, encoding='utf-8') as fh:
        content = fh.read()
    m = re.search(r'permalink:\s*/articles/([\w-]+)\.html', content)
    if not m:
        continue
    slug = m.group(1)
    mt = re.search(r'<title>(.*?)</title>', content, re.DOTALL)
    if mt:
        raw = mt.group(1).strip()
        raw = re.sub(r'\s*[|｜]\s*存勤法税.*$', '', raw)
        raw = re.sub(r'\s*-\s*存勤法税.*$', '', raw)
        slug_to_title[slug] = raw.strip()

print(f'标题库: {len(slug_to_title)} 篇')

# Fix each article
fixed_count = 0
for fname in sorted(os.listdir(ARTICLES_DIR)):
    if not fname.endswith('.html'):
        continue
    fpath = os.path.join(ARTICLES_DIR, fname)
    with open(fpath, encoding='utf-8') as fh:
        content = fh.read()
    
    original = content
    
    def replace_title(match):
        global fixed_count
        href = match.group(1)
        h4 = match.group(2)
        target_slug = href.replace('.html', '')
        actual = slug_to_title.get(target_slug, '')
        if actual and h4.strip() != actual:
            fixed_count += 1
            return f'<a href="{href}" class="related-card">{match.group(0)[len(f"<a href=\"{href}\" class=\"related-card\">"):-len(f"</a>")]}'.replace(f'<h4>{h4}</h4>', f'<h4>{actual}</h4>')
        return match.group(0)
    
    # Find all related-card blocks and fix h4
    pattern = re.compile(
        r'(<a href="([\w-]+\.html)" class="related-card">.*?<h4>)(.*?)(</h4>.*?</a>)',
        re.DOTALL
    )
    
    def fix_one(m):
        global fixed_count
        prefix = m.group(1)
        h4_text = m.group(3).strip()
        suffix = m.group(4)
        href = m.group(2)
        target_slug = href.replace('.html', '')
        actual = slug_to_title.get(target_slug, '')
        if actual and h4_text != actual:
            fixed_count += 1
            return f'{prefix}{actual}{suffix}'
        return m.group(0)
    
    content = pattern.sub(fix_one, content)
    
    if content != original:
        with open(fpath, 'w', encoding='utf-8') as fh:
            fh.write(content)

print(f'修复完成: {fixed_count} 处标题')
