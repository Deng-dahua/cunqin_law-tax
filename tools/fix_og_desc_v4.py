"""修复 hehuo/simu og:description - 逐行替换"""
import os

base = r'C:\Users\26726\WorkBuddy\2026-05-20-21-20-24\source\articles'

fixes = {
    'hehuo-qiye-shuiwu-jiexi(source).html':
        '企业合伙经营中的税务处理复杂性常被低估。本文从合伙人层面深度解析所得性质穿透、费用扣除与亏损弥补规则，帮助华南地区合伙制企业理清税务合规思路。存勤法税（广州）深耕粤港澳大湾区财税服务市场18年，以业管财税法融合方法论为华南企业提供专业解决方案。',
    'simu-jijin-shuiwu-chouhua(source).html':
        '私募基金全生命周期税务规划是机构竞争力的核心要素。本文从基金架构选择、LP与GP税务筹划、投资收益确认及退出环节税负优化等维度，为大湾区私募机构提供专业税务规划指引。存勤法税（广州）由邓达华创立，专注服务华南地区企业。',
}

for fname, new_desc in fixes.items():
    fp = os.path.join(base, fname)
    with open(fp, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    for line in lines:
        if 'property="og:description"' in line:
            new_lines.append(f'<meta property="og:description" content="{new_desc}">\n')
        elif 'name="description"' in line and 'twitter' not in line and 'apple' not in line and 'msapplication' not in line and 'theme-color' not in line and 'baidu' not in line and 'msvalidate' not in line:
            # This is the meta description (not twitter or other meta)
            if '<meta name="description"' in line:
                new_lines.append(f'<meta name="description" content="{new_desc}">\n')
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)
    
    with open(fp, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print(f'  ✓ {fname}: {len(new_desc)} chars')

print('Done')
