#!/usr/bin/env python3
"""批量生成 GEO 文章：从数据文件 + 参考模板组装完整 HTML"""
import json, re, os, datetime

TEMPLATE_PATH = "source/articles/企业税务风险管控(source).html"
OUT_DIR = "source/articles"

def load_template():
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        return f.read()

def generate_article(template, data):
    """data 包含: slug, title, description, title_tag, keywords, category,
       date_published, word_count, views_base, hero_subtitle,
       body_html, faq_json, related_cards, cta_em,
       og_description, twitter_description, article_section"""
    
    slug = data["slug"]
    title = data["title"]
    today = "2026-05-27"
    
    # ── frontmatter ──
    result = template.replace(
        "qiye-shuiwu-fengxian.html",
        slug + ".html"
    )
    
    # ── keywords (replace between meta name="keywords" content="..." >) ──
    result = re.sub(
        r'(<meta name="keywords" content=")[^"]*(">)',
        r'\1' + data["keywords"] + r'\2',
        result
    )
    
    # ── canonical ──
    result = re.sub(
        r'<link rel="canonical" href="https://cunqin\.tax/articles/[^"]*\.html">',
        f'<link rel="canonical" href="https://cunqin.tax/articles/{slug}.html">',
        result
    )
    
    # ── og:title ──
    result = re.sub(
        r'<meta property="og:title" content="[^"]*">',
        f'<meta property="og:title" content="{data["og_title"]}">',
        result
    )
    
    # ── og:description ──
    result = re.sub(
        r'<meta property="og:description" content="[^"]*">',
        f'<meta property="og:description" content="{data["og_description"]}">',
        result
    )
    
    # ── og:url ──
    result = re.sub(
        r'<meta property="og:url" content="https://cunqin\.tax/articles/[^"]*\.html">',
        f'<meta property="og:url" content="https://cunqin.tax/articles/{slug}.html">',
        result
    )
    
    # ── twitter:title ──
    result = re.sub(
        r'<meta name="twitter:title" content="[^"]*">',
        f'<meta name="twitter:title" content="{data["og_title"]}">',
        result
    )
    
    # ── twitter:description ──
    result = re.sub(
        r'<meta name="twitter:description" content="[^"]*">',
        f'<meta name="twitter:description" content="{data["twitter_description"]}">',
        result
    )
    
    # ── article:published_time / modified_time ──
    result = re.sub(
        r'<meta property="article:published_time" content="[^"]*">',
        f'<meta property="article:published_time" content="{data["date_published"]}">',
        result
    )
    result = re.sub(
        r'<meta property="article:modified_time" content="[^"]*">',
        f'<meta property="article:modified_time" content="{today}">',
        result
    )
    
    # ── <title> tag ──
    result = re.sub(
        r'<title>[^<]*</title>',
        f'<title>{data["title_tag"]}</title>',
        result
    )
    
    # ── meta description ──
    result = re.sub(
        r'<meta name="description" content="[^"]*">',
        f'<meta name="description" content="{data["og_description"]}">',
        result
    )
    
    # ── Schema: Article ──
    result = result.replace(
        '"headline": "企业税务风险管控：如何建立\\"看得见、防得住\\"的税务风险体系"',
        f'"headline": "{data["schema_headline"]}"'
    )
    result = result.replace(
        '"description": "系统讲解企业税务风险管理体系的建立方法，包括风险识别、评估、控制和预警，帮助企业实现税务风险可视化、可管控"',
        f'"description": "{data["og_description"]}"'
    )
    result = re.sub(r'"wordCount": \d+', f'"wordCount": {data["word_count"]}', result)
    result = result.replace(
        '"articleSection": "财税咨询"',
        f'"articleSection": "{data["article_section"]}"'
    )
    
    # ── Schema: BreadcrumbList ──
    old_breadcrumb_name = '企业税务风险管控：如何建立\\"看得见、防得住\\"的税务风险体系"'
    new_breadcrumb_name = data["schema_headline"] + '"'
    result = result.replace(old_breadcrumb_name, new_breadcrumb_name)
    
    # ── Schema: FAQPage ──
    result = _replace_faq(result, data["faq_items"])
    
    # ── Hero section ──
    # Category tag
    result = result.replace("行业洞察</span>", f'{data["category"]}</span>')
    # Title
    result = result.replace(
        '<h1>企业税务风险管控：如何建立"看得见、防得住"的税务风险体系</h1>',
        f'<h1>{data["hero_title"]}</h1>'
    )
    # Date
    result = result.replace(
        '<time datetime="2026-01-15">2026-01-15</time>',
        f'<time datetime="{data["date_published"]}">{data["date_published"]}</time>'
    )
    # View counter slug
    result = result.replace('data-slug="qiye-shuiwu-fengxian"', f'data-slug="{slug}"')
    result = result.replace('id="view-qiye-shuiwu-fengxian"', f'id="view-{slug}"')
    result = result.replace('>524<', f'>{data["views_base"]}<')
    
    # ── Search bar back button ──
    # Already correct (../archives/)
    
    # ── Breadcrumb HTML ──
    result = result.replace(
        '<span style="color:var(--dt-text);">企业税务风险管控：如何建立"看得见、防得住"的税务风险体系</span>',
        f'<span style="color:var(--dt-text);">{title}</span>'
    )
    
    # ── Article body ──
    result = _replace_body(result, data["body_html"])
    
    # ── Related reading cards ──
    result = _replace_related_cards(result, data["related_cards"])
    
    # ── Related CTA ──
    result = re.sub(
        r'(<p><em>如需了解更多).*?(方案，欢迎联系存勤法税。</em></p>)',
        f'<p><em>如需了解更多{data["cta_em"]}方案，欢迎联系存勤法税。</em></p>',
        result
    )
    
    # ── Views JS ──
    result = result.replace("var slug = 'qiye-shuiwu-fengxian'", f"var slug = '{slug}'")
    result = result.replace("var base = 524", f"var base = {data['views_base']}")
    
    # ── Fix hreflang canonical ──
    result = re.sub(
        r'<link rel="alternate" hreflang="zh-CN" href="https://cunqin\.tax/articles/[^"]*\.html">',
        f'<link rel="alternate" hreflang="zh-CN" href="https://cunqin.tax/articles/{slug}.html">',
        result
    )
    
    return result

def _replace_faq(result, faq_items):
    """替换 FAQPage Schema 中的问答"""
    # Find the FAQPage block and replace it
    faq_start = result.find('"@type": "FAQPage"')
    if faq_start == -1:
        return result
    
    # Build new FAQ JSON
    faq_entities = []
    for q, a in faq_items:
        faq_entities.append(f'''      {{
        "@type": "Question",
        "name": "{q}",
        "acceptedAnswer": {{
          "@type": "Answer",
          "text": "{a}"
        }}
      }}''')
    
    new_faq = ',\n'.join(faq_entities)
    
    # Find the mainEntity array and replace
    pattern = r'("mainEntity":\s*\[)[\s\S]*?(\s*\])'
    replacement = r'\1\n' + new_faq + r'\2'
    result = re.sub(pattern, replacement, result)
    
    return result

def _replace_body(result, body_html):
    """替换文章正文 (从 <article class="article-body"> 到 </article> 之间的内容)"""
    # Find the article start and end markers
    article_start = result.find('<article class="article-body">')
    article_close = result.find('</article>')
    if article_start == -1 or article_close == -1:
        return result
    
    # Keep the article tag, replace everything between
    prefix = result[:article_start + len('<article class="article-body">')]
    suffix = result[article_close:]
    
    return prefix + '\n' + body_html + '\n' + suffix

