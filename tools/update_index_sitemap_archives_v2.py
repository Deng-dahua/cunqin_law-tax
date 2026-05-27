#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新三个文件：
1. source/search-index.json  — 追加 20 篇新文章条目
2. source/sitemap.xml      — 追加 20 个 <url> 条目
3. source/archives/法税洞察(source).html — 在 </div><!-- #articleList --> 前插入 20 个文章卡片
"""

import json, os, re

BASE = r'C:\Users\26726\WorkBuddy\2026-05-20-21-20-24'

# ══════════════════════════════════════════
# 20 篇文章的元数据（与 gen_all20_v3.py 中的 ARTICLES 一致）
# ══════════════════════════════════════════
ARTICLES = [
    {
        "slug":    "qiyesuodeshui-huisuan-qingjiao",
        "title":   "企业所得税汇算清缴全攻略：从准备到申报的实操指南",
        "cat":     "实操指南",
        "date":    "2026-05-10",
        "desc":    "企业所得税汇算清缴是企业每年最重要的税务工作之一。本文从实战角度，系统讲解汇算清缴的全流程操作要点、常见错误规避、税前扣除凭证管理、税收优惠享受条件等核心内容，帮助企业高效完成汇缴工作。",
        "views":   856,
    },
    {
        "slug":    "yanfa-feiyong-jiakou-kouchu",
        "title":   "研发费用加计扣除政策全解析：企业如何合规享受税收优惠",
        "cat":     "政策解读",
        "date":    "2026-05-09",
        "desc":    "研发费用加计扣除是国家鼓励技术创新的核心税收优惠政策之一。本文全面梳理研发费用加计扣除的政策演变、适用条件、归集范围、核算要求及税务风险管理要点，帮助企业最大化政策红利。",
        "views":   723,
    },
    {
        "slug":    "qiye-kuisun-mibu-guize",
        "title":   "企业亏损弥补规则详解：跨年度亏损结转的税务处理",
        "cat":     "政策解读",
        "date":    "2026-05-08",
        "desc":    "企业亏损弥补是企业所得税汇算清缴中的高频难点问题。本文系统讲解亏损弥补的基本规则、结转年限、特殊性税务处理、企业重组中的亏损结转等核心内容，帮助企业合规进行亏损弥补。",
        "views":   612,
    },
    {
        "slug":    "chengben-feiyong-shuiwu-hegui",
        "title":   "企业成本费用的税务合规管理：从凭证到扣除的全流程管控",
        "cat":     "实操指南",
        "date":    "2026-05-07",
        "desc":    "成本费用是企业税前扣除的核心内容，也是税务稽查的高风险领域。本文从发票管理、税前扣除凭证、费用归集、跨期费用处理等维度，系统讲解成本费用的税务合规管理要点。",
        "views":   934,
    },
    {
        "slug":    "zhongxiao-qiye-shuishou-youhui",
        "title":   "中小企业税收优惠政策全景解读：2024年最新政策汇编",
        "cat":     "政策解读",
        "date":    "2026-05-06",
        "desc":    "中小企业是我国经济的重要组成部分，享受多项税收优惠政策。本文全面梳理小型微利企业所得税优惠、增值税小规模纳税人优惠、六税两费减免等最新政策，帮助企业充分享受税收红利。",
        "views":   1567,
    },
    {
        "slug":    "geren-suodeshui-huisuan-qingjiao",
        "title":   "个人所得税综合所得汇算清缴指南：从专项附加扣除到纳税申报",
        "cat":     "实操指南",
        "date":    "2026-05-05",
        "desc":    "个人所得税综合所得汇算清缴关系到每一位纳税人的切身利益。本文系统讲解汇算范围、专项附加扣除填报、年终奖计税方式选择、异议申诉处理等核心内容，帮助纳税人高效完成汇算。",
        "views":   2145,
    },
    {
        "slug":    "guquan-zhuantang-geren-suodeshui",
        "title":   "股权激励个人所得税全解析：从授予、行权到转让的税务处理",
        "cat":     "政策解读",
        "date":    "2026-05-04",
        "desc":    "股权激励是企业吸引和留住核心人才的重要工具，但其个人所得税处理十分复杂。本文系统讲解股票期权、限制性股票、股票增值权的个税处理规则，帮助企业和个人合规纳税、优化税负。",
        "views":   1089,
    },
    {
        "slug":    "guquan-daichi-shuiwu-fengxian",
        "title":   "股权转让的税务风险与合规策略：企业股东和个人股东的差异处理",
        "cat":     "实操指南",
        "date":    "2026-05-03",
        "desc":    "股权转让是企业重组和个人财富管理中的高频交易行为，也是税务稽查的重点领域。本文深入分析企业股东和个人股东股权转让的税务处理差异、合理性原则适用、反避税条款触发条件等核心问题。",
        "views":   876,
    },
    {
        "slug":    "gongzixinjin-gerensuodeshui-chouhua",
        "title":   "工资薪金个人所得税筹划：从税前扣除到年终奖的合规优化",
        "cat":     "实操指南",
        "date":    "2026-05-02",
        "desc":    "工资薪金个人所得税与每位员工息息相关，也是企业薪酬设计中的核心税务议题。本文系统讲解工资薪金的税前扣除项目、年终奖计税方式选择、股权激励配合、补充养老保险的税务处理等筹划要点。",
        "views":   1324,
    },
    {
        "slug":    "gudong-hongli-shuiwu-chouhua",
        "title":   "股东分红个人所得税税务筹划：从分红到股权转让的税负优化路径",
        "cat":     "实操指南",
        "date":    "2026-05-01",
        "desc":    "股东分红个人所得税税率高达20%，是企业股东和高净值个人关注的核心税务问题。本文系统讲解分红个税的基本规则、合理避税路径、先分红后转让与先转让后分红的税负比较、家族信托在分红筹划中的应用等话题。",
        "views":   756,
    },
    {
        "slug":    "xukai-fapiao-falv-houguo",
        "title":   "虚开发票的法律后果与防范：从行政处罚到刑事责任的全景解析",
        "cat":     "政策解读",
        "date":    "2026-04-30",
        "desc":    "虚开发票是中国税务机关重点打击的税收违法行为，涉及行政责任、刑事责任和信用惩戒多重后果。本文系统讲解虚开发票的认定标准、法律后果、相关人员责任划分、企业防范体系建设等核心内容。",
        "views":   1890,
    },
    {
        "slug":    "shuiwu-xingzheng-fuyi",
        "title":   "税务行政复议实务指南：从申请到决定的全流程解析",
        "cat":     "实操指南",
        "date":    "2026-04-29",
        "desc":    "税务行政复议是纳税人权利救济的重要途径，也是化解税务争议的首选方式。本文系统讲解税务行政复议的申请条件、时限要求、证据准备、复议决定类型及后续救济途径，帮助企业有效维护自身权益。",
        "views":   645,
    },
    {
        "slug":    "yinhua-shuifa-shishi-yaodian",
        "title":   "印花税法实施要点解读：企业合同管理的税务合规新动向",
        "cat":     "政策解读",
        "date":    "2026-04-28",
        "desc":    "《中华人民共和国印花税法》已于2022年7月1日正式实施，标志着印花税立法取得重大进展。本文系统解读印花税法的主要变化、应税合同范围、计税依据确定、免税优惠及企业合同管理中的合规要点。",
        "views":   1087,
    },
    {
        "slug":    "zengzhishui-liudi-tuishui",
        "title":   "增值税留抵退税政策详解：企业如何合规申请并防范税务风险",
        "cat":     "政策解读",
        "date":    "2026-04-27",
        "desc":    "增值税留抵退税政策是近年来力度最大的减税政策之一，对缓解企业资金压力、优化现金流具有重要意义。本文系统讲解留抵退税的申请条件、计算方式、申报流程及税务风险管理要点，帮助企业合规享受政策红利。",
        "views":   1456,
    },
    {
        "slug":    "chukou-tuishui-hegui-fengkong",
        "title":   "出口退税合规与风险防控：从备案到申报的全流程管理",
        "cat":     "实操指南",
        "date":    "2026-04-26",
        "desc":    "出口退税是外贸企业最重要的税收优惠政策之一，但合规要求极高，风险管控难度大。本文系统讲解出口退税的备案管理、单证准备、申报流程、函调配合及风险防控体系建设，帮助企业建立合规高效的出口退税管理体系。",
        "views":   978,
    },
    {
        "slug":    "CRS-kuajing-zichan-shenbao",
        "title":   "CRS与跨境资产申报：高净值人群的税务合规新挑战",
        "cat":     "行业洞察",
        "date":    "2026-04-25",
        "desc":    "CRS（共同申报准则）的全球推行，标志着跨境资产信息透明化进入新阶段。对于拥有境外资产的高净值人群而言，合规申报已成为不可回避的义务。本文系统讲解CRS的运行机制、中国CRS申报要求、常见风险点及合规策略。",
        "views":   1567,
    },
    {
        "slug":    "hehuo-qiye-shuiwu-jiexi",
        "title":   "合伙企业税务实务全解析：从先分后税到合伙人所得税",
        "cat":     "实操指南",
        "date":    "2026-04-24",
        "desc":    "合伙企业以其灵活的组织形式和税收穿透特性，成为股权投资、员工持股平台、家族办公室等场景的首选载体。但其税务处理规则独特，易产生理解偏差。本文系统讲解合伙企业的税务处理原则、先分后税规则、合伙人所得税计算等核心内容。",
        "views":   834,
    },
    {
        "slug":    "IPO-shuiwu-hegui-jiagou",
        "title":   "IPO过程中的税务合规与架构优化：从上市前税务体检到上市后税务管理",
        "cat":     "行业洞察",
        "date":    "2026-04-23",
        "desc":    "IPO是企业发展的重要里程碑，但税务合规问题往往是上市审核中的高频问询事项。本文系统讲解IPO过程中税务合规的自查要点、历史税务风险清理、股权架构税务优化、上市后税务管理体系搭建等核心内容，帮助企业顺利过会。",
        "views":   1123,
    },
    {
        "slug":    "simu-jijin-shuiwu-chouhua",
        "title":   "私募投资基金税务筹划：从产品架构到投资人纳税的全流程管理",
        "cat":     "行业洞察",
        "date":    "2026-04-22",
        "desc":    "私募基金行业税务处理复杂，涉及基金管理人、基金产品、投资人三方的税务协调。本文系统讲解私募基金的主要产品架构（公司型、合伙型、契约型）的税务差异、增值税与所得税处理、投资人纳税时点等核心问题。",
        "views":   967,
    },
    {
        "slug":    "shuzihua-shuiwu-guanli-zhuanxing",
        "title":   "企业税务管理数字化转型：从Excel到智能税务系统的升级路径",
        "cat":     "行业洞察",
        "date":    "2026-04-21",
        "desc":    "金税四期的全面推开，对企业税务管理的数字化水平提出了更高要求。本文系统讲解企业税务管理数字化的驱动因素、技术路径、系统选型、实施步骤及与财务系统、业务系统的集成策略，帮助企业实现税务管理转型升级。",
        "views":   734,
    },
]

# ══════════════════════════════════════════
# 1. 更新 search-index.json
# ══════════════════════════════════════════
print("=== 1. 更新 search-index.json ===")
idx_path = os.path.join(BASE, 'source', 'search-index.json')
with open(idx_path, 'r', encoding='utf-8') as f:
    idx = json.load(f)

print(f"  当前条目数: {len(idx)}")
new_entries = []
for a in ARTICLES:
    entry = {
        "title":    a["title"],
        "url":      f'/articles/{a["slug"]}.html',
        "text":      a["desc"][:120] + ("…" if len(a["desc"])>120 else ""),
        "date":      a["date"],
        "category":  a["cat"],
    }
    new_entries.append(entry)

idx.extend(new_entries)

with open(idx_path, 'w', encoding='utf-8') as f:
    json.dump(idx, f, ensure_ascii=False, indent=2)

print(f"  更新后条目数: {len(idx)}")
print("  ✅ search-index.json 更新完成")

# ══════════════════════════════════════════
# 2. 更新 sitemap.xml
# ══════════════════════════════════════════
print("\n=== 2. 更新 sitemap.xml ===")
sitemap_path = os.path.join(BASE, 'source', 'sitemap.xml')
with open(sitemap_path, 'r', encoding='utf-8') as f:
    sitemap = f.read()

# 在 </urlset> 前插入新 url 条目
new_urls = []
for a in ARTICLES:
    block = f"""  <url>
    <loc>https://cunqin.tax/articles/{a["slug"]}.html</loc>
    <lastmod>2026-05-24</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
    <xhtml:link rel="alternate" hreflang="zh-CN" href="https://cunqin.tax/articles/{a["slug"]}.html"/>
  </url>
