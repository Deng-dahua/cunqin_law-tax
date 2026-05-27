"""修复 hehuo 和 simu 两篇文章中 og:description 内嵌引号破坏 HTML 属性的问题"""
import os

base = r'C:\Users\26726\WorkBuddy\2026-05-20-21-20-24\source\articles'

fixes = {
    'hehuo-qiye-shuiwu-jiexi(source).html': {
        'old_text': '"先分后税"',
        'new_desc': '企业合伙经营中的税务处理复杂性常被低估。本文从合伙人层面深度解析所得性质穿透、费用扣除与亏损弥补规则，帮助华南地区合伙制企业理清税务合规思路。存勤法税（广州）深耕粤港澳大湾区财税服务市场18年，提供业管财税法融合解决方案。',
    },
    'simu-jijin-shuiwu-chouhua(source).html': {
        'old_text': '"募投管退"',
        'new_desc': '私募基金全生命周期税务规划是机构竞争力的核心要素。本文从基金架构选择、LP与GP税务筹划、投资收益确认及退出环节税负优化等维度，为大湾区私募机构提供专业税务规划指引。存勤法税（广州）由邓达华创立，专注服务华南地区企业。',
    },
}

for fname, info in fixes.items():
    fp = os.path.join(base, fname)
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace og:description entirely
    import re
    # Match the broken og:description line
    pattern = r'<meta property="og:description" content="[^"]*' + re.escape(info['old_text']) + r'[^"]*"'
    repl_og = f'<meta property="og:description" content="{info["new_desc"]}"'
    content = re.sub(pattern, repl_og, content)
    
    # Replace meta description
    pattern_md = r'<meta name="description" content="[^"]*' + re.escape(info['old_text']) + r'[^"]*"'
    repl_md = f'<meta name="description" content="{info["new_desc"]}"'
    content = re.sub(pattern_md, repl_md, content)
    
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f'  ✓ {fname}: {len(info["new_desc"])} chars')

print('Done')
