"""
GEO 关键词深度挖掘与优化分析
分析62篇文章的关键词覆盖、发现缺口、给出优化建议
"""
import sys, re, glob, os, json
from collections import Counter, defaultdict
sys.stdout.reconfigure(encoding='utf-8')

BASE = r'C:\Users\26726\WorkBuddy\2026-05-20-21-20-24'
articles_dir = os.path.join(BASE, 'source', 'articles')

# ============ 1. 提取并分析所有文章的关键词 ============
all_keywords = Counter()
article_meta = []  # [(filename, h1, keywords list, category)]

files = sorted(glob.glob(os.path.join(articles_dir, '*.html')))
for fp in files:
    bn = os.path.basename(fp).replace('(source).html', '')
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract keywords
    kw_match = re.search(r'name="keywords"\s+content="([^"]*)"', content)
    keywords = []
    if kw_match:
        keywords = [k.strip() for k in kw_match.group(1).split(',')]
        for k in keywords:
            all_keywords[k] += 1
    
    # Extract H1
    h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', content)
    h1 = h1_match.group(1) if h1_match else 'N/A'
    
    # Extract category from permalink context
    article_meta.append((bn, h1, keywords))

# ============ 2. 分析关键词分布 ============
print("=" * 70)
print("一、关键词频率分析 (Top 30)")
print("=" * 70)
for kw, count in all_keywords.most_common(30):
    bar = '█' * min(count, 10)
    print(f"  {kw:30s}  {count:3d}次  {bar}")

# 品牌关键词
brand_kws = ['存勤法税', '业管财税法', '邓达华', '财税顾问', '税务筹划']
brand_count = sum(all_keywords.get(k, 0) for k in brand_kws)
print(f"\n品牌关键词覆盖: {brand_count} 次")

# ============ 3. 关键词类别分析 ============
print("\n" + "=" * 70)
print("二、关键词主题维度分析")
print("=" * 70)

dimensions = {
    '税种维度': ['增值税', '企业所得税', '个人所得税', '土地增值税', '印花税', '关税',
              '消费税', '房产税', '契税', '资源税', '环保税'],
    '业务场景': ['股权转让', '股权激励', '企业重组', '减资撤资', '注销清算',
              '合并分立', 'IPO上市', '投融资', '关联交易', '转让定价'],
    '合规管理': ['税务合规', '税务风险', '税务稽查', '税务筹划', '税务规划',
              '税务顾问', '税务代理', '税务争议', '行政复议'],
    '行业领域': ['跨境电商', '房地产', '高新技术企业', '专精特新', '中小企业',
              '金融', '私募基金', '制造业', '平台经济', '直播带货'],
    '政策热点': ['金税四期', '数电发票', '以数治税', 'CRS', 'BEPS',
              '碳关税', '双支柱', '自贸港', '大湾区', '新公司法'],
    '地域特色': ['广州', '粤港澳大湾区', '华南', '广东', '海南自贸港', '境外', '跨境'],
}

for dim_name, dim_kws in dimensions.items():
    covered = [(k, all_keywords.get(k, 0)) for k in dim_kws if all_keywords.get(k, 0) > 0]
    missing = [k for k in dim_kws if all_keywords.get(k, 0) == 0]
    total_hits = sum(v for _, v in covered)
    print(f"\n{dim_name}:")
    print(f"  已覆盖: {len(covered)}/{len(dim_kws)} ({total_hits}次)")
    if covered:
        top = sorted(covered, key=lambda x: -x[1])[:5]
        print(f"  Top: {', '.join(f'{k}({v})' for k,v in top)}")
    if missing:
        print(f"  缺失: {', '.join(missing)}")

# ============ 4. 每篇文章关键词质量评分 ============
print("\n" + "=" * 70)
print("三、关键词质量评估（按数量 + 覆盖率）")
print("=" * 70)

