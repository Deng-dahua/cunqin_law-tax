"""Fix JSON-LD trailing commas in 12 articles, then enhance their schemas"""
import re, os, json, glob

base = 'C:/Users/26726/WorkBuddy/2026-05-20-21-20-24'

# Find articles with JSON parse errors
bad_files = []
for fp in sorted(glob.glob(f'{base}/source/articles/*.html')):
    with open(fp, 'r', encoding='utf-8') as f:
        c = f.read()
    ld = re.search(r'<script type="application/ld\+json">(.*?)</script>', c, re.DOTALL)
    if ld:
        try:
            json.loads(ld.group(1))
        except:
            bad_files.append(fp)

print(f"Found {len(bad_files)} articles with broken JSON-LD")

# Fix: remove trailing comma before closing ]
ok = 0
for fp in bad_files:
    with open(fp, 'r', encoding='utf-8') as f:
        c = f.read()
    
    ld = re.search(r'<script type="application/ld\+json">(.*?)</script>', c, re.DOTALL)
    if not ld:
        continue
    
    js = ld.group(1)
    
    # Fix pattern: },\n\n] at end → }\n]
    # The issue is trailing comma before array closing
    js_fixed = re.sub(r'},\s*\n\s*\]', r'}\n  ]', js)
    
    if js_fixed != js:
        c = c[:ld.start(1)] + '\n' + js_fixed + '\n  ' + c[ld.end(1):]
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(c)
        ok += 1
        short = os.path.basename(fp).replace('(source).html', '')[:30]
        print(f"  FIXED {short}")

print(f"\nFixed: {ok} files")

# Now re-run Part 1 of enhance_schemas_v2 on these files
print("\n" + "=" * 60)
print("Re-running Article Schema enhancement on fixed files")
print("=" * 60)

ok2 = 0
for fp in bad_files:
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()
    
    body_match = re.search(r'<article class="article-body">(.*?)</article>', content, re.DOTALL)
    if not body_match:
        body_match = re.search(r"<article class='article-body'>(.*?)</article>", content, re.DOTALL)
    if not body_match:
        print(f"  SKIP {os.path.basename(fp)}: no article-body")
        continue
    
    body_text = re.sub(r'<[^>]+>', ' ', body_match.group(1))
    body_text = re.sub(r'\s+', ' ', body_text).strip()
    word_count = len(body_text)
    
    cat_match = re.search(r'<meta name="keywords"[^>]*content="([^"]*)"', content)
    category = "财税咨询"
    if cat_match:
        kw = cat_match.group(1)
        if '实操' in kw: category = '实操指南'
        elif '政策' in kw: category = '政策解读'
        elif '行业' in kw: category = '行业洞察'
    
    ld_match = re.search(r'<script type="application/ld\+json">(.*?)</script>', content, re.DOTALL)
    if not ld_match:
        continue
    
    try:
        schemas = json.loads(ld_match.group(1))
    except:
        print(f"  STILL BROKEN {os.path.basename(fp)}")
        continue
    
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
        content = content[:ld_match.start(1)] + '\n' + new_json + '\n  ' + content[ld_match.end(1):]
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(content)
        ok2 += 1
        short = os.path.basename(fp).replace('(source).html', '')[:30]
        print(f"  OK [{word_count}字] {short}")

print(f"\nSecond pass enhanced: {ok2} articles")
print(f"Total articles enhanced: {27 + ok2}/39")
