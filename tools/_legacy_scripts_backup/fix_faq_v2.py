#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix FAQPage Schema using line-based replacement."""
import os

BASE = r'C:\Users\26726\WorkBuddy\2026-05-20-21-20-24\source\articles'

FAQ_NEW = {
    '税务稽查应对实战手册(source).html': '''  {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
      {
        "@type": "Question",
        "name": "收到税务稽查通知书后该怎么办？",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "首先冷静下来，稽查不等于定罪。24小时内完成：仔细阅读通知书（明确稽查期间、范围、税种）、成立内部应对小组（含企业负责人、财务主管、律师或税务顾问）、启动内部自查梳理问题点、联系专业税务顾问制定应对策略。切记不要销毁任何资料，那是刑事红线。"
        }
      },
      {
        "@type": "Question",
        "name": "税务稽查罚款能减免吗？",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "可以争取。法定从轻或减轻处罚的情形包括：主动消除或减轻违法行为危害后果、配合税务机关查处有立功表现、违法行为轻微并及时纠正且未造成危害后果。在收到处理决定书后的陈述申辩阶段，用事实和法律组织申辩材料，尤其是证明你积极配合、主动整改的证据，都可能成为从轻处罚的依据。"
        }
      },
      {
        "@type": "Question",
        "name": "主动补税能减轻处罚吗？",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "能。在稽查结论作出之前主动补缴税款和滞纳金的，可以从轻或减轻处罚。若稽查后发现后才补税，罚款标准为少缴税款的50%至5倍。关键窗口期是在稽查结论作出之前——不是收到通知书之前。主动补税的代价：补税+滞纳金（按日万分之五，不可免），但罚款可大幅降低甚至免除。"
        }
      },
      {
        "@type": "Question",
        "name": "税务行政复议的成功率有多少？",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "客观而言，税务行政复议的胜率不高，尤其在事实清楚、法律适用正确的情况下。但如果存在程序违法、证据不足或明显的事实认定错误，复议和诉讼是有效的维权手段。时效要求：收到处理决定书60日内申请行政复议，收到复议决定15日内或收到原决定6个月内提起行政诉讼。复议需要先缴清税款或提供担保。"
        }
      },
      {
        "@type": "Question",
        "name": "被税务稽查时要不要请律师？",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "建议税务顾问和律师组合使用。税务顾问负责专业领域的实体问题（税务政策适用、计算方法、业务定性），律师负责程序问题（证据合法性审查、法律文书应对、复议和诉讼代理）。当稽查涉及大额补税和罚款、或可能涉及移送公安时，律师的参与尤为重要。"
        }
      }
    ]
  }''',

    '企业税务健康体检30项(source).html': '''  {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
      {
        "@type": "Question",
        "name": "企业税务健康检查有什么用？",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "税务健康检查是在被税务机关稽查之前，主动对企业进行全面自查，发现潜在的税务问题并提前整改。它的价值在于：把主动权掌握在自己手里——查出问题可以主动补申报争取从轻处理，而不是等到被稽查后再被动应对。覆盖增值税、企业所得税、发票管理、个人所得税、优惠资质五大维度，共30项具体指标。"
        }
      },
      {
        "@type": "Question",
        "name": "公司税务有没有问题怎么查？",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "可以从五个维度入手自查：增值税维度——检查税负率是否与行业平均水平偏差过大、进销项是否匹配、留抵退税是否合规；企业所得税维度——核实收入是否全部申报、成本费用凭证是否合规、关联交易定价是否合理；发票管理维度——确认进项发票是否有真实交易背景、是否存在买票行为；个税维度——核实工资薪金是否全员全额申报、股东分红是否完税；优惠资质维度——检查高新资质、小微条件等是否持续达标。"
        }
      },
      {
        "@type": "Question",
        "name": "中小企业也需要税务体检吗？",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "非常需要。越是中小企业，税务风险越高。原因有三：中小企业通常缺乏专门的税务管理团队，问题更隐蔽；金税四期的数据比对不因企业规模而区别对待——大企业和小企业一样被监控；中小企业抗风险能力更弱，一次大额补税就可能影响正常经营。建议至少每半年做一次自检，每年请专业机构做一次深度体检。"
        }
      },
      {
        "@type": "Question",
        "name": "税务自检查出问题后该怎么办？",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "按风险等级分层处理：红色（高风险）问题立即联系税务顾问，评估是否需要主动补申报，30天内处理；黄色（中风险）问题在3个月内内部整改，完善制度和流程；绿色（低风险）问题纳入日常管理定期复查。查出问题不是坏事——发现得越早，解决的代价越小，主动权越大。"
        }
      },
      {
        "@type": "Question",
        "name": "中小企业常见的税务风险有哪些？",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "最常见的五大问题：私户收款未申报——用个人账户收经营款项，金税四期银行流水比对极易发现；虚增成本费用——白条入账、无真实交易的发票（买票）；发票管理混乱——进销项不匹配或发票品名与实际业务不符；收入确认不完整——未开票收入未申报；关联交易不合规——通过关联企业转移利润未按独立交易原则定价。"
        }
      }
    ]
  }''',

    '私户收款被查补救指南(source).html': '''  {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
      {
        "@type": "Question",
        "name": "个人卡收款被查到怎么办？",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "分三种情况处理：还未被查——立即盘点全部私户收款金额，主动补申报补税+滞纳金，可从轻或减轻处罚；收到风险提示——立即响应并主动自查补税，仍可争取从轻处理；已被稽查立案——配合检查、争取从轻，主动提供整改措施和补税意愿作为从轻依据。无论在哪个阶段，联系专业税务顾问评估具体情形、制定最优策略都是第一步。"
        }
      },
      {
        "@type": "Question",
        "name": "私户收款补税有时间限制吗？",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "如果被认定为偷税（具有主观故意），不受追征期限制，理论上可以追溯到企业开业以来的所有年份。如果被认定为一般计算错误或失误，追征期一般为3年，特殊情况下可延长到5年。是否构成偷税取决于行为表现和证据——如是否刻意隐匿收入、使用多个账户分拆收款等。因此，主动补申报的时机很重要，早点处理可以避免被认定为偷税。"
        }
      },
      {
        "@type": "Question",
        "name": "私户收款性质严重吗？是偷税吗？",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "性质取决于情节：如果是有组织、故意地通过个人账户隐匿经营收入以逃避纳税义务，构成偷税，需要补税+滞纳金+0.5-5倍罚款，情节严重的可能移送公安机关追究刑事责任。如果是因为对税法不熟悉、无意中使用个人账户收款但账面上有相应记录，可能被认定为一般申报不实，处理相对较轻。关键是证据——是否有主观故意，需要由税务顾问帮你评估。"
        }
      },
      {
        "@type": "Question",
        "name": "微信支付宝收款需要报税吗？",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "需要。微信和支付宝的商户收款码属于经营收款渠道，交易记录可追溯。个人收款码用于经营收款的，同样构成经营收入，需要依法申报纳税。金税四期可以从支付平台获取交易数据并与申报数据进行比对。补救方法：从账单中导出经营性的收款记录，按年度汇总未申报金额，纳入主动补申报的范围。不要遗漏——被发现时漏报的部分同样会被追缴和处罚。"
        }
      },
      {
        "@type": "Question",
        "name": "怎么把私户收款转成合规经营？",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "分三步走：止血——即日起所有新业务收款走对公账户或已申报的商户收款码；清旧——制定3个月内计划，将存量私户余额分批转入对公账户并申报；建体系——建立合同流、资金流、发票流三流合一的合规收款体系，每月进行银行流水与申报数据的自动对账。对于规模较小的企业，也可考虑通过个体工商户或个人独资企业进行合规化处理，但需关注2026年核定征收政策的收紧。"
        }
      }
    ]
  }'''
}

