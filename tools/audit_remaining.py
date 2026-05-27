#!/usr/bin/env python3
"""针对性检查：cta-section height、margin-bottom、section-title font-size、hero h1 font-size"""
import re, os
from pathlib import Path

SOURCE = Path(r"C:\Users\26726\WorkBuddy\2026-05-20-21-20-24\source")
BENCHMARK = SOURCE / "articles" / "企业税务风险管控(source).html"

def find_htmls(subdir=None):
    files = []
    search_dir = SOURCE / subdir if subdir else SOURCE
    for root, dirs, filenames in os.walk(search_dir):
        dirs[:] = [d for d in dirs if not d.startswith('_')]
        for f in filenames:
            if f.endswith('.html'):
                fp = Path(root) / f
                with open(fp, 'r', encoding='utf-8') as fh:
                    content = fh.read()
                files.append({'path': str(fp), 'rel': str(fp.relative_to(SOURCE)), 'content': content})
    return files

def extract_property(css, selector, prop):
    """Extract a CSS property value from a selector"""
    # Match selector { ... } block
    escaped = re.escape(selector)
    # Try multi-line match
    m = re.search(rf'\.{escaped}\s*\{{(.*?)\}}', css, re.DOTALL)
    if not m:
        return None
    body = m.group(1)
    # Find the property
    pm = re.search(rf'{re.escape(prop)}\s*:\s*([^;]+);', body)
    return pm.group(1).strip() if pm else None

def main():
    print("=" * 60)
    print("针对性格式检查")
    print("=" * 60)
    
    # Read benchmark
    with open(BENCHMARK, 'r', encoding='utf-8') as f:
        bench_content = f.read()
    
    # Extract benchmark values
    bench_css = re.search(r'<style>(.*?)</style>', bench_content, re.DOTALL)
    bench_css = bench_css.group(1) if bench_css else ""
    
    checks = [
        ("cta-section height", extract_property(bench_css, "cta-section", "min-height")),
        ("section-title font-size", extract_property(bench_css, "section-title-dt", "font-size")),
        ("article-hero h1 font-size", None),  # Will check via regex
    ]
    
    # Benchmark hero h1 (from the .article-hero h1 rule)
    hm = re.search(r'\.article-hero\s+h1\s*\{(.*?)\}', bench_css, re.DOTALL)
    bench_hero_h1 = ""
    if hm:
        fm = re.search(r'font-size:\s*([^;]+);', hm.group(1))
        if fm:
            bench_hero_h1 = fm.group(1).strip()
    checks[2] = ("article-hero h1 font-size", bench_hero_h1)
    
    print(f"\nBenchmark ({BENCHMARK.name}):")
    for name, val in checks:
        print(f"  {name}: {val}")
    
    # Check all articles
    articles = find_htmls('articles')
    issues = []
    
    for a in articles:
        m = re.search(r'<style>(.*?)</style>', a['content'], re.DOTALL)
        css = m.group(1) if m else ""
        
        # 1. cta-section height
        val = extract_property(css, "cta-section", "min-height")
        if val and val != checks[0][1]:
            issues.append(("cta-section min-height", a['rel'], checks[0][1], val))
        
        # 2. article-hero h1 font-size
        hm = re.search(r'\.article-hero\s+h1\s*\{(.*?)\}', css, re.DOTALL)
        if hm:
            fm = re.search(r'font-size:\s*([^;]+);', hm.group(1))
            if fm:
                val = fm.group(1).strip()
                if val != bench_hero_h1:
                    issues.append(("article-hero h1 font-size", a['rel'], bench_hero_h1, val))
    
    # Check non-article pages for section-title-dt
    print("\n--- Non-article pages: section-title-dt font-size ---")
    non_articles = find_htmls('about') + find_htmls('services') + find_htmls('contact') + find_htmls('cases') + find_htmls('archives')
    
    section_title_vals = {}
    for f in non_articles:
        m = re.search(r'<style>(.*?)</style>', f['content'], re.DOTALL)
        css = m.group(1) if m else ""
        val = extract_property(css, "section-title-dt", "font-size")
        if val:
            if val not in section_title_vals:
                section_title_vals[val] = []
            section_title_vals[val].append(f['rel'])
    
    for val, paths in sorted(section_title_vals.items()):
        print(f"  font-size: {val} → {len(paths)} files")
        for p in paths[:3]:
            print(f"    - {p}")
    
    # Check margin-bottom on article-body h2/h3
    print("\n--- Article body h2/h3 margin-bottom ---")
    h2_margins = {}
    h3_margins = {}
    for a in articles:
        m = re.search(r'<style>(.*?)</style>', a['content'], re.DOTALL)
        css = m.group(1) if m else ""
        for tag in ['h2', 'h3']:
            rm = re.search(rf'\.article-body\s+{tag}\s*\{{(.*?)\}}', css, re.DOTALL)
            if rm:
                mb = re.search(r'margin-bottom:\s*([^;]+);', rm.group(1))
                if mb:
                    val = mb.group(1).strip()
                    if tag == 'h2':
                        h2_margins[val] = h2_margins.get(val, 0) + 1
                    else:
                        h3_margins[val] = h3_margins.get(val, 0) + 1
    
    print(f"  h2 margin-bottom: {h2_margins}")
    print(f"  h3 margin-bottom: {h3_margins}")
    
    # Report issues
    print("\n" + "=" * 60)
    print(f"ISSUES FOUND: {len(issues)}")
    for iss in issues:
        print(f"  [{iss[0]}] {iss[1]}")
        print(f"    Expected: {iss[2]}  Actual: {iss[3]}")
    
    if not issues and len(section_title_vals) <= 1:
        print("  ALL CLEAN - No format issues remaining!")

if __name__ == '__main__':
    main()
