#!/usr/bin/env python3
"""批量生成文章：从模板替换生成新文章"""
import re, sys

# ── 文章定义 ──────────────────────────────────────────
ARTICLES = [
    {
        "filename": "税务稽查应对实战手册(source).html",
        "slug": "shuiwu-jicha-yingdui-shouce",
        "title": "税务稽查应对实战手册：从收到稽查通知书到结案的每一步",
        "category": "财税咨询",
        "date": "2026-05-27",
        "keywords": "存勤法税,业管财税法,财税顾问,税务筹划,邓达华,税务稽查应对,稽查通知书,补税协商,罚款减免,税务行政复议,广州",
        "og_desc": "收到税务稽查通知书后的全流程应对指南：从黄金24小时紧急响应、现场检查配合策略、主动补税窗口期判断，到罚款滞纳金协商技巧与行政复议路径，每一步都有章可循。覆盖2026年稽查新规与真实案例，帮助企业在被查时从容应对、最大限度降低损失。",
        "meta_desc": "收到税务稽查通知书后的全流程应对指南：从黄金24小时紧急响应、现场检查配合策略、主动补税窗口期判断，到罚款滞纳金协商技巧与行政复议路径，每一步都有章可循。",
        "twitter_desc": "收到稽查通知书后怎么办？全流程应对指南：24小时紧急响应、现场配合、补税窗口、罚款协商、复议诉讼，每一步都有章可循",
        "wordCount": 4200,
        "base_views": 320,
    },
    {
        "filename": "企业税务健康体检30项(source).html",
        "slug": "qiye-shuiwu-jiankang-tijian",
        "title": "企业税务健康体检清单：30个指标自查你的公司有没有税务问题",
        "category": "财税咨询",
        "date": "2026-05-27",
        "keywords": "存勤法税,业管财税法,财税顾问,税务筹划,邓达华,税务体检,税务自查,风险排查,税负率,发票管理,广州",
        "og_desc": "企业税务健康体检30项指标清单：从税负率、发票管理、收入成本匹配、关联交易到优惠资质维护，逐项标注红黄绿风险等级。附查出问题后的处理优先级与行动指南，帮助企业主在税务风险爆发前主动发现隐患。",
        "meta_desc": "企业税务健康体检30项指标清单：从税负率、发票管理、收入成本匹配、关联交易到优惠资质维护，逐项标注红黄绿风险等级。附查出问题后的处理优先级与行动指南。",
        "twitter_desc": "30项指标自查你的公司有没有税务问题。税负率、发票、收入成本、关联交易逐项排查，红黄绿分级，查出问题立刻知道怎么办",
        "wordCount": 4600,
        "base_views": 280,
    },
    {
        "filename": "私户收款被查补救指南(source).html",
        "slug": "sihu-shoukuan-bujiu-zhinan",
        "title": "私户收款被查怎么办？金税四期下的补救窗口期与合规路径全解析",
        "category": "财税咨询",
        "date": "2026-05-27",
        "keywords": "存勤法税,业管财税法,财税顾问,税务筹划,邓达华,私户收款,个人卡收款,金税四期,银行流水比对,合规补救,广州",
        "og_desc": "金税四期银行流水与税务申报自动比对后，私户收款成为税务稽查第一入口。本文详解补救窗口期、主动补申报操作流程、过渡期合规方案与长期转型路径，覆盖建筑、贸易、餐饮等高频行业，帮助企业主在风险爆发前完成合规转型。",
        "meta_desc": "金税四期银行流水与税务申报自动比对后，私户收款成为税务稽查第一入口。本文详解补救窗口期、主动补申报操作流程、过渡期合规方案与长期转型路径。",
        "twitter_desc": "私户收款被查怎么办？金税四期补救窗口期+合规路径全解析：主动补申报、过渡方案、长期转型，覆盖建筑贸易餐饮行业",
        "wordCount": 4300,
        "base_views": 350,
    },
]

# ── 模板文件 ──────────────────────────────────────────
TEMPLATE = "source/articles/企业税务风险管控(source).html"

