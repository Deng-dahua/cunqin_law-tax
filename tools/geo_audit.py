#!/usr/bin/env python3
"""
GE0 Audit Tool for cunqin.tax
Checks: meta tags, OG tags, Twitter tags, Schema.org JSON-LD, keywords, baidu verification
Fully rewritten 2026-05-31 — handles all known edge cases.
"""

import sys, os, re, json

sys.stdout.reconfigure(encoding='utf-8')

SITE_URL   = 'https://cunqin.tax'
BAIDU_TOKEN = 'codeva-9SPpSVW5X6'

# ---- file path lists ----
STATIC_PAGES = [
    ('source/首页(source).html',            'Homepage'),
    ('source/about/index.html',             'About'),
    ('source/contact/联系我们(source).html', 'Contact'),
    ('source/archives/法税洞察(source).html', 'Archives'),
]

SERVICES_DIR = 'source/services'
ARTICLES_DIR = 'source/articles'

ERRORS   = []
WARNINGS = []

def err(msg):  ERRORS.append(msg)
def warn(msg): WARNINGS.append(msg)

# ──────────────────────────────────────────────
#  helpers
# ──────────────────────────────────────────────
META_DESC_RE   = re.compile(r'<meta\s+name="description"\s+content="([^"]*)"', re.I)
META_KW_RE     = re.compile(r'<meta\s+name="keywords"\s+content="([^"]*)"', re.I)
OG_DESC_RE      = re.compile(r'<meta\s+property="og:description"\s+content="([^"]*)"', re.I)
TW_DESC_RE      = re.compile(r'<meta\s+name="twitter:description"\s+content="([^"]*)"', re.I)
CANONICAL_RE    = re.compile(r'<link\s+rel="canonical"\s+href="([^"]*)"', re.I)
BAIDU_RE        = re.compile(r'baidu-site-verification"\s+content="([^"]*)"', re.I)
SCHEMA_BLOCK_RE = re.compile(r'<script\s+type="application/ld\+json">\s*([\s\S]*?)\s*</script>', re.I)

def extract_schema_types(content):
    """Return a list of all @type values from ALL schema blocks."""
    types = []
    has_context = False
    blocks = SCHEMA_BLOCK_RE.findall(content)
    for block in blocks:
        try:
            obj = json.loads(block)
            if isinstance(obj, list):
                for item in obj:
                    if not isinstance(item, dict):
                        continue
                    if '@context' in item and 'schema.org' in str(item['@context']):
                        has_context = True
                    t = item.get('@type', '')
                    if isinstance(t, str):
                        types.append(t)
                    elif isinstance(t, list):
                        types.extend(t)
            else:
                if not isinstance(obj, dict):
                    continue
                if '@context' in obj and 'schema.org' in str(obj['@context']):
                    has_context = True
                t = obj.get('@type', '')
                if isinstance(t, str):
                    types.append(t)
                elif isinstance(t, list):
                    types.extend(t)
        except json.JSONDecodeError:
            pass
    return types, has_context


