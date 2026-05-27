#!/usr/bin/env python3
"""全站格式一致性审查工具
检查：CSS变量、font-size、line-height、color、navbar、footer 的一致性
"""
import re, os, json
from pathlib import Path
from collections import defaultdict, Counter

SOURCE_DIR = Path(r"C:\Users\26726\WorkBuddy\2026-05-20-21-20-24\source")

def find_html_files():
    """Find all source HTML files"""
    files = []
    for root, dirs, filenames in os.walk(SOURCE_DIR):
        # Skip _post_backup etc
        dirs[:] = [d for d in dirs if not d.startswith('_')]
        for f in filenames:
            if f.endswith('.html'):
                fp = Path(root) / f
                with open(fp, 'r', encoding='utf-8') as fh:
                    content = fh.read()
                files.append({
                    'path': str(fp),
                    'relpath': str(fp.relative_to(SOURCE_DIR)),
                    'content': content
                })
    return files

def empty_css():
    return {
        'css_vars': {}, 'font_sizes': [], 'line_heights': [], 'colors': [],
        'section_padding': [], 'hero_padding_count': 0,
        'nav_classes': {}, 'footer_classes': {}, 'article_body': {}
    }

def extract_css(content):
    """Extract CSS rules from a <style> block"""
    m = re.search(r'<style>(.*?)</style>', content, re.DOTALL)
    if not m:
        return empty_css()
    css = m.group(1)
    
    # Parse CSS variables
    vars_match = re.findall(r'--([\w-]+)\s*:\s*([^;]+);', css)
    css_vars = {k.strip(): v.strip() for k, v in vars_match}
    
    # Parse font-size values (key patterns)
    font_sizes = re.findall(r'font-size:\s*([^;]+);', css)
    
    # Parse line-height values
    line_heights = re.findall(r'line-height:\s*([^;]+);', css)
    
    # Parse color values (not in var references)
    colors = re.findall(r'color:\s*([^;]+);', css)
    
    # Parse section padding
    section_paddings = re.findall(r'\.section-dt\s*\{[^}]*padding:\s*([^;]+);', css)
    
    # Parse hero padding
    hero_paddings = re.findall(r'\.(?:page-hero|article-hero|hero-dt)\s*\{[^}]*\}', css, re.DOTALL)
    
    # Parse nav rules
    nav_classes = {}
    for cls in ['navbar-dt', 'nav-container', 'nav-brand', 'nav-logo', 'nav-menu', 'nav-links']:
        m = re.search(rf'\.{cls}\s*\{{(.*?)\}}', css, re.DOTALL)
        if m:
            nav_classes[cls] = m.group(1).strip()
    
    # Parse footer rules
    footer_classes = {}
    for cls in ['footer-dt', 'footer-grid-dt', 'footer-bottom-dt', 'footer-copyright-dt']:
        m = re.search(rf'\.{cls}\s*\{{(.*?)\}}', css, re.DOTALL)
        if m:
            footer_classes[cls] = m.group(1).strip()
    
    # Parse article-body specific rules
    article_body = {}
    for rule in ['h2', 'h3', 'h4', 'p', 'li', 'strong', 'blockquote']:
        m = re.search(rf'\.article-body\s+{rule}\s*\{{(.*?)\}}', css, re.DOTALL)
        if m:
            article_body[rule] = m.group(1).strip()
    
    uniq_font_sizes = sorted(set(s.strip() for s in font_sizes))
    uniq_line_heights = sorted(set(s.strip() for s in line_heights))
    uniq_colors = sorted(set(s.strip() for s in colors))
    
    result = empty_css()
    result.update({
        'css_vars': css_vars,
        'font_sizes': uniq_font_sizes[:50],
        'line_heights': uniq_line_heights[:30],
        'colors': uniq_colors[:50],
        'section_padding': section_paddings,
        'hero_padding_count': len(hero_paddings),
        'nav_classes': nav_classes,
        'footer_classes': footer_classes,
        'article_body': article_body
    })
    return result

