"""P1: Enhance Article / Person / Service Schema across all pages"""
import re, os, glob

base = 'C:/Users/26726/WorkBuddy/2026-05-20-21-20-24'

# ============================
# Part 1: Article Schema (39 articles)
# ============================
print("=" * 60)
print("Part 1: Enhancing Article Schema (39 articles)")
print("=" * 60)

article_files = sorted(glob.glob(f'{base}/source/articles/*.html'))
article_count = 0

for fp in article_files:
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract article body for word count
    body_match = re.search(r'<article class=.article-body.>(.*?)</article>', content, re.DOTALL)
    if not body_match:
        print(f"  SKIP {os.path.basename(fp)}: no article-body")
        continue
    
    body_text = re.sub(r'<[^>]+>', ' ', body_match.group(1))
    body_text = re.sub(r'\s+', ' ', body_text).strip()
    word_count = len(body_text)
    
    # Extract category from meta keywords or h1
    cat_match = re.search(r'<meta name="keywords"[^>]*content="([^"]*)"', content)
    category = "财税咨询"
    if cat_match:
        keywords = cat_match.group(1)
        if '实操' in keywords:
            category = '实操指南'
        elif '政策' in keywords:
            category = '政策解读'
        elif '行业' in keywords:
            category = '行业洞察'
    
    # Find the Article Schema closing (after mainEntityOfPage)
    schema_pattern = r'("mainEntityOfPage":\s*\{[^}]+\})\s*\}'
    # Actually, let's find the Article block end more precisely
    # The Article schema ends with `},` followed by BreadcrumbList or FAQPage
    # Pattern: mainEntityOfPage block → closing brace → comma
    
    # Insert enhanced fields after mainEntityOfPage
    old = '}'
    new_fields = f''',
    "wordCount": {word_count},
    "articleSection": "{category}",
    "inLanguage": "zh-CN",
    "isAccessibleForFree": true
  }}'''
    
    # Match: mainEntityOfPage WebPage block ending with }},
    # Then close the Article with },
    pattern = r'(("mainEntityOfPage":\s*\{[^}]+\})\s*\})'
    
    match = re.search(pattern, content)
    if not match:
        print(f"  SKIP {os.path.basename(fp)}: no mainEntityOfPage")
        continue
    
    # Insert new fields before the closing brace of Article
    article_end = match.end()
    # Find the exact closing: the match ends at the first `}`, but Article might have another `}`
    # Let me be more precise - find the 2nd `}` after mainEntityOfPage
    
    idx = match.start()
    # Find the Article opening
    art_start = content.rfind('"@type": "Article"', 0, idx)
    if art_start < 0:
        print(f"  SKIP {os.path.basename(fp)}: can't find Article start")
        continue
    
    # Find the Article closing - after mainEntityOfPage, there should be `  },\n` then next schema
    # or `  }\n` if last
    idx2 = match.end()
    # Count braces to find Article's closing
    brace_count = 0
    article_close = -1
    for i in range(idx2, min(idx2 + 200, len(content))):
        if content[i] == '{':
            brace_count += 1
        elif content[i] == '}':
            if brace_count == 0:
                article_close = i + 1
                break
            brace_count -= 1
    
    if article_close < 0:
        print(f"  SKIP {os.path.basename(fp)}: can't find Article close")
        continue
    
    # Insert enhanced fields before the Article closing brace
    enhanced = (
        content[:article_close - 1]
        + f',\n    "wordCount": {word_count},\n'
        + f'    "articleSection": "{category}",\n'
        + '    "inLanguage": "zh-CN",\n'
        + '    "isAccessibleForFree": true\n'
        + content[article_close - 1:]
    )
    
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(enhanced)
    
    article_count += 1
    short = os.path.basename(fp).replace('(source).html', '')[:30]
    print(f"  OK [{word_count}字] {short}")

print(f"\nArticles enhanced: {article_count}/{len(article_files)}")

# ============================
# Part 2: Person Schema (About page)
# ============================
print("\n" + "=" * 60)
print("Part 2: Enhancing Person Schema (About page)")
print("=" * 60)

about_path = f'{base}/source/about/关于我们(source).html'
with open(about_path, 'r', encoding='utf-8') as f:
    about_content = f.read()

