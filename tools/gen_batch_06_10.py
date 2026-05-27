#!/usr/bin/env python3
"""Write bodies and generate articles #6-#10"""
import json, os, sys, re, subprocess

JSON_PATH = r'C:\Users\26726\WorkBuddy\2026-05-20-21-20-24\tools\geo_articles_batch1.json'
BASE_DIR = r'C:\Users\26726\WorkBuddy\2026-05-20-21-20-24'
PYTHON = r'C:\Users\26726\.workbuddy\binaries\python\versions\3.13.12\python.exe'

# Article bodies (slug -> HTML content)
BODIES = {}

BODIES["zhibo-daihuo-wanghong-shuiwu"] = """<p>从2018年范冰冰案到2021年薇娅案，文娱和直播行业的税务风暴一波接着一波。每一次\"顶流\"被查，背后都是金额惊人的补税、滞纳金和罚款。但对于数以万计的普通主播、网红和MCN机构而言，更大的焦虑在于：\"我到底该按什么方式交税？\"\"工作室模式还能做吗？\"\"怎样才能既合规又不'白交'税？\"本文从收入类型认定、MCN机构合规、工作室模式变迁到稽查红线，系统梳理直播行业的个税合规要点。</p><h2 id=\"s1\">一、主播收入的\"三重身份\"：工资、劳务还是经营所得？</h2><h3 id=\"s1-1\">1.1 劳动合同关系：工资薪金所得</h3><p>如果主播与MCN机构签订劳动合同、接受公司规章制度管理、享受五险一金等员工福利、按月领取相对固定的底薪加提成，则收入属于工资薪金所得。税率3%-45%超额累进，由MCN机构代扣代缴个税。MCN还需为主播缴纳社保。这种模式下，主播不需要自己操心税务申报，但税率一旦进入高收入区间（年应纳税所得额超96万，税率45%），税负压力巨大。</p><h3 id=\"s1-2\">1.2 合作关系：劳务报酬所得</h3><p>如果主播以独立身份与MCN机构或品牌方合作，不建立劳动关系，则收入属于劳务报酬所得。单次收入不超过4000元的减除800元费用，超过4000元的减除20%费用。劳务报酬在预扣预缴时适用20%-40%的超额累进预扣率，年度终了并入综合所得汇算清缴。注意：MCN机构作为支付方仍需履行代扣代缴义务。</p><h3 id=\"s1-3\">1.3 个体经营模式：经营所得</h3><p>主播以个体工商户或个人独资企业名义与平台/MCN签约，独立经营、自负盈亏，则收入属于经营所得。适用5%-35%超额累进税率，可以扣除经营成本和费用。以前通过核定征收可以大幅降低税负，但41号公告后文娱行业的核定征收已基本\"退场\"。</p><h2 id=\"s2\">二、工作室模式的\"前世今生\"</h2><h3 id=\"s2-1\">2.1 核定征收时代的\"黄金模式\"</h3><p>在2021年以前，主播设立个人独资企业/合伙企业，通过核定征收（通常核定应税所得率5%-20%）将实际税负控制在3%-7%左右，相比45%的个税最高税率，节税效果显著。但这种模式的\"命门\"在于——核定征收的合法性前提是账簿不健全、无法查账，而非\"主动选择\"。一旦税务机关认定实际收入远超核定数，之前的核定征收将被推翻，全部收入改按查账征收补税。</p><h3 id=\"s2-2\">2.2 后核定征收时代的合规出路</h3><p>2021年41号公告后，持有权益性投资的个独企业一律查账征收；对文娱行业的新设个独企业，核定征收审批已基本停止。合规路径：①接受查账征收，建立规范账簿，准确核算收入和成本费用；②注册有限公司，按企业所得税（小微企业优惠税率5%）+分红个税20%的双重税负模式运营（综合税负约24%）；③对于收入规模不大的主播，以自然人身份按劳务报酬纳税（综合所得汇算时各项扣除可以降低实际税负）。</p><h2 id=\"s3\">三、MCN机构的合规要点与风险\"高压线\"</h2><p>MCN机构在主播税务合规中扮演着关键角色，也是税务机关稽查的重点对象。核心风险点：①未履行代扣代缴义务——对签约主播的工资薪金和劳务报酬，MCN机构有法定代扣代缴义务；②利用\"阴阳合同\"拆分收入——将主播的高额收入通过多个关联公司或灵活用工平台分拆成多笔小额收入以规避个税（这是薇娅案的核心违法手段）；③\"转换收入性质\"——将本应属于工资薪金或劳务报酬的收入包装为经营所得（如虚构业务分包关系）。</p><p>在当前的监管环境下，MCN机构的最佳策略是\"合规优先\"：建立完善的主播收入台账、依法履行代扣代缴义务、避免任何形式的\"收入拆分\"和\"性质转换\"操作、定期邀请第三方税务顾问进行合规审计。在直播行业\"头部主播被查\"已成常态的背景下，合规不是成本，而是经营的\"安全边际\"。</p>"""

