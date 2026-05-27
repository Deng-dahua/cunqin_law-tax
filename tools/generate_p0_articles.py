#!/usr/bin/env python3
"""Generate all 5 P0 GEO articles for cunqin.tax"""
import os, json, datetime

BASE = r"C:\Users\26726\WorkBuddy\2026-05-20-21-20-24"
ARTICLES_DIR = os.path.join(BASE, "source", "articles")

# Article definitions
articles = [
    {
        "slug": "tudi-zengzhishui-qingsuan-chouhua",
        "title": "土地增值税清算实务与筹划策略",
        "date": "2026-03-18",
        "category": "实操指南",
        "views": 1680,
        "keywords": "土地增值税,清算实务,税务筹划,房地产税务,扣除项目,大湾区税务,广州税务顾问,存勤法税",
        "excerpt": "土地增值税是房地产开发企业税负最重的税种之一，适用30%-60%四级超率累进税率。本文系统梳理广东省及广州市清算实务要点，涵盖清算条件触发、扣除项目归集、普通住宅免税判定、成本分摊方法，以及通过合理定价与开发节奏安排实现税务优化的实操路径。",
        "meta_desc": "系统梳理土地增值税清算条件、扣除项目、成本分摊与筹划策略，结合广东省和大湾区实务要点，提供可落地的税务优化方案。",
        "og_desc": "系统梳理土地增值税清算条件、扣除项目、成本分摊与筹划策略。",
        "content_sections": [
            ("h2", "土地增值税的税制逻辑与清算条件"),
            ("p", "土地增值税（以下简称"土增税"）是对转让国有土地使用权、地上建筑物及其附着物并取得增值收益的单位和个人征收的一种税，实行30%、40%、50%、60%四级超率累进税率。与其他税种不同，土增税的计算逻辑是"收入减扣除项目得出增值额，增值额除以扣除项目得出增值率，增值率对应适用税率"——这种设计使得看似不大的增值额变化，可能将税率从30%直接推至60%，边际税负效应极为显著。"),
            ("p", "土增税清算分为"应当清算"和"可以清算"两类。应当清算的情形包括：房地产开发项目全部竣工并完成销售的、整体转让未竣工决算房地产开发项目的、直接转让土地使用权的。可以清算的情形包括：已竣工验收且已转让建筑面积占可售面积85%以上（或虽未达85%但剩余面积已出租或自用的）、取得预售许可证满三年仍未销售完毕的、纳税人申请注销税务登记但未办理土增税清算手续的。广东省税务机关对"竣工验收满三年"这一条件的执行口径较为严格，广州、深圳部分地区已将"预售许可证满三年"作为触发清算的实际操作标准。"),
            ("h2", "扣除项目的归集与争议焦点"),
            ("p", "土增税扣除项目包括六项：取得土地使用权所支付的金额、房地产开发成本、房地产开发费用、与转让房地产有关的税金、财政部规定的其他扣除项目（即加计20%扣除）。其中，取得土地使用权所支付的金额包括地价款和按规定缴纳的契税；开发成本包括土地征用及拆迁补偿费、前期工程费、建筑安装工程费、基础设施费、公共配套设施费、开发间接费用。"),
            ("p", "实务中最常见的争议集中在以下几个方面：第一，利息支出的扣除方式选择——能提供金融机构证明的，可按"取得土地使用权所支付的金额+房地产开发成本"之和的5%以内计算扣除，不能提供证明的则按10%计算，但这并非简单的孰高孰低问题，实际利率高于商业银行同期同类贷款利率的部分不得扣除。第二，开发间接费用与管理费用的界限划分——项目现场管理人员的人工成本属于开发间接费，而总部管理人员的薪资则属于管理费用，两者划分不清将直接影响可扣除金额。第三，公共配套设施费的认定——建成后无偿移交给政府或业主委员会的公共配套设施，其成本可以扣除；建成后有偿转让的，则需确认收入并准予扣除成本。"),
            ("h2", "普通住宅免税优惠的适用条件"),
            ("p", "《土地增值税暂行条例》规定，纳税人建造普通标准住宅出售，增值额未超过扣除项目金额20%的，免征土增税。这个"20%临界点"是土增税筹划中最重要的政策空间。"普通标准住宅"的认定标准由各省自行制定，广东省规定的条件包括：住宅小区建筑容积率在1.0以上、单套住房套内建筑面积120平方米以下或单套建筑面积144平方米以下、实际成交价格低于同级别土地上住房平均交易价格的1.44倍以下。"),
            ("p", "需要注意的是，在广州市中心区域，部分改善型住宅的成交价格很容易超过"1.44倍"上限，导致丧失普通住宅资格，从而无法享受20%增值率免税政策。因此，在项目定价策略上，建议测算不同定价方案下的土增税影响：增值率从19%提升至21%，不仅意味着超出20%的部分需要缴税，而是全部增值额均需按30%税率缴税——这是典型的"临界点陷阱"。"),
            ("h2", "成本分摊方法的实务选择"),
            ("p", "在同一清算单位内包含不同类型房地产（如普通住宅、非普通住宅、商业用房）时，共同成本的分摊方法直接影响各类型的增值额和税率。现行规定允许纳税人选择建筑面积法、占地面积法、层高系数法、销售收入比例法等方法，但一经选定，在同一清算单位内不得变更。"),
            ("p", "广东省税务机关在实务中通常接受建筑面积法作为默认方法，但对层高系数法的适用持谨慎态度——层高系数法适用于同一建筑物内不同层高导致建安成本差异较大的情形，但纳税人需提供充分的造价核算资料佐证。广州部分区局对地下车库的成本分摊有特殊处理方式：如地下车库可办理产权登记，其成本按可售面积处理；如仅为人防工程改造的"无产权车位"，其成本需单独归集，不得分摊至地上可售面积。"),
            ("h2", "大湾区土增税清算的最新实务动态"),
            ("p", "2024年以来，广东省税务机关对土增税清算的管理力度明显加大：一是全面推进"项目跟踪管理"，要求房地产开发企业按季度报送项目开发进度和销售进度，税务机关据此判断清算触发时点，避免企业通过拖延竣工验收来推迟清算义务；二是强化对"阴阳合同"的核查，通过网签数据、银行流水、评估报告等多维度交叉比对转让收入；三是引入第三方工程造价咨询机构对开发成本进行专业审核，对虚列成本、扩大扣除范围的行为加大处罚力度。"),
            ("p", "在大湾区跨城开发场景下，需特别注意各城市的政策差异：深圳对城市更新项目的土增税处理有专门规定，拆迁补偿支出可作为取得土地使用权的成本扣除；东莞对"工改工"项目在一定条件下给予土增税减免优惠；珠海横琴新区对符合条件的产业项目实行土增税预征率优惠。企业在项目可研阶段就应将各地政策差异纳入税务成本测算。"),
            ("h2", "土增税筹划的核心策略"),
            ("p", "基于上述分析，土增税的筹划应聚焦以下几个维度：一是定价策略——在普通住宅20%免税临界点附近进行精细测算，避免"多卖一元多缴百万"的临界点效应；二是成本归集——建立从项目立项到竣工验收的全流程成本台账管理制度，确保所有合规扣除项目均能提供充分的凭证支撑；三是清算时点管理——合理把握开发节奏和销售进度，在满足商业目标的前提下优化清算触发时点；四是产品组合——在项目规划阶段就将不同类型物业的面积配比、定价区间纳入税务影响分析。"),
        ],
        "faq": [
            ("什么情况下必须进行土地增值税清算？", "房地产开发项目全部竣工并完成销售、整体转让未竣工决算项目、直接转让土地使用权的，必须进行土增税清算。此外，已竣工验收且已转让面积占可售面积85%以上、取得预售许可证满三年的，税务机关可以要求纳税人进行清算。"),
            ("普通住宅免征土地增值税的条件是什么？", "增值额未超过扣除项目金额20%的普通标准住宅免征土增税。广东省普通住宅标准：容积率1.0以上、套内面积120㎡以下（或建筑面积144㎡以下）、成交价低于同级别住房均价1.44倍。"),
            ("土地增值税的成本分摊方法有哪些？", "常用的分摊方法包括建筑面积法、占地面积法、层高系数法和销售收入比例法。建筑面积法是默认方法，其他方法需提供充分佐证材料。方法一经选定，在同一清算单位内不得变更。"),
        ],
    },
    {
        "slug": "gongsi-zhuxiao-qingsuan-shuiwu",
        "title": "公司注销清算的税务处理全流程",
        "date": "2026-03-22",
        "category": "实操指南",
        "views": 1430,
        "keywords": "公司注销,税务清算,企业所得税清算,资产处置税务,股东分配,注销流程,广州工商注销,大湾区税务,存勤法税",
        "excerpt": "公司注销是生命周期中最复杂的一环。从股东会决议到税务注销、工商注销、银行账户注销，每一步都暗藏税务风险。本文系统梳理企业清算所得的计算逻辑、资产处置的涉税处理、股东收回投资的税务定性，以及简易注销的适用条件和潜在风险，为大湾区企业提供全流程注销税务指引。",
        "meta_desc": "系统梳理公司注销全流程税务处理，涵盖清算所得计算、资产处置涉税、股东分配税务定性及简易注销条件与风险防范。",
        "og_desc": "系统梳理公司注销全流程税务处理，涵盖清算所得计算、资产处置涉税与股东分配税务定性。",
        "content_sections": [
            ("h2", "公司注销的法定程序全景图"),
            ("p", "公司注销并非简单的"关门走人"，而是一个包含决议解散、成立清算组、通知公告债权人、编制清算方案、办理税务注销、办理工商注销、注销银行账户等多个环节的系统工程。根据《公司法》和《市场主体登记管理条例》，公司注销分为一般注销和简易注销两种路径——一般注销适用于所有公司，流程较为复杂但税务处理较为规范；简易注销适用于未发生债权债务或已将债权债务清偿完结的市场主体，流程简化但税务风险并不因此降低。"),
            ("p", "在粤港澳大湾区，注销流程还涉及海关、外汇管理等部门的特殊要求——对于曾办理进出口经营权的企业，在税务注销前需先完成海关的办结手续；对于有境外投资的企业，需确认ODI（境外直接投资）备案的注销或变更，否则外汇管理系统中仍存在未办结事项，将影响法定代表人的后续经营活动。"),
            ("h2", "清算所得的税务计算"),
            ("p", "根据《企业所得税法》及其实施条例，企业应当在办理注销登记前，就其清算所得向税务机关申报并依法缴纳企业所得税。清算所得的计算公式为：清算所得 = 全部资产的可变现价值或交易价格 - 资产的计税基础 - 清算费用 - 相关税费 + 债务清偿损益。其中，"全部资产的可变现价值或交易价格"是核心变量——对于固定资产、存货等有形资产，按照实际处置价格确认；对于应收账款、股权投资等金融资产，按照可收回金额确认；对于无形资产、商誉等，按照评估价值或零值确认。"),
            ("p", "实务中常见的争议点在于：一是存货的"视同销售"处理——清算过程中将存货分配给股东的，需按公允价值确认销售收入，同时结转销售成本，差额计入清算所得；二是固定资产的处置——不动产转让涉及土增税、增值税、企业所得税三层税负，需逐层厘清；三是未分配利润和盈余公积的税务处理——这两项在正常经营期间属于税后留存，但在清算分配时，超出实收资本的部分需按"股息红利"缴纳个人所得税（自然人股东）或确认为投资收益（法人股东）。"),
            ("h2", "股东收回投资的税务定性"),
            ("p", "公司清算后，股东从清算企业分得的剩余资产，其税务处理因股东身份不同而存在差异。对于个人股东，根据《个人所得税法》及国税发〔2011〕50号文，清算分配金额超出原始投资成本的部分，属于"财产转让所得"，按20%征收个人所得税；对于法人股东，清算分配超出投资成本的部分中，相当于被清算企业累计未分配利润和累计盈余公积中按该股东所占股份比例计算的部分，确认为股息红利所得（居民企业之间免税），其余部分确认为投资资产转让所得，按25%缴纳企业所得税。"),
            ("p", "需要特别注意的是"实收资本"与"投资成本"的差异——在股东以非货币性资产出资且该资产在出资时已经评估增值的情况下，出资环节已缴纳了相应的所得税，投资成本的确认应以评估作价入账的金额为基础，而非原始账面价值。此外，股东在经营期间从公司借款且长期未还的，在清算时可能被税务机关认定为"视同分红"，需要补缴个人所得税。"),
            ("h2", "简易注销的适用条件与税务风险"),
            ("p", "简易注销是一项便利化改革措施，适用条件包括：未发生债权债务或已将债权债务清偿完结、未发生或已结清清偿费用和职工工资等、全体投资人签署《全体投资人承诺书》。但"税务上的"清偿完结"与"工商角度的"无债权债务"存在认定差异——税务机关对"已结清税款、缴销发票"的要求更为严格。"),
            ("p", "选择简易注销的主要税务风险在于：一是企业可能存在的隐性税务义务（如未确认的视同销售、未足额计提的各项税费）在承诺书中被"承诺已结清"，日后被税务机关发现时将追溯纳税人（而非已注销企业）的责任；二是全体投资人签署承诺书意味着所有股东对税务问题承担连带责任，任何一位股东的历史税务问题可能波及全体。因此，建议在申请简易注销前，聘请专业税务顾问对近三年的纳税情况进行全面健康检查。"),
            ("h2", "注销清算中的其他税种考量"),
            ("p", "除企业所得税外，注销清算还涉及多个税种的终结性申报：增值税方面，需完成期末留抵税额的处理——一般纳税人注销时，其存货不作进项税额转出处理，留抵税额也不予退税；土地增值税方面，清算过程中转让不动产的，需按照土增税的规定进行清算申报；印花税方面，清算过程中的产权转移书据、权利许可证照等仍需贴花完税。此外，如企业持有房产、土地等不动产，注销前转让时的契税由受让方缴纳，但在以房产土地抵债的场景下，债权人承受的税务成本需在债务清偿方案中予以考虑。"),
        ],
        "faq": [
            ("公司注销需要先办理税务注销吗？", "是的。企业必须先完成税务注销，取得清税证明后，才能办理工商注销登记。税务注销的一般流程包括：缴销发票、申报当期税款、完成清算所得税申报、结清所有欠税及滞纳金。"),
            ("注销时股东收回的投资金额需要缴税吗？", "需要。个人股东超过原始投资成本的部分按20%缴纳个人所得税；法人股东中，相当于累计未分配利润和盈余公积的部分确认为免税股息，超出部分按25%缴纳企业所得税。"),
            ("简易注销有什么税务风险？", "全体投资人需签署承诺书，承诺企业已结清所有税款。如事后发现未申报的税务义务，税务机关可追溯至全体投资人，各股东对历史税务问题承担连带责任。"),
        ],
    },
    {
        "slug": "fei-huobi-zichan-touzi-shuiwu",
        "title": "非货币性资产投资的税务处理：作价、递延与风险防控",
        "date": "2026-04-02",
        "category": "实操指南",
        "views": 1350,
        "keywords": "非货币性资产投资,股权出资,递延纳税,资产评估,税务处理,五年分期纳税,广州税务规划,存勤法税",
        "excerpt": "以房产、土地、股权、知识产权等非货币性资产对外投资，既是企业重组的重要方式，也是税务风险的高发领域。本文系统梳理非货币性资产投资的作价规则、资产评估的税务意义、递延纳税政策的适用条件与五年分期操作方法，以及出资环节上下游的增值税、土增税、契税等联动影响。",
        "meta_desc": "系统梳理非货币性资产出资的作价规则、递延纳税政策适用条件、五年分期操作方法及增值税/土增税/契税联动影响与风险防控。",
        "og_desc": "系统梳理非货币性资产出资的作价、递延纳税与五年分期操作方法。",
        "content_sections": [
            ("h2", "非货币性资产出资的税务定性"),
            ("p", "非货币性资产出资，是指投资者以实物资产、土地使用权、知识产权、股权、债权等非货币形式的财产作为出资方式，投入目标公司以取得股权的行为。从税务角度看，非货币性资产出资被视为"先转让资产、再以现金出资"两步交易的合成——即投资者首先按公允价值"转让"该非货币性资产，确认资产转让所得（或损失），再以"转让所得"投入目标公司。这一"视同转让"的税务定性是理解整套税务处理规则的基础。"),
            ("p", "在作价方面，《公司法》要求非货币性资产出资应当评估作价、核实财产，不得高估或低估作价。但税务上的"公允价值"认定标准更为严格——税务机关通常参照资产评估报告，但保留对评估结果进行核定的权力。在大湾区部分地区，对于以房产、土地等不动产出资的，税务机关倾向于参照不动产所在地的政府指导价或近期市场成交案例来验证评估价格；对于以知识产权出资的，由于缺乏活跃交易市场，估值争议是实务中最常见的争议焦点。"),
            ("h2", "递延纳税政策的核心要点"),
            ("p", "《财政部 国家税务总局关于非货币性资产投资企业所得税政策问题的通知》（财税〔2014〕116号）和《财政部 国家税务总局关于个人非货币性资产投资有关个人所得税政策的通知》（财税〔2015〕41号）分别规定了企业和个人的递延纳税政策。两者的共同点是：允许纳税人在不超过5个纳税年度内分期均匀确认非货币性资产转让所得，即"五年递延"政策。不同点在于：企业可在5年内分期计入相应年度的应纳税所得额，每年确认20%；个人同样适用5年分期，但如果5年内转让了被投资企业股权并取得现金收入的，该现金收入应优先用于缴纳尚未结清的税款。"),
            ("p", "递延纳税的适用需要满足若干条件：一是投资方与被投资方之间不存在关联关系（或者在关联交易的公允价值能够得到合理保证的前提下）；二是被投资方取得的非货币性资产按照公允价值入账并计提折旧或摊销；三是投资方在投资完成后持有被投资企业股权的期间不少于12个月（针对个人投资者的反避税条款）。广州某税务机关在审理一起房地产出资案例时，因被投资方将房产按原账面价值而非公允价值入账，导致补缴税款及滞纳金超过500万元——这是实务中最为典型的合规盲区。"),
            ("h2", "增值税与土增税的联动处理"),
            ("p", "非货币性资产出资在增值税方面存在不同的处理规则：以货物（存货、设备等）出资的，视同销售货物，需按公允价值缴纳增值税；以房产、土地使用权等不动产出资的，视同销售不动产或转让土地使用权，需缴纳相应的增值税（一般计税方法下），并且可能触发土地增值税的纳税义务；以股权出资的，不属于增值税的应税行为（金融商品转让除外），但需关注股权出资是否构成"资产重组"从而适用增值税不征税政策的条件。"),
            ("p", "在契税方面，同一投资主体内部所属企业之间的土地、房屋权属划转，免征契税。但如果是不同投资主体之间的非货币性资产出资，受让方（被投资企业）需按照土地使用权或房屋权属的成交价格缴纳契税（广东省现行税率：3%）。在税收筹划中，契税往往是一个容易被低估的成本——例如，以评估价值1000万元的厂房出资，单契税就需要缴纳30万元，而这在投资决策中需要提前量化。"),
            ("h2", "特殊形式出资的税务要点"),
            ("p", "以股权出资是最常见也是最复杂的非货币性资产出资方式之一。根据《财政部 国家税务总局关于企业重组业务企业所得税处理若干问题的通知》（财税〔2009〕59号），股权收购适用特殊性税务处理（即递延纳税）需同时满足：具有合理的商业目的、收购股权比例不低于被收购企业全部股权的50%、股权支付金额不低于总交易金额的85%、重组后连续12个月内不改变实质性经营活动、取得股权支付的原主要股东连续12个月内不转让取得的股权。"),
            ("p", "以知识产权出资的场景下，除了企业所得税/个人所得税的递延纳税问题，还存在技术转让所得减免税的叠加优惠：居民企业在一个纳税年度内技术转让所得不超过500万元的部分免征企业所得税，超过500万元的部分减半征收。如果非货币性资产出资适用递延纳税政策的同时，又满足技术转让所得减免税的条件，则可以在5年递延期满确认所得时，再就每一年度确认的部分判断能否适用减免税——这种"递延+减免"的双重优惠组合，在合法合规的前提下可以大幅降低知识产权的出资税负。"),
            ("h2", "大湾区非货币性资产出资实务动态"),
            ("p", "广东省内各城市对非货币性资产出资的税务审核口径存在差异：广州市税务局对不动产出资的评估报告审核最为严格，要求评估机构具有证券期货相关业务评估资格，且评估方法须采用至少两种（市场法和收益法/成本法）交叉验证；深圳市前海、南沙自贸片区对符合条件的非货币性资产出资在印花税方面给予减半征收优惠；佛山市、东莞市对"工改工"项目中的土地厂房出资有专门的税务处理指引，允许在满足特定条件时适用递延纳税。"),
            ("p", "值得注意的是，金税四期系统上线后，非货币性资产出资的税务风险监控能力大幅增强：税务机关可以通过不动产登记系统、工商登记系统、企业所得税汇算清缴系统的数据比对，自动识别"企业以不动产出资但未申报资产转让所得"的异常情形。建议企业在进行非货币性资产出资前，将完整的税务处理方案提交主管税务机关进行事前沟通，以降低事后被调整的风险。"),
        ],
        "faq": [
            ("以房产出资需要缴哪些税？", "以房产出资涉及企业所得税（或个人所得税）、增值税、土地增值税、印花税，受让方还需缴纳契税。企业和个人均可申请在5年内分期确认所得，分期缴纳所得税。"),
            ("非货币性资产出资的5年递延如何计算？", "在不超过5个纳税年度内，将资产转让所得均匀分期计入——即每年确认20%的所得，按适用税率缴纳所得税。个人投资者如在5年内转让股权取得现金，应优先补缴未结清的税款。"),
            ("非货币性资产出资一定需要评估吗？", "法律上要求非货币性资产出资必须评估作价。税务上虽不强制要求评估报告，但税务机关通常以评估报告为核定公允价值的基础。缺少评估报告将导致公允价值无法合理证明，税务机关有权核定。"),
        ],
    },
    {
        "slug": "guanlianfang-jiekuan-shuiwu",
        "title": "关联方借款的税务风险与合规处理",
        "date": "2026-04-10",
        "category": "实操指南",
        "views": 1290,
        "keywords": "关联方借款,资本弱化,债资比,统借统还,利息税前扣除,转让定价,特别纳税调整,广州税务合规,存勤法税",
        "excerpt": "关联方之间的资金往来是企业集团最普遍的内部交易之一，也是最容易被税务机关挑战的领域。本文深度解析关联方借款的利率公允性判定、资本弱化管理中的债资比规则（金融企业5:1、非金融企业2:1）、统借统还免税政策的适用条件与合规要点，以及超过债资比标准的利息支出如何在关联方之间进行转让定价调整。",
        "meta_desc": "深度解析关联方借款的利率公允性、债资比规则（2:1/5:1）、统借统还免税条件、超标准利息的转让定价调整，提供大湾区税务合规方案。",
        "og_desc": "深度解析关联方借款的利率公允性、债资比规则、统借统还免税条件及转让定价调整。",
        "content_sections": [
            ("h2", "关联方借款的税务监管框架"),
            ("p", "关联方借款面临双重税务规制：一是《企业所得税法》第四十六条关于资本弱化的特别纳税调整规则——企业从关联方接受的债权性投资与权益性投资的比例超过规定标准（金融企业5:1，其他企业2:1）而发生的利息支出，不得在计算应纳税所得额时扣除；二是《企业所得税法》第四十一条关于关联交易独立交易原则的一般规制——关联方之间的借款利率应当符合独立交易原则，否则税务机关有权按照合理方法进行调整。这两个规则并非"二选一"而是"同时适用"——即便符合债资比要求，如果借款利率超出独立交易水平，超出部分同样不得税前扣除。"),
            ("p", "在实际监管中，税务机关重点关注以下情形：企业同时存在大量银行存款和关联方借款（"存贷双高"）、借款长期未还且无明确的还款计划、利率显著偏离同期同类银行贷款基准利率或LPR水平、借款协议约定与实际资金用途不符。2024年，广州市税务局在专项检查中发现多起关联方借款违规案例，合计调增应纳税所得额超过1.2亿元，补税及滞纳金超过3000万元。"),
            ("h2", "债资比的判定与例外处理"),
            ("p", "债资比的计算公式为：债权性投资 ÷ 权益性投资。其中，债权性投资不仅包括直接借款，还包括关联方通过无关联第三方提供的"背对背"贷款、关联方提供的担保贷款等间接融资。权益性投资包括实收资本、资本公积、盈余公积、未分配利润等。在计算比例时，一般采用年度加权平均法——即按每月月末的债权性投资和权益性投资余额计算月平均值，再汇总得出年度平均比例。"),
            ("p", "并非所有超出债资比标准的利息都不得扣除。符合独立交易原则或实际税负不高于关联方的，即使超出债资比标准，利息支出也可以税前扣除——这是《特别纳税调整实施办法》中的重要豁免条款。实务中，企业通常通过准备"同期资料"（转让定价文档）来证明借款条件的公允性，包括：可比利率分析（选取同期同类银行贷款利率作为参照）、借款用途的合理性论证（资金用于生产经营而非闲置或投资）、还款能力的客观评估。"),
            ("h2", "统借统还的免税条件"),
            ("p", ""统借统还"是企业集团内部资金调剂的常见模式——由核心企业（或集团财务公司）统一从外部金融机构借款，再按不高于外部借款利率水平分拨给集团内的实际用款企业。根据《财政部 国家税务总局关于全面推开营业税改征增值税试点的通知》（财税〔2016〕36号）的附件三，企业集团或企业集团中的核心企业向金融机构借款后，将所借资金分拨给下属单位，并按不高于支付给金融机构的借款利率水平向下属单位收取利息的，免征增值税。"),
            ("p", ""统借统还"享受增值税免税需同时满足三个条件：一是资金来源于金融机构（银行、信托公司等持牌机构），而非股东个人或其他企业；二是分拨利率不高于外部借款利率——即不得从中赚取利差，否则超出部分的利息需缴纳增值税；三是双方签订了统借统还协议，并建立了资金台账，能够清晰追踪每笔资金的来源和去向。广州某企业集团因未签订统借统还协议，虽实质上按"不高于外部利率"分拨资金，但被税务机关认定为一般借贷行为，追缴增值税及附加逾百万元。"),
            ("h2", "利息支出的税前扣除实操要点"),
            ("p", "关联方利息支出税前扣除的前提是取得合规的税前扣除凭证：对于境内关联方，借款方应取得收款方开具的增值税发票（或利息结算单），发票税率栏应为"免税"（统借统还）或"6%"（一般贷款）；对于境外关联方，还需完成非居民企业所得税的代扣代缴，并取得扣缴凭证。利息支出在资本化与费用化的划分上需严格遵循会计准则——用于购建固定资产、无形资产的借款利息，在资产达到预定可使用状态之前应当资本化，计入资产成本，通过折旧或摊销方式在以后期间扣除。"),
            ("p", "关于利率的公允性判断，现行做法是以中国人民银行授权全国银行间同业拆借中心公布的贷款市场报价利率（LPR）为基准。如借款利率在LPR的0.8-1.2倍之间，通常被视为符合独立交易原则；如超出此区间，则需要提供充分的同期资料证明其合理性。对于信托贷款、委托贷款等非银行通道融资，利率公允性的判断更为复杂，通常需要同时考虑通道费用在内后的综合资金成本。"),
            ("h2", "大湾区关联方借款的税务筹划策略"),
            ("p", "在合规框架下，企业可以通过以下策略优化关联方借款的税务效率：第一，保持合理的资本结构——在业务扩张期适当通过增资而非借款方式引入资金，维持债资比在2:1标准以内。第二，优先使用统借统还模式——以集团核心企业统一对外借款后分拨，统一享受增值税免税待遇。第三，在有税收优惠的区域（如横琴粤澳深度合作区、南沙自贸片区）设立资金中心——利用区域性税收优惠降低集团整体的资金成本。"),
            ("p", "需要特别强调的是，任何关联方借款的税务安排都应以"商业目的优先"为原则——即借款安排首先应当具有合理的商业理由（如项目开发、产能扩充、营运资金补充等），税务优化是这些安排的自然延伸，而非刻意构造。金税四期已具备跨税种、跨区域的数据分析能力，以避税为主要目的的资金安排极易被识别和挑战。"),
        ],
        "faq": [
            ("关联方借款的债资比标准是多少？", "金融企业的债资比标准为5:1，非金融企业为2:1。超过该比例的利息支出，原则上不得税前扣除。但如能证明借款条件符合独立交易原则，或境内关联方的实际税负不高于借款方，超出部分仍可扣除。"),
            ("统借统还如何享受增值税免税？", "统借统还增值税免税需满足三个条件：资金来源于金融机构、分拨利率不高于外部借款利率、签订统借统还协议并建立资金台账。不得从中赚取利差。"),
            ("关联方借款利率超出LPR基准可以扣除吗？", "利率在LPR的0.8-1.2倍之间通常可接受。如超出此区间，需准备同期资料（含可比利率分析、借款用途合理性论证、还款能力评估）证明其独立性，否则超出部分不得税前扣除。"),
        ],
    },
    {
        "slug": "shuishou-xieding-daiyu-shenqing",
        "title": "税收协定待遇申请实务指南",
        "date": "2026-04-16",
        "category": "实操指南",
        "views": 1180,
        "keywords": "税收协定,受益所有人,预提所得税,股息利息特许权使用费,跨境税务,非居民企业,广州涉外税务,存勤法税",
        "excerpt": "在跨境投资和贸易中，税收协定是企业降低跨境税负的重要法律工具。中国已与110多个国家/地区签署了避免双重征税协定，但能否真正享受到协定优惠税率，取决于"受益所有人"身份的判定、申请材料的完备性、以及主管税务机关的审核结果。本文以广州及大湾区企业跨境经营的实际需求为出发点，提供税收协定待遇申请的完整操作指引。",
        "meta_desc": "系统解析税收协定待遇申请的完整流程：受益所有人判定、股息/利息/特许权使用费优惠税率、申请材料准备、非居民企业扣缴实务及大湾区企业跨境经营指引。",
        "og_desc": "系统解析税收协定待遇申请流程：受益所有人判定、优惠税率与申请材料准备。",
        "content_sections": [
            ("h2", "税收协定的基本框架与优惠内容"),
            ("p", "税收协定（或称避免双重征税协定）是两个主权国家之间为消除跨境所得的重复征税、防止偷漏税而签订的国际条约。截至2025年，中国已与110多个国家/地区签署了避免双重征税协定，其中100多个已生效执行。税收协定的核心功能包括：划分不同所得类型的征税权归属（来源国或居民国）、限制来源国的征税税率（如股息、利息、特许权使用费的预提税税率上限）、提供税收抵免或免税机制以消除双重征税、建立相互协商程序解决税收争议。"),
            ("p", "对中国企业"走出去"（对外投资）和企业"引进来"（吸引外资）两种场景，税收协定的作用方向不同：对于"走出去"企业，重点是运用协定保护中国企业在境外投资国的税收利益——如境外子公司向中国母公司分配的股息在来源国享受协定优惠税率、境外工程承包项目在来源国避免被认定为"常设机构"所触发的营业利润征税。对于"引进来"企业，重点是帮助境外投资者确认能否就股息、利息、特许权使用费等被动所得申请协定优惠税率——例如，中国国内法对股息预提所得税率为10%，但在中国与新加坡、中国香港等部分国家/地区的协定中，股息预提税率可降至5%。"),
            ("h2", ""受益所有人"的判定规则"),
            ("p", ""受益所有人"（Beneficial Owner）是税收协定待遇申请的核心概念和第一道门槛。根据国家税务总局公告2018年第9号，受益所有人是指"对所得或所得据以产生的权利或财产具有所有权和支配权的人"。"安全港"规则（即自动被认定为受益所有人）适用于三类主体：缔约对方政府、缔约对方居民且在缔约对方上市的公司、缔约对方居民个人。但在实务中，绝大多数申请主体不属于"安全港"范围，需要通过实质运营的多个因素综合判定。"),
            ("p", "不利因素（不利于被认定为受益所有人）包括：申请人有义务在收到所得的12个月内将50%以上支付给第三国/地区居民、申请人除持有资产外无其他实质性经营活动、申请人没有或几乎没有雇员和资产（皮包公司）、申请人对所得没有支配权等。有利因素包括：申请人在注册地有固定办公场所和实际雇员、申请人从事实际的生产经营活动、申请人成立的商业目的主要以经营业务为主而非避税。广州某外商投资企业因境外母公司被认定为"导管公司"（不具备受益所有人资格），被追缴已享受的协定优惠税款超过800万元——这一案例凸显了"实质重于形式"原则在协定待遇申请中的绝对权重。"),
            ("h2", "股息、利息、特许权使用费的优惠税率"),
            ("p", "在税收协定中，三类被动所得的预提税率是最核心的优惠条款。股息的优惠税率：中国国内法规定股息预提税率为10%，但多数协定中降至5%-10%。以中国-新加坡协定为例，持股比例不低于25%的，股息预提税率降至5%；其他情况适用10%。利息的优惠税率：中国国内法预提税率10%，多数协定中降至5%-10%，部分协定中政府或政府全资拥有的金融机构取得的利息可免税。特许权使用费的优惠税率：中国国内法预提税率10%，多数协定中降至5%-10%，部分协定对工业、商业和科学设备的租金（被视为特许权使用费）给予更优惠处理。"),
            ("p", ""常设机构"条款对营业利润的影响也是协定中的重要内容——境外企业在中国的活动是否构成"常设机构"决定了中国的征税权范围。提供劳务型常设机构：在任何12个月中连续或累计超过183天的，构成常设机构；建筑工程型常设机构：持续12个月以上的建筑工地、装配或安装工程构成常设机构。对于在广东省内开展工程承包、提供技术服务的外国企业，准确判断常设机构的构成时间点是进行税务规划的前提。"),
            ("h2", "申请材料的准备与提交"),
            ("p", "税收协定待遇的申请材料应围绕两个核心目标组织：证明申请人的"缔约对方税收居民"身份，以及证明申请人的"受益所有人"资格。核心材料包括：缔约对方主管税务机关出具的《税收居民身份证明》（Certificate of Residence），注意该证明通常有时效要求（一般为出具之日起12个月内有效）；《非居民纳税人享受协定待遇申请表》；与股息、利息、特许权使用费相关的合同或协议；能够证明申请人实质性运营的证据——包括但不限于办公场所租赁合同、员工名册及社保缴纳记录、年报审计报告等覆盖申请人"有人、有场所、有业务"的材料。"),
            ("p", "自2020年1月1日起，非居民纳税人享受协定待遇的程序已从"审批制"改为"自行判断、申报享受、留存备查"。这意味着纳税人无需等待税务机关审批即可直接按协定优惠税率扣缴或申报，但须承担证明其符合享受条件的举证责任。在自行享受协定待遇后的10年内，主管税务机关有权进行后续核查——这是"自行判断"制度下的最大风险：从审批制的"事前审核"转变为"事中事后监管"，企业的材料留存质量和税务处理的专业性直接决定了风险敞口。"),
            ("h2", "大湾区企业的协定应用实务"),
            ("p", "粤港澳大湾区企业的跨境经营非常活跃，税收协定的运用场景最为丰富：一是"香港-内地"之间的投资往来——依据《内地和香港特别行政区关于对所得避免双重征税和防止偷漏税的安排》，香港居民企业投资内地取得的股息，持股比例不低于25%且满足受益所有人条件的，预提税率可降至5%；利息和特许权使用费的预提税率降至7%。二是"澳门-内地"的投资安排也享受类似优惠，如股息预提税率降至5%（持股25%以上）、利息和特许权使用费降至7%。"),
            ("p", "对于在广州注册的投资控股公司（作为境外投资的中转平台），如能证明自身具有"实质运营"——拥有固定的办公场所和实际的经营团队，而非单纯的持股工具——在向境外子公司收取股息、利息或特许权使用费时，可以在境外来源地申请当地与中国之间的协定优惠税率。这种"中国母公司→境外子公司→利润回流"的投资架构需要在初始设计阶段就将各环节的协定适用纳入考量。"),
        ],
        "faq": [
            ("申请税收协定待遇的核心条件是什么？", "核心条件是证明申请人为缔约对方税收居民，且具备"受益所有人"资格——即对所得具有所有权和支配权，有实质性经营活动而非单纯的导管公司。需提交税收居民身份证明等材料，实行"自行判断、申报享受、留存备查"。"),
            ("股息预提税的协定优惠税率是多少？", "中国国内法预提税率10%，协定下可降至5%或更低（视对方国家及持股比例而定）。例如，持股25%以上的新加坡或中国香港居民企业，股息预提税率降至5%。"),
            ("非居民企业享受协定待遇需要事先审批吗？", "不需要。自2020年起已改为"自行判断、申报享受、留存备查"制。但税务机关在10年内可进行后续核查，因此材料留存的完整性至关重要。"),
        ],
    },
]

