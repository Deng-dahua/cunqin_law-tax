"""审计文章HTML结构对标金标准"""
import os, re, json
from collections import Counter, defaultdict

SOURCE = r"C:\Users\26726\WorkBuddy\2026-05-20-21-20-24\source\articles"
BENCHMARK = "企业税务风险管控(source).html"

def load_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def extract_sections(html):
    """Extract key HTML structural markers"""
    result = {}
    
    # TOC presence
    result['has_toc'] = bool(re.search(r'class="toc-dt"', html))
    result['toc_title'] = bool(re.search(r'文章目录|目录', html))
    
    # Search bar
    result['has_search_bar'] = bool(re.search(r'article-search-bar|articleSearchInput', html))
    
    # Nav: count nav links
    nav_links = re.findall(r'<nav[^>]*>.*?</nav>', html, re.DOTALL)
    result['nav_links_count'] = len(re.findall(r'<a\s', nav_links[0])) if nav_links else 0
    
    # Hero section
    result['has_hero'] = bool(re.search(r'class="hero-dt"', html))
    result['hero_has_meta'] = bool(re.search(r'hero-dt.*?<div[^>]*class="article-meta', html, re.DOTALL))
    result['hero_has_category'] = bool(re.search(r'article-category', html))
    
    # Schema
    schemas = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.DOTALL)
    result['schema_count'] = len(schemas)
    result['has_article_schema'] = any('Article' in s for s in schemas)
    result['has_breadcrumb'] = any('BreadcrumbList' in s for s in schemas)
    result['has_faq'] = any('FAQPage' in s for s in schemas)
    
    # CTA section
    result['has_cta'] = bool(re.search(r'class="cta-section"', html))
    result['cta_has_h2'] = bool(re.search(r'cta-section.*?<h2', html, re.DOTALL))
    
    # Related reading
    result['has_related'] = bool(re.search(r'延伸阅读|相关文章', html))
    result['related_count'] = len(re.findall(r'延伸阅读-section.*?<a\s', html, re.DOTALL))
    
    # More articles section
    result['has_more_articles'] = bool(re.search(r'更多文章|home-insights', html))
    
    # Scroll buttons
    result['has_scroll_btns'] = bool(re.search(r'scroll-top-btn|scrollToTop', html))
    
    # Footer
    result['has_footer'] = bool(re.search(r'class="footer-dt"', html))
    
    # View counter
    result['has_view_counter'] = bool(re.search(r'pageViewCounter|cunqin-counter', html))
    
    # Scripts
    scripts = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL)
    result['script_count'] = len(scripts)
    result['has_view_script'] = any('fetch(./__counter__/' in s for s in scripts)
    result['has_search_script'] = any('doArticleSearch' in s for s in scripts)
    
    # meta tags
    result['has_canonical'] = bool(re.search(r'rel="canonical"', html))
    result['has_og'] = bool(re.search(r'og:', html))
    result['has_twitter'] = bool(re.search(r'twitter:', html))
    result['has_hreflang'] = bool(re.search(r'hreflang', html))
    
    # Keyword density check
    result['has_meta_keywords'] = bool(re.search(r'<meta name="keywords"', html))
    
    return result

def main():
    benchmark_html = load_file(os.path.join(SOURCE, BENCHMARK))
    benchmark_struct = extract_sections(benchmark_html)
    
    print(f"=== 金标准：{BENCHMARK} ===")
    for k, v in sorted(benchmark_struct.items()):
        print(f"  {k}: {v}")
    
    print(f"\n=== 47篇文章逐篇对比 ===")
    
    issues = defaultdict(list)
    all_ok = []
    
    files = sorted([f for f in os.listdir(SOURCE) if f.endswith('.html') and not f.startswith('_')])
    
    for fname in files:
        html = load_file(os.path.join(SOURCE, fname))
        s = extract_sections(html)
        
        diffs = []
        for k, expected in benchmark_struct.items():
            actual = s.get(k)
            if actual != expected and k not in ('schema_count', 'related_count', 'nav_links_count'):
                # Skip counters that vary by article content
                if k in ('script_count',):  # scripts vary legitimately
                    continue
                diffs.append(f"{k}: expected={expected}, got={actual}")
        
        if diffs:
            for d in diffs:
                issues[d].append(fname)
        else:
            all_ok.append(fname)
    
    print(f"\n完全匹配：{len(all_ok)}/{len(files)} 篇")
    if issues:
        print(f"\n差异汇总（{len(issues)} 类）：")
        for diff_type, affected in sorted(issues.items()):
            print(f"\n  [{len(affected)}篇] {diff_type}")
            for f in affected[:5]:
                print(f"    - {f}")
            if len(affected) > 5:
                print(f"    ... 共 {len(affected)} 篇")
    else:
        print("\n全部47篇与金标准完全一致！")

if __name__ == '__main__':
    main()
