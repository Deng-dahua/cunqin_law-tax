#!/usr/bin/env python3
"""Generate all 20 tax articles from template"""
import os, re, json

TPL = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'source', 'articles', '金税四期全面解读(source).html')
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'source', 'articles')

def read_tpl():
    with open(TPL, 'r', encoding='utf-8') as f:
        return f.read()

def subst(tpl, slug, title, cat, date, views, body, faqs):
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
    h = re.sub(r'id="view-jinshui-siqi-yingdui"', 'id="view-%s"' % slug, h)
    h = re.sub(r"'view-jinshui-siqi-yingdui'", "'view-%s'" % slug, h)
    # 10. Article body
    ms = h.find('<!-- ===== 正文 ===== -->')
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
        q = f['q'].replace('"', '&quot;').replace('\', '\\')
        a = f['a'].replace('"', '&quot;').replace('\', '\\')
        faq_items.append('    {\n      "@type": "Question",\n      "name": "%s",\n      "acceptedAnswer": {\n        "@type": "Answer",\n        "text": "%s"\n      }\n    }' % (q, a))
    faq_json = ',\n'.join(faq_items)
    faq_schema = '  {\n    "@context": "https://schema.org",\n    "@type": "FAQPage",\n    "mainEntity": [\n%s\n    ]\n  }' % faq_json
    h = re.sub(
        r'\{\s*"@context":\s*"https://schema\.org",\s*"@type":\s*"FAQPage".*?"mainEntity".*?\}\s*\]',
        faq_schema + '\n  ]',
        h, flags=re.DOTALL
    )
    # 13. Article schema
    article_schema = '  {\n    "@context": "https://schema.org",\n    "@type": "Article",\n    "headline": "%s",\n    "description": "%s",\n    "image": "https://cunqin.tax/images/founder-new.webp",\n    "datePublished": "%s",\n    "dateModified": "2026-05-25",\n    "author": {\n      "@type": "Person",\n      "name": "邓达华",\n      "url": "https://cunqin.tax/about/"\n    },\n    "publisher": {\n      "@type": "Organization",\n      "name": "存勤法税服务（广州）有限公司",\n      "logo": {\n        "@type": "ImageObject",\n        "url": "https://cunqin.tax/images/nav-logo.webp"\n      }\n    },\n    "mainEntityOfPage": {\n      "@type": "WebPage",\n      "@id": "https://cunqin.tax/articles/%s.html"\n    }\n  }' % (title, desc, date, slug)
    h = re.sub(
        r'\{\s*"@context":\s*"https://schema\.org",\s*"@type":\s*"Article".*?"mainEntityOfPage".*?\}\}',
        article_schema,
        h, flags=re.DOTALL
    )
    # 14. BreadcrumbList schema
    bc_schema = '  {\n    "@context": "https://schema.org",\n    "@type": "BreadcrumbList",\n    "itemListElement": [\n      {\n        "@type": "ListItem",\n        "position": 1,\n        "name": "首页",\n        "item": "https://cunqin.tax"\n      },\n      {\n        "@type": "ListItem",\n        "position": 2,\n        "name": "法税洞察",\n        "item": "https://cunqin.tax/archives/"\n      },\n      {\n        "@type": "ListItem",\n        "position": 3,\n        "name": "%s"\n      }\n    ]\n  }' % title
    h = re.sub(
        r'\{\s*"@context":\s*"https://schema\.org",\s*"@type":\s*"BreadcrumbList".*?\}\}',
        bc_schema,
        h, flags=re.DOTALL
    )
    return h

# ===== ARTICLE DATA =====
# Article 1: 企业所得税汇算清缴
A1 = {
"slug": "qiyesuodeshui-huisuan-qingjiao",
"title": "企业所得税汇算清缴实务指南：从填报到筹划的全流程解析",
"cat": "税务实务",
"date": "2026-05-10",
"views": 850,
"body": """<h2 id="前言">前言</h2>
<p>企业所得税汇算清缴是每个企业年度税务管理的核心工作，也是税务风险的高发环节。本文从实操角度，系统梳理汇算清缴的全流程要点，帮助企业合规、高效地完成年度汇算工作。</p>
<h2 id="汇算清缴基本流程">汇算清缴基本流程</h2>
<h3 id="时间节点与申报期限">时间节点与申报期限</h3>
<p>企业所得税汇算清缴的法定申报期限为年度终了后<strong>5个月内</strong>（即5月31日前）。企业应统筹安排以下关键节点：</p>
<ul>
<li><strong>1月1日─3月31日</strong>：完成年度账务处理，获取各类税前扣除凭证</li>
<li><strong>4月1日─5月20日</strong>：完成纳税申报表填报、内部审核</li>
<li><strong>5月21日─5月31日</strong>：完成申报提交、税款缴纳</li>
</ul>
<p><strong>重要提示</strong>：延期申报需经税务机关批准，且需在延期期间预缴税款，否则将面临滞纳金和罚款风险。</p>""",
"faqs": [
    {"q": "企业所得税汇算清缴的申报期限是什么？", "a": "企业所得税汇算清缴的法定申报期限为年度终了后5个月内，即每年5月31日前。"},
    {"q": "业务招待费的税前扣除限额如何计算？", "a": "业务招待费税前扣除限额为发生额的60%，且不超过当年销售（营业）收入的5‰。"},
    {"q": "汇算清缴时发现扣除凭证不合规怎么办？", "a": "应在汇算清缴期结束前（5月31日）积极补开发票或其他合规凭证。"},
    {"q": "高新技术企业优惠和研发费用加计扣除可以同时享受吗？", "a": "可以。高新技术企业15%优惠税率和研发费用加计扣除是两项独立的税收优惠政策。"},
    {"q": "汇算清缴后发现申报错误怎么办？", "a": "汇算清缴后发现申报错误的，可通过更正申报方式处理。"}
]
}

# Generate article 1
tpl = read_tpl()
print("Template loaded: %d bytes" % len(tpl))
print("Generating article 1: %s" % A1['title'])

result = subst(tpl, A1['slug'], A1['title'], A1['cat'], A1['date'], A1['views'], A1['body'], A1['faqs'])
if result:
    fn = os.path.join(OUT, '%s(source).html' % A1['title'])
    with open(fn, 'w', encoding='utf-8') as f:
        f.write(result)
    print("  OK: %s" % os.path.basename(fn))
else:
    print("  FAILED")

print("Done (article 1 only - append remaining 19 articles to ARTICLE_DATA section)")