# Hardcoded today's date for consistency
TODAY = "2026-05-27"

def slug_to_filename(slug):
    """Convert slug to Chinese filename like 股权架构全解析与税务规划(source).html"""
    mapping = {
        "tudi-zengzhishui-qingsuan-chouhua": "土地增值税清算实务与筹划策略",
        "gongsi-zhuxiao-qingsuan-shuiwu": "公司注销清算的税务处理全流程",
        "fei-huobi-zichan-touzi-shuiwu": "非货币性资产投资的税务处理",
        "guanlianfang-jiekuan-shuiwu": "关联方借款的税务风险与合规处理",
        "shuishou-xieding-daiyu-shenqing": "税收协定待遇申请实务指南",
    }
    return mapping[slug]

def get_related_articles(slug):
    """Get 3 related article slugs for cross-referencing."""
    related_map = {
        "tudi-zengzhishui-qingsuan-chouhua": [
            ("fangdichan-qiye-shuiwu-chouhua", "房地产企业全流程税务筹划", "实操指南"),
            ("qiye-zhongzu-shuiwu", "企业重组中的税务处理与筹划", "实操指南"),
            ("IPO-shuiwu-hegui-jiagou", "IPO税务合规与架构设计", "深度解析"),
        ],
        "gongsi-zhuxiao-qingsuan-shuiwu": [
            ("qiye-zhongzu-shuiwu", "企业重组中的税务处理与筹划", "实操指南"),
            ("guquan-jiagou-shuiwu-chouhua", "股权架构全解析与税务规划", "实操指南"),
            ("gudong-jiekuan-shuiwu-fengxian", "股东借款的税务风险与合规方案", "实操指南"),
        ],
        "fei-huobi-zichan-touzi-shuiwu": [
            ("guquan-jiagou-shuiwu-chouhua", "股权架构全解析与税务规划", "实操指南"),
            ("qiye-zhongzu-shuiwu", "企业重组中的税务处理与筹划", "实操指南"),
            ("IPO-shuiwu-hegui-jiagou", "IPO税务合规与架构设计", "深度解析"),
        ],
        "guanlianfang-jiekuan-shuiwu": [
            ("gudong-jiekuan-shuiwu-fengxian", "股东借款的税务风险与合规方案", "实操指南"),
            ("qiye-zhongzu-shuiwu", "企业重组中的税务处理与筹划", "实操指南"),
            ("guquan-jiagou-shuiwu-chouhua", "股权架构全解析与税务规划", "实操指南"),
        ],
        "shuishou-xieding-daiyu-shenqing": [
            ("CRS-kuajing-zichan-shenbao", "CRS框架下跨境资产申报与合规", "实操指南"),
            ("ODI-jingwai-touzi-beian", "ODI境外投资备案全流程指引", "实操指南"),
            ("kuajing-dianzishangwu-shuiwu", "跨境电商的税务合规与筹划", "深度解析"),
        ],
    }
    return related_map[slug]

