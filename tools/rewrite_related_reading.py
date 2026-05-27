#!/usr/bin/env python3
"""批量重写文章页「延伸阅读」卡片的标题和摘要为概括性文案"""

import os
import re
import sys

# Fix encoding for Windows console
sys.stdout.reconfigure(encoding='utf-8')

ARTICLES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'source', 'articles')

# 每个被引文章 href → (新标题, 新摘要)
REWRITE_MAP = {
    'CRS-kuajing-zichan-shenbao.html': (
        'CRS框架下跨境金融账户信息交换与申报义务',
        'CRS机制的运作原理、高净值个人海外金融账户的申报范围、信息交换流程及合规应对措施'
    ),
    'IPO-shuiwu-hegui-jiagou.html': (
        'IPO前企业税务合规要点：股权架构与关联交易',
        '上市审核中的税务关注重点、历史税务问题清理、股权架构调整的税务影响及关联交易合规处理'
    ),
    'ODI-jingwai-touzi-beian.html': (
        'ODI境外投资备案政策与操作流程',
        '发改委项目核准与备案、商务部境外投资备案、外汇管理局外汇登记的审核要点与办理流程'
    ),
    'dawanqu-geshui-butie.html': (
        '粤港澳大湾区外籍与港澳人才个人所得税财政补贴政策',
        '大湾区个税补贴的适用条件、补贴计算方式、申请材料与审批流程'
    ),
    'fangdichan-qiye-shuiwu-chouhua.html': (
        '房地产企业全周期税务管理要点',
        '房地产开发各阶段涉及的增值税、土地增值税、企业所得税处理要点与税负管理方法'
    ),
    'fapiao-hongchong-zuofei-diu-shi.html': (
        '增值税发票红冲、作废与丢失的税务处理',
        '发票红冲的适用情形与操作流程、发票作废的条件与限制、发票丢失的补救措施及税务影响'
    ),
    'gaoxin-qiye-shuiwu.html': (
        '高新技术企业税务管理要点：资质认定与研发费用加计扣除',
        '高新技术企业认定的税务条件、资格维护的合规要求、研发费用加计扣除的归集标准与核查应对'
    ),
    'gaoxinjishu-qiye-shuiwu-guihua.html': (
        '高新技术企业认定标准与税收优惠政策适用',
        '高新技术企业资质申请流程、15%优惠税率的适用条件、研发费用归集管理和税务核查应对要点'
    ),
    'geren-suodeshui-huisuan-qingjiao.html': (
        '个人所得税综合所得汇算清缴政策与操作要点',
        '汇算清缴的适用人群、专项附加扣除填报、多处收入合并计税规则和年终奖计税方式选择'
    ),
    'geti-gongshanghu-gerenduquan-shuiwu.html': (
        '个体工商户与个人独资企业税务处理要点',
        '个体工商户与个人独资企业的税种适用、核定征收与查账征收差异、申报纳税流程'
    ),
    'gongsi-zhuxiao-qingsuan-shuiwu.html': (
        '公司注销与清算的税务处理要点',
        '注销前的企业所得税汇算清缴、清算所得的计算与申报、资产处置的税费处理及剩余财产分配'
    ),
    'gongzixinjin-gerensuodeshui-chouhua.html': (
        '工资薪金个人所得税计算与薪酬结构安排',
        '工资、薪金所得的个税计算规则、年终奖与各类津贴补贴的税务处理差异及薪酬结构的合规安排'
    ),
    'guanlianfang-jiekuan-shuiwu.html': (
        '关联方借款的税务处理与风险防范',
        '关联方资金借贷的增值税纳税义务、企业所得税利息扣除限制及独立交易原则的适用'
    ),
    'gudong-hongli-shuiwu-chouhua.html': (
        '股东取得公司利润的税务处理：股息红利与工资薪金的税负比较',
        '股东取得公司利润的不同方式及其税务处理、股息红利个人所得税与企业所得税的衔接、工资薪金与分红的税负对比'
    ),
    'gudong-jiekuan-shuiwu-fengxian.html': (
        '股东向公司借款的税务处理与视同分红风险',
        '股东借款视同分红的适用条件、年末未归还借款的个税处理及合规路径'
    ),
    'guquan-daichi-shuiwu-fengxian.html': (
        '股权代持还原的税务处理与合规要点',
        '代持关系解除时的个人所得税和企业所得税纳税义务、代持人与实际股东的税务责任划分及合规方案'
    ),
    'guquan-jiagou-quanjiexi.html': (
        '股权架构设计的税务考量：不同持股方式的税负比较',
        '自然人直接持股、公司持股、合伙企业持股三种方式的所得税税负差异、适用场景与架构选择'
    ),
    'guquan-jiagou-shuiwu-chouhua.html': (
        '股权架构税务规划：从设立到退出的税务考量',
        '企业设立阶段的股权架构选择、运营期间的分红税务处理和退出阶段的股权转让税负分析'
    ),
    'guquan-jili-shuiwu-chouhua.html': (
        '股权激励的个人所得税处理：股票期权与限制性股票',
        '股权激励授予、行权、转让三阶段的个人所得税计算规则及递延纳税政策的适用条件'
    ),
    'guquan-jili-shuiwu-guihua.html': (
        '股权激励的税务处理与规划：上市公司与非上市公司的比较',
        '上市公司与非上市公司股权激励的税务处理差异、不同激励工具的个税计算方式及纳税时点选择'
    ),
    'guquan-zhuantang-geren-suodeshui.html': (
        '自然人股权转让个人所得税计算与申报',
        '股权转让收入的确定方法、平价转让的税务风险、核定征收的触发条件及反避税规则'
    ),
    'hainan-ziyougang-shuangshiwu.html': (
        '海南自由贸易港双15%税收优惠政策解析',
        '海南自贸港15%企业所得税优惠税率和15%个人所得税优惠的适用条件、实质性运营要求及申请流程'
    ),
    'jianzi-chezi-shuiwu-chuli.html': (
        '企业减资与撤资的税务处理要点',
        '股东减资退出的不同路径、减资所得的企业所得税处理、个人股东的个税计算及申报要求'
    ),
    'jiayi-shuangshijing.html': (
        '业管财税法融合：甲乙双方视角下的税务顾问价值',
        '甲方财税管理经验和乙方专业服务的互补优势，以及业管财税法融合对企业税务管理的意义'
    ),
    'jingwai-suode-dijiang-zhinan.html': (
        '境外所得税收抵免的计算方法与政策选择',
        '分国不分项抵免与综合抵免的计算方式、抵免限额的确定、境外已纳税额的超额结转规则'
    ),
    'jinshui-siqi-quanmian-jiedu.html': (
        '金税四期系统架构与数据驱动的税收监管模式',
        '金税四期的技术架构、数据采集来源、企业画像机制及"以数治税"对税收征管模式的变革'
    ),
    'jinshui-siqi-yingdui.html': (
        '金税四期下企业财税合规要点与应对措施',
        '金税四期对企业的核心影响、税务风险高发领域及企业合规管理的重点调整方向'
    ),
    'kuajing-dianshang-shuiwu.html': (
        '跨境电商的增值税出口退税与所得税处理要点',
        '跨境电商出口退税的条件与流程、核定征收企业所得税的适用规则及跨境转让定价的税务合规要求'
    ),
    'nashui-xinyong-dengji-xiufu.html': (
        '纳税信用等级评定标准与修复机制',
        '纳税信用评级的指标体系、各级别对应的激励与惩戒措施、信用修复的申请条件与流程'
    ),
    'nianzhongjiang-jishui-xuanze.html': (
        '全年一次性奖金的个人所得税计税方式选择',
        '年终奖单独计税与并入综合所得的计税规则、不同收入水平下的税负比较与选择策略'
    ),
    'odi-beian-quanliucheng.html': (
        'ODI境外投资备案的办理流程与审核要点',
        '发改委项目核准/备案、商务部境外投资证书、外汇登记三个环节的申请材料、审核标准与办理时限'
    ),
    'pingtai-jingji-linghuo-yonggong.html': (
        '平台经济灵活用工的税务处理与合规要点',
        '平台从业者收入的所得性质认定、平台企业的代扣代缴义务及灵活用工的增值税与个人所得税处理'
    ),
    'qiye-kuisun-mibu-guize.html': (
        '企业所得税亏损弥补的年限与规则',
        '亏损结转弥补的年限规定、亏损弥补的先后顺序、合并与分立中的亏损承继规则'
    ),
    'qiye-shuiwu-fengxian-guankong.html': (
        '企业税务风险管理：内控制度建设与执行',
        '企业税务风险的识别方法、风险评估机制、内部控制制度建设及税务管理流程的落地执行'
    ),
    'qiye-shuiwu-fengxian.html': (
        '企业税务风险识别、评估与应对体系',
        '企业税务风险的分类与识别方法、风险评估标准、风险应对策略及税务管理体系的搭建'
    ),
    'qiye-zhongzu-shuiwu.html': (
        '企业重组的税务处理：合并、分立与股权收购',
        '企业重组中特殊性税务处理与一般性税务处理的适用条件、各重组形式的税负比较与选择'
    ),
    'qiyesuodeshui-huisuan-qingjiao.html': (
        '企业所得税年度汇算清缴的申报要点',
        '年度汇算清缴的收入确认、成本费用扣除、纳税调整项目填报及常见申报错误的防范'
    ),
    'qiyesuodeshui-yujiao-huisuan-chayi.html': (
        '企业所得税预缴与年度汇算的差异分析与处理',
        '季度预缴与年度汇算产生差异的原因、会计处理方法及少缴税款的补税与滞纳金规则'
    ),
    'shebao-rushui-xinchou-guihua.html': (
        '社保征收体制改革对企业薪酬管理的影响',
        '社保缴费基数的核定规则、税务征收后的合规要求及企业薪酬结构的调整方向'
    ),
    'shudian-fapiao-quanmian-shishi.html': (
        '全面数字化电子发票的实施与企业应对',
        '数电发票与传统发票的差异、企业开票与受票系统的改造要求、过渡期注意事项'
    ),
    'shuishou-xieding-daiyu.html': (
        '税收协定待遇的申请条件与适用流程',
        '股息、利息、特许权使用费等跨境所得的协定优惠税率、"受益所有人"判定标准及申请流程'
    ),
    'shuiwu-jicha-2026-yujing.html': (
        '2026年税务稽查方向与高风险领域分析',
        '税务稽查的大数据选案机制、重点行业与事项的稽查关注点及企业自查清单'
    ),
    'shuiwu-xingzheng-fuyi.html': (
        '税务行政复议的程序与应对策略',
        '税务行政复议的申请条件与时限、证据材料准备、听证程序及行政复议与行政诉讼的衔接'
    ),
    'tudi-zengzhishui-qingsuan-chouhua.html': (
        '土地增值税清算中的成本分摊与税务处理',
        '土地增值税清算的触发条件、成本对象的划分标准、不同分摊方法的选择与税负影响'
    ),
    'xin-gongsifa-shijiao-shuiwu.html': (
        '新公司法注册资本制度改革对企业税务的影响',
        '注册资本五年实缴要求下的减资税务处理、知识产权出资的税务影响及过桥资金的税务风险'
    ),
    'xukai-fapiao-falv-houguo.html': (
        '虚开增值税发票的法律责任与风险防范',
        '虚开发票的认定标准、行政责任与刑事责任、善意取得虚开发票的认定条件及补救措施'
    ),
    'yanfa-feiyong-jiakou-kouchu.html': (
        '研发费用加计扣除的归集标准与申报要点',
        '可加计扣除的研发费用范围、费用归集与辅助账管理、备查资料清单及常见税务核查关注点'
    ),
    'yecai-fasui-ronghe.html': (
        '业务、管理、财务、税务、法务融合的实践路径',
        '业管财税法融合的理念、五维联动的实施方法及对企业合规管理和经营决策的实际价值'
    ),
    'zengzhishuifa-shishi-yingdui.html': (
        '《增值税法》正式实施后的政策变化与企业应对',
        '视同销售范围调整、混合销售规则变化、留抵退税制度化等增值税法核心修订内容及企业应对措施'
    ),
    'zhongxiao-qiye-shuishou-youhui.html': (
        '中小企业适用的税收优惠政策汇总',
        '小型微利企业所得税减免、六税两费减半征收、研发费用加计扣除等优惠政策的适用条件与享受方式'
    ),
    'ziranren-guquan-zhuanrang-heding-chazhang.html': (
        '自然人股权转让核定征收的触发条件与争议处理',
        '税务机关核定股权转让收入的法定情形、核定方法、纳税人的救济途径及争议解决方式'
    ),
}


