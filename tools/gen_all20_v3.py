#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量生成20篇法税洞察文章(source).html
基于 金税四期全面解读(source).html 模板，精确替换关键字段
v3: 修复 og:description / twitter:description / title / cat-tag 替换不准确的问题
"""

import os, re, json

TEMPLATE = r"C:\Users\26726\WorkBuddy\2026-05-20-21-20-24\source\articles\金税四期全面解读(source).html"
OUT_DIR   = r"C:\Users\26726\WorkBuddy\2026-05-20-21-20-24\source\articles"
BODY_DIR = r"C:\Users\26726\WorkBuddy\2026-05-20-21-20-24\tools\article_bodies"

ARTICLES = [
  { "slug":"qiyesuodeshui-huisuan-qingjiao",  "file":"01_qiyesuodeshui_huisuan_qingjiao.txt",
    "title":"企业所得税汇算清缴实务指南：从填报到筹划的全流程解析",
    "cat":"税务实务", "cat_en":"tax-practice", "date":"2026-05-10", "views":850,
    "desc":"企业所得税汇算清缴全流程实操指南，从前期准备、纳税调整到申报填写，提供可落地的完整解决方案，帮助企业合法降低税务成本。"},
  { "slug":"yanfa-feiyong-jiakou-kouchu",  "file":"02_yanfa_feiyong_jiakou_kouchu.txt",
    "title":"研发费用加计扣除实操全攻略：从立项到申报的合规路径",
    "cat":"税收优惠", "cat_en":"tax-incentive", "date":"2026-05-12", "views":920,
    "desc":"研发费用加计扣除政策深度解析与实操全攻略，涵盖研发活动界定、费用归集范围、辅助账设置、汇算清缴申报及备查资料清单。"},
  { "slug":"qiye-kuisun-mibu-guize",  "file":"03_qiye_kuisun_mibu_guize.txt",
    "title":"企业所得税亏损弥补规则深度解析：年限、顺序与筹划空间",
    "cat":"税务实务", "cat_en":"tax-practice", "date":"2026-05-14", "views":680,
    "desc":"深度解析企业所得税亏损弥补的基本规则、各复杂情形的税务处理，以及合法合规的亏损弥补筹划空间。"},
  { "slug":"chengben-feiyong-shuiwu-hegui",  "file":"04_chengben_feiyong_shuiwu_hegui.txt",
    "title":"成本费用税前扣除合规管理：凭证、标准与风险排查",
    "cat":"税务合规", "cat_en":"tax-compliance", "date":"2026-05-16", "views":750,
    "desc":"系统讲解成本费用税前扣除的四大要件、各费用项目的扣除标准，以及金税四期下的风险新特征和合规管理实操要点。"},
  { "slug":"zhongxiao-qiye-shuishou-youhui",  "file":"05_zhongxiao_qiye_shuishou_youhui.txt",
    "title":"中小企业税收优惠政策全景解读：让每一分优惠都落到实处",
    "cat":"税收优惠", "cat_en":"tax-incentive", "date":"2026-05-18", "views":880,
    "desc":"全景解读适用于中小企业的各项税收优惠政策，包括小型微利企业、增值税小规模、六税两费、研发加计扣除等，帮助企业用足用好政策红利。"},
  { "slug":"geren-suodeshui-huisuan-qingjiao",  "file":"06_geren_suodeshui_huisuan_qingjiao.txt",
    "title":"个人所得税汇算清缴关键要点：从申报到退税的全流程指南",
    "cat":"个税实务", "cat_en":"individual-tax", "date":"2026-05-20", "views":1050,
    "desc":"系统讲解个人所得税汇算清缴的适用人群、计算逻辑、专项附加扣除、年终奖计税方式选择，以及申报流程和风险防控要点。"},
  { "slug":"guquan-zhuantang-geren-suodeshui",  "file":"07_guquan_zhuantang_geren_suodeshui.txt",
    "title":"股权转让个人所得税筹划实务：定价、申报与风险防控",
    "cat":"个税实务", "cat_en":"individual-tax", "date":"2026-05-22", "views":780,
    "desc":"深度解析股权转让个人所得税的基本规则、股权原值确定、申报义务与扣缴义务，以及合法合规的税务筹划策略。"},
  { "slug":"guquan-daichi-shuiwu-fengxian",  "file":"08_guquan_daichi_shuiwu_fengxian.txt",
    "title":"股权代持的税务风险与合规处理：还原、分红与转让的完整方案",
    "cat":"税务风险", "cat_en":"tax-risk", "date":"2026-05-24", "views":650,
    "desc":"深度解析股权代持的法律架构、税务风险（双重征税、高额税负、代持还原被征税等），以及合规处理方案和风险防控体系。"},
  { "slug":"gongzixinjin-gerensuodeshui-chouhua",  "file":"09_gongzixinjin_gerensuodeshui_chouhua.txt",
    "title":"工资薪金个人所得税筹划策略：薪酬结构、福利与激励的税务优化",
    "cat":"个税实务", "cat_en":"individual-tax", "date":"2026-04-28", "views":920,
    "desc":"系统讲解工资薪金个税的基本规则、专项附加扣除、年终奖筹划策略、股权激励税务处理，以及合规筹划的风险防控。"},
  { "slug":"gudong-hongli-shuiwu-chouhua",  "file":"10_gudong_hongli_shuiwu_chouhua.txt",
    "title":"股东分红与薪酬的税务优化：利润分配、借款与费用报销的合规路径",
    "cat":"个税实务", "cat_en":"individual-tax", "date":"2026-04-30", "views":710,
    "desc":"对比分析股东分红与薪酬的税负差异，讲解合法合规的优化策略，以及股东借款、费用报销的合规边界与风险防控。"},
  { "slug":"xukai-fapiao-falv-houguo",  "file":"11_xukai_fapiao_falv_houguo.txt",
    "title":"虚开发票的法律后果与防范指南：从行政责任到刑事风险的全面警示",
    "cat":"税务风险", "cat_en":"tax-risk", "date":"2026-05-01", "views":1100,
    "desc":"系统梳理虚开发票的法律定义、行政责任与刑事责任，金税四期下的查处机制，以及企业的防范策略和常见风险场景解析。"},
  { "slug":"shuiwu-xingzheng-fuyi",  "file":"12_shuiwu_xingzheng_fuyi.txt",
    "title":"税务行政复议实战指南：程序、策略与权利救济",
    "cat":"税务合规", "cat_en":"tax-compliance", "date":"2026-05-03", "views":620,
    "desc":"系统讲解税务行政复议的适用范围、程序要求（时限、申请书内容、复议机关）、复议策略与技巧，以及复议结果与后续程序。"},
  { "slug":"yinhua-shuifa-shishi-yaodian",  "file":"13_yinhua_shuifa_shishi_yaodian.txt",
    "title":"印花税法实施要点与合规管理：应税凭证、税率变化与申报实务",
    "cat":"政策解读", "cat_en":"policy", "date":"2026-05-05", "views":730,
    "desc":"深度解读印花税法实施的核心变化（税目简化、税率下调、申报方式调整），以及印花税的计税依据、优惠政策和合规管理要点。"},
  { "slug":"zengzhishui-liudi-tuishui",  "file":"14_zengzhishui_liudi_tuishui.txt",
    "title":"增值税留抵退税实操指南：条件、计算与风险防控",
    "cat":"税务实务", "cat_en":"tax-practice", "date":"2026-05-07", "views":850,
    "desc":"系统讲解增值税留抵退税的申请条件、计算步骤（增量留抵税额、进项构成比例、允许退还税额）、申请流程及风险防控要点。"},
  { "slug":"chukou-tuishui-hegui-fengkong",  "file":"15_chukou_tuishui_hegui_fengkong.txt",
    "title":"出口退税合规与风险防范：从申报到稽查的全链条管理",
    "cat":"税务合规", "cat_en":"tax-compliance", "date":"2026-05-09", "views":690,
    "desc":"系统讲解出口退税的基本原理、申报条件与流程，高风险的识别与防控，以及金税四期下出口退税的全链条监控机制。"},
  { "slug":"CRS-kuajing-zichan-shenbao",  "file":"16_CRS_kuajing_zichan_shenbao.txt",
    "title":"CRS框架下跨境资产申报与合规：信息交换机制与中国居民应对策略",
    "cat":"跨境税务", "cat_en":"cross-border", "date":"2026-04-20", "views":750,
    "desc":"深度解析CRS（通用报告准则）的运作机制、信息交换范围，以及中国税收居民在CRS框架下的合规义务、风险场景与应对策略。"},
  { "slug":"hehuo-qiye-shuiwu-jiexi",  "file":"17_hehuo_qiye_shuiwu_jiexi.txt",
    "title":"合伙企业税务处理深度解析：先分后税、穿透原则与筹划空间",
    "cat":"税务实务", "cat_en":"tax-practice", "date":"2026-04-22", "views":580,
    "desc":"深度解析合伙企业先分后税的核心逻辑、不同合伙人类型的税务处理、有限合伙企业的特殊安排，以及税务风险防控要点。"},
  { "slug":"IPO-shuiwu-hegui-jiagou",  "file":"18_IPO_shuiwu_hegui_jiagou.txt",
    "title":"IPO税务合规与架构设计：上市前必须解决的六大税务问题",
    "cat":"资本运作", "cat_en":"capital", "date":"2026-04-24", "views":820,
    "desc":"系统梳理IPO前必须解决的六大税务问题（历史股权架构、历史税务申报、关联交易、大股东资金占用、高新资质、架构重组），以及IPO税务合规的四步走策略。"},
  { "slug":"simu-jijin-shuiwu-chouhua",  "file":"19_simu_jijin_shuiwu_chouhua.txt",
    "title":"私募基金税务筹划要点：基金架构、收益分配与投资人税负优化",
    "cat":"资本运作", "cat_en":"capital", "date":"2026-04-26", "views":640,
    "desc":"系统解析私募基金的三种法律形式（契约型、合伙型、公司型）的税务特征、三个核心税务环节的税务处理，以及私募基金税务筹划的核心策略。"},
  { "slug":"shuzihua-shuiwu-guanli-zhuanxing",  "file":"20_shuzihua_shuiwu_guanli_zhuanxing.txt",
    "title":"数字化税务管理转型路径：从手工申报到智能风控的进化之路",
    "cat":"税务实务", "cat_en":"tax-practice", "date":"2026-04-18", "views":780,
    "desc":"系统阐述企业数字化税务管理转型的四阶段路径（基础数字化、流程自动化、智能风控、价值创造），以及不同规模企业（大型、中型、小型）的转型策略。"},
]

# 每篇文章的5个FAQ
def make_faq(title, cat_en):
    return [
        {"@type":"Question", "name": f"{title}的核心要点是什么？",
         "acceptedAnswer":{"@type":"Answer", "text": f"本文系统讲解了{title}的核心内容，重点涵盖政策解读、实操要点和风险防控体系，建议重点阅读前言、核心规则解析和筹划策略部分，掌握合法合规的操作要点。"}},
        {"@type":"Question", "name": f"企业在处理{cat_en}相关事务时，最常见的错误有哪些？",
         "acceptedAnswer":{"@type":"Answer", "text": "最常见的错误包括对政策理解不准确、备查资料不完整、未按期申报或扣缴、混淆不同税目的适用条件等。建议企业在处理前咨询专业税务顾问，确保合规。"}},
        {"@type":"Question", "name": f"{title}相关的税收优惠有哪些？",
         "acceptedAnswer":{"@type":"Answer", "text": "具体优惠内容因文章主题而异，建议仔细阅读本文「税收优惠」或「筹划策略」章节，并在申报时依法享受，用足用好各项扣除、抵免和减免政策。"}},
        {"@type":"Question", "name": f"金税四期对{title}相关税务处理有什么影响？",
         "acceptedAnswer":{"@type":"Answer", "text": "金税四期通过大数据比对、AI智能分析、跨部门数据互通，实现了对企业税务行为的全方位监控。建议企业建立完善的合规管理体系，确保「四流合一」，让每一笔税务处理都经得起查。"}},
        {"@type":"Question", "name": f"如果我对{title}的税务处理仍有疑问，应该怎么解决？",
         "acceptedAnswer":{"@type":"Answer", "text": "建议联系存勤法税。我们是专注业财税法融合的专业顾问机构，可提供一对一的定制化税务解决方案。咨询热线：13556116691（微信同号）。"}},
    ]

def read_template():
    with open(TEMPLATE, 'r', encoding='utf-8') as f:
        return f.read()

def read_body(filename):
    path = os.path.join(BODY_DIR, filename)
    with open(path, 'r', encoding='utf-8') as f:
        return f.read().strip()

def gen_html(tpl, art):
    slug  = art["slug"]
    title = art["title"]
    cat   = art["cat"]
    date  = art["date"]
    views = str(art["views"])
    desc  = art["desc"]
    body  = read_body(art["file"])
    faqs  = make_faq(title, art["cat_en"])

    h = tpl

    # ---- 1. YAML frontmatter: permalink ----
    h = h.replace(
        'permalink: /articles/jinshui-siqi-yingdui.html',
        f'permalink: /articles/{slug}.html'
    )

    # ---- 2. <title> tag ----
    # 模板实际内容：注意 "以数治税新时代的全面策略"
    h = h.replace(
        '<title>金税四期全面解读：企业如何从容应对以数治税新时代的全面策略 - 存勤法税服务（广州）有限公司</title>',
        f'<title>{title} - 存勤法税服务（广州）有限公司</title>'
    )

    # ---- 3. meta description (name="description") ----
    h = h.replace(
        'content="金税四期全面解读与应对策略：从发票电子化改革趋势、大数据风险画像机制、全税种联动监控原理三个维度，深入剖析金税四期对企业财税管理的实质性影响，提供发票管理升级路径、业务合规整改方案、风险自查机制建设等实操应对指南。面对金税四期，企业需要的不是恐慌，而是专业的合规升级路径。"',
        f'content="{desc}"'
    )

    # ---- 4. og:title ----
    h = h.replace(
        'content="金税四期全面解读：企业如何从容应对&quot;以数治税&quot;新时代 - 存勤法税服务（广州）有限公司"',
        f'content="{title} - 存勤法税服务（广州）有限公司"'
    )

    # ---- 5. og:description ----
    h = h.replace(
        'content="金税四期全面解读与应对策略：从发票电子化改革趋势、大数据风险画像机制、全税种联动监控原理三个维度，深入剖析金税四期对企业财税管理的实质性影响，提供发票管理升级路径、业务合规整改方案、风险自查机制建设等实操应对指南。面对金税四期，企业需要的不是恐慌，而是专业的合规升级路径。"',
        f'content="{desc}"'
    )

    # ---- 6. og:url ----
    h = h.replace(
        'content="https://cunqin.tax/articles/jinshui-siqi-yingdui.html"',
        f'content="https://cunqin.tax/articles/{slug}.html"'
    )

    # ---- 7. canonical URL ----
    h = h.replace(
        'href="https://cunqin.tax/articles/jinshui-siqi-yingdui.html"',
        f'href="https://cunqin.tax/articles/{slug}.html"'
    )

    # ---- 8. hreflang ----
    h = h.replace(
        'href="https://cunqin.tax/articles/jinshui-siqi-yingdui.html"',
        f'href="https://cunqin.tax/articles/{slug}.html"'
    )

    # ---- 9. twitter:title ----
    h = h.replace(
        'content="金税四期全面解读：企业如何从容应对&quot;以数治税&quot;新时代 - 存勤法税服务（广州）有限公司"',
        f'content="{title} - 存勤法税服务（广州）有限公司"'
    )

    # ---- 10. twitter:description ----
    h = h.replace(
        'content="深度解读金税四期政策要点与实施背景，剖析发票电子化、大数据风险监控对企业财税管理的影响，提供切实可行的税务合规应对策略"',
        f'content="{desc}"'
    )

    # ---- 11. article:published_time / modified_time ----
    h = h.replace('content="2026-04-15"', f'content="{date}"')
    h = h.replace('content="2026-05-21"', 'content="2026-05-24"')

    # ---- 12. Hero: cat-tag（只替换 hero 里的，用上下文精确定位）----
    # Hero 里的结构：<span class="cat-tag">政策解读</span>
    h = h.replace(
        '<span class="cat-tag">政策解读</span>',
        f'<span class="cat-tag">{cat}</span>'
    )

    # ---- 13. Hero: h1 ----
    h = h.replace(
        '金税四期全面解读：企业如何从容应对"以数治税"新时代',
        title
    )

    # ---- 14. Hero: date ----
    h = h.replace('<time datetime="2026-04-15">2026-04-15</time>',
                   f'<time datetime="{date}">{date}</time>')

    # ---- 15. Hero: view counter slug + id ----
    h = h.replace("'jinshui-siqi-yingdui'", f"'{slug}'")
    h = h.replace('id="view-jinshui-siqi-yingdui"', f'id="view-{slug}"')
    h = h.replace('data-slug="jinshui-siqi-yingdui"', f'data-slug="{slug}"')

    # ---- 16. Breadcrumb: 第三项的 name ----
    h = h.replace(
        '"name": "金税四期全面解读：企业如何从容应对\\"以数治税\\"新时代"',
        f'"name": "{title}"'
    )

    # ---- 17. Breadcrumb: 第二项的 item URL（archives 链接，不动） ----

    # ---- 18. Schema Article: headline, datePublished, dateModified ----
    h = h.replace(
        '"headline": "金税四期全面解读：企业如何从容应对\\"以数治税\\"新时代"',
        f'"headline": "{title}"'
    )
    h = h.replace('"datePublished": "2026-04-15"', f'"datePublished": "{date}"')
    h = h.replace('"dateModified": "2026-05-21"', '"dateModified": "2026-05-24"')

    # ---- 19. Schema Article: mainEntityOfPage @id ----
    h = h.replace(
        '"@id": "https://cunqin.tax/articles/jinshui-siqi-yingdui.html"',
        f'"@id": "https://cunqin.tax/articles/{slug}.html"'
    )

    # ---- 20. Schema BreadcrumbList: 第三项 name ----
    # 已经包含在 #16 中（同一个 JSON 字符串）

    # ---- 21. Replace article body ----
    body_start = h.find('<article class="article-body">')
    body_end   = h.find('</article>', body_start)
    if body_start == -1 or body_end == -1:
        print(f"  ✗ 找不到正文区域: {slug}")
        return None
    new_body = f'<article class="article-body">\n{body}\n</article>'
    h = h[:body_start] + new_body + h[body_end + len('</article>'):]

    # ---- 22. JS: slug 变量 ----
    h = h.replace("var slug = 'jinshui-siqi-yingdui';", f"var slug = '{slug}';")
    h = h.replace("'view-jinshui-siqi-yingdui'", f"'view-{slug}'")
    h = h.replace("'cq_view_jinshui-siqi-yingdui'", f"'cq_view_{slug}'")
    h = h.replace("'cq_sess_jinshui-siqi-yingdui'", f"'cq_sess_{slug}'")

    # ---- 23. FAQPage Schema ----
    faq_schema_str = json.dumps(faqs, ensure_ascii=False, indent=8)
    # 找到 FAQPage 中 mainEntity 的位置并替换
    # 策略：找到 "mainEntity": [ 到结束 ] 的位置
    me_start = h.find('"mainEntity": [', h.find('"@type": "FAQPage"'))
    if me_start != -1:
        # 找到对应的 ] 位置（FAQPage 对象内的 mainEntity 数组结束）
        bracket_depth = 0
        pos = me_start + len('"mainEntity": ')
        # pos 现在指向 [
        assert h[pos] == '['
        bracket_depth = 1
        pos += 1
        while pos < len(h) and bracket_depth > 0:
            if h[pos] == '[':
                bracket_depth += 1
            elif h[pos] == ']':
                bracket_depth -= 1
                if bracket_depth == 0:
                    me_end = pos  # 指向 ]
                    break
            pos += 1
        else:
            print(f"  ✗ FAQPage mainEntity 括号不匹配: {slug}")
            return None
        new_me = f'"mainEntity": {faq_schema_str}'
        h = h[:me_start] + new_me + h[me_end+1:]
    else:
        print(f"  ✗ 找不到 FAQPage mainEntity: {slug}")

    return h

def main():
    tpl = read_template()
    print(f"模板读取成功: {len(tpl)} 字符")

    for art in ARTICLES:
        print(f"生成: {art['slug']}.html ...")
        try:
            html = gen_html(tpl, art)
            if html is None:
                print(f"  ✗ 跳过: {art['slug']}")
                continue
            out_path = os.path.join(OUT_DIR, f"{art['slug']}(source).html")
            with open(out_path, 'w', encoding='utf-8') as f:
                f.write(html)
            print(f"  ✓ 已写入: {out_path}  ({len(html)} 字符)")
        except Exception as e:
            print(f"  ✗ 错误: {art['slug']}: {e}")

    print("\n全部完成！")

if __name__ == "__main__":
    main()
