#!/usr/bin/env python3
"""
从 tools/articles_batch1-3.json 批量生成 11 篇新文章 HTML
使用金税四期文章作为模板，替换变量部分。
"""
import json
import os
import re
from datetime import datetime

TEMPLATE_PATH = r'C:\Users\26726\WorkBuddy\2026-05-20-21-20-24\source\articles\金税四期全面解读(source).html'
ARTICLES_DIR = r'C:\Users\26726\WorkBuddy\2026-05-20-21-20-24\source\articles'
JSON_DIR = r'C:\Users\26726\WorkBuddy\2026-05-20-21-20-24\tools'

# Site-wide constants
SITE_URL = 'https://cunqin.tax'
AUTHOR = '邓达华'
PUBLISHER = '存勤法税服务（广州）有限公司'
DEFAULT_DATE_MODIFIED = '2026-05-24'
DEFAULT_VIEWS = 100


def load_template():
    with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
        return f.read()


def load_all_articles():
    articles = []
    for batch in ['articles_batch1.json', 'articles_batch2.json', 'articles_batch3.json']:
        path = os.path.join(JSON_DIR, batch)
        with open(path, 'r', encoding='utf-8') as f:
            articles.extend(json.load(f))
    return articles


def escape_html_attr(s):
    """Escape quotes for HTML attributes"""
    return s.replace('&', '&amp;').replace('"', '&quot;').replace('<', '&lt;').replace('>', '&gt;')


def expand_description(article, min_len=120):
    """Ensure meta description is at least min_len characters"""
    desc = article.get('meta_description', '')
    if len(desc) >= min_len:
        return desc
    
    # Extract plain text from body
    body = article.get('body', '')
    plain = re.sub(r'<[^>]+>', '', body)
    plain = re.sub(r'\s+', '', plain)
    
    # Append more text from body
    remaining = min_len - len(desc)
    if len(plain) > 100:
        # Add meaningful content from body (enough margin)
        extra = plain[:remaining + 50]
        # Try to end at a sentence boundary
        best_pos = len(extra)
        for sep in ['。', '！', '？']:
            pos = extra.rfind(sep)
            if remaining - 10 <= pos < best_pos:
                best_pos = pos + 1
        if best_pos < remaining + 10:
            # Sentence boundary found
            desc = desc + extra[:best_pos]
        else:
            # No good boundary, just pad to min_len
            desc = desc + extra[:remaining + 10]
    
    # If still under min_len, brute force it
    if len(desc) < min_len and len(plain) > min_len:
        desc = desc + plain[:min_len - len(desc) + 10]
    
    return desc[:160]  # Cap at 160 for OG


def generate_meta_section(article):
    """Generate the <head> meta tags section"""
    slug = article['slug']
    title = article['title']
    headline = article.get('headline', title)
    category = article.get('category', '实操指南')
    date = article.get('date', '2026-05-21')
    keywords = article.get('keywords', '')
    meta_desc = expand_description(article)
    
    permalink = f'/articles/{slug}.html'
    url = f'{SITE_URL}{permalink}'
    title_full = f'{headline} - {PUBLISHER}'
    
    # Build meta tags
    meta = f'''---
permalink: {permalink}
layout: false
---
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta name="msvalidate.01" content="643F9F9C5376BCE8168CB8533417070C" />
  <meta name="baidu-site-verification" content="codeva-9SPpSVW5X6" />
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="robots" content="index, follow">
<meta name="keywords" content="{escape_html_attr(keywords)}">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="zh-CN" href="{url}">
<link rel="apple-touch-icon" href="{SITE_URL}/images/nav-logo.webp">
<link rel="apple-touch-icon" sizes="180x180" href="{SITE_URL}/images/nav-logo.webp">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="存勤法税">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="theme-color" content="#003f6c">
<meta name="msapplication-TileColor" content="#003f6c">
<meta property="og:title" content="{escape_html_attr(title_full)}">
<meta property="og:description" content="{escape_html_attr(meta_desc)}">
<meta property="og:image" content="{SITE_URL}/images/nav-logo.webp">
<meta property="og:url" content="{url}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="存勤法税官网">
<meta property="og:locale" content="zh_CN">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{escape_html_attr(title_full)}">
<meta name="twitter:description" content="{escape_html_attr(meta_desc[:120])}">
<meta name="twitter:image" content="{SITE_URL}/images/nav-logo.webp">
<meta property="article:published_time" content="{date}">
<meta property="article:modified_time" content="{DEFAULT_DATE_MODIFIED}">
<meta property="article:author" content="{AUTHOR}">
  <title>{escape_html_attr(title_full)}</title>
  <meta name="description" content="{escape_html_attr(meta_desc)}">'''
    return meta