def _replace_related_cards(result, cards):
    """替换延伸阅读卡片"""
    # Find the related-grid div and replace its content
    grid_pattern = r'(<div class="related-grid">)[\s\S]*?(</div>\s*</div>\s*<div class="related-cta">)'
    
    cards_html = ""
    for card in cards:
        cards_html += f'''
      <a href="{card['url']}" class="related-card">
        <span class="related-cat">{card['cat']}</span>
        <div class="related-info">
          <h4>{card['title']}</h4>
          <p>{card['desc']}</p>
        </div>
        <span class="related-arrow"><i class="fas fa-arrow-right"></i></span>
      </a>'''
    
    replacement = r'\1' + cards_html + '\n    </div>\n  </div>\n  <div class="related-cta">'
    result = re.sub(grid_pattern, replacement, result)
    
    return result

# ═══════════════════════════════════════════════════════
# Article data
# ═══════════════════════════════════════════════════════

ARTICLES = []

def add_article(**kw):
    ARTICLES.append(kw)

# ── Batch 1: Articles #4-7 ──

add_article(
    slug="xiaofeishui-shuiwu-guihua",
    title="消费税税务规划：从征税范围到纳税筹划的全流程指南",
    hero_title="消费税税务规划：从征税范围到纳税筹划的全流程指南",
    schema_headline='消费税税务规划：从征税范围到纳税筹划的全流程指南',
    title_tag="消费税税务规划全攻略：征税范围、纳税筹划与合规管理 - 存勤法税服务（广州）有限公司",
    og_title="消费税税务规划全攻略：征税范围、纳税筹划与合规管理 - 存勤法税服务（广州）有限公司",
    og_description="全面解读消费税征税范围、税率结构及纳税筹划策略，涵盖烟酒、化妆品、汽车、成品油、高档手表等15类应税消费品。结合广州及大湾区企业实际案例，系统讲解如何在合法合规前提下优化消费税负，降低企业税务成本，规避消费税稽查风险。",
    twitter_description="全面解读消费税征税范围与纳税筹划策略，帮助企业合法合规优化税负",
    keywords="存勤法税,业管财税法,财税顾问,税务筹划,邓达华,消费税,消费税纳税筹划,应税消费品,消费税税率,消费税稽查,消费税申报",
    category="行业洞察",
    article_section="税务规划",
    date_published="2026-05-27",
    word_count=3200,
    views_base=380,
    cta_em="消费税合规与筹划",
    faq_items=[
        ("什么是消费税？哪些商品需要缴纳消费税？",
         "消费税是对特定消费品在生产和进口环节征收的间接税。目前中国消费税涵盖烟、酒、化妆品、贵重首饰及珠宝玉石、鞭炮焰火、成品油、汽车轮胎、摩托车、小汽车、高尔夫球及球具、高档手表、游艇、木制一次性筷子、实木地板、电池、涂料等15类商品。不同品类税率差异较大，从3%到56%不等。"),
        ("消费税的纳税环节是什么？",
         "消费税主要在生产和进口环节征收，部分品类（如金银首饰）在零售环节征收，卷烟在批发环节加征一道。近年来政策趋势是推进消费税征收环节后移并下划地方，企业需要关注这一变化对未来税务安排的影响。"),
        ("企业如何合法进行消费税筹划？",
         "合法筹划路径包括：①合理选择产品分类，利用税率差异；②优化委托加工与自行加工的税负比较；③充分利用外购已税消费品抵扣政策；④关注消费税改革动向，提前布局征收环节变化。所有筹划必须在税法框架内进行，不得采取虚报品名、低报价格等违法手段。"),
        ("消费税申报有哪些常见风险点？",
         "常见风险包括：①兼营不同税率消费品未分别核算，从高适用税率；②委托加工消费品代收代缴不完整；③外购已税消费品抵扣计算错误；④出口退税申报不实。建议企业建立消费税专项台账，定期进行自查自纠。"),
        ("广州企业需要特别关注哪些消费税问题？",
         "广州作为华南商贸中心，酒类、化妆品、汽车等应税消费品的批发零售企业较多。需特别关注：批发环节的涉税风险、进口环节消费税的合规申报、以及消费税改革对大湾区企业的影响。建议借助专业法税顾问进行定期税务健康检查。"),
    ],
    related_cards=[
        {"url": "zengzhishuifa-shishi-yingdui.html", "cat": "政策解读", "title": "增值税法实施后企业税务管理的调整重点", "desc": "增值税法实施后税率、抵扣、优惠的主要变化及企业需要提前准备的应对措施"},
        {"url": "guquan-jiagou-shuiwu-chouhua.html", "cat": "行业洞察", "title": "股权架构设计与税务筹划策略", "desc": "不同持股架构下的税务成本比较、组织形式的税务考量及架构优化的实操要点"},
        {"url": "qiye-shuiwu-jiankang-tijian.html", "cat": "财税咨询", "title": "企业税务健康体检30项：自我诊断指南", "desc": "企业税务健康体检的完整框架及30项重点检查指标"},
    ],
    body_html='''
<h2 id="前言">前言</h2>
<p>消费税作为中国税制中的重要税种之一，虽然在整体税收收入中占比不如增值税和企业所得税，但对于特定行业的企业而言，消费税负担可能占到产品成本的10%甚至50%以上。随着消费税改革的持续推进——征收环节后移、收入归属调整、征收范围扩大——企业面临的消费税合规要求将越来越高。</p>
<p>本文从消费税的基本制度出发，系统讲解消费税的征税范围、税率结构、纳税筹划策略以及合规管理要点，帮助广州及粤港澳大湾区企业全面把握消费税管理的核心要领。</p>
<!-- more -->

<h2 id="消费税基本制度">消费税基本制度</h2>
<h3 id="消费税的征税范围">消费税的征税范围</h3>
<p>根据《中华人民共和国消费税法》，消费税目前对以下15类应税消费品征收：</p>
<table>
<thead><tr><th>类别</th><th>具体品目</th><th>典型税率</th></tr></thead>
<tbody>
<tr><td>烟</td><td>卷烟、雪茄烟、烟丝</td><td>36%-56%+从量</td></tr>
<tr><td>酒</td><td>白酒、黄酒、啤酒、其他酒</td><td>10%-20%+从量</td></tr>
<tr><td>化妆品</td><td>高档化妆品</td><td>15%</td></tr>
<tr><td>贵重首饰</td><td>金银首饰、铂金首饰、钻石</td><td>5%-10%</td></tr>
<tr><td>鞭炮焰火</td><td>鞭炮、焰火</td><td>15%</td></tr>
<tr><td>成品油</td><td>汽油、柴油、航空煤油等</td><td>1.2-1.52元/升</td></tr>
<tr><td>汽车轮胎</td><td>汽车轮胎</td><td>3%</td></tr>
<tr><td>摩托车</td><td>排量250ml以上</td><td>3%-10%</td></tr>
<tr><td>小汽车</td><td>乘用车、中轻型商用车</td><td>1%-40%</td></tr>
<tr><td>高尔夫球及球具</td><td>高尔夫球、球杆等</td><td>10%</td></tr>
<tr><td>高档手表</td><td>单价1万元以上手表</td><td>20%</td></tr>
<tr><td>游艇</td><td>机动游艇</td><td>10%</td></tr>
<tr><td>一次性筷子</td><td>木制一次性筷子</td><td>5%</td></tr>
<tr><td>实木地板</td><td>实木地板</td><td>5%</td></tr>
<tr><td>电池、涂料</td><td>电池、涂料</td><td>4%</td></tr>
</tbody></table>
<p>在广州及粤港澳大湾区，烟、酒、化妆品、汽车、贵重首饰等行业企业众多，消费税管理是这些企业税务工作的核心之一。</p>
<h3 id="消费税的纳税环节">消费税的纳税环节</h3>
<p>消费税的纳税环节设计是其区别于其他税种的重要特征：</p>
<ul>
<li><strong>生产环节</strong>：绝大多数应税消费品在出厂销售时缴纳消费税</li>
<li><strong>进口环节</strong>：进口应税消费品在报关进口时缴纳</li>
<li><strong>委托加工环节</strong>：委托加工的应税消费品，由受托方在交货时代收代缴</li>
<li><strong>零售环节</strong>：金银首饰、铂金首饰、钻石及钻石饰品在零售环节缴纳</li>
<li><strong>批发环节</strong>：卷烟在批发环节加征一道消费税</li>
</ul>

<h2 id="消费税筹划的核心策略">消费税筹划的核心策略</h2>
<h3 id="利用税率差异进行筹划">利用税率差异进行筹划</h3>
<p>不同应税消费品的税率差异巨大——比如白酒20%，而啤酒从量计征每吨220-250元。企业可以通过合理的产品分类和定价策略，在合法范围内选择最优的税负方案。</p>
<p><strong>实践要点</strong>：</p>
<ol>
<li>仔细研读《消费税税目税率表》，准确界定产品归属的税目</li>
<li>对于跨税目的产品，评估分拆核算的可行性和成本</li>
<li>关注子税目之间的税率梯度，如小汽车按排量分档（1%-40%），排量选择直接影响消费税负</li>
</ol>
<h3 id="委托加工与自行加工的选择">委托加工与自行加工的选择</h3>
<p>在消费税的计税规则下，委托加工和自行加工的税负可能不同：</p>
<ul>
<li><strong>自行加工</strong>：以最终产品的销售额计税</li>
<li><strong>委托加工</strong>：以受托方同类产品的销售价格或组成计税价格计税</li>
</ul>
<p>企业需要综合比较两种模式的税负差异，同时考虑商业逻辑的合理性。</p>
<h3 id="外购已税消费品的抵扣策略">外购已税消费品的抵扣策略</h3>
<p>以已税消费品为原料继续生产的，外购部分已缴纳的消费税可以按规定抵扣。关键操作要点：</p>
<ul>
<li>确保取得合法的完税凭证</li>
<li>准确核算可抵扣税额</li>
<li>建立完整的台账记录</li>
</ul>

<h2 id="典型行业的消费税管理">典型行业的消费税管理</h2>
<h3 id="酒类企业">酒类企业</h3>
<p>酒类行业是消费税管理的重点领域。白酒适用20%从价税率加0.5元/斤从量税，税负较重。</p>
<table>
<thead><tr><th>酒类品种</th><th>从价税率</th><th>从量税额</th></tr></thead>
<tbody>
<tr><td>白酒</td><td>20%</td><td>0.5元/500克（500ml）</td></tr>
<tr><td>黄酒</td><td>-</td><td>240元/吨</td></tr>
<tr><td>啤酒（甲类）</td><td>-</td><td>250元/吨</td></tr>
<tr><td>啤酒（乙类）</td><td>-</td><td>220元/吨</td></tr>
</tbody></table>
<p><strong>筹划要点</strong>：</p>
<ul>
<li>设立独立销售公司，合理确定出厂价格</li>
<li>关注啤酒甲乙类划分标准，合理规划产品线</li>
<li>出口酒类可申请免征消费税</li>
</ul>
<h3 id="化妆品企业">化妆品企业</h3>
<p>高档化妆品（完税价格10元/毫升或15元/片及以上）适用15%消费税税率。</p>
<p><strong>筹划要点</strong>：</p>
<ul>
<li>准确界定"高档"标准，避免误报</li>
<li>套装销售的税务处理（分别核算vs从高适用）</li>
<li>跨境电商零售进口的综合税率考量</li>
</ul>
<h3 id="汽车企业">汽车企业</h3>
<p>小汽车消费税按排量分7档，从1%到40%不等：</p>
<table>
<thead><tr><th>排量</th><th>税率</th></tr></thead>
<tbody>
<tr><td>1.0升以下</td><td>1%</td></tr>
<tr><td>1.0-1.5升</td><td>3%</td></tr>
<tr><td>1.5-2.0升</td><td>5%</td></tr>
<tr><td>2.0-2.5升</td><td>9%</td></tr>
<tr><td>2.5-3.0升</td><td>12%</td></tr>
<tr><td>3.0-4.0升</td><td>25%</td></tr>
<tr><td>4.0升以上</td><td>40%</td></tr>
</tbody></table>

<h2 id="消费税改革的趋势与应对">消费税改革的趋势与应对</h2>
<h3 id="征收环节后移">征收环节后移</h3>
<p>国家已明确提出"推进消费税征收环节后移并稳步下划地方"。对企业的潜在影响：</p>
<ul>
<li><strong>税基扩大</strong>：从出厂价变为零售价计税，税负可能显著增加</li>
<li><strong>纳税人数量增加</strong>：批发、零售企业可能成为消费税纳税人</li>
<li><strong>征管模式变化</strong>：申报和缴纳流程可能调整</li>
</ul>
<p>在政策落地前，企业应提前做好预案——评估税负变化幅度、调整定价策略、建立零售环节的核算能力。</p>
<h3 id="征收范围可能扩大">征收范围可能扩大</h3>
<p>消费税改革也可能涉及征收范围的调整，部分高耗能、高污染产品及高端服务可能被纳入征税范围。企业应持续关注政策动向。</p>

<h2 id="消费税合规管理要点">消费税合规管理要点</h2>
<h3 id="申报与缴纳">申报与缴纳</h3>
<ul>
<li>纳税期限：一般按月申报，自期满之日起15日内申报缴纳</li>
<li>申报资料：消费税纳税申报表、完税凭证、进销存明细账等</li>
<li>重点关注：兼营不同税率消费品的分别核算</li>
</ul>
<h3 id="发票管理">发票管理</h3>
<ul>
<li>已税消费品的完税证明是抵扣的关键依据</li>
<li>委托加工需取得受托方开具的代收代缴凭证</li>
<li>出口退税需提供完整单证</li>
</ul>
<h3 id="台账管理">台账管理</h3>
<p>建议企业建立以下台账：</p>
<ol>
<li>应税消费品进销存台账</li>
<li>外购已税消费品抵扣台账</li>
<li>委托加工消费税代收代缴台账</li>
<li>出口退税申报台账</li>
</ol>

<h2 id="常见问题">常见问题</h2>
<p><strong>问：兼营不同税率应税消费品未分别核算怎么办？</strong></p>
<p>答：税法规定，兼营不同税率的应税消费品未分别核算销售额、销售数量的，从高适用税率。因此，企业必须建立分开核算的制度，避免被从高征税。</p>
<p><strong>问：出口应税消费品可以退消费税吗？</strong></p>
<p>答：可以。生产企业直接出口或委托外贸企业代理出口的应税消费品，免征消费税；外贸企业出口的应税消费品，可以申请退还已缴纳的消费税。</p>
<p><strong>问：委托加工收回的消费品直接出售还需要缴纳消费税吗？</strong></p>
<p>答：委托加工收回的应税消费品，如果以不高于受托方的计税价格直接出售的，不再缴纳消费税；如果以高于受托方计税价格出售的，需要申报缴纳消费税，但准予扣除受托方已代收代缴的消费税。</p>

<h2 id="结语">结语</h2>
<p>消费税管理是一个专业性极强的领域，涉及产品分类、税率适用、环节判断、抵扣计算等复杂问题。对于广州及粤港澳大湾区的生产型企业和贸易型企业而言，<strong>建立系统化的消费税管理体系，既是合规经营的基础，也是优化税负、提升竞争力的重要手段。</strong></p>
<p>建议企业定期进行消费税专项自查，在税务顾问的指导下制定符合自身业务特点的消费税管理方案。</p>
''',
)

