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
        'CRS全球税务透明时代，跨境资产如何合规申报',
        'CRS信息交换机制下，高净值人士海外账户的申报义务与合规策略'
    ),
    'IPO-shuiwu-hegui-jiagou.html': (
        'IPO前的税务合规必修课：股权架构与关联交易怎么整',
        '上市前必须解决的五大税务隐患，从股权梳理到历史问题清理'
    ),
    'ODI-jingwai-touzi-beian.html': (
        '企业出海第一关：ODI境外投资备案全解析',
        '发改委、商务部、外汇局三线审核要点与自贸区便利化通道'
    ),
    'dawanqu-geshui-butie.html': (
        '大湾区外籍与港澳人才个税补贴实操指南',
        '15%个税封顶的财政补贴怎么拿？申请条件、流程和续期详解'
    ),
    'fangdichan-qiye-shuiwu-chouhua.html': (
        '房地产企业全周期税务筹划：拿地到清盘的税负优化',
        '土增税清算、预售阶段预缴、完工年度汇算的系统性税负管理'
    ),
    'fapiao-hongchong-zuofei-diu-shi.html': (
        '发票红冲、作废与丢失的正确处理方式',
        '增值税专票红冲的最新规则、丢失发票的补救流程与税务影响'
    ),
    'gaoxin-qiye-shuiwu.html': (
        '高新技术企业税务筹划核心要点：认定、维护与加计扣除',
        '15%优惠税率不是一劳永逸——资质维护、研发费用归集与备查资料全攻略'
    ),
    'gaoxinjishu-qiye-shuiwu-guihua.html': (
        '高新技术企业如何从认定到享受税收优惠一条龙',
        '资质申请、台账管理、核查应对，让15%税率优惠稳稳落地'
    ),
    'geren-suodeshui-huisuan-qingjiao.html': (
        '个税汇算清缴必知要点：多退少补的正确姿势',
        '多处收入、专项附加扣除、年终奖计税选择——汇算清缴不踩坑'
    ),
    'geti-gongshanghu-gerenduquan-shuiwu.html': (
        '个体工商户与个人独资企业的税务管理实操',
        '从注册登记到注销清算，个体经营者的税种选择与申报要点'
    ),
    'gongsi-zhuxiao-qingsuan-shuiwu.html': (
        '公司注销清算的税务处理全流程',
        '注销前的所得税汇算、资产处置税费、剩余财产分配的税务要点'
    ),
    'gongzixinjin-gerensuodeshui-chouhua.html': (
        '工资薪金个税优化：薪酬结构怎么搭才省税',
        '年终奖、津贴补贴、福利费的个税处理差异与最优选择'
    ),
    'guanlianfang-jiekuan-shuiwu.html': (
        '关联方借款的税务风险：增值税、所得税怎么算',
        '企业向股东、关联公司借款的利息扣除限制与独立交易原则'
    ),
    'gudong-hongli-shuiwu-chouhua.html': (
        '股东从公司拿钱的最优税务路径：分红还是薪酬',
        '分红20%个税 vs 工资薪金累进税率，哪种方式更省税'
    ),
    'gudong-jiekuan-shuiwu-fengxian.html': (
        '股东借款不还的税务雷区：视同分红怎么避免',
        '年末未归还借款的个税风险、合规处理方案与替代路径'
    ),
    'guquan-daichi-shuiwu-fengxian.html': (
        '股权代持还原的税务处理：谁来交税、怎么交',
        '代持还原时的个人所得税与企业所得税处理及合规方案'
    ),
    'guquan-jiagou-quanjiexi.html': (
        '股权架构设计全解析：不同持股方式的税负比较',
        '自然人、公司、合伙企业三种持股主体的税负差异与架构选择'
    ),
    'guquan-jiagou-shuiwu-chouhua.html': (
        '股权架构的税务规划：从设立到退出的全周期考量',
        '不同持股方式的综合税负测算与架构优化，让股东税后收益最大化'
    ),
    'guquan-jili-shuiwu-chouhua.html': (
        '股权激励怎么省税：股票期权与限制性股票的个税差异',
        '授予、行权、转让三阶段的个税计算与递延纳税政策运用'
    ),
    'guquan-jili-shuiwu-guihua.html': (
        '股权激励全套税务规划：从授予到退出的合规安排',
        '上市公司与非上市公司的激励工具选择、纳税时点和税负比较'
    ),
    'guquan-zhuantang-geren-suodeshui.html': (
        '股权转让个税筹划：定价、申报与反避税应对',
        '自然人股权转让的价格确定、核定征收与平价转让的风险防控'
    ),
    'hainan-ziyougang-shuangshiwu.html': (
        '海南自贸港双15%税收优惠：企业该怎么用',
        '企业所得税和个税15%封顶的实际享受条件与实质性运营要求'
    ),
    'jianzi-chezi-shuiwu-chuli.html': (
        '企业减资撤资的税务处理全流程',
        '股东退出的多重路径选择及各环节的税务处理要点'
    ),
    'jiayi-shuangshijing.html': (
        '甲乙双视角看税务：为什么企业需要"自己人"的顾问',
        '甲方经验知道痛点在哪，乙方经验知道怎么解决——双视角的独特价值'
    ),
    'jingwai-suode-dijiang-zhinan.html': (
        '境外所得税收抵免怎么算：分国不分项还是综合抵免',
        '境外已纳税额在国内的抵扣规则、限额计算与最优选择'
    ),
    'jinshui-siqi-quanmian-jiedu.html': (
        '金税四期系统架构全解析：从发票到数据的监管升级',
        '金税四期的技术底层、数据来源和企业画像机制——为什么"以票控税"变成了"以数治税"'
    ),
    'jinshui-siqi-yingdui.html': (
        '金税四期下企业财税合规的生存法则',
        '解读金税四期核心变化，梳理企业必须调整的六大合规要点与应对方案'
    ),
    'kuajing-dianshang-shuiwu.html': (
        '跨境电商税务合规指南：出口退税、核定征收与转让定价',
        '亚马逊、TikTok Shop卖家必知的跨境税务风险与合规整改路径'
    ),
    'nashui-xinyong-dengji-xiufu.html': (
        '纳税信用等级怎么评、怎么修：A级到D级的差距有多大',
        '评分标准、扣分项、修复路径——信用等级对贷款、招投标的实质影响'
    ),
    'nianzhongjiang-jishui-xuanze.html': (
        '年终奖单独计税还是并入综合所得？一个公式帮你算',
        '不同收入水平下的最优选择策略，年终奖计税方式的实操测算'
    ),
    'odi-beian-quanliucheng.html': (
        'ODI境外投资备案全流程：从申请到落地的每一步',
        '发改委立项、商务部备案、外汇登记三线实操手册，附自贸区便利通道'
    ),
    'pingtai-jingji-linghuo-yonggong.html': (
        '平台经济灵活用工的税务合规：谁交税、怎么交',
        '平台从业者的收入性质认定、代扣代缴义务与灵活用工平台的选择要点'
    ),
    'qiye-kuisun-mibu-guize.html': (
        '企业亏损弥补的税务规则：年限、顺序与筹划空间',
        '五年or十年？亏损弥补的年限限制、先后顺序和税务筹划机会'
    ),
    'qiye-shuiwu-fengxian-guankong.html': (
        '企业税务风险怎么管：建立可落地的内控体系',
        '从被动应对到主动防控，搭建企业税务风险识别、评估、应对的管理闭环'
    ),
    'qiye-shuiwu-fengxian.html': (
        '企业税务风险管控全攻略：看得见才防得住',
        '覆盖风险识别、评估、应对全流程，帮助企业建立主动防御型税务管理体系'
    ),
    'qiye-zhongzu-shuiwu.html': (
        '企业重组税务规划：合并、分立、股权收购的税负优化',
        '特殊重组 vs 一般重组的税务处理差异，如何合法降低交易税负'
    ),
    'qiyesuodeshui-huisuan-qingjiao.html': (
        '企业所得税汇算清缴实操指南：申报表怎么填',
        '收入确认、成本扣除、纳税调整——汇算清缴的关键环节与常见错误'
    ),
    'qiyesuodeshui-yujiao-huisuan-chayi.html': (
        '企业所得税预缴与汇算的差异怎么处理',
        '季度预缴和年度汇算之间产生差异的原因及会计税务处理'
    ),
    'shebao-rushui-xinchou-guihua.html': (
        '社保入税后薪酬怎么规划：合规省钱两手抓',
        '社保缴费基数的确定规则、合规优化空间与常见踩坑点'
    ),
    'shudian-fapiao-quanmian-shishi.html': (
        '数电发票全面实施：企业要做哪些准备',
        '数电发票与传统发票的核心差异、系统对接要求与过渡期安排'
    ),
    'shuishou-xieding-daiyu.html': (
        '税收协定待遇怎么申请：跨境经营者的节税利器',
        '股息、利息、特许权使用费的协定优惠税率及"受益所有人"判定'
    ),
    'shuiwu-jicha-2026-yujing.html': (
        '2026年税务稽查重点预警：哪些行业和事项是高风险',
        '大数据选案逻辑解析，企业自查清单与稽查前的应对准备'
    ),
    'shuiwu-xingzheng-fuyi.html': (
        '对税务处理决定不服怎么办：行政复议实战指南',
        '复议申请的时限、材料准备、听证策略与诉讼衔接'
    ),
    'tudi-zengzhishui-qingsuan-chouhua.html': (
        '土地增值税清算：成本分摊与筹划空间',
        '土增税清算的核心难点——成本对象划分、分摊方法选择与税务筹划'
    ),
    'xin-gongsifa-shijiao-shuiwu.html': (
        '新公司法注册资本五年实缴的税务影响',
        '减资、知识产权出资、过桥资金的税务风险与合规路径'
    ),
    'xukai-fapiao-falv-houguo.html': (
        '虚开发票的法律红线：刑事责任与自救路径',
        '什么是虚开、量刑标准、善意取得的认定与补救措施'
    ),
    'yanfa-feiyong-jiakou-kouchu.html': (
        '研发费用加计扣除实操全解：从归集到申报',
        '哪些费用可以加计、人员工时如何记录、备查资料清单'
    ),
    'yecai-fasui-ronghe.html': (
        '业管财税法融合：五维一体如何帮企业降本增效',
        '打破财务、税务、法务的部门壁垒，从经营全局解决合规问题'
    ),
    'zengzhishuifa-shishi-yingdui.html': (
        '增值税法正式实施：哪些变化影响你的企业',
        '视同销售范围调整、混合销售规则变化、留抵退税制度化的应对'
    ),
    'zhongxiao-qiye-shuishou-youhui.html': (
        '中小企业税收优惠怎么用：优惠政策全盘点',
        '小微企业减免、六税两费减半、加计扣除等优惠政策的享受条件'
    ),
    'ziranren-guquan-zhuanrang-heding-chazhang.html': (
        '自然人股权转让被核定征收怎么办',
        '税务机关核定股权转让收入的触发条件、计算方法与争议解决'
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