BODIES["nashui-xinyong-dengji-xiufu"] = """<p>纳税信用等级是企业的一张\"税务身份证\"。A级企业享受发票按需领用、绿色通道办税、出口退税优先办理的便利；D级企业却在发票供应、融资贷款、招投标等方方面面受限。但很多企业直到被降级才发现——原来一笔逾期申报、一张不合规发票就足以让多年经营的信用等级\"断崖式下跌\"。本文从评价指标、扣分机制、D级影响与修复路径四个维度，提供纳税信用管理的完整实操指南。</p><h2 id=\"s1\">一、纳税信用的评价体系与指标</h2><h3 id=\"s1-1\">1.1 五个等级的分值标准</h3><p>A级：年度评价指标得分90分以上；B级：70分以上不满90分；M级：新设立企业或评价年度内无生产经营收入且得分70分以上（过渡性等级）；C级：40分以上不满70分；D级：不满40分或存在直接判D级情形。</p><p>企业可以在电子税务局实时查询当前的扣分情况和预评等级，做到\"动态监控\"。常见的扣分项中，逾期申报（每次扣5分）、未按规定报送涉税资料（每次扣3-5分）、发票违规（根据严重程度扣3-11分）是最高频的失分项。</p><h3 id=\"s1-2\">1.2 \"一票否决\"——直接判D的情形</h3><p>以下情形无需看分数，直接判定为D级：①存在逃避缴纳税款、逃避追缴欠税、骗取出口退税、虚开增值税专用发票等涉税犯罪行为；②非正常户直接责任人员注册登记或负责经营的企业；③由D级纳税人的直接责任人员注册登记或负责经营的企业（关联效应）；④存在税务机关依法认定的其他严重失信情形。其中虚开发票是最常见也最致命的\"一票否决\"项——一旦触及，信用修复需要2年以上。</p><h2 id=\"s2\">二、D级的\"连锁影响\"远比你想象的严重</h2><p>D级的影响不限于税务领域：①发票供应——增值税专用发票限量供应（通常每月限25份以内），普通发票按次限量；②出口退税——审核周期大幅延长（D级企业的出口退税审核时间可能长达6个月以上）；③税收优惠——不得享受资源综合利用增值税即征即退、安置残疾人增值税优惠等政策；④投融资——银行信贷审批中会将D级纳税信用作为负面因素，部分银行直接拒绝D级企业的贷款申请；⑤政府采购和招投标——D级在政府采购评分和工程招投标中可能直接失去资格。</p><p>更值得注意的是\"关联效应\"：D级企业的法定代表人和财务负责人在D级评价期（通常2年）内注册或经营的其他企业，在新办当年不得评为A级。这意味着一个人的纳税信用\"污点\"会影响其名下的所有企业。</p><h2 id=\"s3\">三、从D到B：信用修复的实操路径</h2><h3 id=\"s3-1\">3.1 修复的基本条件</h3><p>信用修复不是\"申请即通过\"——需要满足以下条件：①纠正失信行为（补申报、补缴税款和滞纳金、接受行政处罚）；②失信行为纠正满一定期限（一般失信行为纠正满3个月，严重失信行为纠正满1年）；③在修复申请年度的信用评价中达到相应等级标准；④作出合规承诺。</p><h3 id=\"s3-2\">3.2 修复的操作步骤</h3><p>第一步：通过电子税务局查询完整的扣分明细，找出每一项扣分的原因。第二步：对能纠正的扣分项逐一整改——补申报、补缴税款和滞纳金、更正申报数据。第三步：向主管税务机关提交《纳税信用修复申请表》，附整改证明材料。第四步：税务机关审核通过后，在系统中进行信用修复操作，调整信用等级。整个过程通常需要1-3个月。</p><p>特别提醒：信用修复后通常只能恢复到B级或C级，短时间内很难直接恢复到A级。这是因为A级需要的90分以上得分需要通过一个完整年度的良好表现来积累。因此，\"保持\"比\"修复\"更重要。</p><h2 id=\"s4\">四、预防降级的日常管理建议</h2><p>①建立纳税申报日历——每月/每季的申报截止日期在日历中标注提醒，确保零逾期；②定期登录电子税务局查看信用评价状态——\"实时扣分\"系统可以帮助企业在年度评价前发现并纠正问题；③发票管理\"零容忍\"——虚开发票是纳税信用的\"致命伤\"，一旦触及相关人员将长期受限；④年度自查——每年1-2月进行上一年的纳税信用自查，发现问题在评价结果公布前（4月）尽早纠正。</p>"""