add_article(
    slug="qishui-zhengce-jiedu",
    title="契税政策全面解读：征税范围、税率优惠与实务操作",
    hero_title="契税政策全面解读：征税范围、税率优惠与实务操作",
    schema_headline="契税政策全面解读：征税范围、税率优惠与实务操作",
    title_tag="契税政策全面解读：征税范围、税率、优惠与实务操作指南 - 存勤法税服务（广州）有限公司",
    og_title="契税政策全面解读：征税范围、税率、优惠与实务操作指南 - 存勤法税服务（广州）有限公司",
    og_description="全面解读契税法核心制度：土地使用权出让与转让、房屋买卖赠与互换的征税规则、法定税率与优惠税率适用条件、契税计税依据确定方法、纳税义务发生时间及申报期限。结合广州及粤港澳大湾区房地产交易实务，帮助企业准确把握契税申报要点，降低税务风险。",
    twitter_description="全面解读契税法核心制度，涵盖征税范围、税率、计税依据等实务要点",
    keywords="存勤法税,业管财税法,财税顾问,税务筹划,邓达华,契税,契税法,不动产交易,房屋买卖契税,土地使用契税,契税优惠,契税申报",
    category="政策解读",
    article_section="税务规划",
    date_published="2026-05-27",
    word_count=3100,
    views_base=410,
    cta_em="契税合规与筹划",
    faq_items=[
        ("契税是什么？什么情况下需要缴纳契税？",
         "契税是在中国境内转移土地、房屋权属时，对承受单位和个人征收的一种财产税。需要缴纳契税的情形包括：土地使用权出让、土地使用权转让（包括出售、赠与、互换）、房屋买卖、房屋赠与、房屋互换，以及以作价投资入股、抵债、划转、奖励等方式转移土地、房屋权属。"),
        ("契税的税率是多少？有什么优惠政策？",
         "契税法定税率为3%-5%，具体适用税率由省级政府确定。个人购买家庭唯一住房面积90平米以下减按1%、90平米以上减按1.5%；第二套改善性住房面积90平米以下减按1%、90平米以上减按2%。企业购房不享受上述优惠。"),
        ("契税的计税依据如何确定？",
         "计税依据一般为成交价格，包括实物交换差价、土地使用权出让金、土地收益等。成交价格明显低于市场价格且无正当理由的，税务机关有权核定。以划拨方式取得土地使用权经批准转让的，补缴的土地使用权出让金也需计入计税依据。"),
        ("契税应该在什么时候申报缴纳？",
         "纳税义务发生时间为签订土地、房屋权属转移合同当日，或取得具有合同效力的凭证当日。纳税人应在纳税义务发生之日起10日内，向不动产所在地税务机关申报缴纳契税。逾期缴纳将产生滞纳金。"),
        ("广州企业如何做好契税合规管理？",
         "广州及大湾区企业涉及土地使用权取得、厂房购置、办公楼购买等业务时，应做到：①准确判断是否属于契税征税范围；②正确确定计税依据，避免低价申报风险；③关注企业间资产划转的契税优惠政策；④在合同签订环节前置税务审核，避免事后被动。"),
    ],
    related_cards=[
        {"url": "fangdichan-qiye-shuiwu-chouhua.html", "cat": "行业洞察", "title": "房地产企业全流程税务筹划", "desc": "从土地取得到销售交付，房地产企业全生命周期的关键税务规划节点"},
        {"url": "qiye-zhongzu-shuiwu.html", "cat": "财税咨询", "title": "企业重组税务处理要点", "desc": "企业合并、分立、资产划转等重组业务的税务处理规则与筹划建议"},
        {"url": "jianzi-chezi-shuiwu-chuli.html", "cat": "财税咨询", "title": "减资撤资的税务处理与风险防控", "desc": "企业减资、撤资的所得税与流转税处理规则及实务操作要点"},
    ],
    body_html='''
<h2 id="前言">前言</h2>
<p>契税是不动产交易中不可回避的税种。2021年9月《契税法》正式施行后，契税征管进入了法治化新阶段。对于企业而言，无论是取得土地使用权、购买厂房办公楼，还是通过重组方式承接不动产，都需要准确理解和适用契税政策。</p>
<p>本文系统梳理契税的核心制度、税率体系、优惠政策及实务操作要点，帮助广州及粤港澳大湾区企业在不动产交易中做好契税合规与筹划。</p>
<!-- more -->

<h2 id="契税的征税范围">契税的征税范围</h2>
<h3 id="应税行为有哪些">应税行为有哪些</h3>
<p>根据《契税法》第一条，在中国境内转移土地、房屋权属，承受的单位和个人为契税纳税人。具体应税行为包括：</p>
<table>
<thead><tr><th>序号</th><th>应税行为</th><th>说明</th></tr></thead>
<tbody>
<tr><td>1</td><td>土地使用权出让</td><td>国家将国有土地使用权出让给使用者</td></tr>
<tr><td>2</td><td>土地使用权转让</td><td>出售、赠与、互换等</td></tr>
<tr><td>3</td><td>房屋买卖</td><td>包括商品房、二手房交易</td></tr>
<tr><td>4</td><td>房屋赠与</td><td>无偿转让房产</td></tr>
<tr><td>5</td><td>房屋互换</td><td>以房换房</td></tr>
<tr><td>6</td><td>视同转移</td><td>作价入股、抵债、划转、奖励等</td></tr>
</tbody></table>
<p>在广州及粤港澳大湾区，无论是制造业企业取得工业用地，还是服务业企业购买办公楼，抑或是通过并购重组方式承接不动产，均涉及契税的申报缴纳。</p>
<h3 id="哪些情形不征税或免税">哪些情形不征税或免税</h3>
<p>《契税法》第六条明确规定了免征契税的情形：</p>
<ul>
<li>国家机关、事业单位、社会团体、军事单位承受土地、房屋权属用于办公、教学、医疗、科研、军事设施的</li>
<li>非营利性学校、医疗机构、社会福利机构承受土地、房屋权属用于相关用途的</li>
<li>承受荒山荒地荒滩土地使用权用于农林牧渔业生产的</li>
<li>夫妻因离婚分割共同财产的</li>
<li>法定继承人继承土地、房屋权属的</li>
</ul>
<p>此外，根据财税政策，企业改制重组中符合条件的土地、房屋权属转移，可以享受免征或减征契税的优惠。</p>

<h2 id="契税的税率与计税依据">契税的税率与计税依据</h2>
<h3 id="法定税率与优惠税率">法定税率与优惠税率</h3>
<p>契税法定税率为3%-5%，由各省、自治区、直辖市在此幅度内确定具体适用税率。广东省现行契税适用税率为3%。</p>
<p><strong>个人购房优惠税率</strong>：</p>
<table>
<thead><tr><th>购房类型</th><th>面积</th><th>优惠税率</th></tr></thead>
<tbody>
<tr><td>家庭唯一住房</td><td>≤90㎡</td><td>1%</td></tr>
<tr><td>家庭唯一住房</td><td>＞90㎡</td><td>1.5%</td></tr>
<tr><td>第二套改善性住房</td><td>≤90㎡</td><td>1%</td></tr>
<tr><td>第二套改善性住房</td><td>＞90㎡</td><td>2%</td></tr>
</tbody></table>
<p>注意：上述优惠仅适用于个人购买住房。企业购买住房或非住房的不动产，按法定税率（广东省3%）全额缴纳契税。</p>
<h3 id="计税依据的确定">计税依据的确定</h3>
<p>契税的计税依据为不动产的成交价格，不同交易类型的确定方式如下：</p>
<ul>
<li><strong>买卖</strong>：以成交价格为计税依据</li>
<li><strong>赠与</strong>：参照市场价格核定</li>
<li><strong>互换</strong>：以差价为计税依据</li>
<li><strong>土地使用权出让</strong>：以成交价格为计税依据（含出让金、补偿费等）</li>
<li><strong>划拨改出让</strong>：以补缴的土地出让金为计税依据</li>
</ul>
<p><strong>特别提醒</strong>：成交价格明显低于市场价格且无正当理由的，税务机关有权按照评估价格核定计税依据。通过"阴阳合同"方式低报成交价格，不仅面临补税和滞纳金，还可能被认定为偷税而受到处罚。</p>

<h2 id="企业常见契税业务场景">企业常见契税业务场景</h2>
<h3 id="取得土地使用权">取得土地使用权</h3>
<p>企业无论是以出让、转让还是划拨方式取得土地使用权，均需缴纳契税。计税依据包括土地出让金、拆迁补偿费、市政配套费等全部经济利益。</p>
<p><strong>实务要点</strong>：</p>
<ul>
<li>分期支付土地出让金的，应以合同总价作为计税依据</li>
<li>以"毛地"出让的，后续拆迁费用应并入计税依据</li>
<li>竞拍土地时，应在报价中充分考虑契税成本</li>
</ul>
<h3 id="购买办公用房或厂房">购买办公用房或厂房</h3>
<p>企业购买商品房、写字楼、厂房等不动产，应按规定申报缴纳契税。广东省适用税率3%，无面积优惠政策。</p>
<h3 id="企业重组中的契税处理">企业重组中的契税处理</h3>
<p>企业改制重组中涉及不动产转移的，符合特定条件可以享受契税优惠：</p>
<table>
<thead><tr><th>重组类型</th><th>优惠政策</th><th>适用条件</th></tr></thead>
<tbody>
<tr><td>企业改制</td><td>免征</td><td>整体改制，原投资主体存续且持股≥75%</td></tr>
<tr><td>合并</td><td>免征</td><td>原投资主体存续</td></tr>
<tr><td>分立</td><td>免征</td><td>分立为与原投资主体相同的企业</td></tr>
<tr><td>资产划转</td><td>免征</td><td>同一投资主体内部划转</td></tr>
<tr><td>债转股</td><td>免征</td><td>经国务院批准实施</td></tr>
</tbody></table>
<p>这需要企业特别关注——一次普通的集团内部资产划转就可能触发契税，但满足条件是可以免税的。提前规划至关重要。</p>

<h2 id="契税申报与缴纳实务">契税申报与缴纳实务</h2>
<h3 id="纳税义务发生时间">纳税义务发生时间</h3>
<p>契税纳税义务发生时间为纳税人签订土地、房屋权属转移合同当日，或取得其他具有合同效力的凭证当日。纳税人应在纳税义务发生之日起10日内申报缴纳。</p>
<h3 id="申报流程">申报流程</h3>
<ol>
<li><strong>准备资料</strong>：不动产权属转移合同、身份证明、完税或免税凭证等</li>
<li><strong>填报申报表</strong>：《契税纳税申报表》</li>
<li><strong>提交审核</strong>：向不动产所在地税务机关或不动产登记中心税务窗口提交</li>
<li><strong>缴纳税款</strong>：取得契税完税凭证后办理不动产登记</li>
</ol>
<h3 id="常见风险提示">常见风险提示</h3>
<ul>
<li><strong>拆分合同风险</strong>：将装修款、设备款从房屋价款中剔除以减少计税依据，可能被税务机关否定</li>
<li><strong>延迟申报风险</strong>：签订合同后长期不申报，将产生每日万分之五的滞纳金</li>
<li><strong>以房抵债风险</strong>：债权人承受抵债房产，需要缴纳契税</li>
</ul>

<h2 id="常见问题">常见问题</h2>
<p><strong>问：购买期房什么时候缴纳契税？</strong></p>
<p>答：纳税义务发生时间为签订商品房买卖合同当日。但实践中，期房通常在办理产权证前申报缴纳。建议不要拖延至交房后才申报，以避免滞纳金风险。</p>
<p><strong>问：企业购买土地后未开发，可以申请退还契税吗？</strong></p>
<p>答：不可以。契税是财产取得税，在权属转移环节一次性征收。事后土地未开发、或转让土地使用权，已缴纳的契税不予退还。</p>
<p><strong>问：通过司法拍卖取得不动产，谁负担契税？</strong></p>
<p>答：根据税法规定，契税由承受方（买方）缴纳。司法拍卖公告中如约定"交易税费均由买方承担"的，买受人需同时承担卖方应缴的增值税、土地增值税等税费，实际成本会显著增加，竞拍前务必算清账。</p>

<h2 id="结语">结语</h2>
<p>契税虽然计征方式相对简单，但在企业不动产交易和重组业务中涉及的金额往往较大，一个交易环节的疏忽可能造成数十万甚至上百万的税务损失。<strong>对于广州及粤港澳大湾区企业而言，在涉及土地使用权取得、不动产交易和企业重组时，前置契税合规审核，是控制交易成本、防范税务风险的关键步骤。</strong></p>
''',
)

