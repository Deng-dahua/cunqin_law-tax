"""Fix 2 format issues in all 15 GEO articles:
1. H3_NOT_CLOSED: <h3 id="延伸阅读"...> missing </h3> 
2. CTA_NO_REGIONAL: related-cta missing Guangdong-HK-Macao regional tip line
"""
import os, re

geo_dir = 'source/articles/'

geo_articles = [
    '自然人股权转让核定征收与查账征收(source).html',
    '个体工商户与个人独资企业税务全攻略(source).html',
    '年终奖计税方式选择(source).html',
    '税务注销全流程指南(source).html',
    '发票红冲作废丢失实操指南(source).html',
    '直播带货与网红经济税务合规(source).html',
    '纳税信用等级评定与修复(source).html',
    '大湾区外籍人士个税补贴(source).html',
    '海南自贸港双15税收优惠(source).html',
    '社保入税薪酬合规规划(source).html',
    '企业所得税预缴汇算差异调整(source).html',
    '个人综合所得汇算10种情形(source).html',
    '境外所得税收抵免指南(source).html',
    '碳关税CBAM出口税务影响(source).html',
    '简易计税一般计税选择策略(source).html',
]

# Regional tip line (matching reference article exactly)
REGIONAL_TIP = '<p>对于广州及粤港澳大湾区企业而言，提前做好税务合规布局，是在复杂监管环境下稳健经营的关键。</p>'

for fname in geo_articles:
    fpath = os.path.join(geo_dir, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    changes = []
    
    # Fix 1: H3 closing tag
    # Match: <h3 id="延伸阅读" class="related-heading"><span>延伸阅读</span>
    # Replace with: ...<span>延伸阅读</span></h3>
    old_h3 = '<h3 id="延伸阅读" class="related-heading"><span>延伸阅读</span>'
    new_h3 = '<h3 id="延伸阅读" class="related-heading"><span>延伸阅读</span></h3>'
    if old_h3 in content and new_h3 not in content:
        content = content.replace(old_h3, new_h3)
        changes.append('H3 closed')
    
    # Fix 2: Add regional tip before </div> in related-cta
    # The GEO articles have related-cta ending with </p>\n  </div>
    # We need to add the regional tip before the closing </div>
    # Pattern: the line with 咨询热线</strong>：13556116691（微信同号）</p>
    # followed by whitespace and </div>
    
    # Match the phone line (both literal emoji and HTML entity versions)
    phone_pattern = r'(<p>(?:&#x1f4de;|📞) <strong>咨询热线</strong>：13556116691（微信同号）</p>\s*)</div>\s*\n\s*</article>'
    replacement = r'\1' + REGIONAL_TIP + '\n\n  </div>\n\n</article>'
    new_content = re.sub(phone_pattern, replacement, content)
    
    if new_content != content:
        changes.append('Regional tip added')
        content = new_content
    
    if changes:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'[OK] {fname[:40]}: {", ".join(changes)}')
    else:
        print(f'[SKIP] {fname[:40]}: no changes needed')

print('\nDone!')
