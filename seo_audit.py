import re, glob, os

os.chdir("C:/Users/26726/WorkBuddy/2026-05-20-21-20-24/source/articles")
files = sorted(glob.glob("*.html"))

print("="*100)
print("ARTICLE SEO/GEO COMPREHENSIVE AUDIT REPORT")
print("="*100)

results = []

for f in files:
    with open(f, "r", encoding="utf-8") as fh:
        raw = fh.read()

    print(f"\n### {f}")
    print("-"*80)

    title_match = re.search(r"<title>(.*?)</title>", raw)
    title = title_match.group(1) if title_match else "MISSING"
    title_len = len(title)
    print(f"  Title Length: {title_len} chars (optimal: 50-60)")

    desc_match = re.search(r'<meta name="description" content="(.*?)"', raw)
    desc = desc_match.group(1) if desc_match else "MISSING"
    desc_len = len(desc)
    print(f"  Description Length: {desc_len} chars (optimal: 120-160)")

    kw_match = re.search(r'<meta name="keywords" content="(.*?)"', raw)
    kw = kw_match.group(1) if kw_match else "MISSING"
    kw_list = [k.strip() for k in kw.split(",")] if kw != "MISSING" else []
    print(f"  Keywords Count: {len(kw_list)}")

    can_match = re.search(r'<link rel="canonical" href="(.*?)"', raw)
    print(f"  Canonical: {can_match.group(1) if can_match else 'MISSING'}")

    og_title = re.search(r'<meta property="og:title" content="(.*?)"', raw)
    og_desc = re.search(r'<meta property="og:description" content="(.*?)"', raw)
    og_image = re.search(r'<meta property="og:image" content="(.*?)"', raw)
    og_type = re.search(r'<meta property="og:type" content="(.*?)"', raw)
    og_url = re.search(r'<meta property="og:url" content="(.*?)"', raw)
    og_site = re.search(r'<meta property="og:site_name"', raw)
    og_locale = re.search(r'<meta property="og:locale"', raw)
    
    og_ok = "OK" if og_title and og_desc and og_image and og_type and og_url else "PARTIAL"
    print(f"  OG Tags: {og_ok} (title={len(og_title.group(1)) if og_title else 0}c, desc={len(og_desc.group(1)) if og_desc else 0}c)")

    tw_card = re.search(r'<meta name="twitter:card"', raw)
    tw_all = "OK" if tw_card and re.search(r'twitter:title', raw) and re.search(r'twitter:description', raw) and re.search(r'twitter:image', raw) else "PARTIAL"
    print(f"  Twitter Tags: {tw_all}")

    pub_time = re.search(r'<meta property="article:published_time" content="(.*?)"', raw)
    mod_time = re.search(r'<meta property="article:modified_time" content="(.*?)"', raw)
    author = re.search(r'<meta property="article:author" content="(.*?)"', raw)
    print(f"  Published: {pub_time.group(1) if pub_time else 'MISSING'} | Modified: {mod_time.group(1) if mod_time else 'MISSING'} | Author: {author.group(1) if author else 'MISSING'}")

    robots = re.search(r'<meta name="robots" content="(.*?)"', raw)
    print(f"  Robots: {robots.group(1) if robots else 'MISSING'}")

    hreflang = re.search(r'<link rel="alternate" hreflang="(.*?)"', raw)
    print(f"  Hreflang: {hreflang.group(1) if hreflang else 'MISSING'}")

    jsonld_matches = re.findall(r'<script type="application/ld\+json">(.*?)</script>', raw, re.DOTALL)
    if jsonld_matches:
        types_found = []
        for ld in jsonld_matches:
            ld_type = re.search(r'"@type"\s*:\s*"(.*?)"', ld)
            if ld_type:
                types_found.append(ld_type.group(1))
        print(f"  JSON-LD: PRESENT ({len(jsonld_matches)} blocks) Types: {types_found}")
    else:
        print(f"  JSON-LD: MISSING")

    h1s = re.findall(r"<h1[^>]*>(.*?)</h1>", raw, re.DOTALL)
    h2s = re.findall(r"<h2[^>]*>(.*?)</h2>", raw, re.DOTALL)
    h3s = re.findall(r"<h3[^>]*>(.*?)</h3>", raw, re.DOTALL)
    print(f"  H1={len(h1s)} | H2={len(h2s)} | H3={len(h3s)}")

    imgs = re.findall(r"<img[^>]*>", raw)
    imgs_with_alt = re.findall(r'<img[^>]*alt="[^"]+"[^>]*>', raw)
    imgs_with_empty_alt = re.findall(r'<img[^>]*alt=""[^>]*>', raw)
    print(f"  Images: {len(imgs)} total | {len(imgs_with_alt)} w/alt | {len(imgs) - len(imgs_with_alt)} missing")

    int_links = re.findall(r'href="(?:/[a-z]|\.\./)[^"]*\.html"', raw)
    ext_nofollow = re.findall(r'href="https?://(?!cunqin\.tax)[^"]*"', raw)
    print(f"  Links: {len(int_links)} internal | {len(ext_nofollow)} external/cdn")

    body_match = re.search(r"<body[^>]*>(.*?)</body>", raw, re.DOTALL)
    if body_match:
        body = body_match.group(1)
    else:
        body = raw
    body = re.sub(r"<style[^>]*>.*?</style>", "", body, flags=re.DOTALL)
    body = re.sub(r"<script[^>]*>.*?</script>", "", body, flags=re.DOTALL)
    text = re.sub(r"<[^>]+>", "", body)
    text = re.sub(r"\s+", " ", text).strip()
    chinese_chars = len(re.findall(r"[\u4e00-\u9fff]", text))
    english_words = len(re.findall(r"[a-zA-Z]+", text))
    total_words = chinese_chars + english_words
    print(f"  Word Count: ~{total_words} ({chinese_chars} CN chars + {english_words} EN words)")

    bc_ok = "PRESENT" if re.search(r'breadcrumb', raw) else "MISSING"
    cta_ok = "PRESENT" if re.search(r'class="[^"]*cta', raw) else "MISSING"
    print(f"  Breadcrumb: {bc_ok} | CTA: {cta_ok}")

    generic_kw = [kw for kw in kw_list if kw in ["存勤法税","业管财税法","财税顾问","税务筹划","邓达华"]]
    specific_kw = [kw for kw in kw_list if kw not in ["存勤法税","业管财税法","财税顾问","税务筹划","邓达华"]]
    print(f"  Keywords: {len(generic_kw)} generic + {len(specific_kw)} specific")

    results.append({
        "file": f[:45], "title_len": title_len, "desc_len": desc_len,
        "kw_count": len(kw_list), "h1": len(h1s), "h2": len(h2s),
        "h3": len(h3s), "imgs": len(imgs), "imgs_alt": len(imgs_with_alt),
        "int_links": len(int_links), "words": total_words,
        "bc": bc_ok, "cta": cta_ok, "jsonld": "YES" if jsonld_matches else "NO",
        "pub": pub_time.group(1) if pub_time else "N/A"
    })