def generate_jsonld(article):
    """Generate JSON-LD Schema array"""
    slug = article['slug']
    title = article['title']
    meta_desc = expand_description(article)
    date = article.get('date', '2026-05-21')
    faq = article.get('faq', [])
    category = article.get('category', '实操指南')
    
    permalink = f'/articles/{slug}.html'
    url = f'{SITE_URL}{permalink}'
    
    # Escape title for JSON
    title_escaped = title.replace('"', '\\"')
    desc_escaped = meta_desc.replace('"', '\\"').replace('\n', ' ')
    
    # Build Article schema
    article_schema = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "description": meta_desc,
        "image": f"{SITE_URL}/images/founder-new.webp",
        "datePublished": date,
        "dateModified": DEFAULT_DATE_MODIFIED,
        "author": {
            "@type": "Person",
            "name": AUTHOR,
            "url": f"{SITE_URL}/about/"
        },
        "publisher": {
            "@type": "Organization",
            "name": PUBLISHER,
            "logo": {
                "@type": "ImageObject",
                "url": f"{SITE_URL}/images/nav-logo.webp"
            }
        },
        "mainEntityOfPage": {
            "@type": "WebPage",
            "@id": url
        }
    }
    
    # Build BreadcrumbList
    breadcrumb = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "首页", "item": SITE_URL},
            {"@type": "ListItem", "position": 2, "name": "法税洞察", "item": f"{SITE_URL}/archives/"},
            {"@type": "ListItem", "position": 3, "name": title}
        ]
    }
    
    # Build FAQPage from JSON
    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": faq
    }
    
    schema_list = [article_schema, breadcrumb, faq_schema]
    json_str = json.dumps(schema_list, ensure_ascii=False, indent=2)
    return f'<script type="application/ld+json">\n{json_str}\n</script>'


def generate_hero_section(article):
    """Generate the hero section HTML"""
    title = article['title']
    category = article.get('category', '实操指南')
    date = article.get('date', '2026-05-21')
    slug = article['slug']
    base_views = article.get('base_views', DEFAULT_VIEWS)
    
    # Format views
    views_str = f'{base_views:,}'
    
    return f'''<!-- ===== Hero ===== -->
<section class="article-hero">
  <div class="container-dt">
    <span class="cat-tag">{category}</span> <span style="display:inline-block;background:#e8f5e9;color:#2e7d32;padding:0.3rem 1rem;border-radius:50px;font-size:0.82rem;margin-left:0.8rem;font-weight:600;">原创</span>
    <h1>{title}</h1>
    <div class="art-meta">
      <span><i class="fas fa-calendar-alt"></i> <time datetime="{date}">{date}</time></span>
      <span><i class="fas fa-user-edit"></i> {AUTHOR}丨{PUBLISHER}</span>
      <span class="art-view-counter" data-slug="{slug}"><i class="fas fa-eye"></i> <span class="view-num" id="view-{slug}">{views_str}</span> 阅读</span>
    </div>
  </div>


</section>'''


def generate_breadcrumb(article):
    """Generate breadcrumb HTML"""
    title = article['title']
    return f'''<!-- ===== 面包屑 ===== -->
<div style="max-width:860px;margin:0 auto;padding:0.8rem 1rem;font-size:0.85rem;color:var(--dt-text-light);">
  <a href="../index.html" style="color:var(--dt-text-light);">首页</a> &gt;
  <a href="../archives/" style="color:var(--dt-text-light);">法税洞察</a> &gt;
  <span style="color:var(--dt-text);">{title}</span>
</div>'''