def replace_article(base_content, art):
    """替换模板中的文章特定内容"""
    c = base_content

    # --- Frontmatter ---
    c = c.replace(
        "permalink: /articles/qiye-shuiwu-fengxian.html",
        f"permalink: /articles/{art['slug']}.html"
    )

    # --- Meta keywords ---
    c = re.sub(
        r'<meta name="keywords" content="[^"]*">',
        f'<meta name="keywords" content="{art["keywords"]}">',
        c, count=1
    )

    # --- Canonical ---
    c = c.replace(
        'href="https://cunqin.tax/articles/qiye-shuiwu-fengxian.html"',
        f'href="https://cunqin.tax/articles/{art["slug"]}.html"'
    )

    # --- OG title ---
    c = re.sub(
        r'<meta property="og:title" content="[^"]*">',
        f'<meta property="og:title" content="{art["title"]} - 存勤法税服务（广州）有限公司">',
        c, count=1
    )

    # --- OG description ---
    c = re.sub(
        r'<meta property="og:description" content="[^"]*">',
        f'<meta property="og:description" content="{art["og_desc"]}">',
        c, count=1
    )

    # --- OG URL ---
    c = c.replace(
        'content="https://cunqin.tax/articles/qiye-shuiwu-fengxian.html"',
        f'content="https://cunqin.tax/articles/{art["slug"]}.html"'
    )

    # --- Twitter title ---
    c = re.sub(
        r'<meta name="twitter:title" content="[^"]*">',
        f'<meta name="twitter:title" content="{art["title"]} - 存勤法税服务（广州）有限公司">',
        c, count=1
    )

    # --- Twitter description ---
    c = re.sub(
        r'<meta name="twitter:description" content="[^"]*">',
        f'<meta name="twitter:description" content="{art["twitter_desc"]}">',
        c, count=1
    )

    # --- Page title ---
    c = re.sub(
        r'<title>[^<]*</title>',
        f'<title>{art["title"]} - 存勤法税服务（广州）有限公司</title>',
        c, count=1
    )

    # --- Meta description ---
    c = re.sub(
        r'<meta name="description" content="[^"]*">',
        f'<meta name="description" content="{art["meta_desc"]}">',
        c, count=1
    )

    # --- Article published/modified time ---
    c = re.sub(
        r'<meta property="article:published_time" content="[^"]*">',
        f'<meta property="article:published_time" content="{art["date"]}">',
        c, count=1
    )
    c = re.sub(
        r'<meta property="article:modified_time" content="[^"]*">',
        f'<meta property="article:modified_time" content="{art["date"]}">',
        c, count=1
    )

    # --- Schema headline ---
    c = c.replace(
        '"headline": "企业税务风险管控：如何建立\\"看得见、防得住\\"的税务风险体系"',
        f'"headline": "{art["title"]}"'
    )

    # --- Schema description ---
    c = re.sub(
        r'"description": "系统讲解企业税务风险管理体系的建立方法[^"]*"',
        f'"description": "{art["meta_desc"]}"',
        c, count=1
    )

    # --- Schema datePublished/dateModified ---
    c = re.sub(r'"datePublished": "[^"]*"', f'"datePublished": "{art["date"]}"', c, count=1)
    c = re.sub(r'"dateModified": "[^"]*"', f'"dateModified": "{art["date"]}"', c, count=1)

    # --- Schema wordCount ---
    c = re.sub(r'"wordCount": \d+', f'"wordCount": {art["wordCount"]}', c, count=1)

    # --- Schema articleSection ---
    c = c.replace('"articleSection": "财税咨询"', f'"articleSection": "{art["category"]}"')

    # --- Schema WebPage @id ---
    c = c.replace(
        '"@id": "https://cunqin.tax/articles/qiye-shuiwu-fengxian.html"',
        f'"@id": "https://cunqin.tax/articles/{art["slug"]}.html"'
    )

    # --- Schema BreadcrumbList position 3 name ---
    c = c.replace(
        '"name": "企业税务风险管控：如何建立\\"看得见、防得住\\"的税务风险体系"',
        f'"name": "{art["title"]}"'
    )

    # --- Hero cat-tag ---
    c = c.replace(
        '<span class="cat-tag">行业洞察</span>',
        f'<span class="cat-tag">{art["category"]}</span>'
    )

    # --- Hero h1 ---
    c = re.sub(
        r'<h1>[^<]*</h1>',
        f'<h1>{art["title"]}</h1>',
        c, count=1
    )

    # --- Hero time ---
    c = re.sub(
        r'<time datetime="[^"]*">[^<]*</time>',
        f'<time datetime="{art["date"]}">{art["date"]}</time>',
        c, count=1
    )

    # --- View counter slug ---
    c = c.replace('data-slug="qiye-shuiwu-fengxian"', f'data-slug="{art["slug"]}"')
    c = c.replace('id="view-qiye-shuiwu-fengxian"', f'id="view-{art["slug"]}"')
    c = c.replace(">524<", f">{art['base_views']}<")

    # --- Breadcrumb ---
    c = c.replace(
        '<span style="color:var(--dt-text);">企业税务风险管控：如何建立"看得见、防得住"的税务风险体系</span>',
        f'<span style="color:var(--dt-text);">{art["title"]}</span>'
    )

    # --- View counter JS slug ---
    c = c.replace(
        "var slug = 'qiye-shuiwu-fengxian';",
        f"var slug = '{art['slug']}';"
    )

    return c


def main():
    with open(TEMPLATE, "r", encoding="utf-8") as f:
        base = f.read()

    for art in ARTICLES:
        output = replace_article(base, art)
        outpath = f"source/articles/{art['filename']}"
        with open(outpath, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"[OK] Generated: {outpath}")

    print("\nDone! Next steps:")
    print("1. Replace article body content in each file")
    print("2. Replace related reading cards")
    print("3. Replace related CTA")
    print("4. Replace FAQPage Q&A")
    print("5. Run GEO audit + article validation")

if __name__ == "__main__":
    main()
