import re, glob, os

os.chdir("C:/Users/26726/WorkBuddy/2026-05-20-21-20-24/source/articles")
files = sorted(glob.glob("*.html"))

# ====== 1. NEAR-DUPLICATE CONTENT CHECK ======
print("="*80)
print("1. NEAR-DUPLICATE CONTENT ANALYSIS")
print("="*80)

def get_article_body(raw):
    """Extract article main content, removing nav, footer, styles, scripts"""
    body_match = re.search(r"<article[^>]*>(.*?)</article>", raw, re.DOTALL)
    if not body_match:
        body_match = re.search(r'<div[^>]*class="[^"]*article-content[^"]*"[^>]*>(.*?)</div>', raw, re.DOTALL)
    if not body_match:
        body_match = re.search(r"<main[^>]*>(.*?)</main>", raw, re.DOTALL)
    if body_match:
        text = body_match.group(1)
    else:
        body_match = re.search(r"<body[^>]*>(.*?)</body>", raw, re.DOTALL)
        text = body_match.group(1) if body_match else raw
    
    text = re.sub(r"<style[^>]*>.*?</style>", "", text, flags=re.DOTALL)
    text = re.sub(r"<script[^>]*>.*?</script>", "", text, flags=re.DOTALL)
    text = re.sub(r"<nav[^>]*>.*?</nav>", "", text, flags=re.DOTALL)
    text = re.sub(r"<footer[^>]*>.*?</footer>", "", text, flags=re.DOTALL)
    text = re.sub(r"<header[^>]*>.*?</header>", "", text, flags=re.DOTALL)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

contents = {}
for f in files:
    with open(f, "r", encoding="utf-8") as fh:
        contents[f] = get_article_body(fh.read())

# Jaccard similarity on word-level n-grams
def jaccard_similarity(t1, t2, n=50):
    def ngrams(s, n):
        chars = list(s)
        return set("".join(chars[i:i+n]) for i in range(0, len(chars)-n+1, max(1, n//2)))
    ng1, ng2 = ngrams(t1, n), ngrams(t2, n)
    if not ng1 or not ng2:
        return 0
    return len(ng1 & ng2) / min(len(ng1), len(ng2))

print("\nPairwise similarity (char 50-grams):")
for i, f1 in enumerate(files):
    for f2 in files[i+1:]:
        sim = jaccard_similarity(contents[f1], contents[f2])
        flag = " *** HIGH ***" if sim > 0.4 else " ++ MEDIUM ++" if sim > 0.25 else ""
        if sim > 0.15:
            print(f"  {f1[:35]:<35} vs {f2[:35]:<35} => {sim:.2%}{flag}")

# ====== 2. CTA SECTION TEXT EXTRACTION ======
print("\n" + "="*80)
print("2. CTA SECTION TEXT ANALYSIS")
print("="*80)

cta_texts = {}
for f in files:
    with open(f, "r", encoding="utf-8") as fh:
        raw = fh.read()
    cta_match = re.search(r'<section[^>]*class="[^"]*cta[^"]*"[^>]*>(.*?)</section>', raw, re.DOTALL)
    if cta_match:
        cta_text = re.sub(r"<[^>]+>", " ", cta_match.group(1))
        cta_text = re.sub(r"\s+", " ", cta_text).strip()[:300]
        cta_texts[f] = cta_text
        print(f"\n  {f}:")
        print(f"    [{cta_text[:200]}...]")
    else:
        print(f"\n  {f}: NO CTA SECTION")

# Check CTA uniqueness
print("\nCTA similarity check:")
for i, f1 in enumerate(files):
    for f2 in files[i+1:]:
        if f1 in cta_texts and f2 in cta_texts:
            sim = jaccard_similarity(cta_texts[f1], cta_texts[f2], n=30)
            if sim > 0.5:
                print(f"  {f1[:35]} vs {f2[:35]} => {sim:.2%} (near-duplicate CTA)")

# ====== 3. JSON-LD STRUCTURED DATA QUALITY ======
print("\n" + "="*80)
print("3. JSON-LD STRUCTURED DATA QUALITY CHECK")
print("="*80)

for f in files:
    with open(f, "r", encoding="utf-8") as fh:
        raw = fh.read()
    jsonld_matches = re.findall(r'<script type="application/ld\+json">(.*?)</script>', raw, re.DOTALL)
    print(f"\n  {f}:")
    for i, ld in enumerate(jsonld_matches):
        has_context = '"@context"' in ld
        has_type = '"@type"' in ld
        has_headline = '"headline"' in ld
        has_author = '"author"' in ld
        has_date = '"datePublished"' in ld
        has_image = '"image"' in ld
        has_publisher = '"publisher"' in ld
        has_desc = '"description"' in ld
        
        checks = [
            f"@context={'OK' if has_context else 'MISS'}",
            f"@type={'OK' if has_type else 'MISS'}",
            f"headline={'OK' if has_headline else 'MISS'}",
            f"author={'OK' if has_author else 'MISS'}",
            f"datePub={'OK' if has_date else 'MISS'}",
            f"image={'OK' if has_image else 'MISS'}",
            f"publisher={'OK' if has_publisher else 'MISS'}",
            f"description={'OK' if has_desc else 'MISS'}"
        ]
        print(f"    Block #{i+1}: {', '.join(checks)}")

# ====== 4. INTERNAL LINKING STRUCTURE ======
print("\n" + "="*80)
print("4. INTERNAL LINKING ANALYSIS")
print("="*80)

all_internal_links = set()
for f in files:
    with open(f, "r", encoding="utf-8") as fh:
        raw = fh.read()
    links = re.findall(r'href="(/(?:about|articles|services|cases|contact|archives)/[^"]*\.html)"', raw)
    for link in links:
        all_internal_links.add(link)

print(f"\n  Total unique internal links across all articles: {len(all_internal_links)}")
print("  Links found:")
for link in sorted(all_internal_links):
    print(f"    {link}")

# ====== 5. HEADING HIERARCHY CHECK ======
print("\n" + "="*80)
print("5. HEADING HIERARCHY DEEP DIVE")
print("="*80)

for f in files:
    with open(f, "r", encoding="utf-8") as fh:
        raw = fh.read()
    h2s = re.findall(r"<h2[^>]*>(.*?)</h2>", raw, re.DOTALL)
    print(f"\n  {f}:")
    print(f"    H1 count: {len(re.findall(r'<h1[^>]*>', raw))}")
    for j, h2 in enumerate(h2s):
        h2_text = re.sub(r"<[^>]+>", "", h2).strip()[:80]
        print(f"    H2 #{j+1}: {h2_text}")

# ====== 6. FREQUENT KEYWORDS IN BODY ======
print("\n" + "="*80)
print("6. TOP KEYWORD FREQUENCY IN BODY TEXT")
print("="*80)

from collections import Counter

for f in files:
    text = contents[f]
    # Count bigrams of Chinese characters
    words = re.findall(r"[\u4e00-\u9fff]{2,4}", text)
    counter = Counter(words)
    top_terms = counter.most_common(15)
    
    print(f"\n  {f}:")
    kw_str = " | ".join([f"{term}({count})" for term, count in top_terms[:10]])
    print(f"    Top terms: {kw_str}")

print("\n" + "="*80)
print("AUDIT COMPLETE")
print("="*80)
