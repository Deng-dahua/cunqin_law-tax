"""批量扩展20篇新文章的 og:description 到 120-160 字符 + 嵌入地域关键词"""
import re, os

base = r'C:\Users\26726\WorkBuddy\2026-05-20-21-20-24\source\articles'

# 每篇文章的完整 og:description (120-160字符)，嵌入地域关键词
descs = {
    'chengben-feiyong-shuiwu-hegui(source).html':
        '成本费用税前扣除是企业所得税管理的核心环节。本文系统解析四大扣除要件、各费用项目扣除标准及金税四期下的风险新特征，为广州及粤港澳大湾区企业提供合规管理实操指引。',
    'chukou-tuishui-hegui-fengkong(source).html':
        '出口退税合规风控全解析：从基本原理到申报实务，深度剖析高风险行为识别与防控策略，解读金税四期下出口退税全链条监控机制，面向华南地区外贸企业提供专业指引。',
    'CRS-kuajing-zichan-shenbao(source).html':
        'CRS共同申报准则对跨境资产配置影响深远。本文系统讲解CRS运作机制、中国实施要点、高净值人士申报义务及合规规划路径，为大湾区跨境企业与个人提供专业分析。',
    'geren-suodeshui-huisuan-qingjiao(source).html':
        '个人所得税汇算清缴实操指南：覆盖综合所得预扣预缴、专项附加扣除最新政策、境外所得抵免及补退税流程解析，为广东地区纳税人提供全面、准确的申报指导。',
    'gongzixinjin-gerensuodeshui-chouhua(source).html':
        '工资薪金个人所得税筹划深度解析：对比全年一次性奖金单独计税与并入综合所得的税负差异，剖析大湾区人才政策下的个税优惠空间及合规筹划策略。',
    'gudong-hongli-shuiwu-chouhua(source).html':
        '股东分红与薪酬的税负优化策略全解析：对比两种方式的综合税负差异，深度剖析合法合规的利润分配路径及股东借款、费用报销的合规边界，为华南地区民营企业主提供实操指引。',
    'guquan-daichi-shuiwu-fengxian(source).html':
        '股权代持在实务中极为普遍但税务风险不容忽视。本文系统解析显名与隐名股东的税务处理规则、代持还原的税务成本及增值税风险，为大湾区企业提供股权架构合规方案。',
    'guquan-zhuantang-geren-suodeshui(source).html':
        '自然人股权转让涉及复杂的个人所得税处理。本文全面解析转让收入核定、原值确认、纳税时点及地点规则，并结合金税四期大数据监控特点，为广州地区投资者提供税务合规指引。',
    'hehuo-qiye-shuiwu-jiexi(source).html':
        '合伙企业"先分后税"的税务处理一直是实务难点。本文从合伙人层面深度解析所得性质穿透、费用扣除与亏损弥补规则，帮助华南地区合伙制企业理清税务合规思路。',
    'IPO-shuiwu-hegui-jiagou(source).html':
        'IPO过程中税务合规是审核红线之一。本文系统梳理上市前税务健康体检要点、历史遗留问题清理路径、股权架构重组涉税处理，为粤港澳大湾区拟上市企业提供全流程税务规划框架。',
    'qiye-kuisun-mibu-guize(source).html':
        '企业亏损弥补规则看似简单，实操中却暗藏诸多陷阱。本文全面解读五年结转、高新技术企业延长至十年等特殊规则，为广州地区企业财税人员提供精准的税务处理指引。',
    'qiyesuodeshui-huisuan-qingjiao(source).html':
        '企业所得税汇算清缴是企业年度财税工作的重中之重。本文系统梳理收入确认、税前扣除、资产损失及优惠备案等关键环节的处理要点，为华南地区企业顺利完成汇算清缴提供全程指导。',
    'shuiwu-xingzheng-fuyi(source).html':
        '企业对税务机关处理决定不服时，税务行政复议是重要救济渠道。本文详解复议申请条件、期限、审理程序及常见争议焦点，为广州及大湾区企业维护合法权益提供实务操作指南。',
    'shuzihua-shuiwu-guanli-zhuanxing(source).html':
        '数字经济背景下企业税务管理面临深刻变革。本文系统分析电子发票、大数据风控、智能申报等趋势对企业税务的影响，为华南地区企业规划数字化转型路径提供策略建议。',
    'simu-jijin-shuiwu-chouhua(source).html':
        '私募基金"募投管退"全周期涉及复杂的税务处理。本文从基金架构选择、LP与GP税务筹划、投资收益确认及退出环节税负优化等维度，为大湾区私募机构提供专业税务规划。',
    'xukai-fapiao-falv-houguo(source).html':
        '虚开增值税专用发票是涉税刑事风险的重灾区。本文全面解析虚开的认定标准、行政与刑事法律后果、善意取得虚开发票的处理及企业防范策略，为广东地区企业敲响合规警钟。',
    'yanfa-feiyong-jiakou-kouchu(source).html':
        '研发费用加计扣除是力度最大的企业所得税优惠之一。本文深度解析适用条件、归集口径、辅助账管理及留存备查要求，为粤港澳大湾区科技创新企业充分享受政策红利提供权威指引。',
    'yinhua-shuifa-shishi-yaodian(source).html':
        '新印花税法已于2022年7月1日正式实施。本文逐条解读新法核心变化：税目简并、计税依据明确化、申报期限调整等，帮助广州地区企业全面掌握合规要点，规避申报风险。',
    'zengzhishui-liudi-tuishui(source).html':
        '增值税留抵退税是当前减税降费的重要举措。本文系统梳理增量留抵退税与存量留抵退税的适用条件、计算方法和申请流程，帮助大湾区企业用好用足退税红利，缓解资金压力。',
    'zhongxiao-qiye-shuishou-youhui(source).html':
        '中小企业税收优惠政策体系庞杂、更新频繁。本文全面整理小微企业所得税减免、增值税小规模纳税人优惠及六税两费减半等核心政策，为广东地区中小企业提供系统化的税务优惠指南。',
}

count = 0
for fname, new_desc in descs.items():
    fp = os.path.join(base, fname)
    if not os.path.exists(fp):
        print(f'  ✗ NOT FOUND: {fname}')
        continue
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 替换 og:description (匹配 content="...")
    old = re.search(r'<meta property="og:description" content="[^"]*"', content)
    if not old:
        print(f'  ✗ No og:description: {fname}')
        continue
    
    # 同时替换 twitter:description (取前半段)
    twitter_desc = new_desc[:100] + ('…' if len(new_desc) > 100 else '')
    
    # 替换 meta description
    content = re.sub(
        r'<meta name="description" content="[^"]*"',
        f'<meta name="description" content="{new_desc}"',
        content
    )
    
    # 替换 og:description
    content = re.sub(
        r'<meta property="og:description" content="[^"]*"',
        f'<meta property="og:description" content="{new_desc}"',
        content
    )
    
    # 替换 twitter:description
    content = re.sub(
        r'<meta name="twitter:description" content="[^"]*"',
        f'<meta name="twitter:description" content="{twitter_desc}"',
        content
    )
    
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(content)
    count += 1
    print(f'  ✓ {fname} ({len(new_desc)} chars)')

print(f'\nDone: {count} files updated')