CTA_OLD = '<h2 id="准备好开启专业财税法服务">准备好开启专业财税法服务？'
CTA_MAP = {
    '税务稽查应对实战手册(source).html': '<h2 id="被查了？立即获取专业支持">被查了？立即获取专业支持',
    '企业税务健康体检30项(source).html': '<h2 id="做好体检，防患于未然">做好体检，防患于未然',
    '私户收款被查补救指南(source).html': '<h2 id="私户收款？立即合规处理">私户收款？立即合规处理',
}

for filename, new_faq in FAQ_NEW.items():
    filepath = os.path.join(BASE, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Find FAQPage block: lines between "  {\n    \"@context\": ..." and "  }\n"
    # Start: line with '"@type": "FAQPage",'
    faq_start = None
    faq_end = None
    for i, line in enumerate(lines):
        if '"@type": "FAQPage",' in line:
            faq_start = i - 2  # Go back 2 lines to include "@context"
            break
    
    if faq_start is not None:
        # Walk forward to find the closing "  }" that ends this JSON object
        # We expect: lines[faq_start] = '  {\n', then content, then '  }\n'
        for j in range(faq_start + 1, min(faq_start + 60, len(lines))):
            if lines[j].strip() == '}' and j > faq_start + 10:
                faq_end = j + 1
                break
    
    if faq_start is not None and faq_end is not None:
        print(f'Replacing FAQPage lines {faq_start+1}-{faq_end} in {filename}')
        new_lines = lines[:faq_start] + [new_faq + '\n'] + lines[faq_end:]
        
        # Also replace CTA
        new_content = ''.join(new_lines).replace(CTA_OLD, CTA_MAP[filename])
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'  [OK]')
    else:
        print(f'  [FAIL] FAQPage block not found in {filename}')

# Verify
for filename in FAQ_NEW:
    filepath = os.path.join(BASE, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        c = f.read()
    q_count = c.count('"@type": "Question"')
    print(f'  {filename}: Questions = {q_count}')
