#!/usr/bin/env python3
"""
从 tools/geo_articles_batch*.json 生成 GEO 文章 HTML
复用 generate_articles.py 的核心函数
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from generate_articles import (
    TEMPLATE_PATH, ARTICLES_DIR, SITE_URL, AUTHOR, PUBLISHER,
    DEFAULT_DATE_MODIFIED, DEFAULT_VIEWS,
    load_template, load_static_sections, expand_description,
    generate_meta_section, generate_jsonld, generate_hero_section,
    generate_breadcrumb, generate_related_cards, generate_article_notice,
    generate_view_counter_js, escape_html_attr
)
import re

def load_articles(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_article(article, static):
    slug = article['slug']
    parts = []
    parts.append(generate_meta_section(article))
    parts.append(static['css'])
    parts.append('\n')
    parts.append(generate_jsonld(article))
    parts.append('</head>\n<body>\n')
    parts.append(static['nav'])
    parts.append('\n<main>\n')
    parts.append(generate_hero_section(article))
    parts.append(static['search'])
    parts.append(static['layout_start'])
    parts.append(generate_breadcrumb(article))
    parts.append('\n<!-- ===== 正文 ===== -->\n<article class="article-body">\n')
    parts.append(article['body'])
    parts.append('\n')
    parts.append(generate_related_cards(article))
    parts.append('  <div class="related-cta">\n    <p><em>如需了解更多专业财税服务，欢迎联系存勤法税。</em></p>\n    <p>&#x1f4de; <strong>咨询热线</strong>：13556116691（微信同号）</p>\n  </div>\n\n</article>\n\n')
    parts.append(generate_article_notice())
    parts.append('\n  </div><!-- .article-main -->\n</div><!-- .article-layout -->\n')
    parts.append(static['more'])
    footer = static['footer']
    old_vc_pattern = re.compile(
        r'<script>\s*/\* ===== 动态阅读量计数 ===== \*/\s*\(function\(\).*?\}\)\)\(\);\s*</script>',
        re.DOTALL
    )
    footer = old_vc_pattern.sub(generate_view_counter_js(article), footer)
    parts.append(footer)
    return '\n'.join(parts)

def main():
    if len(sys.argv) < 2:
        json_path = os.path.join(os.path.dirname(__file__), 'geo_articles_batch1.json')
    else:
        json_path = sys.argv[1]
    
    print(f'Loading: {json_path}')
    articles = load_articles(json_path)
    print(f'Found {len(articles)} articles')
    
    print('Loading template sections...')
    static = load_static_sections()
    
    for i, article in enumerate(articles):
        slug = article['slug']
        sf = article.get('source_filename', f'{slug}(source).html')
        fp = os.path.join(ARTICLES_DIR, sf)
        
        print(f'  [{i+1}/{len(articles)}] {sf}')
        html = generate_article(article, static)
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(html)
        
        size = len(html)
        ok = all([
            'jumpToMatch' in html,
            f'view-{slug}' in html,
            '"@type": "Article"' in html,
            '"@type": "FAQPage"' in html,
            'og:title' in html
        ])
        status = 'OK' if ok else 'WARN'
        print(f'    [{status}] {size} chars | jump={("jumpToMatch" in html)} view={("view-"+slug in html)} article={("\"@type\": \"Article\"" in html)} faq={("\"@type\": \"FAQPage\"" in html)} og={("og:title" in html)}')

    print('\nDone!')

if __name__ == '__main__':
    main()