def rewrite_file(filepath, changes):
    """Rewrite a single file's related-reading titles and summaries"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    modified = False
    for href, (new_title, new_summary) in REWRITE_MAP.items():
        # Match the related-card for this href and replace h4 and p
        # Pattern: the entire related-card block for this specific href
        pattern = re.compile(
            r'(<a href="' + re.escape(href) + r'" class="related-card">\s*'
            r'<span class="related-cat">[^<]*</span>\s*'
            r'<div class="related-info">\s*'
            r')<h4>[^<]*</h4>(\s*)<p>[^<]*</p>',
            re.DOTALL
        )
        
        replacement = r'\1<h4>' + new_title + r'</h4>\2<p>' + new_summary + r'</p>'
        new_content = pattern.sub(replacement, content)
        
        if new_content != content:
            modified = True
            href_short = href.split('.')[0]
            changes.append(f'  [OK] {href_short} -> "{new_title[:40]}..."')
        
        content = new_content

    if modified:
        with open(filepath, 'r', encoding='utf-8') as f:
            original = f.read()
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
    return False


def main():
    files = sorted([f for f in os.listdir(ARTICLES_DIR) if f.endswith('.html')])
    
    total_modified = 0
    total_changes = 0
    
    for fname in files:
        fpath = os.path.join(ARTICLES_DIR, fname)
        changes = []
        if rewrite_file(fpath, changes):
            total_modified += 1
            total_changes += len(changes)
            print(f'{fname}:')
            for c in changes:
                print(c)
            print()
    
    print(f'总计: 修改了 {total_modified} 个文件, {total_changes} 处替换')


if __name__ == '__main__':
    main()
