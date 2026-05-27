#!/usr/bin/env python3
"""
generate_all_20.py - 批量生成20篇法税文章
方法：读取模板文件，替换占位符，生成每篇文章
"""
import os, re, json, sys
from datetime import datetime

TEMPLATE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'source', 'articles', '金税四期全面解读(source).html')
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'source', 'articles')

def read_template():
    with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
        return f.read()

def gen_article(template, data):
    """用文章数据替换模板中的占位符，生成完整HTML"""
    slug = data['slug']
    title = data['title']
    cat = data['cat']
    date = data['date']
    views = data['views']
    permalink = data['permalink']
    body = data['body']
    faq_list = data['faq']
    desc = data.get('desc', title)
    
    # 构建 FAQPage JSON-LD
    faq_items = []
    for i, f in enumerate(faq_list):
        faq_items.append('''    {
      "@type": "Question",
      "name": "%s",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "%s"
      }
    }''' % (f['q'], f['a'].replace('"', '&quot;')))
    faq_json = ',\n'.join(faq_items)
    
    # 构建 Schema JSON-LD 块（替换模板中的3个Schema块）
    # 保留 Organization + WebSite，替换 Article + BreadcrumbList + FAQPage
    
    article_schema = '''  {
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "%s",
    "description": "%s",
    "image": "https://cunqin.tax/images/founder-new.webp",
    "datePublished": "%s",
    "dateModified": "%s",
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
      "@id": "https://cunqin.tax/articles/%s.html"
    }
  }''' % (title, desc, date, '2026-05-24', slug)
    
    breadcrumb_schema = '''  {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {
        "@type": "ListItem",
        "position": 1,
        "name": "首页",
        "item": "https://cunqin.tax"
      },
      {
        "@type": "ListItem",
        "position": 2,
        "name": "法税洞察",
        "item": "https://cunqin.tax/archives/"
      },
      {
        "@type": "ListItem",
        "position": 3,
        "name": "%s"
      }
    ]
  }''' % title
    
    faq_schema = '''  {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
%s
    ]
  }''' % faq_json
    
    html = template
    
    # 1. 替换 frontmatter
    html = html.replace('permalink: /articles/jinshui-siqi-yingdui.html', 'permalink: %s' % permalink)
    
    # 2. 替换 title 标签
    html = re.sub(r'<title>.*?</title>', '<title>%s - 存勤法税服务（广州）有限公司</title>' % title, html)
    
    # 3. 替换 meta description
    html = re.sub(r'<meta name="description".*?content=".*?"', '<meta name="description" content="%s"' % desc, html)
    
    # 4. 替换 OG/Twitter meta
    html = re.sub(r'property="og:title".*?content=".*?"', 'property="og:title" content="%s"' % title, html)
    html = re.sub(r'property="og:description".*?content=".*?"', 'property="og:description" content="%s"' % desc, html)
    html = re.sub(r'property="og:url".*?content=".*?"', 'property="og:url" content="https://cunqin.tax/articles/%s.html"' % slug, html)
    html = re.sub(r'name="twitter:title".*?content=".*?"', 'name="twitter:title" content="%s"' % title, html)
    html = re.sub(r'name="twitter:description".*?content=".*?"', 'name="twitter:description" content="%s"' % desc, html)
    html = re.sub(r'name="twitter:image".*?content=".*?"', 'name="twitter:image" content="https://cunqin.tax/images/nav-logo.webp"', html)
    html = re.sub(r'property="article:published_time".*?content=".*?"', 'property="article:published_time" content="%s"' % date, html)
    html = re.sub(r'property="article:modified_time".*?content=".*?"', 'property="article:modified_time" content="2026-05-24"', html)
    
    # 5. 替换 canonical URL
    html = re.sub(r'<link rel="canonical".*?href=".*?"', '<link rel="canonical" href="https://cunqin.tax/articles/%s.html">' % slug, html)
    html = re.sub(r'<link rel="alternate".*?href=".*?"', '<link rel="alternate" hreflang="zh-CN" href="https://cunqin.tax/articles/%s.html">' % slug, html)
    
    # 6. 替换 Schema JSON-LD 中的 Article 块
    # 找到第一个 @type: Article 的块并替换
    html = re.sub(
        r'\{\s*"@context":\s*"https://schema\.org",\s*"@type":\s*"Article".*?"mainEntityOfPage".*?\}',
        article_schema,
        html, count=1, flags=re.DOTALL
    )
    
    # 7. 替换 BreadcrumbList 块
    html = re.sub(
        r'\{\s*"@context":\s*"https://schema\.org",\s*"@type":\s*"BreadcrumbList".*?\}\s*\}',
        breadcrumb_schema + '\n  ]',
        html, count=1, flags=re.DOTALL
    )
    
    # 8. 替换 FAQPage 块
    html = re.sub(
        r'\{\s*"@context":\s*"https://schema\.org",\s*"@type":\s*"FAQPage".*?\}\s*\}\s*\]',
        faq_schema + '\n  }\n]',
        html, count=1, flags=re.DOTALL
    )
    
    # 9. 替换 Hero 区
    html = re.sub(r'<span class="cat-tag">.*?</span>', '<span class="cat-tag">%s</span>' % cat, html)
    html = re.sub(r'<h1>.*?</h1>', '<h1>%s</h1>' % title, html)
    html = re.sub(r'<time datetime=".*?">.*?</time>', '<time datetime="%s">%s</time>' % (date, date), html)
    html = re.sub(r"'view-jinshui-siqi-yingdui'[^<]*", "'view-%s\">&nbsp;' % slug, html)
    html = re.sub(r'id="view-jinshui-siqi-yingdui"[^<]*', 'id="view-%s">' % slug, html)
    html = re.sub(r'var slug = \'jinshui-siqi-yingdui\'', "var slug = '%s'" % slug, html)
    html = re.sub(r"var slug = 'jinshui-siqi-yingdui'", "var slug = '%s'" % slug, html)
    
    # 10. 替换文章正文
    # 找到 <!-- ===== 正文 ===== --> 之后的 <article class="article-body"> 内容，替换到 </article>
    body_start = html.find('<!-- ===== 正文 ===== -->')
    if body_start == -1:
        print("  ERROR: cannot find article body marker")
        return None
    article_start = html.find('<article class="article-body">', body_start)
    article_end = html.find('</article>', article_start)
    if article_start == -1 or article_end == -1:
        print("  ERROR: cannot find article body tags")
        return None
    
    new_body = '<article class="article-body">\n' + body + '\n</article>'
    html = html[:article_start] + new_body + html[article_end + len('</article>'):]
    
    # 11. 替换面包屑导航中的文章标题
    html = re.sub(r'存勤法税"以数治税"新时代', title, html)
    
    # 12. 更新 dateModified 为今天
    html = re.sub(r'"dateModified":\s*"\d{4}-\d{2}-\d{2}"', '"dateModified": "2026-05-25"', html)
    
    return html

# ===== 20篇文章数据 =====
ARTICLES = [
  {
    "slug": "qiyesuodeshui-huisuan-qingjiao",
    "title": "企业所得税汇算清缴实务指南：从填报到筹划的全流程解析",
    "cat": "税务实务",
    "date": "2026-05-10",
    "views": 850,
    "permalink": "/articles/qiyesuodeshui-huisuan-qingjiao.html",
    "desc": "系统梳理企业所得税汇算清缴全流程要点，涵盖收入确认、扣除凭证、纳税调整、税收优惠等核心事项，提供可落地的实操指南。",
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
<p><strong>重要提示</strong>：延期申报需经税务机关批准，且需在延期期间预缴税款，否则将面临滞纳金和罚款风险。</p>
<h3 id="申报表填报架构">申报表填报架构</h3>
<p>企业所得税年度申报表（A类）由<strong>1张主表 + 37张附表</strong>组成，核心逻辑为：</p>
<ol>
<li>收入、成本、费用数据分别填入对应附表</li>
<li>纳税调整事项通过《纳税调整项目明细表》（A105000）汇总</li>
<li>主表最终计算实际应纳所得税额</li>
</ol>
<p>企业应根据自身业务类型，重点关注相关附表的填报要求。例如，高新技术企业需填报《高新技术企业优惠情况及明细表》（A107041），研发费用加计扣除需填报《研发费用加计扣除优惠明细表》（A107012）。</p>
<h2 id="重要税务处理要点">重要税务处理要点</h2>
<h3 id="收入确认要点">收入确认要点</h3>
<p>汇算清缴中收入确认的核心原则是<strong>权责发生制</strong>，需重点关注：</p>
<ul>
<li><strong>视同销售</strong>：将货物用于捐赠、赞助、职工福利等，需按公允价值确认收入</li>
<li><strong>不征税收入</strong>：财政拨款、行政事业性收费等，需满足专项用途、单独核算等条件</li>
<li><strong>分期确认收入</strong>：长期使用资产使用权收入、跨年度工程结算收入等</li>
</ul>
<h3 id="税前扣除凭证管理">税前扣除凭证管理</h3>
<p>根据《企业所得税税前扣除凭证管理办法》（国家税务总局公告2018年第28号），税前扣除凭证分为：</p>
<table>
<thead><tr><th>凭证类型</th><th>适用范围</th><th>备注</th></tr></thead>
<tbody>
<tr><td>发票</td><td>增值税应税项目支出</td><td>境内购进货物或服务</td></tr>
<tr><td>财政票据</td><td>行政事业性收费、政府性基金</td><td>省级以上财政部门监制</td></tr>
<tr><td>内部凭证</td><td>小额零星支出（500元以下）</td><td>需附收款凭证</td></tr>
<tr><td>境外凭证</td><td>境外购进货物或服务</td><td>需翻译并公证</td></tr>
</tbody></table>
<p><strong>实务提示</strong>：汇算清缴前，企业应全面梳理成本费用支出，确保扣除凭证合规、完整。无法补开发票的，需在汇算清缴期结束前（5月31日）取得税前扣除凭证，或按规定提供相关资料证明支出真实性。</p>
<h3 id="税收优惠叠加享受">税收优惠叠加享受</h3>
<p>企业在汇算清缴时，常涉及多项税收优惠的叠加享受问题：</p>
<ul>
<li><strong>高新技术企业15%税率</strong> + <strong>研发费用加计扣除</strong>：可同时享受</li>
<li><strong>小型微利企业优惠</strong> + <strong>研发费用加计扣除</strong>：可同时享受</li>
<li><strong>西部大开发15%税率</strong> + <strong>研发费用加计扣除</strong>：可同时享受</li>
<li><strong>不同区域性优惠</strong>：不得叠加享受，需选择最优方案</li>
</ul>
<h2 id="常见纳税调整事项">常见纳税调整事项</h2>
<h3 id="业务招待费">业务招待费</h3>
<p>业务招待费税前扣除限额为<strong>发生额的60%</strong>，且不超过当年销售（营业）收入的<strong>5‰</strong>。超支部分需进行纳税调增。</p>
<p><strong>筹划提示</strong>：业务招待费超支时，可将部分支出转为<strong>业务宣传费</strong>（限额15%，部分行业30%）或<strong>会议费</strong>（需保留完整会议资料）。</p>
<h3 id="广告费和业务宣传费">广告费和业务宣传费</h3>
<p>一般企业扣除限额为销售（营业）收入的<strong>15%</strong>，超过部分可结转以后年度扣除。化妆品制造、医药制造、饮料制造（不含酒类）企业扣除限额为<strong>30%</strong>。</p>
<h3 id="职工薪酬相关调整">职工薪酬相关调整</h3>
<ul>
<li><strong>职工福利费</strong>：扣除限额为工资薪金总额的14%</li>
<li><strong>工会经费</strong>：扣除限额为工资薪金总额的2%</li>
<li><strong>职工教育经费</strong>：扣除限额为工资薪金总额的8%，超支可结转</li>
<li><strong>补充养老保险/医疗保险</strong>：扣除限额分别为工资薪金总额的5%</li>
</ul>
<h2 id="汇算清缴后的事项">汇算清缴后的事项</h2>
<h3 id="退税处理">退税处理</h3>
<p>汇算结果若为<strong>多缴税款</strong>，企业可选择：</p>
<ol>
<li>申请退税（需提交《退（抵）税申请表》）</li>
<li>抵减下一年度应纳所得税额（更常用，操作更简便）</li>
</ol>
<p><strong>注意</strong>：选择退税的，税务机关将在受理之日起<strong>30日内</strong>完成审核办理。</p>
<h3 id="补税处理">补税处理</h3>
<p>汇算结果若为<strong>少缴税款</strong>，企业应在5月31日前完成补缴，否则自6月1日起按日加收<strong>万分之五的滞纳金</strong>。</p>
<h3 id="税务稽查应对">税务稽查应对</h3>
<p>汇算清缴完成后，企业仍可能面临税务稽查。建议企业：</p>
<ul>
<li>妥善保管汇算清缴相关资料（申报表、备查资料、凭证等）<strong>至少10年</strong></li>
<li>如收到《税务事项通知书》，应在规定期限内提交说明资料</li>
<li>涉及纳税调整的，应积极配合，必要时聘请专业税务顾问协助</li>
</ul>
<h2 id="结语">结语</h2>
<p>企业所得税汇算清缴是一项系统性工作，涉及收入确认、扣除凭证、纳税调整、税收优惠等多个专业领域。企业应建立汇算清缴内控机制，提前规划、规范操作，必要时引入专业税务顾问，确保汇算合规、风险可控。</p>""",
    "faq": [
        {"q":"企业所得税汇算清缴的申报期限是什么？","a":"企业所得税汇算清缴的法定申报期限为年度终了后5个月内，即每年5月31日前。企业需在此期限内完成年度纳税申报表的填报、审核和提交。"},
        {"q":"业务招待费的税前扣除限额如何计算？","a":"业务招待费税前扣除限额为发生额的60%，且不超过当年销售（营业）收入的5‰。两种限额取较小者作为实际可扣除金额，超支部分需进行纳税调增，且不得结转以后年度扣除。"},
        {"q":"汇算清缴时发现扣除凭证不合规怎么办？","a":"应在汇算清缴期结束前（5月31日）积极补开发票或其他合规凭证。确实无法补开、换开的，可凭无法补开换开的证明资料、相关业务合同、非现金支付凭证、运输和入库证明等资料，证明支出真实性，按规定程序向税务机关申报扣除。"},
        {"q":"高新技术企业优惠和研发费用加计扣除可以同时享受吗？","a":"可以。高新技术企业15%优惠税率和研发费用加计扣除是两项独立的税收优惠政策，企业可同时享受。但需注意，研发费用加计扣除需在汇算清缴时同步填报《研发费用加计扣除优惠明细表》（A107012）。"},
        {"q":"汇算清缴后发现申报错误怎么办？","a":"汇算清缴后发现申报错误的，可通过更正申报方式处理。在法定申报期限内（5月31日前）发现错误的，可直接修改申报表重新提交；超过期限的，需向税务机关申请更正申报，并说明更正原因。"}
    ]
  },
]

print("数据定义完成，共 %d 篇文章" % len(ARTICLES))
# 注意：此处仅展示第1篇数据结构，实际脚本需包含全部20篇
# 因篇幅限制，先在服务器上测试第1篇生成效果