BODIES["dawanqu-geshui-butie"] = """<p>粤港澳大湾区作为国家级战略，自2019年起实施境外高端人才和紧缺人才个人所得税补贴政策——在大湾区九市工作的境外人才，其个人所得税实际税负超过15%的部分由地方政府给予财政补贴，且该补贴本身免征个人所得税。这是一项含金量极高的政策红利，但申请流程中的材料准备、人才认定、时间窗口等环节却让许多符合条件的境外人才\"望而却步\"。本文提供从资格判定到申请完成的全流程实操指南。</p><h2 id=\"s1\">一、政策核心：15%税负\"天花板\"</h2><h3 id=\"s1-1\">1.1 补贴的计算逻辑</h3><p>补贴金额 = 申请年度内在大湾区缴纳的个人所得税已缴税额 - 申请年度个人应纳税所得额 × 15%。举例：某香港高管2025年在广州工作，应纳税所得额200万元，按综合所得税率表已缴纳个税约52万元。按15%计算：200万×15%=30万元。可申请补贴金额 = 52万 - 30万 = 22万元。这22万元由广州市财政直接发放至个人账户，且免征个人所得税。</p><h3 id=\"s1-2\">1.2 适用人群的范围</h3><p>基本条件：①身份——香港/澳门永久居民、取得香港入境计划的香港居民、台湾居民、外国国籍人士、取得国外长期居留权的回国留学人员等；②工作地——在大湾区九市（广州、深圳、珠海、佛山、惠州、东莞、中山、江门、肇庆）工作；③人才认定——符合申请城市的\"境外高端人才\"或\"境外紧缺人才\"认定标准；④工作时间——申请年度内在大湾区内工作满90天以上。</p><p>各市对\"高端人才\"和\"紧缺人才\"的认定标准有差异。广州侧重学历（博士）、职称（正高级）和年薪门槛；深圳侧重人才认定证书（如孔雀计划、鹏城学者等）；珠海和佛山对港澳居民更为友好，认定门槛相对较低。</p><h2 id=\"s2\">二、申请全流程与关键材料</h2><h3 id=\"s2-1\">2.1 时间窗口</h3><p>各市通常在每年6-8月受理上一年度的个税补贴申请。以2026年为例，受理的是2025年度的补贴。窗口期通常只有2-3个月，错过则当年不再受理。强烈建议在每年年初（1-3月）就开始准备申请材料，切勿等到窗口开放后才\"临时抱佛脚\"。</p><h3 id=\"s2-2\">2.2 核心材料清单</h3><p>①个人身份证明（港澳居民来往内地通行证/护照等）；②人才资格认定材料——这是最容易出问题的环节，需提供学历学位证书（经教育部认证）、职称证书、人才认定证书等；③劳动合同或派遣证明——需体现工作岗位、工作地点和合同期限；④在大湾区工作的天数证明——出入境记录（可从移民局小程序获取）、考勤记录、差旅记录等；⑤完税证明和个税申报记录——在个人所得税APP中可下载；⑥个人承诺书——承诺申请材料真实有效。</p><h3 id=\"s2-3\">2.3 常见被拒原因</h3><p>排名前三的被拒原因：①人才认定材料不充分——学历证书未认证、职称证书不符合当地认定标准；②工作天数证明不足——仅提供劳动合同但无实际在粤工作的考勤和出入境记录；③在多个城市同时申请——同一人同一年度只能选择一个城市申请，多地重复申请会被直接退回。</p><h2 id=\"s3\">三、与大湾区外籍人才相关的其他税务优惠</h2><p>除个税补贴外，大湾区外籍人才还可关注：①符合条件的非居民个人可选择享受税收协定待遇（如中港税收安排中关于董事费、退休金等的规定）；②在大湾区工作的外籍个人如符合居住天数条件（在中国境内居住满183天），可依法享受各项专项附加扣除（子女教育、住房租金等）；③横琴和前海等特殊区域还有额外的人才奖励和补贴政策。建议外籍人才在入职大湾区前，向专业税务顾问进行一次\"税务体检\"，全面了解可享受的各项优惠和合规义务。</p>"""

