#!/usr/bin/env python3
"""gen_full20.py - 生成全部20篇文章（完整版）"""
import os, re, json

TPL = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'source', 'articles', '金税四期全面解读(source).html')
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'source', 'articles')

def read_tpl():
    with open(TPL, 'r', encoding='utf-8') as f:
        return f.read()

def gen(tpl, slug, title, cat, date, views, body, faqs):
    h = tpl
    # 1. frontmatter
    h = h.replace('permalink: /articles/jinshui-siqi-yingdui.html',
                 'permalink: /articles/%s.html' % slug)
    # 2. title
    h = re.sub(r'<title>.*?</title>', '<title>%s - 存勤法税服务（广州）有限公司</title>' % title, h)
    # 3. meta description
    desc = title[:100]
    h = re.sub(r'<meta name="description".*?content=".*?"', '<meta name="description" content="%s"' % desc, h, flags=re.DOTALL)
    # 4. OG
    h = re.sub(r'property="og:title".*?content=".*?"', 'property="og:title" content="%s"' % title, h, flags=re.DOTALL)
    h = re.sub(r'property="og:description".*?content=".*?"', 'property="og:description" content="%s"' % desc[:120], h, flags=re.DOTALL)
    h = re.sub(r'property="og:url".*?content=".*?"', 'property="og:url" content="https://cunqin.tax/articles/%s.html"' % slug, h, flags=re.DOTALL)
    # 5. Twitter
    h = re.sub(r'name="twitter:title".*?content=".*?"', 'name="twitter:title" content="%s"' % title, h, flags=re.DOTALL)
    h = re.sub(r'name="twitter:description".*?content=".*?"', 'name="twitter:description" content="%s"' % desc[:120], h, flags=re.DOTALL)
    # 6. canonical
    h = re.sub(r'<link rel="canonical".*?href=".*?"', '<link rel="canonical" href="https://cunqin.tax/articles/%s.html">' % slug, h, flags=re.DOTALL)
    h = re.sub(r'<link rel="alternate".*?href=".*?"', '<link rel="alternate" hreflang="zh-CN" href="https://cunqin.tax/articles/%s.html">' % slug, h, flags=re.DOTALL)
    # 7. date
    h = re.sub(r'property="article:published_time".*?content=".*?"', 'property="article:published_time" content="%s"' % date, h, flags=re.DOTALL)
    h = re.sub(r'property="article:modified_time".*?content=".*?"', 'property="article:modified_time" content="2026-05-25"', h, flags=re.DOTALL)
    # 8. Hero
    h = re.sub(r'<span class="cat-tag">.*?</span>', '<span class="cat-tag">%s</span>' % cat, h)
    h = re.sub(r'<h1>.*?</h1>', '<h1>%s</h1>' % title, h)
    h = re.sub(r'<time datetime=".*?".*?</time>', '<time datetime="%s">%s</time>' % (date, date), h, flags=re.DOTALL)
    # 9. view counter
    h = re.sub(r"var slug = 'jinshui-siqi-yingdui'", "var slug = '%s'" % slug, h)
    h = re.sub(r"'view-jinshui-siqi-yingdui'", "'view-%s'" % slug, h)
    h = re.sub(r'id="view-jinshui-siqi-yingdui"', 'id="view-%s"' % slug, h)
    # 10. Article body
    marker = '<!-- ===== 正文 ===== -->'
    ms = h.find(marker)
    if ms == -1:
        print("  ERROR: no body marker for %s" % slug)
        return None
    astart = h.find('<article class="article-body">', ms)
    aend = h.find('</article>', astart)
    if astart == -1 or aend == -1:
        print("  ERROR: article tags not found for %s" % slug)
        return None
    new_body = '<article class="article-body">\n' + body + '\n</article>'
    h = h[:astart] + new_body + h[aend + len('</article>'):]
    # 11. Breadcrumb text
    h = h.replace('金税四期全面解读：企业如何从容应对"以数治税"新时代', title)
    # 12. FAQPage schema
    faq_items = []
    for f in faqs:
        q = f['q'].replace('"', '&quot;')
        a = f['a'].replace('"', '&quot;')
        faq_items.append('    {\n      "@type": "Question",\n      "name": "%s",\n      "acceptedAnswer": {\n        "@type": "Answer",\n        "text": "%s"\n      }\n    }' % (q, a))
    faq_json = ',\n'.join(faq_items)
    faq_block = '  {\n    "@context": "https://schema.org",\n    "@type": "FAQPage",\n    "mainEntity": [\n%s\n    ]\n  }' % faq_json
    # Replace FAQPage block
    h = re.sub(
        r'\{\s*"@context":\s*"https://schema\.org",\s*"@type":\s*"FAQPage".*?"mainEntity".*?\}[^]]*][^]]*\]',
        faq_block,
        h, flags=re.DOTALL
    )
    # 13. Article schema
    article_schema = '  {\n    "@context": "https://schema.org",\n    "@type": "Article",\n    "headline": "%s",\n    "description": "%s",\n    "image": "https://cunqin.tax/images/founder-new.webp",\n    "datePublished": "%s",\n    "dateModified": "2026-05-25",\n    "author": {\n      "@type": "Person",\n      "name": "邓达华",\n      "url": "https://cunqin.tax/about/"\n    },\n    "publisher": {\n      "@type": "Organization",\n      "name": "存勤法税服务（广州）有限公司",\n      "logo": {\n        "@type": "ImageObject",\n        "url": "https://cunqin.tax/images/nav-logo.webp"\n      }\n    },\n    "mainEntityOfPage": {\n      "@type": "WebPage",\n      "@id": "https://cunqin.tax/articles/%s.html"\n    }\n  }' % (title, desc, date, slug)
    h = re.sub(
        r'\{\s*"@context":\s*"https://schema\.org",\s*"@type":\s*"Article".*?"mainEntityOfPage".*?\}[^]]*][^]]*\}',
        article_schema,
        h, flags=re.DOTALL
    )
    # 14. BreadcrumbList schema
    bc_schema = '  {\n    "@context": "https://schema.org",\n    "@type": "BreadcrumbList",\n    "itemListElement": [\n      {\n        "@type": "ListItem",\n        "position": 1,\n        "name": "首页",\n        "item": "https://cunqin.tax"\n      },\n      {\n        "@type": "ListItem",\n        "position": 2,\n        "name": "法税洞察",\n        "item": "https://cunqin.tax/archives/"\n      },\n      {\n        "@type": "ListItem",\n        "position": 3,\n        "name": "%s"\n      }\n    ]\n  }' % title
    h = re.sub(
        r'\{\s*"@context":\s*"https://schema\.org",\s*"@type":\s*"BreadcrumbList".*?\}[^]]*\}',
        bc_schema,
        h, flags=re.DOTALL
    )
    return h

# ===== 20篇文章数据 =====
# 每篇文章：slug, title, cat, date, views, body, faqs
# 因篇幅限制，此处先定义结构，正文内容通过追加方式添加

print("gen_full20.py: base engine written OK")
print("Need to append all 20 article bodies.")