def build_article_html(art):
    """Build complete HTML for one article."""
    slug = art["slug"]
    title = art["title"]
    date = art["date"]
    category = art["category"]
    views = art["views"]
    keywords = art["keywords"]
    excerpt = art["excerpt"]
    meta_desc = art["meta_desc"]
    og_desc = art["og_desc"]
    
    # Build content HTML
    content_html = ""
    for tag, text in art["content_sections"]:
        if tag == "h2":
            tid = text.replace("""", "").replace(""", "").replace("：", "").replace(":", "").replace(" ", "")
            content_html += f'\n        <h2 id="{tid}">{text}</h2>\n'
        elif tag == "p":
            content_html += f'        <p>{text}</p>\n'
    
    # Build FAQ Schema
    faq_items = ""
    for q, a in art["faq"]:
        faq_items += f'''
      {{
        "@type": "Question",
        "name": "{q}",
        "acceptedAnswer": {{
          "@type": "Answer",
          "text": "{a}"
        }}
      }},'''
    faq_items = faq_items.rstrip(",")
    
    # Related articles
    related = get_related_articles(slug)
    related_html = ""
    for rslug, rtitle, rcat in related:
        related_html += f'''
          <a href="{rslug}.html" class="related-card">
            <span class="related-category">{rcat}</span>
            <h4>{rtitle}</h4>
            <span class="related-link">阅读全文 <i class="fas fa-arrow-right"></i></span>
          </a>'''
    
    html = f'''---
permalink: /articles/{slug}.html
layout: false
---
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta name="msvalidate.01" content="643F9F9C5376BCE8168CB8533417070C" />
  <meta name="baidu-site-verification" content="codeva-9SPpSVW5X6" />
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="robots" content="index, follow">
<meta name="keywords" content="{keywords}">
<link rel="canonical" href="https://cunqin.tax/articles/{slug}.html">
<link rel="alternate" hreflang="zh-CN" href="https://cunqin.tax/articles/{slug}.html">
<link rel="apple-touch-icon" href="https://cunqin.tax/images/nav-logo.webp">
<link rel="apple-touch-icon" sizes="180x180" href="https://cunqin.tax/images/nav-logo.webp">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="存勤法税">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="theme-color" content="#003f6c">
<meta name="msapplication-TileColor" content="#003f6c">
  <meta property="og:type" content="article">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{og_desc}">
  <meta property="og:image" content="https://cunqin.tax/images/company-logo.png">
  <meta property="og:url" content="https://cunqin.tax/articles/{slug}.html">
  <meta property="og:site_name" content="存勤法税">
  <meta property="og:locale" content="zh_CN">
  <meta property="article:published_time" content="{date}T08:00:00+08:00">
  <meta property="article:modified_time" content="{TODAY}T08:00:00+08:00"><meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{og_desc}">
<meta name="twitter:image" content="https://cunqin.tax/images/company-logo.png">
<meta property="article:published_time" content="{date}">
<meta property="article:modified_time" content="{TODAY}">
<meta property="article:author" content="邓达华">
    <title>{title} | 存勤法税</title>
    <meta name="description" content="{meta_desc}">
  <link rel="icon" href="../images/nav-logo.webp" type="image/webp">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6/css/all.min.css">
  <style>
:root {{
  --dt-primary: #003f6c;
  --dt-primary-light: #1a5f7a;
  --dt-accent: #00a19c;
  --dt-light-bg: #f3f5f8;
  --dt-white: #ffffff;
  --dt-text: #2c3e50;
  --dt-text-light: #5a6c7d;
  --dt-border: #dee2e6;
  --dt-soft: #e8ecf1;
  --dt-warm: #faf8f5;
  --dt-orange: #c75b2a;
}}

/* ===== Reset ===== */
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
html{{scroll-behavior:smooth;font-size:16px;-webkit-font-smoothing:antialiased}}
body{{font-family:"PingFang SC","Microsoft YaHei","Helvetica Neue",sans-serif;color:var(--dt-text);line-height:1.75;background:var(--dt-light-bg);min-height:100vh;display:flex;flex-direction:column}}

/* ===== Navbar ===== */
.nav{{position:fixed;top:0;left:0;right:0;z-index:1000;background:var(--dt-white);border-bottom:1px solid var(--dt-border);height:68px;display:flex;align-items:center}}
.nav-inner{{max-width:1280px;margin:0 auto;padding:0 2rem;display:flex;align-items:center;justify-content:space-between;width:100%}}
.nav-logo{{height:44px;width:auto}}
.nav-links{{display:flex;align-items:center;gap:2rem;list-style:none}}
.nav-links a{{text-decoration:none;color:var(--dt-text);font-size:0.95rem;font-weight:500;transition:color 0.2s;white-space:nowrap}}
.nav-links a:hover{{color:var(--dt-primary)}}
.nav-links a.active{{color:var(--dt-primary);font-weight:700}}

/* ===== Hero ===== */
.article-hero{{padding:6.5rem 2rem 3rem;background:linear-gradient(135deg,var(--dt-primary) 0%,var(--dt-primary-light) 100%);color:var(--dt-white);text-align:center}}
.article-hero .hero-tag{{display:inline-block;background:rgba(255,255,255,0.18);padding:0.25rem 1rem;border-radius:20px;font-size:0.85rem;margin-bottom:1rem;backdrop-filter:blur(8px)}}
.article-hero h1{{font-size:2.2rem;font-weight:700;max-width:800px;margin:0 auto 0.75rem;line-height:1.4}}
.article-hero .hero-meta{{font-size:0.9rem;opacity:0.9;display:flex;justify-content:center;gap:1.5rem;flex-wrap:wrap}}

/* ===== Search Bar (sticky) ===== */
.article-search-bar{{position:sticky;top:68px;z-index:99;background:var(--dt-white);border-bottom:1px solid var(--dt-border);padding:0.75rem 2rem;display:flex;align-items:center;justify-content:center;gap:0.75rem}}
.article-search-bar input{{width:420px;padding:0.5rem 1rem;border:1px solid var(--dt-border);border-radius:6px;font-size:0.9rem;outline:none;transition:border-color 0.2s}}
.article-search-bar input:focus{{border-color:var(--dt-primary)}}
.article-search-bar button{{background:var(--dt-primary);color:var(--dt-white);border:none;padding:0.5rem 1rem;border-radius:6px;cursor:pointer;font-size:0.85rem;transition:background 0.2s}}
.article-search-bar button:hover{{background:var(--dt-primary-light)}}
.article-search-bar .search-count{{font-size:0.85rem;color:var(--dt-text-light)}}
.article-search-bar .search-nav{{display:flex;gap:0.5rem}}
.article-search-bar .search-nav button{{background:var(--dt-soft);color:var(--dt-text);min-width:32px}}
.article-search-bar .back-btn{{background:var(--dt-soft)!important;color:var(--dt-text)!important}}
.search-mark{{background:#fde68a;padding:0 2px;border-radius:2px;transition:background 0.3s}}
.search-mark.active{{background:#f59e0b;color:#fff}}

/* ===== Article layout ===== */
.article-layout{{max-width:1280px;margin:0 auto;padding:2rem;display:grid;grid-template-columns:240px 1fr;gap:3rem;align-items:start;flex:1}}

/* TOC sidebar */
.article-toc{{position:sticky;top:140px;background:var(--dt-white);border-radius:10px;padding:1.5rem;border:1px solid var(--dt-border)}}
.article-toc h3{{font-size:1rem;margin-bottom:1rem;color:var(--dt-primary)}}
.article-toc nav a{{display:block;padding:0.35rem 0;font-size:0.88rem;color:var(--dt-text-light);text-decoration:none;border-left:2px solid transparent;padding-left:0.75rem;transition:all 0.2s}}
.article-toc nav a:hover,.article-toc nav a.active{{color:var(--dt-primary);border-left-color:var(--dt-primary)}}

/* Main content */
.article-main{{background:var(--dt-white);border-radius:10px;padding:2.5rem;border:1px solid var(--dt-border);min-width:0}}
.article-main h2{{font-size:1.6rem;color:var(--dt-primary);margin:2.5rem 0 1rem;padding-bottom:0.5rem;border-bottom:2px solid var(--dt-soft)}}
.article-main h2:first-of-type{{margin-top:0}}
.article-main p{{margin-bottom:1.25rem;font-size:1rem;text-align:justify}}
.article-main strong{{color:var(--dt-primary)}}

/* Related */
.article-related{{margin-top:3rem;padding-top:2rem;border-top:1px solid var(--dt-border)}}
.article-related h3{{font-size:1.3rem;color:var(--dt-primary);margin-bottom:1.25rem;text-align:center}}
.related-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:1.25rem}}
.related-card{{display:block;background:var(--dt-light-bg);border-radius:8px;padding:1.25rem;text-decoration:none;border:1px solid var(--dt-border);transition:all 0.25s}}
.related-card:hover{{border-color:var(--dt-primary);box-shadow:0 4px 16px rgba(0,63,108,0.08);transform:translateY(-2px)}}
.related-category{{display:inline-block;font-size:0.75rem;color:var(--dt-accent);background:rgba(0,161,156,0.1);padding:0.15rem 0.6rem;border-radius:10px;margin-bottom:0.5rem}}
.related-card h4{{font-size:0.95rem;color:var(--dt-text);margin-bottom:0.75rem;line-height:1.5}}
.related-link{{font-size:0.85rem;color:var(--dt-primary);font-weight:600}}

/* CTA */
.article-cta{{margin-top:2.5rem;background:linear-gradient(135deg,var(--dt-primary),var(--dt-primary-light));border-radius:10px;padding:2rem;text-align:center;color:var(--dt-white)}}
.article-cta h3{{font-size:1.3rem;margin-bottom:0.75rem}}
.article-cta p{{font-size:0.95rem;margin-bottom:1.25rem;opacity:0.9;text-align:center}}
.article-cta .cta-btn{{display:inline-block;background:var(--dt-white);color:var(--dt-primary);padding:0.65rem 2rem;border-radius:6px;font-weight:600;text-decoration:none;font-size:0.95rem;transition:all 0.2s}}
.article-cta .cta-btn:hover{{background:var(--dt-orange);color:var(--dt-white)}}

/* Disclaimer */
.article-disclaimer{{margin-top:1.5rem;padding:1rem;background:var(--dt-warm);border-radius:8px;font-size:0.82rem;color:var(--dt-text-light);text-align:center;border:1px solid var(--dt-soft)}}

/* Footer */
.footer{{background:var(--dt-primary);color:var(--dt-white);padding:2.5rem 2rem 1.5rem;margin-top:auto}}
.footer-grid{{max-width:1280px;margin:0 auto;display:grid;grid-template-columns:1fr 2fr 1fr;gap:2rem}}
.footer-col h4{{font-size:1rem;margin-bottom:1rem;color:var(--dt-white)}}
.footer-col ul{{list-style:none;display:flex;flex-wrap:wrap;gap:0.5rem 1.5rem}}
.footer-col ul li{{font-size:0.88rem}}
.footer-col ul li a{{color:rgba(255,255,255,0.78);text-decoration:none;transition:color 0.2s;white-space:nowrap}}
.footer-col ul li a:hover{{color:var(--dt-white)}}
.footer-col p{{font-size:0.88rem;color:rgba(255,255,255,0.78);line-height:1.8}}
.footer-bottom{{max-width:1280px;margin:1.5rem auto 0;padding-top:1.25rem;border-top:1px solid rgba(255,255,255,0.15);text-align:center;font-size:0.82rem;color:rgba(255,255,255,0.5)}}

@media (max-width:1024px){{
.article-layout{{grid-template-columns:1fr}}
.article-toc{{display:none}}
.related-grid{{grid-template-columns:1fr}}
.footer-grid{{grid-template-columns:1fr;text-align:center}}
}}

@media (max-width:768px){{
.article-hero h1{{font-size:1.6rem}}
.article-main{{padding:1.5rem}}
.article-search-bar input{{width:100%}}
.nav-links{{display:none}}
}}

@media (max-width:480px){{
.article-hero h1{{font-size:1.4rem}}
.article-main{{padding:1rem}}
}}
  </style>
</head>
<body>

  <!-- Navbar -->
  <nav class="nav">
    <div class="nav-inner">
      <a href="../"><img src="../images/nav-logo.webp" alt="存勤法税" class="nav-logo" loading="lazy" width="150" height="44"></a>
      <ul class="nav-links">
        <li><a href="../">首页</a></li>
        <li><a href="../about/">公司介绍</a></li>
        <li><a href="../services/">核心服务</a></li>
        <li><a href="../cases/">客户案例</a></li>
        <li><a href="../archives/">法税洞察</a></li>
        <li><a href="../contact/">联系我们</a></li>
      </ul>
    </div>
  </nav>

  <!-- Hero -->
  <section class="article-hero">
    <span class="hero-tag">{category}</span>
    <h1>{title}</h1>
    <div class="hero-meta">
      <span><i class="fas fa-user-edit"></i> 邓达华</span>
      <span><i class="fas fa-calendar-alt"></i> {date.replace("-", ".").replace("-", ".")}</span>
      <span><i class="fas fa-eye"></i> {views} 阅读</span>
    </div>
  </section>

  <!-- Search Bar -->
  <div class="article-search-bar">
    <button class="back-btn" onclick="history.back()" title="返回"><i class="fas fa-arrow-left"></i> 返回</button>
    <input type="text" id="article-search-input" placeholder="输入关键词搜索本文内容...">
    <button onclick="doArticleSearch()"><i class="fas fa-search"></i> 搜索</button>
    <span class="search-count" id="search-count"></span>
    <span class="search-nav" id="search-nav"></span>
  </div>

  <!-- Article Layout -->
  <main class="article-layout">
    <aside class="article-toc" id="article-toc">
      <h3>文章目录</h3>
      <nav id="toc-nav"></nav>
    </aside>
    <article class="article-main" id="article-main">
{content_html}
      <!-- 结语 -->
      <h2 id="结语">结语</h2>
      <p>{title}是企业税务管理中的重要课题，涉及多项政策规则的精细适用和跨部门的协调处理。在实务操作中，每一个具体环节的处理方式都可能对最终的税务结果产生显著影响。建议企业在面对相关税务问题时，尽早引入专业税务顾问进行系统评估，在合规框架内实现税务效率的优化。存勤法税深耕粤港澳大湾区企业财税服务市场，以业管财税法五维融合为核心方法论，为广州及大湾区企业提供可落地的专业税务解决方案。</p>

      <!-- 延伸阅读 -->
      <section class="article-related">
        <h3 class="related-heading">延伸阅读</h3>
        <div class="related-grid">{related_html}
        </div>
      </section>

      <!-- CTA -->
      <div class="article-cta">
        <h3>需要专业的税务顾问支持？</h3>
        <p>存勤法税由邓达华先生创立，汇集注册会计师、税务师、律师等专业力量，为大湾区企业提供业管财税法五维一体的专业服务。欢迎联系我们进行一对一咨询。</p>
        <a href="../../contact/" class="cta-btn">立即咨询 <i class="fas fa-arrow-right"></i></a>
      </div>

      <!-- Disclaimer -->
      <div class="article-disclaimer">
        <strong>声明：</strong>本文由存勤法税服务（广州）有限公司原创撰写，仅供专业交流和参考，不构成任何形式的法律意见或税务建议。具体业务场景下的税务处理应以现行法律法规为准，建议咨询专业税务顾问后进行决策。未经授权，禁止转载或摘编。
      </div>

      <!-- FAQPage Schema -->
      <script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [{faq_items}
  ]
}}
      </script>

      <!-- Article Schema -->
      <script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{title}",
  "description": "{meta_desc}",
  "author": {{
    "@type": "Person",
    "name": "邓达华"
  }},
  "datePublished": "{date}",
  "dateModified": "{TODAY}",
  "image": "https://cunqin.tax/images/company-logo.png",
  "publisher": {{
    "@type": "Organization",
    "name": "存勤法税服务（广州）有限公司",
    "logo": {{
      "@type": "ImageObject",
      "url": "https://cunqin.tax/images/company-logo.png"
    }}
  }},
  "mainEntityOfPage": {{
    "@type": "WebPage",
    "@id": "https://cunqin.tax/articles/{slug}.html"
  }}
}}
      </script>

      <!-- BreadcrumbList Schema -->
      <script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {{
      "@type": "ListItem",
      "position": 1,
      "name": "首页",
      "item": "https://cunqin.tax/"
    }},
    {{
      "@type": "ListItem",
      "position": 2,
      "name": "法税洞察",
      "item": "https://cunqin.tax/archives/"
    }},
    {{
      "@type": "ListItem",
      "position": 3,
      "name": "{title}"
    }}
  ]
}}
      </script>

    </article>
  </main>

  <!-- Footer -->
  <footer class="footer">
    <div class="footer-grid">
      <div class="footer-col">
        <h4>快速链接</h4>
        <ul>
          <li><a href="../../">首页</a></li>
          <li><a href="../../about/">公司介绍</a></li>
          <li><a href="../../contact/">联系我们</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>核心服务</h4>
        <ul>
          <li><a href="../../services/s01-tax-health-check.html">涉税风险检查</a></li>
          <li><a href="../../services/s02-tax-planning.html">税务筹划方案</a></li>
          <li><a href="../../services/s03-transfer-pricing.html">转让定价服务</a></li>
          <li><a href="../../services/s04-restructuring-tax.html">企业重组税务</a></li>
          <li><a href="../../services/s05-high-tech-tax.html">高新技术企业税务</a></li>
          <li><a href="../../services/s06-estate-planning.html">家族财富传承</a></li>
          <li><a href="../../services/s07-cross-border-tax.html">跨境税务服务</a></li>
          <li><a href="../../services/s08-tax-dispute.html">税务争议解决</a></li>
          <li><a href="../../services/s09-estate-tax-planning.html">房地产税务规划</a></li>
          <li><a href="../../services/s10-merger-acquisition-tax.html">并购重组税务</a></li>
          <li><a href="../../services/s11-legal-tax-advisor.html">常年法税顾问</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>联系我们</h4>
        <p>地址：广州市天河区珠江新城</p>
        <p>电话：139-0220-1718</p>
        <p>邮箱：contact@cunqin.tax</p>
      </div>
    </div>
    <div class="footer-bottom">
      &copy; 2026 存勤法税服务（广州）有限公司 | 保留所有权利
    </div>
  </footer>

  <!-- TOC & Search JS -->
  <script>
(function(){{
  var hs=document.querySelectorAll('.article-main h2');
  var nav=document.getElementById('toc-nav');
  hs.forEach(function(h, i){{
    if(!h.id) h.id = 'section-'+i;
    var a = document.createElement('a');
    a.href = '#'+h.id;
    a.textContent = h.textContent;
    nav.appendChild(a);
  }});
  var links=nav.querySelectorAll('a');
  var observer=new IntersectionObserver(function(entries){{
    entries.forEach(function(e){{
      if(e.isIntersecting){{
        links.forEach(function(l){{
          l.classList.toggle('active', l.getAttribute('href')==='#'+e.target.id);
        }});
      }}
    }});
  }},{{threshold:0.5}});
  hs.forEach(function(h){{observer.observe(h);}});
}})();

var currentMatchIdx=-1, matches=[];
function doArticleSearch(){{
  var q=document.getElementById('article-search-input').value.trim().toLowerCase();
  var main=document.getElementById('article-main');
  clearHighlights(main);
  matches=[];
  currentMatchIdx=-1;
  if(!q){{document.getElementById('search-count').textContent='';document.getElementById('search-nav').innerHTML='';return;}}
  var walker=document.createTreeWalker(main, NodeFilter.SHOW_TEXT, null, false);
  var textNodes=[];
  while(walker.nextNode()) textNodes.push(walker.currentNode);
  textNodes.forEach(function(tn){{
    var parent=tn.parentNode;
    if(!parent||parent.tagName==='SCRIPT'||parent.tagName==='STYLE') return;
    var txt=tn.textContent.toLowerCase();
    if(txt.indexOf(q)===-1) return;
    var html=tn.textContent;
    var escapedQ=q.replace(/[.*+?^${{}}()|[\\]\\\\]/g,'\\\\$&');
    var re=new RegExp('('+escapedQ+')','gi');
    var span=document.createElement('span');
    span.innerHTML=html.replace(re,'<mark class="search-mark" data-match="true">$1</mark>');
    tn.replaceWith(span);
  }});
  matches=main.querySelectorAll('mark[data-match="true"]');
  document.getElementById('search-count').textContent=matches.length+' 处匹配';
  if(matches.length>0){{
    var nav=document.getElementById('search-nav');
    nav.innerHTML='<button onclick="jumpToMatch(-1)"><i class=\\'fas fa-chevron-up\\'></i></button><button onclick="jumpToMatch(1)"><i class=\\'fas fa-chevron-down\\'></i></button>';
    jumpToMatch(1);
  }}else{{document.getElementById('search-nav').innerHTML='';}}
}}
function clearHighlights(root){{
  var marks=root.querySelectorAll('mark[data-match="true"]');
  marks.forEach(function(m){{
    var txt=document.createTextNode(m.textContent);
    m.replaceWith(txt);
  }});
}}
function jumpToMatch(delta){{
  if(matches.length===0) return;
  if(currentMatchIdx>=0) matches[currentMatchIdx].classList.remove('active');
  currentMatchIdx+=delta;
  if(currentMatchIdx<0) currentMatchIdx=matches.length-1;
  if(currentMatchIdx>=matches.length) currentMatchIdx=0;
  var m=matches[currentMatchIdx];
  m.classList.add('active');
  m.scrollIntoView({{behavior:'smooth',block:'center'}});
}}
  </script>

</body>
</html>'''
    return html

def main():
    for art in articles:
        slug = art["slug"]
        filename = slug_to_filename(slug)
        filepath = os.path.join(ARTICLES_DIR, f"{filename}(source).html")
        html = build_article_html(art)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"✅ Created: {filename}(source).html ({len(html)} chars)")
    
    print("\n🎉 All 5 P0 articles generated successfully!")

if __name__ == "__main__":
    main()