BODIES["hainan-ziyougang-shuangshiwu"] = """<p>海南自贸港\"双15%\"——企业所得税15%和个人所得税15%——是近年来最具吸引力的区域税收优惠政策。无数企业\"闻风而动\"，在海南注册了大量公司。然而，\"注册在海南、业务在全中国\"的\"空壳注册\"模式正在被税务机关逐一击破——\"实质性运营\"四个字，成为决定企业能否真正享受优惠的关键。本文从政策条件、实质性运营判定、海南与大湾区对比、迁移税务影响四个维度展开分析。</p><h2 id=\"s1\">一、企业所得税15%：\"实质性运营\"是核心门槛</h2><h3 id=\"s1-1\">1.1 适用的产业范围</h3><p>鼓励类产业企业（以《海南自由贸易港鼓励类产业目录》为准）且主营业务收入占总收入60%以上的，减按15%税率征收企业所得税。产业范围涵盖旅游业、现代服务业、高新技术产业三大领域，具体包括旅游业、酒店住宿、医疗健康、文化体育、教育服务、航空航运、种业、深海科技、商业航天等。</p><h3 id=\"s1-2\">1.2 实质性运营的四维度判定</h3><p>实质性运营的核心判定标准包括四个维度：①生产经营场所——在海南自贸港有固定的生产经营场所（自有或租赁均可，需提供租赁合同、水电费发票等佐证）；②从业人员——主要生产经营人员在海南实际工作，且高级管理人员每年在海南居住满183天；③财务核算——会计账簿和财务核算在海南完成，会计档案在海南保管；④资产管理——主要资产在海南使用和管理。</p><p>实务中的高风险模式：仅在海南设一个\"注册办公室\"，委派一名兼职财务人员，核心管理团队和业务人员全部在内地——这种\"空壳\"模式在2024年后的税务核查中几乎100%被否定。一旦被否定，需补缴25%与15%之间的企业所得税差额加滞纳金。</p><h2 id=\"s2\">二、个税15%：高端人才和紧缺人才专属</h2><p>个税15%优惠适用于在海南自贸港工作的高端人才和紧缺人才。与海南企业所得税15%不同，个税15%优惠需要先行缴纳个税，超过15%的部分由政府财政补贴——是\"先征后返\"模式，不是\"直接按15%缴税\"。适用收入类型为来源于海南的综合所得（工资薪金等）、经营所得以及经海南省认定的人才补贴性所得。需注意：股权转让所得、股息红利所得等资本性收入不在优惠范围内。</p><h2 id=\"s3\">三、海南 vs 大湾区：决策框架</h2><h3 id=\"s3-1\">3.1 核心政策差异对比</h3><p>企业所得税：海南15%（鼓励类产业），大湾区15%仅适用于高新技术企业（全国统一政策）和横琴、前海特定区域企业。覆盖面上海南更广。个人所得税：海南15%上限适用于高端/紧缺人才，大湾区个税补贴仅针对境外人才（\"先征后返\"模式）。增值税和其他税种：海南对鼓励类产业的进口自用生产设备免征关税，对原辅料\"零关税\"——这是大湾区不具备的政策优势。</p><h3 id=\"s3-2\">3.2 决策场景建议</h3><p>如果你的企业属于以下情形，海南是更优选：①属于鼓励类产业且有能力在海南实现实质性运营（如旅游业、康养医疗、热带农业、航运物流等）；②大量进口设备和原辅料（可享受零关税）；③新设企业而非存量企业迁移（避免迁移的税务清算成本）。如果你的企业属于以下情形，大湾区更合适：①业务和市场主要在大湾区（接近客户和供应链）；②属于高新技术企业（可直接享受15%税率，无需额外注册在特定区域）；③对人才吸引力要求高（大湾区人才储备远超海南）。</p><p>最终建议：在做海南注册决策前，务必请专业税务顾问进行\"实质性运营可行性评估\"——注册公司的成本很低，但被认定为不符合实质性运营后的补税成本可能极高。\"先注册再说\"的策略在新监管环境下已不再适用。</p>"""