def generate_related_cards(article):
    """Generate related reading cards HTML"""
    related = article.get('related', [])
    if not related:
        return '<div class="related-reading">\n    <h3 id="延伸阅读" class="related-heading"><span>延伸阅读</span>\n  </div>'
    
    cards = []
    for r in related:
        cards.append(f'''      <a href="{r['slug']}.html" class="related-card">
        <span class="related-cat">{r.get('cat', '实操指南')}</span>
        <div class="related-info">
          <h4>{r.get('title', '')}</h4>
          <p>{r.get('desc', '')}</p>
        </div>
        <span class="related-arrow"><i class="fas fa-arrow-right"></i></span>
      </a>''')
    
    return f'''<div class="related-reading">
    <h3 id="延伸阅读" class="related-heading"><span>延伸阅读</span>
    <div class="related-grid">
{chr(10).join(cards)}
    </div>
  </div>'''


def generate_article_notice():
    return '''<!-- ===== 文章声明 ===== -->
<div class="article-notice" style="max-width:860px;margin:0 auto 2rem;padding:1.2rem 1.5rem;background:var(--dt-bg-light);border-left:4px solid var(--dt-accent);border-radius:0 8px 8px 0;font-size:0.85rem;color:var(--dt-text-light);line-height:1.8;">
  <p style="margin-bottom:0.5rem;"><strong style="color:var(--dt-primary);">原创声明：</strong>本文为存勤法税服务（广州）有限公司原创文章，作者邓达华。</p>
  <p style="margin-bottom:0.5rem;"><strong style="color:var(--dt-primary);">免责声明：</strong>本文内容仅供一般信息参考，不构成任何形式的专业建议或服务邀约。具体税务问题请咨询专业顾问并结合企业实际情况判断。</p>
  <p><strong style="color:var(--dt-primary);">版权声明：</strong>未经书面授权，禁止任何形式的转载、摘编或使用。</p>
</div>'''


def generate_view_counter_js(article):
    """Generate view counter JS"""
    slug = article['slug']
    base = article.get('base_views', DEFAULT_VIEWS)
    return f'''<script>
  /* ===== 动态阅读量计数 ===== */
  (function(){{
    var slug = '{slug}';
    var base = {base};
    var storageKey = 'cq_view_' + slug;
    var sessionKey = 'cq_sess_' + slug;
    var el = document.getElementById('view-' + slug);
    if (!el) return;

    // 从localStorage获取当前计数
    var stored = localStorage.getItem(storageKey);
    var count = stored ? parseInt(stored, 10) : base;

    // 新会话则递增
    if (!sessionStorage.getItem(sessionKey)) {{
      count += 1;
      localStorage.setItem(storageKey, count);
      sessionStorage.setItem(sessionKey, '1');
    }}

    // 格式化并显示
    el.textContent = count.toLocaleString();
  }})();
</script>'''


def load_static_sections():
    """Load the CSS and static HTML sections from the template"""
    with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
        template = f.read()
    
    # Extract CSS block (from </head> backwards to <link rel="icon"...)
    css_start = template.find('<link rel="icon" href="../images/nav-logo.webp"')
    css_end = template.find('</head>')
    css_block = template[css_start:css_end]
    
    # Extract nav bar
    nav_start = template.find('<!-- ===== 导航栏 ===== -->')
    main_start = template.find('<main>')
    nav_block = template[nav_start:main_start]
    
    # Extract search bar
    search_start = template.find('<!-- ===== 文内搜索栏 ===== -->')
    toc_start = template.find('<!-- ===== 文章布局（目录 + 正文） ===== -->')
    search_block = template[search_start:toc_start]
    
    # Extract article layout start + TOC
    layout_start = template.find('<!-- ===== 文章布局（目录 + 正文） ===== -->')
    breadcrumb_start = template.find('<!-- ===== 面包屑 ===== -->')
    layout_block = template[layout_start:breadcrumb_start]
    
    # Extract "more articles" section
    more_start = template.find('<!-- ===== 更多文章 ===== -->')
    cta_start = template.find('<!-- ===== CTA ===== -->')
    more_block = template[more_start:cta_start]
    
    # Extract CTA + footer + JS (TOC, scroll buttons, search)
    footer_block = template[cta_start:]
    
    return {
        'css': css_block,
        'nav': nav_block,
        'search': search_block,
        'layout_start': layout_block,
        'more': more_block,
        'footer': footer_block
    }