add_article(
    slug="ziyuanshui-huanbao-shuiwu",
    title="资源税与环境保护税实务指南：征税规则与企业合规要点",
    hero_title="资源税与环境保护税实务指南：征税规则与企业合规要点",
    schema_headline="资源税与环境保护税实务指南：征税规则与企业合规要点",
    title_tag="资源税与环境保护税实务指南：征税规则、申报要点与企业合规管理 - 存勤法税服务（广州）有限公司",
    og_title="资源税与环境保护税实务指南：征税规则、申报要点与企业合规管理 - 存勤法税服务（广州）有限公司",
    og_description="系统讲解资源税与环境保护税两大绿色税种：资源税的征税范围（能源矿产、金属矿产、非金属矿产、水气矿产、盐）、从价与从量计征规则；环境保护税的四大应税污染物（大气、水、固体废物、噪声）及计税方法。帮助广州及大湾区企业准确把握两大绿色税种的申报与合规要求。",
    twitter_description="系统讲解资源税与环保税征税规则，帮助企业做好绿色税种合规管理",
    keywords="存勤法税,业管财税法,财税顾问,税务筹划,邓达华,资源税,环境保护税,环保税,资源税法,绿色税收,环保税申报,资源税申报",
    category="政策解读",
    article_section="税务规划",
    date_published="2026-05-27",
    word_count=3100,
    views_base=360,
    cta_em="资源税与环保税合规",
    faq_items=[
        ("什么是资源税？哪些企业需要缴纳？",
         "资源税是对在中国领域和管辖海域开采矿产品或者生产盐的单位和个人征收的税种。征税范围包括能源矿产（原油、天然气、煤等）、金属矿产（黑色金属、有色金属）、非金属矿产、水气矿产和盐五大类。开采或生产上述应税资源的企业需要缴纳资源税。"),
        ("环境保护税的征税对象是什么？",
         "环保税对向环境直接排放应纳税污染物的企业事业单位和其他生产经营者征收。应税污染物包括：大气污染物（二氧化硫、氮氧化物、烟尘等）、水污染物、固体废物（煤矸石、尾矿等）和工业噪声四大类。居民个人排放污染物不征收环保税。"),
        ("资源税的计税方法是什么？",
         "资源税采用从价计征和从量计征两种方式：从价计征以销售额乘以适用税率（如原油、天然气、煤）；从量计征以销售数量乘以适用税额（如粘土、砂石）。具体税目税率由《资源税税目税率表》确定。"),
        ("环保税如何计算？有什么减免政策？",
         "环保税应纳税额=污染当量数（或排放量）×适用税额。减免政策包括：排放应税大气或水污染物浓度值低于规定标准30%的减按75%征税，低于50%的减按50%征税。城乡污水处理厂和生活垃圾处理场达标排放的免征环保税。"),
        ("广州企业如何做好资源税和环保税合规？",
         "建议企业：①建立应税资源购进、消耗、销售台账；②配备或委托监测污染物排放量；③准确计算应纳税额并及时申报；④关注环保技术改造带来的税收减免机会；⑤利用绿色税收政策引导节能减排，将税务合规与ESG战略结合推进。"),
    ],
    related_cards=[
        {"url": "qiye-shuiwu-fengxian.html", "cat": "财税咨询", "title": "企业税务风险管控全攻略", "desc": "建立看得见、防得住的税务风险体系，覆盖风险识别、评估、控制与预警全流程"},
        {"url": "gaoxin-qiye-shuiwu.html", "cat": "行业洞察", "title": "高新技术企业税务优惠与申报要点", "desc": "高新企业认定条件、税收优惠政策及研发费用加计扣除实操指南"},
        {"url": "chengben-feiyong-shuiwu-hegui.html", "cat": "财税咨询", "title": "成本费用税前扣除的合规要点", "desc": "各类成本费用的税前扣除条件、凭证要求及常见税务风险防范"},
    ],
    body_html='''
<h2 id="前言">前言</h2>
<p>在"双碳"目标和绿色发展理念的推动下，以资源税和环境保护税为代表的绿色税制体系正在加速完善。这两大税种不仅是企业税务合规的重要组成部分，更直接关系到企业的生产成本和绿色竞争力。</p>
<p>本文系统梳理资源税和环境保护税的核心政策、计税方法、申报要点及合规策略，帮助广州及粤港澳大湾区相关行业企业准确把握两大绿色税种的实操要求。</p>
<!-- more -->

<h2 id="资源税：制度框架与计税规则">资源税：制度框架与计税规则</h2>
<h3 id="资源税的征税范围">资源税的征税范围</h3>
<p>根据《资源税法》，资源税对五大类资源征税：</p>
<table>
<thead><tr><th>税目</th><th>具体列举</th><th>计征方式</th></tr></thead>
<tbody>
<tr><td>能源矿产</td><td>原油、天然气、煤、煤层气、石煤、油页岩等</td><td>从价为主</td></tr>
<tr><td>金属矿产</td><td>黑色金属（铁、锰等）、有色金属（铜、铝、金、银等）</td><td>从价为主</td></tr>
<tr><td>非金属矿产</td><td>石灰岩、花岗岩、高岭土等</td><td>从价或从量</td></tr>
<tr><td>水气矿产</td><td>矿泉水、二氧化碳气等</td><td>从价或从量</td></tr>
<tr><td>盐</td><td>钠盐、钾盐、镁盐等</td><td>从价或从量</td></tr>
</tbody></table>
<h3 id="计税方法">计税方法</h3>
<p>资源税实行从价计征和从量计征两种方式：</p>
<p><strong>从价计征</strong>：应纳税额 = 销售额 × 适用税率</p>
<ul>
<li>原油、天然气：6%</li>
<li>煤：2%-10%（各地在规定幅度内确定）</li>
<li>大多数金属矿产：1%-8%</li>
</ul>
<p><strong>从量计征</strong>：应纳税额 = 销售数量 × 适用税额</p>
<ul>
<li>粘土、砂石：从量计征为主</li>
<li>部分非金属矿产可选择从价或从量</li>
</ul>
<h3 id="税收优惠">税收优惠</h3>
<ul>
<li>开采原油及油田范围内运输过程中用于加热的原油、天然气免税</li>
<li>煤炭开采企业因安全生产需要抽采的煤层气免税</li>
<li>从衰竭期矿山开采的矿产品减征30%</li>
<li>充填开采置换出来的矿产品减征50%</li>
</ul>

<h2 id="环境保护税：制度框架与计税规则">环境保护税：制度框架与计税规则</h2>
<h3 id="环保税的应税污染物">环保税的应税污染物</h3>
<p>环保税对直接向环境排放应税污染物的行为征税，涵盖四大类：</p>
<table>
<thead><tr><th>污染物类别</th><th>计税单位</th><th>举例</th></tr></thead>
<tbody>
<tr><td>大气污染物</td><td>污染当量</td><td>二氧化硫、氮氧化物、烟尘、一氧化碳</td></tr>
<tr><td>水污染物</td><td>污染当量</td><td>化学需氧量(COD)、氨氮、总磷</td></tr>
<tr><td>固体废物</td><td>排放量（吨）</td><td>煤矸石、尾矿、冶炼渣、粉煤灰</td></tr>
<tr><td>工业噪声</td><td>超标分贝数</td><td>建筑施工噪声、工业设备噪声</td></tr>
</tbody></table>
<h3 id="环保税计算">环保税计算</h3>
<p><strong>大气污染物和水污染物</strong>：</p>
<p>应纳税额 = 污染当量数 × 适用税额</p>
<p>广东省适用税额：大气污染物每污染当量1.8元，水污染物每污染当量2.8元。</p>
<p><strong>固体废物</strong>：</p>
<p>应纳税额 = 排放量（吨）× 适用税额（每吨5-30元不等，按种类划分）</p>
<p><strong>工业噪声</strong>：</p>
<p>应纳税额 = 超标分贝数对应的月税额（350-11200元/月不等）</p>
<h3 id="环保税减免政策">环保税减免政策</h3>
<p>环保税设计了激励性减免政策，鼓励企业主动减排：</p>
<ul>
<li><strong>减按75%</strong>：排放应税大气或水污染物浓度值低于国家和地方规定排放标准30%的</li>
<li><strong>减按50%</strong>：排放浓度值低于标准50%的</li>
<li><strong>免征</strong>：依法设立的城乡污水集中处理、生活垃圾集中处理场所排放相应应税污染物不超过标准的</li>
</ul>

<h2 id="两个税种的申报与管理">两个税种的申报与管理</h2>
<h3 id="资源税申报">资源税申报</h3>
<p>纳税期限：按月或按季申报。自期满之日起15日内申报缴纳。</p>
<p>申报资料：资源税纳税申报表、应税资源产品销售额或销售数量计算表等。</p>
<h3 id="环保税申报">环保税申报</h3>
<p>纳税期限：按月计算，按季申报缴纳。自季度终了之日起15日内申报缴纳。</p>
<p>申报资料：环境保护税纳税申报表、污染物排放量计算方法说明、监测报告等。</p>
<h3 id="污染物排放量的确定方法">污染物排放量的确定方法</h3>
<p>环保税征管的一个特色是，企业需要自行确定污染物排放量作为计税依据。确定方法按优先级排序：</p>
<ol>
<li><strong>自动监测</strong>：安装符合规定的自动监测设备，以其数据为准</li>
<li><strong>监测机构监测</strong>：委托有资质的监测机构</li>
<li><strong>物料衡算</strong>：根据原料、燃料消耗量等推算</li>
<li><strong>排污系数</strong>：采用国家规定的产排污系数</li>
</ol>

<h2 id="粤港澳大湾区企业的特别关注">粤港澳大湾区企业的特别关注</h2>
<h3 id="广东特色政策">广东特色政策</h3>
<p>广东省在国家规定的税率幅度内，确定本省资源税具体适用税率。广州及大湾区制造业企业、矿产开采企业需关注广东省的具体规定。例如，广东省对建筑用砂石实行从量计征，企业应按实际开采量申报。</p>
<h3 id="环保合规与ESG">环保合规与ESG</h3>
<p>在ESG（环境、社会和公司治理）理念日益受到重视的背景下，环保税合规不仅是一项法定义务，更是企业绿色形象和可持续发展能力的重要体现。主动通过技术改造降低污染物排放，既减少税收支出，又提升ESG评级。</p>

<h2 id="常见问题">常见问题</h2>
<p><strong>问：小型企业也需要缴纳环保税吗？</strong></p>
<p>答：只要向环境直接排放应税污染物，不论企业规模大小，都需要缴纳环保税。没有起征点或免征额的规定。但居民个人、农业生产（不包括规模化养殖）排放的污染物不征税。</p>
<p><strong>问：安装了环保处理设施但排放仍超标，可以少缴税吗？</strong></p>
<p>答：环保税的计税依据是实际排放量，与是否安装处理设施无关。安装了处理设施而排放浓度低于标准30%或50%的，可以享受减税；但如果排放超标，不仅要全额缴税，还可能面临环保部门的行政处罚。</p>
<p><strong>问：开采建筑用砂石需要缴纳资源税吗？</strong></p>
<p>答：需要。建筑用砂石属于非金属矿产，应缴纳资源税。广东省对建筑用砂石按从量方式计征。建议企业在开采前确认当地的具体适用税额，做好成本预算。</p>

<h2 id="结语">结语</h2>
<p>资源税和环境保护税是绿色税收体系的重要组成部分，随着生态文明建设的深入推进，这两大税种的征管力度只会加强不会减弱。<strong>对于广州及粤港澳大湾区涉及资源开采和污染物排放的企业而言，建立完善的资源税和环保税管理体系，既是税务合规的底线要求，也是向绿色低碳转型的应有之义。</strong></p>
''',
)