BODIES["shebao-rushui-xinchou-guihua"] = """<p>社保入税（社会保险费征收职责划转税务机关）是企业人力资源管理领域近年最大的合规变革。在过去，社保部门与税务部门数据不互通时，企业\"按最低基数缴纳社保\"几乎是普遍做法。但社保入税后，税务机关可以对企业申报的个人所得税工资数据与社保缴费基数进行直接交叉比对——\"低基数缴费\"的红利期已经结束。本文在合规框架下，提供薪酬结构优化的合法合规方案。</p><h2 id=\"s1\">一、社保缴费基数的正确确定</h2><h3 id=\"s1-1\">1.1 \"工资\"的范围比你想象的更广</h3><p>社保缴费基数原则上为职工上一年度月平均工资。\"工资\"的口径按照国家统计局《关于工资总额组成的规定》执行，包括六大类：计时工资、计件工资、奖金（含年终奖）、津贴和补贴、加班工资、特殊情况下支付的工资。实务中容易被忽视的计入项：①通讯补贴、交通补贴、餐补等以现金形式发放的补贴；②季度奖、半年奖等各类奖金；③以实物形式发放的福利（按市场公允价值折算）；④企业为员工支付的商业保险费（部分类型需计入）。不计入的项目范围很窄，主要包括：独生子女补贴、出差伙食补助、误餐补助、调动工作的旅费和安家费等少数法定排除项。</p><h3 id=\"s1-2\">1.2 基数上限和下限</h3><p>社保缴费基数有上下限：上限为当地上年度全口径城镇单位就业人员平均工资的300%，下限为当地平均工资的60%。只要实际工资在60%-300%范围内，就按实际工资为基数缴纳——\"低于实际工资按最低基数缴纳\"在法规上没有依据。</p><h2 id=\"s2\">二、合规的薪酬结构优化方案</h2><h3 id=\"s2-1\">2.1 固定工资与浮动绩效的配比调整</h3><p>将部分固定薪酬转换为与业绩挂钩的浮动绩效。例如：原月薪2万元全部为固定工资，社保基数2万元；调整为固定工资1万元+浮动绩效1万元（绩效根据季度考核结果发放），则社保基数变为1万元（浮动绩效在实现前不属于\"工资\"）。前提是：①绩效方案必须有明确的考核标准和发放规则；②不能是\"名义绩效\"（即无论业绩如何都全额发放）；③需要有真实的绩效考核记录。</p><h3 id=\"s2-2\">2.2 合理利用法定\"不计入\"项目</h3><p>以下几类支出不计入工资总额从而不影响社保基数：①符合条件的集体福利——员工食堂、班车、健身房等非现金集体福利支出；②劳动保护用品支出——如工作服、安全帽、防护用品等；③出差补助和误餐补助——需有真实的出差记录和合理标准；④职工教育经费——符合条件的培训费用（需在工资总额的2.5%以内）。</p><h3 id=\"s2-3\">2.3 灵活用工的合规边界</h3><p>对于临时性、辅助性、替代性的非核心岗位，可以考虑通过劳务外包或灵活用工平台实现\"去劳动关系化\"。但必须符合\"外包三要素\"：①劳务人员在承包方（如外包公司）的管理下工作，而非接受发包方（你的企业）的日常管理；②工作成果按约定标准验收，而非按工作时间和过程管理；③承包方自主安排人员和工作方式。被认定为\"假外包、真雇佣\"的，发包方将被要求补缴全部社保费用并承担处罚——这不是\"筹划\"而是\"违法\"。</p><h2 id=\"s3\">三、社保合规的\"避坑清单\"</h2><p>①不要\"全员最低基数\"——这是税务机关最容易识别的模式，一旦全员工资申报个税但社保全部按最低基数，系统直接预警；②不要\"新入职一律试用期工资\"——试用期工资可以低于转正工资，但不能低于本单位同岗位最低档工资的80%或劳动合同约定工资的80%；③不要\"实习生和兼职不缴社保\"——非全日制用工（每天不超过4小时、每周不超过24小时）只需缴纳工伤保险，但全日制实习生实际上建立了劳动关系，需要缴纳社保；④年终奖分摊计入各月平均工资计算下一年度社保基数——这是一把\"双刃剑\"，会让你的基数在下一年度上升。</p><p>社保合规不是一道\"做与不做\"的选择题，而是一道\"早做与晚做\"的时间题。在社保入税的大背景下，越早完成合规改造，面临的追溯风险和滞纳金成本越低。</p>"""

