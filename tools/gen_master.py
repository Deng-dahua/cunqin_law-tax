#!/usr/bin/env python3
"""gen_master.py - 生成全部20篇法税文章（含完整正文）"""
import os, re, sys

BASE = os.path.dirname(os.path.abspath(__file__))
TPL_PATH = os.path.join(BASE, '..', 'source', 'articles', '金税四期全面解读(source).html')
OUT_DIR  = os.path.join(BASE, '..', 'source', 'articles')

# ===== 共用正文模板（每篇文章不同部分）=====
# 为了控制文件大小，正文内容直接内嵌在 ARTICLES 列表中

def read_tpl():
    with open(TPL_PATH, 'r', encoding='utf-8') as f:
        return f.read()

def replace_all(tpl, slug, title, cat, date, views, body, faqs):
    h = tpl
    # 1. frontmatter
    h = h.replace('permalink: /articles/jinshui-siqi-yingdui.html',
                 'permalink: /articles/%s.html' % slug)
    # 2. title
    h = re.sub(r'<title>.*?</title>',
                 '<title>%s - 存勤法税服务（广州）有限公司</title>' % title,
                 h)
    # 3. meta description
    desc = title[:100]
    h = re.sub(r'<meta name="description".*?content=".*?"',
                 '<meta name="description" content="%s"' % desc,
                 h, flags=re.DOTALL)
    # 4. OG
    h = re.sub(r'property="og:title".*?content=".*?"',
                 'property="og:title" content="%s"' % title, h, flags=re.DOTALL)
    h = re.sub(r'property="og:description".*?content=".*?"',
                 'property="og:description" content="%s"' % desc[:120], h, flags=re.DOTALL)
    h = re.sub(r'property="og:url".*?content=".*?"',
                 'property="og:url" content="https://cunqin.tax/articles/%s.html"' % slug, h, flags=re.DOTALL)
    # 5. Twitter
    h = re.sub(r'name="twitter:title".*?content=".*?"',
                 'name="twitter:title" content="%s"' % title, h, flags=re.DOTALL)
    h = re.sub(r'name="twitter:description".*?content=".*?"',
                 'name="twitter:description" content="%s"' % desc[:120], h, flags=re.DOTALL)
    # 6. canonical
    h = re.sub(r'<link rel="canonical".*?href=".*?"',
                 '<link rel="canonical" href="https://cunqin.tax/articles/%s.html">' % slug, h, flags=re.DOTALL)
    h = re.sub(r'<link rel="alternate".*?href=".*?"',
                 '<link rel="alternate" hreflang="zh-CN" href="https://cunqin.tax/articles/%s.html">' % slug, h, flags=re.DOTALL)
    # 7. date meta
    h = re.sub(r'property="article:published_time".*?content=".*?"',
                 'property="article:published_time" content="%s"' % date, h, flags=re.DOTALL)
    h = re.sub(r'property="article:modified_time".*?content=".*?"',
                 'property="article:modified_time" content="2026-05-25"', h, flags=re.DOTALL)
    # 8. Hero
    h = re.sub(r'<span class="cat-tag">.*?</span>',
                 '<span class="cat-tag">%s</span>' % cat, h)
    h = re.sub(r'<h1>.*?</h1>', '<h1>%s</h1>' % title, h)
    h = re.sub(r'<time datetime=".*?".*?</time>',
                 '<time datetime="%s">%s</time>' % (date, date), h, flags=re.DOTALL)
    # 9. view counter slug
    h = re.sub(r"'view-jinshui-siqi-yingdui'",
                 "'view-%s'" % slug, h)
    h = re.sub(r'id="view-jinshui-siqi-yingdui"',
                 'id="view-%s"' % slug, h)
    h = re.sub(r"var slug = 'jinshui-siqi-yingdui'",
                 "var slug = '%s'" % slug, h)
    # 10. Schema: Article
    article_schema = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "description": desc,
        "image": "https://cunqin.tax/images/founder-new.webp",
        "datePublished": date,
        "dateModified": "2026-05-25",
        "author": {
            "@type": "Person",
            "name": "邓达华",
            "url": "https://cunqin.tax/about/"
        },
        "publisher": {
            "@type": "Organization",
            "name": "存勤法税服务（广州）有限公司",
            "logo": {
                "@type": "ImageObject",
                "url": "https://cunqin.tax/images/nav-logo.webp"
            }
        },
        "mainEntityOfPage": {
            "@type": "WebPage",
            "@id": "https://cunqin.tax/articles/%s.html" % slug
        }
    }
    # Remove old Article schema and insert new one
    h = re.sub(
        r'\{\s*"@context":\s*"https://schema\.org",\s*"@type":\s*"Article".*?"mainEntityOfPage".*?\}[^]]*\][^]]*\]',
        json.dumps([article_schema, {}], ensure_ascii=False, indent=2)[1:-1].replace('\n', '\n  '),
        h, count=1, flags=re.DOTALL
    )
    # 11. Schema: BreadcrumbList
    bc = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "首页", "item": "https://cunqin.tax"},
            {"@type": "ListItem", "position": 2, "name": "法税洞察", "item": "https://cunqin.tax/archives/"},
            {"@type": "ListItem", "position": 3, "name": title}
        ]
    }
    h = re.sub(
        r'\{\s*"@context":\s*"https://schema\.org",\s*"@type":\s*"BreadcrumbList".*?\}[^]]*\][^]]*\]',
        json.dumps([bc, {}], ensure_ascii=False, indent=2)[1:-1].replace('\n', '\n  '),
        h, count=1, flags=re.DOTALL
    )
    # 12. Schema: FAQPage
    faq_items = []
    for f in faqs:
        faq_items.append({
            "@type": "Question",
            "name": f['q'],
            "acceptedAnswer": {
                "@type": "Answer",
                "text": f['a']
            }
        })
    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": faq_items
    }
    h = re.sub(
        r'\{\s*"@context":\s*"https://schema\.org",\s*"@type":\s*"FAQPage".*?\}[^]]*\][^]]*\]',
        json.dumps([faq_schema, {}], ensure_ascii=False, indent=2)[1:-1].replace('\n', '\n  '),
        h, count=1, flags=re.DOTALL
    )
    # 13. Replace article body
    body_marker = '<!-- ===== 正文 ===== -->'
    idx = h.find(body_marker)
    if idx == -1:
        print("  ERROR: body marker not found for %s" % slug)
        return None
    art_start = h.find('<article class="article-body">', idx)
    art_end = h.find('</article>', art_start)
    if art_start == -1 or art_end == -1:
        print("  ERROR: article tags not found for %s" % slug)
        return None
    new_art = '<article class="article-body">\n' + body + '\n</article>'
    h = h[:art_start] + new_art + h[art_end + len('</article>'):]
    # 14. Breadcrumb text in body
    h = h.replace('金税四期全面解读：企业如何从容应对"以数治税"新时代', title)
    return h

# ===== 20篇文章数据 =====
# （因篇幅限制，ARTICLES列表在文件中继续追加）
# 此处先定义前2篇，后续通过追加方式添加剩余18篇

print("gen_master.py: base script written OK")
print("Need to append ARTICLES data next.")