def check_basic_seo(content, page_name, fpath):
    """Check meta description, OG, Twitter, canonical, baidu, schema — for ANY page."""
    errors_before = len(ERRORS)
    warnings_before = len(WARNINGS)

    # 1. meta description
    m = META_DESC_RE.search(content)
    if not m:
        err(f"[{page_name}] Missing <meta name='description'>")
    else:
        desc = m.group(1)
        if len(desc) < 50:
            warn(f"[{page_name}] meta description too short: {len(desc)} chars")

    # 2. og:description
    m = OG_DESC_RE.search(content)
    if not m:
        err(f"[{page_name}] Missing og:description")
    else:
        og = m.group(1)
        if not (120 <= len(og) <= 160):
            warn(f"[{page_name}] og:description length {len(og)} (should be 120-160)")
        # 3. meta description == og:description
        m2 = META_DESC_RE.search(content)
        if m2 and m2.group(1) != og:
            warn(f"[{page_name}] meta description != og:description")

    # 4. twitter:description
    m = TW_DESC_RE.search(content)
    if not m:
        warn(f"[{page_name}] Missing twitter:description")
    else:
        tw = m.group(1)
        if len(tw) > 100:
            warn(f"[{page_name}] twitter:description too long: {len(tw)} chars (≤100)")

    # 5. baidu verification
    m = BAIDU_RE.search(content)
    if m:
        if m.group(1) != BAIDU_TOKEN:
            err(f"[{page_name}] Wrong baidu token: got '{m.group(1)}', want '{BAIDU_TOKEN}'")
    else:
        if 'baidu-site-verification' in content:
            warn(f"[{page_name}] baidu-site-verification present but token not captured")
        else:
            warn(f"[{page_name}] Missing baidu-site-verification meta")

    # 6. canonical URL
    m = CANONICAL_RE.search(content)
    if not m:
        warn(f"[{page_name}] Missing <link rel='canonical'>")
    else:
        canon = m.group(1)
        if not canon.startswith(SITE_URL):
            warn(f"[{page_name}] Canonical URL does not start with {SITE_URL}: {canon}")

    # 7. Schema.org
    types, has_ctx = extract_schema_types(content)
    if not types:
        err(f"[{page_name}] Missing Schema.org JSON-LD blocks")
    else:
        if not has_ctx:
            err(f"[{page_name}] Schema missing @context with schema.org")
        # Check expected types per page
        if page_name == 'Homepage' and 'WebSite' not in types:
            warn(f"[{page_name}] Missing WebSite Schema (have: {types})")
        if page_name == 'Homepage' and 'Organization' not in types:
            warn(f"[{page_name}] Missing Organization Schema (have: {types})")
        if page_name == 'About' and 'AboutPage' not in types and 'Person' not in types:
            warn(f"[{page_name}] Missing AboutPage/Person Schema (have: {types})")
        if page_name == 'Contact' and 'ContactPage' not in types:
            warn(f"[{page_name}] Missing ContactPage Schema (have: {types})")
        if page_name == 'Archives':
            if 'CollectionPage' not in types and 'WebPage' not in types:
                warn(f"[{page_name}] Missing CollectionPage/WebPage Schema (have: {types})")
        if page_name.startswith('Service:'):
            if 'Service' not in types and 'WebPage' not in types:
                warn(f"[{page_name}] Missing Service/WebPage Schema (have: {types})")

    # 8. keywords (brand 5 + geo)
    m = META_KW_RE.search(content)
    if not m:
        err(f"[{page_name}] Missing <meta name='keywords'>")
    else:
        kw_set = {k.strip() for k in m.group(1).split(',')}
        brand5 = {'存勤法税', '邓达华', '业管财税法', '财税顾问', '税务筹划'}
        missing = brand5 - kw_set
        if missing:
            warn(f"[{page_name}] Missing brand keywords: {missing}")
        geo_terms = {'广州', '大湾区', '粤港澳大湾区'}
        if not any(g in kw_set for g in geo_terms):
            warn(f"[{page_name}] Missing geographic keywords (广州/大湾区)")