def generate_article(article, static):
    """Generate complete article HTML"""
    slug = article['slug']
    
    # Build the HTML
    parts = []
    
    # 1. Meta section (frontmatter + head meta)
    parts.append(generate_meta_section(article))
    
    # 2. CSS block
    parts.append(static['css'])
    
    # 3. JSON-LD
    parts.append('\n')
    parts.append(generate_jsonld(article))
    
    # 4. Close head, open body
    parts.append('</head>\n<body>\n')
    
    # 5. Navbar
    parts.append(static['nav'])
    parts.append('\n<main>\n')
    
    # 6. Hero
    parts.append(generate_hero_section(article))
    
    # 7. Search bar
    parts.append(static['search'])
    
    # 8. Article layout + TOC start
    parts.append(static['layout_start'])
    
    # 9. Breadcrumb
    parts.append(generate_breadcrumb(article))
    
    # 10. Article body
    parts.append('\n<!-- ===== 正文 ===== -->\n<article class="article-body">\n')
    parts.append(article['body'])
    parts.append('\n')
    
    # 11. Related reading
    parts.append(generate_related_cards(article))
    
    # 12. Related CTA
    parts.append('''  <div class="related-cta">
    <p><em>如需了解更多专业财税服务，欢迎联系存勤法税。</em></p>
    <p>&#x1f4de; <strong>咨询热线</strong>：13556116691（微信同号）</p>
  </div>

</article>

''')
    
    # 13. Article notice
    parts.append(generate_article_notice())
    
    # 14. Close article layout
    parts.append('\n  </div><!-- .article-main -->\n</div><!-- .article-layout -->\n')
    
    # 15. More articles section
    parts.append(static['more'])
    
    # 16. CTA + Footer + JS
    footer = static['footer']
    # Replace view counter JS in footer
    # Find the old view counter and replace
    old_vc_pattern = re.compile(
        r'<script>\s*/\* ===== 动态阅读量计数 ===== \*/\s*\(function\(\).*?\}\)\)\(\);\s*</script>',
        re.DOTALL
    )
    footer = old_vc_pattern.sub(generate_view_counter_js(article), footer)
    parts.append(footer)
    
    result = '\n'.join(parts)
    return result


def main():
    print('Loading template...')
    static = load_static_sections()
    
    print('Loading articles JSON...')
    articles = load_all_articles()
    print(f'Found {len(articles)} articles to generate\n')
    
    for i, article in enumerate(articles):
        slug = article['slug']
        source_filename = article.get('source_filename', f'{slug}(source).html')
        filepath = os.path.join(ARTICLES_DIR, source_filename)
        
        print(f'  [{i+1}/{len(articles)}] Generating: {source_filename}')
        
        try:
            html = generate_article(article, static)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html)
            
            # Verify
            size = len(html)
            has_jump = 'jumpToMatch' in html
            has_view = f"view-{slug}" in html
            has_article_schema = '"@type": "Article"' in html
            has_faq = '"@type": "FAQPage"' in html
            has_og = 'og:title' in html
            
            status = '✅' if all([has_jump, has_view, has_article_schema, has_faq, has_og]) else '⚠️'
            print(f'    {status} {size} chars | jump={has_jump} view={has_view} schema={has_article_schema} faq={has_faq} og={has_og}')
        except Exception as e:
            print(f'    ❌ ERROR: {e}')
            import traceback
            traceback.print_exc()
    
    print(f'\nDone! Generated {len(articles)} article files.')


if __name__ == '__main__':
    main()
