"""P1: Enhance Article / Person / Service Schema using JSON parse"""
import re, os, json, glob

base = 'C:/Users/26726/WorkBuddy/2026-05-20-21-20-24'

# ============================
# Part 1: Article Schema enhancements
# ============================
print("=" * 60)
print("Part 1: Article Schema (39 articles)")
print("=" * 60)

article_files = sorted(glob.glob(f'{base}/source/articles/*.html'))
ok = 0

for fp in article_files:
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract body text for word count
    body_match = re.search(r'<article class="article-body">(.*?)</article>', content, re.DOTALL)
    if not body_match:
        body_match = re.search(r"<article class='article-body'>(.*?)</article>", content, re.DOTALL)
    if not body_match:
        print(f"  SKIP {os.path.basename(fp)}: no article-body")
        continue
    
    body_text = re.sub(r'<[^>]+>', ' ', body_match.group(1))
    body_text = re.sub(r'\s+', ' ', body_text).strip()
    word_count = len(body_text)
    
    # Extract category
    cat_match = re.search(r'<meta name="keywords"[^>]*content="([^"]*)"', content)
    category = "财税咨询"
    if cat_match:
        kw = cat_match.group(1)
        if '实操' in kw: category = '实操指南'
        elif '政策' in kw: category = '政策解读'
        elif '行业' in kw: category = '行业洞察'
    
    # Parse JSON-LD
    ld_match = re.search(r'<script type="application/ld\+json">(.*?)</script>', content, re.DOTALL)
    if not ld_match:
        print(f"  SKIP {os.path.basename(fp)}: no JSON-LD")
        continue
    
    try:
        schemas = json.loads(ld_match.group(1))
    except:
        print(f"  SKIP {os.path.basename(fp)}: JSON parse error")
        continue
    
    # Find and enhance Article schema
    modified = False
    for s in schemas:
        if s.get('@type') == 'Article':
            if 'wordCount' not in s:
                s['wordCount'] = word_count
                s['articleSection'] = category
                s['inLanguage'] = 'zh-CN'
                s['isAccessibleForFree'] = True
                modified = True
    
    if modified:
        new_json = json.dumps(schemas, ensure_ascii=False, indent=2)
        new_content = content[:ld_match.start(1)] + '\n' + new_json + '\n  ' + content[ld_match.end(1):]
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(new_content)
        ok += 1
        short = os.path.basename(fp).replace('(source).html', '')[:30]
        print(f"  OK [{word_count}字] {short}")

print(f"\nArticles enhanced: {ok}/{len(article_files)}")

# ============================
# Part 2: Person Schema on About page
# ============================
print("\n" + "=" * 60)
print("Part 2: Person Schema (About page)")
print("=" * 60)

about_path = f'{base}/source/about/关于我们(source).html'
with open(about_path, 'r', encoding='utf-8') as f:
    about_content = f.read()

ld_match = re.search(r'<script type="application/ld\+json">(.*?)</script>', about_content, re.DOTALL)
if ld_match:
    try:
        schemas = json.loads(ld_match.group(1))
    except:
        print("  FAIL: JSON parse error")
        schemas = None
    
    if schemas:
        # Add standalone Person schema
        person = {
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
        }
        schemas.insert(0, person)
        
        new_json = json.dumps(schemas, ensure_ascii=False, indent=2)
        about_content = about_content[:ld_match.start(1)] + '\n' + new_json + '\n  ' + about_content[ld_match.end(1):]
        with open(about_path, 'w', encoding='utf-8') as f:
            f.write(about_content)
        print("  OK Person Schema added")
    else:
        print("  FAIL: no schemas found")

# ============================
# Part 3: Service Schema enhancements
# ============================
print("\n" + "=" * 60)
print("Part 3: Service Schema (11 service pages)")
print("=" * 60)

service_files = sorted(glob.glob(f'{base}/source/services/*.html'))
svc_ok = 0

for fp in service_files:
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()
    
    ld_match = re.search(r'<script type="application/ld\+json">(.*?)</script>', content, re.DOTALL)
    if not ld_match:
        print(f"  SKIP {os.path.basename(fp)}: no JSON-LD")
        continue
    
    try:
        schemas = json.loads(ld_match.group(1))
    except:
        print(f"  SKIP {os.path.basename(fp)}: JSON parse error")
        continue
    
    modified = False
    for s in schemas:
        if s.get('@type') == 'Service':
            if 'offers' not in s:
                s['image'] = 'https://cunqin.tax/images/nav-logo.webp'
                s['offers'] = {
                    "@type": "Offer",
                    "price": "0",
                    "priceCurrency": "CNY",
                    "description": "首次咨询免费"
                }
                s['audience'] = {
                    "@type": "BusinessAudience",
                    "audienceType": "企业主/财务总监"
                }
                modified = True
    
    if modified:
        new_json = json.dumps(schemas, ensure_ascii=False, indent=2)
        content = content[:ld_match.start(1)] + '\n' + new_json + '\n  ' + content[ld_match.end(1):]
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(content)
        svc_ok += 1
        short = os.path.basename(fp).replace('(source).html', '')[:30]
        print(f"  OK {short}")

print(f"\nServices enhanced: {svc_ok}/{len(service_files)}")
print("\nDone!")