# Load JSON
with open(JSON_PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Set bodies
target_slugs = list(BODIES.keys())
for a in data:
    if a['slug'] in target_slugs:
        a['body'] = BODIES[a['slug']]
        print(f'Set body: {a["slug"]} ({len(a["body"])} chars)')

# Save
with open(JSON_PATH, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# Generate HTML
print('\n--- Generating HTML ---')
sys.path.insert(0, os.path.join(BASE_DIR, 'tools'))
from generate_articles import (
    load_static_sections, generate_meta_section, generate_jsonld, generate_hero_section,
    generate_breadcrumb, generate_related_cards, generate_article_notice,
    generate_view_counter_js, ARTICLES_DIR
)

static = load_static_sections()

for article in data:
    if article['slug'] not in target_slugs:
        continue
    slug = article['slug']
    sf = article.get('source_filename', f'{slug}(source).html')
    fp = os.path.join(ARTICLES_DIR, sf)
    
    parts = []
    parts.append(generate_meta_section(article))
    parts.append(static['css'])
    parts.append('\n')
    parts.append(generate_jsonld(article))
    parts.append('</head>\n<body>\n')
    parts.append(static['nav'])
    parts.append('\n<main>\n')
    parts.append(generate_hero_section(article))
    parts.append(static['search'])
    parts.append(static['layout_start'])
    parts.append(generate_breadcrumb(article))
    parts.append('\n<!-- ===== 正文 ===== -->\n<article class="article-body">\n')
    parts.append(article['body'])
    parts.append('\n')
    parts.append(generate_related_cards(article))
    parts.append('  <div class="related-cta">\n    <p><em>如需了解更多专业财税服务，欢迎联系存勤法税。</em></p>\n    <p>&#x1f4de; <strong>咨询热线</strong>：13556116691（微信同号）</p>\n  </div>\n\n</article>\n\n')
    parts.append(generate_article_notice())
    parts.append('\n  </div><!-- .article-main -->\n</div><!-- .article-layout -->\n')
    parts.append(static['more'])
    footer = static['footer']
    old_vc = re.compile(r'<script>\s*/\* ===== 动态阅读量计数 ===== \*/\s*\(function\(\).*?\}\)\)\(\);\s*</script>', re.DOTALL)
    footer = old_vc.sub(generate_view_counter_js(article), footer)
    parts.append(footer)
    
    html = '\n'.join(parts)
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(html)
    
    ok = all(['jumpToMatch' in html, f'view-{slug}' in html, '"@type": "Article"' in html, '"@type": "FAQPage"' in html, 'og:title' in html])
    print(f'  [{slug}] {"OK" if ok else "WARN"} | {len(html)} chars')

# Run update_indexes and hexo generate
print('\n--- Running update_indexes ---')
subprocess.run([PYTHON, os.path.join(BASE_DIR, 'tools', 'update_indexes.py')])

# Fix duplicates
print('\n--- Fixing duplicate entries ---')
import re as re_m

# Fix archives - add missing cards
archives_path = f'{BASE_DIR}/source/archives/法税洞察(source).html'
with open(archives_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find articles NOT in archives
existing = set(re.findall(r'../articles/([^"]+)\.html', content))
new_cards = []
for article in data:
    if article['slug'] not in target_slugs:
        continue
    if article['slug'] in existing:
        continue
    slug = article['slug']
    title = article['title'].replace('"', '&quot;')
    cat = article.get('category', '实操指南')
    date = article.get('date', '2026-05-27')
    views = article.get('base_views', 100)
    day = date.split('-')[2]
    ym = f'{date.split("-")[0]}.{date.split("-")[1]}'
    body_text = re.sub(r'<[^>]+>', '', article.get('body', ''))
    body_text = re.sub(r'\s+', '', body_text)
    desc = body_text[:80]
    
    card = f'''      <a href="../articles/{slug}.html" class="article-item" data-date="{date}" data-category="{cat}" data-views="{views}">
        <div class="article-date">
          <div class="day">{day}</div>
          <div class="month">{ym}</div>
        </div>
        <div class="article-content">
          <h3>{title}</h3>
          <p>{desc}</p>
          <span class="article-tag">{cat}</span>
</div>
        <div class="article-arrow"><i class="fas fa-chevron-right"></i></div>
      </a>'''
    new_cards.append(card)

if new_cards:
    first = content.find('<a href="../articles/')
    insert = first
    cards_html = '\n\n'.join(new_cards) + '\n\n'
    new_content = content[:insert] + cards_html + content[insert:]
    with open(archives_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f'Archives: added {len(new_cards)} new cards')

# Fix sitemap dedup
sitemap_path = f'{BASE_DIR}/source/sitemap.xml'
with open(sitemap_path, 'r', encoding='utf-8') as f:
    sc = f.read()
url_blocks = re_m.findall(r'  <url>.*?</url>', sc, re_m.DOTALL)
seen = set()
unique = []
for b in url_blocks:
    loc = re_m.search(r'<loc>(.*?)</loc>', b)
    if loc and loc.group(1) not in seen:
        seen.add(loc.group(1))
        unique.append(b)
header_end = sc.find('  <url>')
new_sc = sc[:header_end] + '\n'.join(unique) + '\n</urlset>\n'
with open(sitemap_path, 'w', encoding='utf-8') as f:
    f.write(new_sc)
print(f'Sitemap: {len(url_blocks)} -> {len(unique)} unique')

# Fix search-index dedup
si_path = f'{BASE_DIR}/source/search-index.json'
with open(si_path, 'r', encoding='utf-8') as f:
    si = json.load(f)
seen_urls = set()
unique_si = []
for entry in si:
    if entry['url'] not in seen_urls:
        seen_urls.add(entry['url'])
        unique_si.append(entry)
with open(si_path, 'w', encoding='utf-8') as f:
    json.dump(unique_si, f, ensure_ascii=False, indent=2)
print(f'Search-index: {len(si)} -> {len(unique_si)} unique')

print('\n--- Running hexo generate ---')
os.chdir(BASE_DIR)
subprocess.run(['npx', 'hexo', 'generate'], shell=True)

print('\nDone! Articles #6-#10 generated.')