# Calculate keyword density per article
for bn, h1, keywords in article_meta:
    kw_count = len(keywords)
    # Check if brand keywords present
    brand_present = sum(1 for k in brand_kws if k in keywords)
    # Check dimension coverage
    dim_coverage = 0
    for dim_kws in dimensions.values():
        if any(k in keywords for k in dim_kws):
            dim_coverage += 1
    
    quality = '★' * min(5, max(1, kw_count // 3 + brand_present + dim_coverage // 2))
    if kw_count < 5 or brand_present < 2:
        print(f"  {quality:5s} [{kw_count:2d}词/{brand_present}品牌/{dim_coverage}维] {bn[:50]}")

# ============ 5. 关键词优化建议 ============
print("\n" + "=" * 70)
print("四、关键词优化建议")
print("=" * 70)

# 5.1 缺失高频词的补充建议
suggestions = []

# 通用品牌词缺失
brand_missing = []
for bn, h1, keywords in article_meta:
    if '存勤法税' not in keywords:
        brand_missing.append(bn)
if brand_missing:
    print(f"\n[P0] {len(brand_missing)}篇文章缺少品牌词'存勤法税':")
    for b in brand_missing[:5]:
        print(f"  - {b}")

# 5.2 长尾关键词建议
print(f"\n[P1] 建议增加的长尾关键词方向：")
long_tail_suggestions = [
    ('广州企业税务顾问', '地域+服务，高转化意图'),
    ('大湾区税务合规咨询', '地域+需求，精准流量'),
    ('金税四期企业应对措施', '热点+实操，搜索量大'),
    ('股权转让个人所得税计算', '问题导向，长尾精准'),
    ('跨境电商出口退税流程', '行业+流程，搜索意图强'),
    ('高新技术企业认定税务优惠', '资质+优惠，B端精准'),
    ('企业注销税务清算步骤', '流程型，问题解决导向'),
    ('CRS金融账户信息交换申报', '专业+实操，高净值人群'),
    ('新公司法五年实缴税务影响', '政策+影响，时效性强'),
    ('数电发票企业操作指南', '工具+指南，操作型搜索'),
]
for kw, reason in long_tail_suggestions:
    print(f"  - {kw} ({reason})")

# 5.3 竞争分析
print(f"\n[P2] 搜索竞争度分析（建议优先优化的低竞争高价值词）：")
low_competition = [
    '广州法税顾问', '大湾区财税咨询', '企业税务风险诊断',
    '股权架构税务优化', '个人所得税汇算清缴代办',
    '海南自贸港税收优惠申请', '专精特新企业税务规划'
]
print('  ' + ' | '.join(low_competition))

print("\n" + "=" * 70)
print("五、推荐优化优先级")
print("=" * 70)

priority_actions = [
    ("P0-立即", "7篇文章 og:description 扩展到120-160字符", "agent处理中"),
    ("P0-立即", "3篇缺失文章添加到法税洞察页+索引", "agent处理中"),
    ("P0-立即", "6篇文章延伸阅读补全≥3篇", "agent处理中"),
    ("P1-今日", "全站 title 标签统一格式", "待处理"),
    ("P1-今日", "每篇文章 keywords 确保覆盖多维关键词", "待处理"),
    ("P2-周内", "税种维度补全：印花税/关税/消费税/房产税/契税等", "待处理"),
    ("P2-周内", "首页 description 扩展到150-160字符", "待处理"),
    ("P3-持续", "每月新增2-3篇长尾关键词文章", "持续"),
]

for prio, action, status in priority_actions:
    print(f"  [{prio}] {action} — {status}")

# Save report
report_path = os.path.join(BASE, 'tools', 'keyword_analysis_report.md')
with open(report_path, 'w', encoding='utf-8') as f:
    f.write("# GEO 关键词深度挖掘与优化报告\n\n")
    f.write(f"**分析范围**: {len(files)} 篇文章\n")
    f.write(f"**唯一关键词数**: {len(all_keywords)}\n\n")
    
    f.write("## 关键词频率 Top 20\n\n")
    f.write("| 关键词 | 频次 |\n|--------|------|\n")
    for kw, count in all_keywords.most_common(20):
        f.write(f"| {kw} | {count} |\n")
    
    f.write("\n## 维度覆盖\n\n")
    for dim_name, dim_kws in dimensions.items():
        covered = [k for k in dim_kws if all_keywords.get(k, 0) > 0]
        missing = [k for k in dim_kws if all_keywords.get(k, 0) == 0]
        f.write(f"### {dim_name}\n")
        f.write(f"- 已覆盖: {len(covered)}/{len(dim_kws)}\n")
        f.write(f"- 缺失: {', '.join(missing) if missing else '无'}\n\n")
    
    f.write("## 优化优先级\n\n")
    for prio, action, status in priority_actions:
        f.write(f"- [{prio}] {action} — {status}\n")

print(f"\n报告已保存: {report_path}")