def main():
    files = find_html_files()
    print(f"Found {len(files)} HTML files\n")
    
    # Categorize
    articles = [f for f in files if '/articles/' in f['relpath']]
    services = [f for f in files if '/services/' in f['relpath'] and not f['relpath'].endswith('index.html')]
    other = [f for f in files if f not in articles and f not in services]
    
    # Track differences
    issues = []
    
    # ===== 1. Check CSS Variables across all files =====
    print("=" * 80)
    print("1. CSS VARIABLE CONSISTENCY CHECK")
    print("=" * 80)
    
    var_signatures = {}
    for f in files:
        data = extract_css(f['content'])
        # Create a signature of variable names (order-insensitive)
        sig = tuple(sorted(data['css_vars'].items()))
        key = tuple(sorted(data['css_vars'].keys()))
        if key not in var_signatures:
            var_signatures[key] = []
        var_signatures[key].append(f['relpath'])
    
    print(f"\n  CSS variable sets found: {len(var_signatures)} distinct sets")
    for i, (key, paths) in enumerate(var_signatures.items()):
        if len(paths) <= 3:
            print(f"\n  Set {i+1} ({len(paths)} files): Vars = {list(key)}")
        else:
            print(f"\n  Set {i+1} ({len(paths)} files): Vars = {list(key)}")
        for p in paths[:5]:
            print(f"    - {p}")
        if len(paths) > 5:
            print(f"    ... and {len(paths)-5} more")
    
    # Check if all use same variables
    most_common_vars = max(var_signatures.items(), key=lambda x: len(x[1]))
    standard_vars = most_common_vars[0]
    
    for key, paths in var_signatures.items():
        if key != standard_vars:
            missing = set(standard_vars) - set(key)
            extra = set(key) - set(standard_vars)
            for p in paths:
                issues.append({
                    'type': 'CSS_VARS_DIFFER',
                    'file': p,
                    'detail': f"Missing vars: {missing}, Extra vars: {extra}"
                })
    
    # ===== 2. Check article body formatting =====
    print("\n" + "=" * 80)
    print("2. ARTICLE BODY FORMAT CHECK")
    print("=" * 80)
    
    article_body_issues = []
    reference_article = None
    for a in articles:
        data = extract_css(a['content'])
        ab = data['article_body']
        if ab and not reference_article:
            reference_article = a['relpath']
            reference_ab = ab
            print(f"\n  Reference article: {reference_article}")
            for rule, val in ab.items():
                print(f"    .article-body {rule}: {val}")
            continue
        
        if ab and reference_ab:
            for rule in ['h2', 'h3', 'h4', 'p', 'li', 'strong', 'blockquote']:
                if rule in ab and rule in reference_ab:
                    if ab[rule] != reference_ab[rule]:
                        article_body_issues.append({
                            'type': 'ARTICLE_BODY_DIFFER',
                            'file': a['relpath'],
                            'rule': rule,
                            'expected': reference_ab[rule],
                            'actual': ab[rule]
                        })
    
    print(f"\n  Article body format differences: {len(article_body_issues)}")
    for iss in article_body_issues:
        print(f"    {iss['file']}")
        print(f"      .article-body {iss['rule']}:")
        print(f"        Expected: {iss['expected']}")
        print(f"        Actual:   {iss['actual']}")
        issues.append(iss)
    
    # ===== 3. Check Navbar consistency =====
    print("\n" + "=" * 80)
    print("3. NAVBAR CONSISTENCY CHECK")
    print("=" * 80)
    
    nav_issues = []
    reference_nav = None
    
    # First check home page nav
    for f in other:
        if f['relpath'] == '首页(source).html':
            data = extract_css(f['content'])
            reference_nav = data['nav_classes']
            print(f"\n  Reference navbar: {f['relpath']}")
            for cls, val in reference_nav.items():
                print(f"    .{cls}: {val[:80]}...")
            break
    
    if reference_nav:
        # Check all files
        for f in files:
            data = extract_css(f['content'])
            nc = data['nav_classes']
            for cls in reference_nav:
                if cls in nc and cls in reference_nav:
                    if nc[cls] != reference_nav[cls]:
                        nav_issues.append({
                            'type': 'NAV_DIFFER',
                            'file': f['relpath'],
                            'class': cls,
                            'expected': reference_nav[cls][:60],
                            'actual': nc[cls][:60]
                        })
                elif cls not in nc:
                    nav_issues.append({
                        'type': 'NAV_MISSING',
                        'file': f['relpath'],
                        'class': cls,
                        'detail': 'Class not found'
                    })
    
    print(f"\n  Navbar issues: {len(nav_issues)}")
    for iss in nav_issues[:20]:
        print(f"    {iss['file']}: .{iss.get('class','')} - {iss.get('detail','differs')}")
    
    # ===== 4. Check Footer consistency =====
    print("\n" + "=" * 80)
    print("4. FOOTER CONSISTENCY CHECK")
    print("=" * 80)
    
    footer_sigs = defaultdict(list)
    for f in files:
        data = extract_css(f['content'])
        fc = data['footer_classes']
        sig = tuple(sorted((k, v[:100]) for k, v in fc.items()))
        footer_sigs[sig].append(f['relpath'])
    
    print(f"\n  Footer signature variants: {len(footer_sigs)}")
    for i, (sig, paths) in enumerate(footer_sigs.items()):
        print(f"\n  Variant {i+1} ({len(paths)} files):")
        for k, v in sig:
            print(f"    .{k}: {v}")
        for p in paths[:5]:
            print(f"    → {p}")
        if len(paths) > 5:
            print(f"    ... and {len(paths)-5} more")
    
    # ===== 5. Check key CSS property variations across ALL 39 article files =====
    print("\n" + "=" * 80)
    print("5. ARTICLE-TO-ARTICLE CONSISTENCY (DEEP COMPARE)")
    print("=" * 80)
    
    # Read article hero styles
    hero_styles = {}
    for a in articles:
        content = a['content']
        # Extract hero section
        hero_m = re.search(r'\.article-hero\s*\{(.*?)\}', content, re.DOTALL)
        if hero_m:
            hero_styles[a['relpath']] = hero_m.group(1).strip()
    
    hero_sigs = defaultdict(list)
    for path, style in hero_styles.items():
        # Normalize (remove whitespace differences)
        normalized = re.sub(r'\s+', ' ', style).strip()
        hero_sigs[normalized].append(path)
    
    print(f"\n  Article hero style variants: {len(hero_sigs)}")
    for i, (sig, paths) in enumerate(sorted(hero_sigs.items(), key=lambda x: -len(x[1]))):
        print(f"\n  Variant {i+1} ({len(paths)} articles):")
        print(f"    Style: {sig}")
        for p in paths[:3]:
            print(f"    - {p}")
        if len(paths) > 3:
            print(f"    ... and {len(paths)-3} more")
    
    # Check article body section
    body_styles = {}
    for a in articles:
        content = a['content']
        m = re.search(r'\.article-body\s*\{(.*?)\}', content, re.DOTALL)
        if m:
            body_styles[a['relpath']] = m.group(1).strip()
    
    body_sigs = defaultdict(list)
    for path, style in body_styles.items():
        normalized = re.sub(r'\s+', ' ', style).strip()
        body_sigs[normalized].append(path)
    
    print(f"\n  Article body container style variants: {len(body_sigs)}")
    for i, (sig, paths) in enumerate(sorted(body_sigs.items(), key=lambda x: -len(x[1]))):
        print(f"\n  Variant {i+1} ({len(paths)} articles):")
        print(f"    Style: {sig}")
        for p in paths[:3]:
            print(f"    - {p}")
    
    # ===== 6. Check section padding consistency =====
    print("\n" + "=" * 80)
    print("6. SECTION PADDING CONSISTENCY")
    print("=" * 80)
    
    padding_map = defaultdict(list)
    for f in files:
        data = extract_css(f['content'])
        for pad in data['section_padding']:
            padding_map[pad].append(f['relpath'])
    
    print(f"\n  Section padding values found:")
    for pad, paths in sorted(padding_map.items(), key=lambda x: -len(x[1])):
        print(f"    padding: {pad} → {len(paths)} files")
        for p in paths[:5]:
            print(f"      - {p}")
        if len(paths) > 5:
            print(f"      ... and {len(paths)-5} more")
    
    # ===== Summary =====
    print("\n" + "=" * 80)
    print("7. SUMMARY OF ISSUES")
    print("=" * 80)
    
    print(f"\n  Total CSS_VARS_DIFFER: {len([i for i in issues if i['type']=='CSS_VARS_DIFFER'])}")
    print(f"  Total ARTICLE_BODY_DIFFER: {len(article_body_issues)}")
    print(f"  Total NAV_DIFFER: {len(nav_issues)}")
    
    # Save detailed report
    report = {
        'total_files': len(files),
        'articles': len(articles),
        'services': len(services),
        'other': len(other),
        'var_signatures': {str(k): paths for k, paths in var_signatures.items()},
        'article_body_issues': article_body_issues,
        'nav_issues': nav_issues,
        'hero_variants': {sig: paths for sig, paths in hero_sigs.items()},
        'body_variants': {sig: paths for sig, paths in body_sigs.items()},
        'section_padding': {pad: paths for pad, paths in padding_map.items()},
        'footer_variants': len(footer_sigs)
    }
    
    report_path = SOURCE_DIR.parent / 'tools' / 'format_audit_report.json'
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2, default=str)
    print(f"\n  Full report saved to: {report_path}")
    
    return issues

if __name__ == '__main__':
    issues = main()