def check_article(filepath, fname):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    ref = fname
    m_title = re.search(r'<title>([^<]+)</title>', content)
    if m_title:
        ref = f"{fname}  |  {m_title.group(1)[:25]}"
    ref = f"[{ref}]"

    # keywords
    m = META_KW_RE.search(content)
    if not m:
        err(f"{ref} Missing <meta name='keywords'>")
        return
    kw_set = {k.strip() for k in m.group(1).split(',')}

    brand5 = {'存勤法税', '邓达华', '业管财税法', '财税顾问', '税务筹划'}
    missing = brand5 - kw_set
    if missing:
        err(f"{ref} Missing brand keywords: {missing}")

    # generic template abuse — only warn if article topic is UNRELATED to generic keywords
    generic = '金税四期,以数治税,税务稽查,企业合规,税务风险管理'
    fname_lower = fname.lower()
    # Skip warning if article is actually about 金税四期
    topic_match = any(kw in fname_lower or (m_title and kw in m_title.group(1))
                       for kw in ['金税四期', '以数治税', '税务稽查'])
    if generic in m.group(1) and not topic_match:
        warn(f"{ref} Using generic template keywords (not content-matched)")

    # geo keywords
    geo_terms = {'广州', '大湾区', '粤港澳大湾区'}
    if not any(g in kw_set for g in geo_terms):
        warn(f"{ref} Missing geographic keywords (广州/大湾区)")

    # og:description length
    m_og = OG_DESC_RE.search(content)
    if not m_og:
        err(f"{ref} Missing og:description")
    else:
        og = m_og.group(1)
        if not (120 <= len(og) <= 160):
            warn(f"{ref} og:description length {len(og)} (should be 120-160)")

    # meta description == og:description
    m_desc = META_DESC_RE.search(content)
    if m_desc and m_og:
        if m_desc.group(1) != m_og.group(1):
            warn(f"{ref} meta description != og:description")

    # Schema: must have Article, preferably BreadcrumbList + FAQPage
    types, has_ctx = extract_schema_types(content)
    if not types:
        err(f"{ref} Missing Schema.org JSON-LD")
    else:
        if 'Article' not in types:
            err(f"{ref} Missing Article Schema (have: {types})")
        if 'BreadcrumbList' not in types:
            warn(f"{ref} Missing BreadcrumbList Schema")
        # FAQPage — only if article has FAQ section
        has_faq = bool(re.search(r'id="faq"', content, re.I) or
                        re.search(r'id="FAQ"', content, re.I) or
                        '常见问题' in content)
        if has_faq and 'FAQPage' not in types:
            warn(f"{ref} Has FAQ content but missing FAQPage Schema")

    # view count remnants (should have been deleted)
    if 'articleViewCount' in content:
        err(f"{ref} Found remnant articleViewCount (should be deleted)")
    if 'countapi' in content:
        err(f"{ref} Found remnant countapi.xyz code (should be deleted)")
    if '次阅读' in content:
        err(f"{ref} Found remnant '次阅读' text (should be deleted)")

    # baidu verification in article pages
    m_bd = BAIDU_RE.search(content)
    if m_bd and m_bd.group(1) != BAIDU_TOKEN:
        err(f"{ref} Wrong baidu token: {m_bd.group(1)}")


# ──────────────────────────────────────────────
#  MAIN
# ──────────────────────────────────────────────
print("=" * 60)
print("  GEO Audit Report — cunqin.tax")
print("=" * 60)

# 1. Static pages
print("\n--- Checking static pages ---")
for fpath, name in STATIC_PAGES:
    if not os.path.exists(fpath):
        err(f"[{name}] File not found: {fpath}")
        print(f"  SKIP (not found): {name}")
        continue
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    print(f"  Checking: {name} ({len(content)//1024} KB)")
    check_basic_seo(content, name, fpath)

# 2. Service pages
print("\n--- Checking service pages ---")
if os.path.exists(SERVICES_DIR):
    sfiles = sorted(f for f in os.listdir(SERVICES_DIR) if f.endswith('.html'))
    print(f"  Found {len(sfiles)} service files")
    for fname in sfiles:
        fpath = os.path.join(SERVICES_DIR, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        pname = f"Service: {fname}"
        check_basic_seo(content, pname, fpath)
else:
    warn("Service directory not found")

# 3. Articles
print("\n--- Checking 77 articles ---")
if os.path.exists(ARTICLES_DIR):
    afiles = sorted(f for f in os.listdir(ARTICLES_DIR) if f.endswith('.html'))
    print(f"  Found {len(afiles)} article files")
    for fname in afiles:
        fpath = os.path.join(ARTICLES_DIR, fname)
        check_article(fpath, fname)
else:
    err("Articles directory not found!")

# ──────────────────────────────────────────────
#  Results
# ──────────────────────────────────────────────
print("\n" + "=" * 60)
print(f"  RESULTS:  {len(ERRORS)} ERRORS,  {len(WARNINGS)} WARNINGS")
print("=" * 60)

if ERRORS:
    print(f"\n--- ERRORS ({len(ERRORS)}) ---")
    for i, e in enumerate(ERRORS[:60]):
        print(f"  ❌  {e}")
    if len(ERRORS) > 60:
        print(f"  ... and {len(ERRORS)-60} more errors")

if WARNINGS:
    print(f"\n--- WARNINGS ({len(WARNINGS)}) ---")
    for i, w in enumerate(WARNINGS[:40]):
        print(f"  ⚠️  {w}")
    if len(WARNINGS) > 40:
        print(f"  ... and {len(WARNINGS)-40} more warnings")

if not ERRORS and not WARNINGS:
    print("\n✅  All checks passed!  0 ERROR, 0 WARNING")

print(f"\nDone.  ERRORS: {len(ERRORS)},  WARNINGS: {len(WARNINGS)}")