# Add standalone Person with rich fields before the Organization schema
person_schema = '''  {
    "@context": "https://schema.org",
    "@type": "Person",
    "name": "邓达华",
    "url": "https://cunqin.tax/about/",
    "jobTitle": "创始人",
    "image": "https://cunqin.tax/images/founder-new.webp",
    "description": "存勤法税服务（广州）有限公司创始人，拥有18年财税法实战经验（14年甲方企业财税管理经验+4年乙方专业服务经验），致力于为中国企业提供业管财税法五维融合的专业税务解决方案。",
    "worksFor": {
      "@type": "Organization",
      "name": "存勤法税服务（广州）有限公司",
      "url": "https://cunqin.tax"
    },
    "knowsAbout": ["税务筹划", "涉税风险检查", "企业重组税务", "跨境投资税务", "税务争议解决"],
    "sameAs": []
  },
'''

# Insert before Organization schema
org_pattern = r'(\s*\{[^}]*"@type":\s*"Organization"[^}]*\})'
# Actually, let's find the first Organization block
org_match = re.search(r'"@type":\s*"Organization"', about_content)
if org_match:
    # Find the start of this schema block
    idx = org_match.start()
    block_start = about_content.rfind('{', 0, idx)
    # We want to insert before this block starts, after the previous schema's closing
    # Find the closing of previous schema
    prev_end = block_start
    while prev_end > 0 and about_content[prev_end] != ']':
        prev_end -= 1
    
    # Actually simpler: insert after the first `]` (closing of schema array)
    array_start = about_content.find('[')
    if array_start > 0:
        # Insert after `[`
        about_content = about_content[:array_start + 1] + '\n' + person_schema + about_content[array_start + 1:]
        
        with open(about_path, 'w', encoding='utf-8') as f:
            f.write(about_content)
        print("  OK Person Schema added to About page")
    else:
        print("  FAIL: can't find schema array start")
else:
    print("  FAIL: can't find Organization schema")

# ============================
# Part 3: Service Schema (11 service pages)
# ============================
print("\n" + "=" * 60)
print("Part 3: Enhancing Service Schema (11 service pages)")
print("=" * 60)

service_files = sorted(glob.glob(f'{base}/source/services/*.html'))
service_count = 0

for fp in service_files:
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if '"@type": "Service"' not in content:
        print(f"  SKIP {os.path.basename(fp)}: no Service schema")
        continue
    
    # Add offers and image fields to Service schema
    # Insert after author block
    author_pattern = r'("author":\s*\{[^}]+\})\s*\}'
    match = re.search(author_pattern, content)
    if not match:
        print(f"  SKIP {os.path.basename(fp)}: no author field")
        continue
    
    # Find Service's closing brace after author
    idx2 = match.end()
    brace_count = 0
    service_close = -1
    for i in range(idx2, min(idx2 + 200, len(content))):
        if content[i] == '{':
            brace_count += 1
        elif content[i] == '}':
            if brace_count == 0:
                service_close = i + 1
                break
            brace_count -= 1
    
    if service_close < 0:
        print(f"  SKIP {os.path.basename(fp)}: can't find Service close")
        continue
    
    enhanced = (
        content[:service_close - 1]
        + ',\n'
        + '    "image": "https://cunqin.tax/images/nav-logo.webp",\n'
        + '    "offers": {\n'
        + '      "@type": "Offer",\n'
        + '      "price": "0",\n'
        + '      "priceCurrency": "CNY",\n'
        + '      "description": "首次咨询免费"\n'
        + '    },\n'
        + '    "audience": {\n'
        + '      "@type": "BusinessAudience",\n'
        + '      "audienceType": "企业主/财务总监"\n'
        + '    }\n'
        + content[service_close - 1:]
    )
    
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(enhanced)
    
    service_count += 1
    short = os.path.basename(fp).replace('(source).html', '')[:30]
    print(f"  OK {short}")

print(f"\nServices enhanced: {service_count}/{len(service_files)}")

print("\n" + "=" * 60)
print("All Schema enhancements complete!")
print(f"Articles: {article_count}, Person: 1, Services: {service_count}")
print("=" * 60)