add_article(
    slug="qiye-fenli-shuiwu-chuli",
    title="企业分立的税务处理全攻略：所得税、增值税、契税与印花税",
    hero_title="企业分立的税务处理全攻略：所得税、增值税、契税与印花税",
    schema_headline="企业分立的税务处理全攻略：所得税、增值税、契税与印花税",
    title_tag="企业分立税务处理全攻略：所得税、增值税、契税、印花税政策详解 - 存勤法税服务（广州）有限公司",
    og_title="企业分立税务处理全攻略：所得税、增值税、契税、印花税政策详解 - 存勤法税服务（广州）有限公司",
    og_description="全面解析企业分立的税务处理规则：两种分立形式（存续分立与新设分立）、企业所得税特殊性税务处理适用条件、增值税及契税免税规则、印花税处理要点。结合实务案例和风险提示，帮助广州及粤港澳大湾区企业在重组分立中做好税务规划，实现节税与合规的平衡。",
    twitter_description="解析企业分立的税务处理规则，涵盖所得税、增值税、契税等核心税种",
    keywords="存勤法税,业管财税法,财税顾问,税务筹划,邓达华,企业分立,企业重组,特殊性税务处理,分立税务,所得税免税,契税优惠,印花税",
    category="财税咨询",
    article_section="税务规划",
    date_published="2026-05-27",
    word_count=3300,
    views_base=450,
    cta_em="企业分立税务筹划",
    faq_items=[
        ("什么是企业分立？有哪些形式？",
         "企业分立是指一家企业（被分立企业）将部分或全部资产分离转让给现存或新设的企业（分立企业），被分立企业股东换取分立企业的股权或非股权支付。形式上分为存续分立（被分立企业继续存在）和新设分立（被分立企业解散，分立为两个或以上新企业）。"),
        ("企业分立的企业所得税如何处理？",
         "企业分立可选择一般性税务处理或特殊性税务处理。选择特殊性税务处理的适用条件包括：具有合理商业目的、分立企业股东持股比例不变、12个月内不改变资产实质经营活动、股权支付比例不低于85%。特殊性处理下暂不确认所得或损失，但需在后续资产计税基础中延续计算。"),
        ("企业分立涉及哪些税种？",
         "企业分立主要涉及所得税、增值税、契税、印花税等。符合条件的整体资产转让，增值税免税；符合条件的土地房屋权属转移，契税免征；分立合同按万分之三缴纳印花税。各税种的优惠条件和适用规则各不相同，需要逐税种评估确认。"),
        ("分立后的税务合规有哪些要点？",
         "①确保分立后企业的纳税主体资格正常（税务登记、一般纳税人资格等）；②合理安排未抵扣进项税额和未弥补亏损的分摊；③准确界定资产计税基础的承继，避免后续折旧或处置时产生税务争议；④分立后如发生股权变化，需关注特殊性处理的条件是否被破坏。"),
        ("广州企业分立税务筹划需要注意什么？",
         "大湾区企业分立需特别关注：①经营性资产与不动产的合理搭配分立，平衡各税种税负；②跨市经营企业在分立中的税收管辖权协调；③分立后企业是否符合当地税收优惠政策条件；④分立交易文件的税务条款完善，避免事后因约定不清产生争议。"),
    ],
    related_cards=[
        {"url": "qiye-zhongzu-shuiwu.html", "cat": "财税咨询", "title": "企业重组税务处理要点", "desc": "企业合并、分立、资产划转等重组业务的税务处理规则与筹划思路"},
        {"url": "jianzi-chezi-shuiwu-chuli.html", "cat": "财税咨询", "title": "减资撤资的税务处理与风险防控", "desc": "企业减资、撤资的所得税与流转税处理规则及实务操作要点"},
        {"url": "guquan-jiagou-shuiwu-chouhua.html", "cat": "行业洞察", "title": "股权架构设计与税务筹划策略", "desc": "不同持股架构下的税务成本比较及组织形式的税务考量"},
    ],
    body_html='''
<h2 id="前言">前言</h2>
<p>企业分立是企业重组的重要形式之一。无论是为了聚焦主业、剥离非核心资产，还是为上市前做架构梳理、应对反垄断要求，分立都可能是最有效的组织工具。然而，企业分立涉及企业所得税、增值税、契税、印花税等多个税种，处理不当可能导致高额税负甚至引发税务争议。</p>
<p>本文系统梳理企业分立的税务处理全流程，重点解析特殊性税务处理的适用条件与操作要点，帮助广州及粤港澳大湾区企业在重组中实现税负优化与合规管理的双赢。</p>
<!-- more -->

<h2 id="企业分立的基本概念">企业分立的基本概念</h2>
<h3 id="分立的两种形式">分立的两种形式</h3>
<table>
<thead><tr><th>形式</th><th>特点</th><th>被分立企业状态</th></tr></thead>
<tbody>
<tr><td>存续分立</td><td>企业分出一部分资产设立新企业，原企业继续存在</td><td>存续</td></tr>
<tr><td>新设分立</td><td>企业全部资产分割为两个或以上新企业，原企业解散注销</td><td>注销</td></tr>
</tbody></table>
<p>在广州及粤港澳大湾区，存续分立更为常见——企业将某业务板块或子公司剥离成立独立法人，原主体继续经营核心业务。</p>
<h3 id="分立的目的与商业合理性">分立的目的与商业合理性</h3>
<p>企业分立必须具有合理的商业目的，这是享受税收优惠政策的前提条件之一。常见的合理商业目的包括：</p>
<ul>
<li>业务聚焦：剥离非核心业务，聚焦主业发展</li>
<li>风险隔离：将高风险业务与低风险业务分设</li>
<li>上市准备：优化集团架构，满足上市合规要求</li>
<li>引入战略投资者：为特定业务板块单独融资</li>
<li>避免同业竞争：满足监管要求</li>
</ul>
<p><strong>重要提示</strong>：纯粹以避税为目的的分立安排不得适用特殊性税务处理。税务机关会穿透审查商业实质。</p>

<h2 id="企业所得税处理">企业所得税处理</h2>
<h3 id="一般性税务处理">一般性税务处理</h3>
<p>如果企业选择一般性税务处理（或不符合特殊性处理条件）：</p>
<ul>
<li>被分立企业：对分立出去的资产按公允价值确认资产转让所得或损失</li>
<li>分立企业：接受资产的计税基础按公允价值确定</li>
<li>被分立企业股东：取得的分立对价视同分配处理</li>
</ul>
<p><strong>这意味着</strong>：被分立企业可能需要就资产增值缴纳大额企业所得税，对于持有大量土地、房产等增值资产的企业尤其需要关注。</p>
<h3 id="特殊性税务处理">特殊性税务处理</h3>
<p>符合以下全部条件的企业分立，可以选择特殊性税务处理——即暂不确认资产转让所得或损失：</p>
<table>
<thead><tr><th>条件</th><th>具体要求</th></tr></thead>
<tbody>
<tr><td>合理商业目的</td><td>非以避税为主要目的</td></tr>
<tr><td>股东持股比例不变</td><td>分立企业股东持股比例与原企业保持一致</td></tr>
<tr><td>经营连续性</td><td>12个月内不改变资产实质经营活动</td></tr>
<tr><td>股权支付比例</td><td>不低于交易总价的85%</td></tr>
<tr><td>股东承诺</td><td>取得股权后12个月内不转让</td></tr>
</tbody></table>
<p>特殊性处理的核心规则：</p>
<ol>
<li>分立企业接受资产的计税基础，以被分立企业的原有计税基础确定</li>
<li>被分立企业未弥补的亏损，可按分立资产占比分配给分立企业</li>
<li>被分立企业股东取得分立企业股权的计税基础，按原持股比例分摊</li>
</ol>
<h3 id="未弥补亏损的分配">未弥补亏损的分配</h3>
<p>这是分立税务筹划中容易忽视但极其重要的一环。被分立企业的未弥补亏损，可以按照分立资产占全部资产的比例分配给分立企业继续弥补。如果分配不当，可能造成税收利益损失。</p>

<h2 id="增值税与契税处理">增值税与契税处理</h2>
<h3 id="增值税处理">增值税处理</h3>
<p>企业分立中涉及的货物、不动产、无形资产转让，满足以下条件可适用增值税免税政策：</p>
<ul>
<li>通过合并、分立、出售、置换等方式，将全部或部分实物资产以及与其相关联的债权、负债和劳动力一并转让</li>
<li>涉及的不动产、土地使用权转让行为不征收增值税</li>
</ul>
<p><strong>注意</strong>：仅转让部分资产而不转让相关联的债权、负债和劳动力的，不能享受增值税免税。</p>
<h3 id="契税处理">契税处理</h3>
<p>企业分立中，分立后企业承受原企业土地、房屋权属的，满足以下条件免征契税：</p>
<ul>
<li>分立为与原投资主体相同的企业</li>
<li>投资主体存续，且在分立后的企业中持股比例保持不变</li>
</ul>
<p>在广州及大湾区的不动产交易中，契税按3%计征，一套价值1000万元的房产，契税即为30万元。能够享受免税对分立成本影响显著。</p>
<h3 id="印花税处理">印花税处理</h3>
<p>企业分立中签订的产权转移书据属于印花税应税凭证，按所载金额的万分之三缴纳印花税。企业分立后新设企业的资金账簿，按实收资本和资本公积合计金额的万分之二点五缴纳印花税。</p>

<h2 id="分立税务筹划的实操要点">分立税务筹划的实操要点</h2>
<h3 id="第一步：明确分立方案">第一步：明确分立方案</h3>
<p>在启动分立前，应与税务顾问明确以下事项：</p>
<ul>
<li>分立的形式（存续还是新设）</li>
<li>拟分立的资产范围（含不动产、无形资产、债权债务、人员安排）</li>
<li>股权支付比例设计</li>
<li>是否申请特殊性税务处理</li>
</ul>
<h3 id="第二步：逐税种评估税负">第二步：逐税种评估税负</h3>
<p>至少在以下税种维度进行评估：</p>
<ol>
<li><strong>企业所得税</strong>：确认能否满足特殊性处理条件，评估一般性处理的税负</li>
<li><strong>增值税</strong>：确认是否满足整体资产转让免税条件</li>
<li><strong>契税</strong>：涉及不动产的，提前确认免税资格</li>
<li><strong>印花税</strong>：算入整体交易成本</li>
<li><strong>土地增值税</strong>：如涉及房地产开发企业，需专项评估</li>
</ol>
<h3 id="第三步：备案与申报">第三步：备案与申报</h3>
<p>选择特殊性税务处理的，应在企业所得税年度申报时填报《企业重组所得税特殊性税务处理报告表》，并附送相关证明材料。</p>
<h3 id="第四步：分立后持续监控">第四步：分立后持续监控</h3>
<p>特殊性处理并非一劳永逸——如果分立后12个月内发生股权转让、改变资产经营用途等情况，可能导致特殊性处理条件失效，需要补缴税款。</p>

<h2 id="常见风险与防范">常见风险与防范</h2>
<ul>
<li><strong>商业目的不充分</strong>：税务机关可能否定特殊性处理，要求按一般性处理补税</li>
<li><strong>税务基础承继不清</strong>：资产计税基础未准确延续，后续折旧或处置时引发争议</li>
<li><strong>跨税种协调不足</strong>：仅关注所得税而忽略契税、增值税等其他税种</li>
<li><strong>时间条件监控缺失</strong>：12个月的经营连续性和持股比例保持期被忽略</li>
</ul>

<h2 id="常见问题">常见问题</h2>
<p><strong>问：分立后马上转让股权，会有什么后果？</strong></p>
<p>答：如果分立后12个月内，取得股权支付的原主要股东转让所取得的分立企业股权，可能被认定为不符合特殊性税务处理条件，需要补缴企业所得税。建议在分立方案中明确约定股东在12个月内的转让限制。</p>
<p><strong>问：企业分立可以只分资产不分负债吗？</strong></p>
<p>答：从公司法角度看可以，但从税务角度看，仅分资产不分负债可能不满足"整体资产转让"的条件，从而无法享受增值税和契税免税。税务筹划应与商业安排协调一致。</p>
<p><strong>问：分立后分立企业的亏损可以继续弥补吗？</strong></p>
<p>答：被分立企业未弥补的亏损，可按分立出去的资产占全部资产的比例分配给分立企业继续弥补。需注意的是，各分立后的企业都只能弥补分配获得的亏损额度，不得交叉弥补。</p>

<h2 id="结语">结语</h2>
<p>企业分立是一个系统工程，涉及法律、税务、财务、业务等多个维度。<strong>对于广州及粤港澳大湾区企业，在重组中做好分立税务规划，需要提前谋划、逐税种评估、严格把握特殊性处理条件并做好分立后持续监控。</strong>建议在启动分立前聘请专业法税顾问进行全面方案设计，确保分立过程合法合规、税负最优。</p>
''',
)

# ── 写入文件 ──
def main():
    template = load_template()
    
    for i, data in enumerate(ARTICLES):
        slug = data["slug"]
        out_path = os.path.join(OUT_DIR, f"{slug}(source).html")
        
        html = generate_article(template, data)
        
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)
        
        print(f"✅ [{i+1}/{len(ARTICLES)}] Generated: {out_path}")
    
    print(f"\nDone! {len(ARTICLES)} articles generated.")

if __name__ == "__main__":
    main()