"""
    new_urls.append(block)

insert_block = '\n' + '\n'.join(new_urls) + '\n'
sitemap = sitemap.replace('</urlset>', insert_block + '</urlset>')

# 修正 hreflang（原文件中是 zh-CN，应统一为 zh-CN，但 sitemap 中是 zh-CN，保持一致即可）
# 注意：原 sitemap 中有个拼写错误 zh-CN，但百度/Google 都支持，暂不修改历史条目

with open(sitemap_path, 'w', encoding='utf-8') as f:
    f.write(sitemap)

print(f"  ✅ sitemap.xml 已追加 {len(ARTICLES)} 个 <url> 条目")

# ══════════════════════════════════════════
# 3. 更新法税洞察页（archives 页）
# ══════════════════════════════════════════
print("\n=== 3. 更新法税洞察页 ===")
archives_path = os.path.join(BASE, 'source', 'archives', '法税洞察(source).html')
with open(archives_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 在 </div><!-- #articleList --> 之前插入新文章卡片
# 定位点：</div>\n</section>\n<div id="paginationContainer">
# 实际在源码中是：      </a>\n\n    </div>\n</section>\n<div id="paginationContainer">
# 我们在最后一个 </a> 之后、  </div> 之前插入

# 找最后一个 article-item 的结束位置
# 策略：在 `</div>\n</section>\n<div id="paginationContainer">` 前插入
anchor = '    </div>\n</section>\n<div id="paginationContainer">'
if anchor not in content:
    # 备选锚点
    anchor = '</div>\n</section>\n<div id="paginationContainer">'
    if anchor not in content:
        print("  ❌ 找不到插入锚点！")
        # 打印前后文帮助调试
        idx2 = content.find('paginationContainer')
        if idx2 > 0:
            print("  附近内容:", repr(content[max(0,idx2-200):idx2+50]))
        exit(1)

# 构建新文章卡片 HTML
cards = []
for a in ARTICLES:
    # 截取摘要（前80字）
    summary = a["desc"][:80] + "…" if len(a["desc"])>80 else a["desc"]
    # 日期格式：2026.05.10
    date_fmt = a["date"].replace('-', '.')
    card = f"""      <a href="../articles/{a["slug"]}.html" class="article-item" data-date="{a["date"]}" data-category="{a["cat"]}" data-views="{a["views"]}">
        <div class="article-content">
          <h3>{a["title"]}</h3>
          <p>{summary}</p>
          <span class="article-tag">{a["cat"]}</span>
</div>
        <div class="article-arrow"><i class="fas fa-chevron-right"></i></div>
      </a>
"""
    cards.append(card)

insert_html = '\n\n' + '\n'.join(cards) + '\n'
new_content = content.replace(anchor, insert_html + '    </div>\n</section>\n<div id="paginationContainer">')

with open(archives_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"  ✅ 法税洞察页已追加 {len(ARTICLES)} 个文章卡片")

# ══════════════════════════════════════════
# 4. 汇总报告
# ══════════════════════════════════════════
print("\n=== 汇总 ===")
print(f"  search-index.json 条目: {len(idx)}")
# 统计 sitemap url 数
sitemap_new = open(sitemap_path, 'r', encoding='utf-8').read()
url_count = sitemap_new.count('<url>')
print(f"  sitemap.xml <url> 条目: {url_count}")
# 统计 archives 页文章卡片数
archives_new = open(archives_path, 'r', encoding='utf-8').read()
card_count = archives_new.count('class="article-item"')
print(f"  法税洞察页文章卡片数: {card_count}")
print("\n✅ 全部完成！")
