#!/usr/bin/env python3
"""Batch fix all GEO audit issues for cunqin.tax"""
import sys, os, re, json

sys.stdout.reconfigure(encoding='utf-8')

BRAND_5 = {'存勤法税', '邓达华', '业管财税法', '财税顾问', '税务筹划'}
GEO_TERMS = {'广州', '大湾区财税'}
ARTICLES_DIR = 'source/articles'
SERVICES_DIR = 'source/services'

def read(f):
    with open(f, 'r', encoding='utf-8') as fp:
        return fp.read()

def write(f, c):
    with open(f, 'w', encoding='utf-8') as fp:
        fp.write(c)

def fix_keywords(content):
    """Add missing brand words + geo terms to keywords meta tag"""
    m = re.search(r'<meta name="keywords"\s+content="([^"]*)"', content)
    if not m:
        return content, False
    kw_str = m.group(1)
    kw_set = set(k.strip() for k in kw_str.split(','))
    changed = False

    # Add missing brand words
    for b in BRAND_5:
        if b not in kw_set:
            kw_set.add(b)
            changed = True

    # Add geo terms if missing
    if not (GEO_TERMS & kw_set):
        kw_set.add('广州')
        kw_set.add('大湾区财税')
        changed = True

    if not changed:
        return content, False

    # Rebuild keywords: brand first, then original order (minus dups), then geo
    original = [k.strip() for k in kw_str.split(',')]
    brand_order = ['存勤法税', '业管财税法', '财税顾问', '税务筹划', '邓达华']
    brand_part = [b for b in brand_order if b in kw_set]
    # Topic words: original words that are not brand words
    seen = set(brand_part)
    topic_part = []
    for k in original:
        ks = k.strip()
        if ks and ks not in seen:
            topic_part.append(ks)
            seen.add(ks)
    # Geo words at end
    geo_part = [g for g in ['广州', '大湾区财税'] if g in kw_set and g not in seen]
    new_kw = ','.join(brand_part + topic_part + geo_part)
    new_tag = f'<meta name="keywords" content="{new_kw}"'
    return content.replace(m.group(0), new_tag), True

def fix_og_description(content):
    """Truncate og:description to 120-160 chars, sync meta description"""
    m_og = re.search(r'<meta property="og:description"\s+content="([^"]*)"', content)
    if not m_og:
        return content, False
    og_desc = m_og.group(1)
    if 120 <= len(og_desc) <= 160:
        return content, False

    # Need to fix: truncate to ~155 chars at natural break
    target = og_desc[:158].rstrip()
    # Try to break at punctuation
    for sep in ['，', '。', '；', '：', '\n', '  ']:
        idx = target.rfind(sep)
        if idx > 119:
            target = target[:idx] + '，'
            break
    if len(target) > 160:
        target = target[:160]
    if len(target) < 120:
        target = og_desc[:160]
    if target == og_desc:
        return content, False

    # Replace og:description
    old_og_tag = m_og.group(0)
    new_og_tag = f'<meta property="og:description" content="{target}"'
    content = content.replace(old_og_tag, new_og_tag)

    # Also sync meta description
    m_desc = re.search(r'<meta name="description"\s+content="([^"]*)"', content)
    if m_desc:
        new_desc_tag = f'<meta name="description" content="{target}"'
        content = content.replace(m_desc.group(0), new_desc_tag)

    # Also sync twitter:description
    m_tw = re.search(r'<meta name="twitter:description"\s+content="([^"]*)"', content)
    if m_tw:
        tw_target = target[:100] if len(target) > 100 else target
        new_tw_tag = f'<meta name="twitter:description" content="{tw_target}"'
        content = content.replace(m_tw.group(0), new_tw_tag)

    return content, True

# ===== MAIN =====
fixed = 0
skipped = 0

print("=== Fixing static pages: keywords + og:description ===")
static_pages = [
    'source/首页(source).html',
    'source/about/index.html',
    'source/archives/法税洞察(source).html',
    'source/contact/联系我们(source).html',
]
for fpath in static_pages:
    if not os.path.exists(fpath):
        print(f"  SKIP (not found): {fpath}")
        skipped += 1
        continue
    content = read(fpath)
    new_c, c1 = fix_keywords(content)
    new_c2, c2 = fix_og_description(new_c if c1 else content)
    if c1 or c2:
        write(fpath, new_c2 if c2 else new_c)
        print(f"  FIXED: {os.path.basename(fpath)} (keywords={c1}, og_desc={c2})")
        fixed += 1
    else:
        skipped += 1

print(f"\n=== Fixing {len(os.listdir(SERVICES_DIR)) if os.path.exists(SERVICES_DIR) else 0} service pages: keywords ===")
if os.path.exists(SERVICES_DIR):
    for fname in sorted(os.listdir(SERVICES_DIR)):
        if not fname.endswith('.html'):
            continue
        fpath = os.path.join(SERVICES_DIR, fname)
        content = read(fpath)
        new_c, changed = fix_keywords(content)
        if changed:
            write(fpath, new_c)
            print(f"  FIXED keywords: {fname}")
            fixed += 1
        else:
            skipped += 1

print(f"\n=== Fixing articles: og:description length + keywords ===")
if os.path.exists(ARTICLES_DIR):
    for fname in sorted(os.listdir(ARTICLES_DIR)):
        if not fname.endswith('.html'):
            continue
        fpath = os.path.join(ARTICLES_DIR, fname)
        content = read(fpath)
        new_c, c1 = fix_og_description(content)
        new_c2, c2 = fix_keywords(new_c if c1 else content)
        if c1 or c2:
            write(fpath, new_c2 if c2 else new_c)
            print(f"  FIXED: {fname} (og={c1}, kw={c2})")
            fixed += 1
        else:
            skipped += 1

print(f"\nDone: {fixed} fixed, {skipped} skipped")