print("\n" + "="*100)
print("SUMMARY COMPARISON TABLE")
print("="*100)
header = f"{'File':<45} {'Title':>6} {'Desc':>6} {'KW':>4} {'H1':>3} {'H2':>3} {'H3':>3} {'Img':>4} {'Alt':>4} {'Lnks':>5} {'Words':>7} {'BC':>7} {'CTA':>7} {'JSON':>6} {'PubDate':>10}"
print(header)
print("-"*100)

for r in results:
    print(f"{r['file']:<45} {r['title_len']:>6} {r['desc_len']:>6} {r['kw_count']:>4} {r['h1']:>3} {r['h2']:>3} {r['h3']:>3} {r['imgs']:>4} {r['imgs_alt']:>4} {r['int_links']:>5} {r['words']:>7} {r['bc']:>7} {r['cta']:>7} {r['jsonld']:>6} {r['pub']:>10}")

print("="*100)

# Analysis of issues
print("\nISSUES FOUND:")
for r in results:
    issues = []
    if r['title_len'] > 70: issues.append(f"Title too long ({r['title_len']}c)")
    if r['desc_len'] > 200: issues.append(f"Description too long ({r['desc_len']}c)")
    if r['desc_len'] < 100: issues.append(f"Description too short ({r['desc_len']}c)")
    if r['kw_count'] < 5: issues.append(f"Too few keywords ({r['kw_count']})")
    if r['h1'] != 1: issues.append(f"H1 count = {r['h1']} (should be 1)")
    if r['h2'] < 2: issues.append(f"Too few H2 ({r['h2']})")
    if r['imgs'] > 0 and r['imgs_alt'] < r['imgs']: issues.append(f"Missing alt on {r['imgs'] - r['imgs_alt']} images")
    if r['int_links'] < 3: issues.append(f"Too few internal links ({r['int_links']})")
    if r['bc'] == "MISSING": issues.append("No breadcrumb")
    if r['cta'] == "MISSING": issues.append("No CTA section")
    if r['jsonld'] == "NO": issues.append("No JSON-LD structured data")
    if r['words'] < 1000: issues.append(f"Content too short ({r['words']} words)")
    
    if issues:
        print(f"  {r['file']}:")
        for iss in issues:
            print(f"    - {iss}")
    else:
        print(f"  {r['file']}: ALL CHECKS PASSED")
