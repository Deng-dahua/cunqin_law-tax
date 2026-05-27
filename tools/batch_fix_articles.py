"""Batch fix all 28 articles:
1. 4 articles: convert last section heading to 结语
2. 18 articles: add 延伸阅读 + CTA before </article>
3. 6 articles: add 3rd related card
Also ensure all articles have properly closed </h3> for 延伸阅读
"""
import os, re, sys
sys.stdout.reconfigure(encoding='utf-8')

articles_dir = 'source/articles'

# Standard 3-card 延伸阅读 template (static cards, not dynamic)
def make_related_section(card3_info):
    """Generate 延伸阅读 + CTA section. card3_info = (url, cat, title, excerpt)"""
    url, cat, title, excerpt = card3_info
    return f'''<div class="related-reading">
    <h3 id="延伸阅读" class="related-heading"><span>延伸阅读</span></h3>
    <div class="related-grid">
      <a href="jinshui-siqi-yingdui.html" class="related-card">
        <span class="related-cat">政策解读</span>
        <div class="related-info">
          <h4>金税四期全面解读与企业应对策略</h4>
          <p>金税四期的核心变化及企业合规应对路径</p>
        </div>
        <span class="related-arrow"><i class="fas fa-arrow-right"></i></span>
      </a>
      <a href="qiye-shuiwu-fengxian.html" class="related-card">
        <span class="related-cat">实操指南</span>
        <div class="related-info">
          <h4>企业税务风险防控实务</h4>
          <p>常见税务风险点及应对策略</p>
        </div>
        <span class="related-arrow"><i class="fas fa-arrow-right"></i></span>
      </a>
      <a href="{url}" class="related-card">
        <span class="related-cat">{cat}</span>
        <div class="related-info">
          <h4>{title}</h4>
          <p>{excerpt}</p>
        </div>
        <span class="related-arrow"><i class="fas fa-arrow-right"></i></span>
      </a>
    </div>
  </div>
  <div class="related-cta">
    <p><em>如需了解更多专业财税服务，欢迎联系存勤法税。</em></p>
    <p>&#x1f4de; <strong>咨询热线</strong>：13556116691（微信同号）</p>
<p>华南地区企业正面临前所未有的税务合规挑战。存勤法税（广州）以实战经验为依托，为粤港澳大湾区企业保驾护航。</p>

  </div>
'''

# ===== Part 1: Fix 4 articles missing 结语 =====
# Rename the last H2 to "结语", keeping original content below it
jieyu_fixes = ['2026年税务稽查重点预警(source).html',
               '新公司法注册资本实缴的税务影响(source).html',
               '股权激励全周期税务规划(source).html',
               '转让定价与关联交易反避税实战指南(source).html']

for fname in jieyu_fixes:
    path = os.path.join(articles_dir, fname)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    article_end = content.rfind('</article>')
    body_end = content[:article_end]
    
    h2_matches = list(re.finditer(r'<h2 id="([^"]*)">([^<]*)</h2>', body_end))
    
    if h2_matches:
        last_h2 = h2_matches[-1]
        old_id = last_h2.group(1)
        old_text = last_h2.group(2)
        old_tag = f'<h2 id="{old_id}">{old_text}</h2>'
        new_tag = f'<h2 id="结语">结语</h2>'
        # Only replace the last occurrence
        pos = content[:article_end].rfind(old_tag)
        if pos != -1:
            content = content[:pos] + new_tag + content[pos+len(old_tag):]
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f'  [结语] {fname}: {old_text} -> 结语')
        else:
            print(f'  [结语] {fname}: WARNING - tag not at rfind position')
    else:
        print(f'  [结语] {fname}: WARNING - no h2 found')

# ===== Part 2: Add 延伸阅读 + CTA to 18 articles =====
missing_related = [
    'CRS-kuajing-zichan-shenbao(source).html',
    'chengben-feiyong-shuiwu-hegui(source).html',
    'chukou-tuishui-hegui-fengkong(source).html',
    'geren-suodeshui-huisuan-qingjiao(source).html',
    'gongzixinjin-gerensuodeshui-chouhua(source).html',
    'gudong-hongli-shuiwu-chouhua(source).html',
    'guquan-daichi-shuiwu-fengxian(source).html',
    'guquan-zhuantang-geren-suodeshui(source).html',
    'hehuo-qiye-shuiwu-jiexi(source).html',
    'qiye-kuisun-mibu-guize(source).html',
    'qiyesuodeshui-huisuan-qingjiao(source).html',
    'shuiwu-xingzheng-fuyi(source).html',
    'shuzihua-shuiwu-guanli-zhuanxing(source).html',
    'simu-jijin-shuiwu-chouhua(source).html',
    'xukai-fapiao-falv-houguo(source).html',
    'yanfa-feiyong-jiakou-kouchu(source).html',
    'yinhua-shuifa-shishi-yaodian(source).html',
    'zengzhishui-liudi-tuishui(source).html',
    'zhongxiao-qiye-shuishou-youhui(source).html',
]

# Pick appropriate 3rd cards for each article based on topic
card3_map = {
    'CRS-kuajing-zichan-shenbao': ('kuajing-dianshang-shuiwu.html', '跨境税务', '跨境电商税务合规全解析', '跨境电商出口退税与合规要点'),
    'chengben-feiyong-shuiwu-hegui': ('qiye-shuiwu-fengxian.html', '实操指南', '企业税务风险防控实务', '常见税务风险点及应对策略'),
    'chukou-tuishui-hegui-fengkong': ('kuajing-dianshang-shuiwu.html', '跨境税务', '跨境电商税务合规全解析', '跨境电商出口退税与合规要点'),
    'geren-suodeshui-huisuan-qingjiao': ('gongzixinjin-gerensuodeshui-chouhua.html', '个税规划', '工资薪金个人所得税筹划', '薪酬结构优化与个税合规路径'),
    'gongzixinjin-gerensuodeshui-chouhua': ('geren-suodeshui-huisuan-qingjiao.html', '个税指南', '个人所得税汇算清缴实务指南', '年度汇算清缴操作要点与技巧'),
    'gudong-hongli-shuiwu-chouhua': ('guquan-zhuantang-geren-suodeshui.html', '股权税务', '股权转让个人所得税处理实务', '股权转让个税的计算与申报'),
    'guquan-daichi-shuiwu-fengxian': ('guquan-zhuantang-geren-suodeshui.html', '股权税务', '股权转让个人所得税处理实务', '股权转让个税的计算与申报'),
    'guquan-zhuantang-geren-suodeshui': ('gudong-hongli-shuiwu-chouhua.html', '股东税务', '股东红利分配税务筹划', '股息红利的税务处理与优化'),
    'hehuo-qiye-shuiwu-jiexi': ('guquan-jiagou-shuiwu-chouhua.html', '深度分析', '股权架构全解析与税务规划', '不同持股模式下的税务影响与优化方案'),
    'qiye-kuisun-mibu-guize': ('qiyesuodeshui-huisuan-qingjiao.html', '汇算清缴', '企业所得税汇算清缴实务要点', '年度申报操作流程与注意事项'),
    'qiyesuodeshui-huisuan-qingjiao': ('qiye-kuisun-mibu-guize.html', '亏损处理', '企业亏损弥补规则详解', '亏损弥补的年限、顺序与操作要点'),
    'shuiwu-xingzheng-fuyi': ('qiye-shuiwu-fengxian.html', '实操指南', '企业税务风险防控实务', '常见税务风险点及应对策略'),
    'shuzihua-shuiwu-guanli-zhuanxing': ('shudian-fapiao-quanmian-shishi.html', '实操指南', '数电发票全面实施企业应对指南', '数电发票的申领、开具与管理要点'),
    'simu-jijin-shuiwu-chouhua': ('guquan-jiagou-shuiwu-chouhua.html', '深度分析', '股权架构全解析与税务规划', '不同持股模式下的税务影响与优化方案'),
    'xukai-fapiao-falv-houguo': ('qiye-shuiwu-fengxian.html', '实操指南', '企业税务风险防控实务', '常见税务风险点及应对策略'),
    'yanfa-feiyong-jiakou-kouchu': ('gaoxin-qiye-shuiwu.html', '研发优惠', '高新技术企业税务全攻略', '高新技术企业认定的税务优惠体系详解'),
    'yinhua-shuifa-shishi-yaodian': ('shudian-fapiao-quanmian-shishi.html', '实操指南', '数电发票全面实施企业应对指南', '数电发票的申领、开具与管理要点'),
    'zengzhishui-liudi-tuishui': ('zengzhishuifa-shishi-yingdui.html', '政策解读', '增值税法正式实施企业影响与应对', '增值税法核心变化及企业实操应对'),
    'zhongxiao-qiye-shuishou-youhui': ('gaoxin-qiye-shuiwu.html', '税收优惠', '高新技术企业税务全攻略', '高新技术企业认定的税务优惠体系详解'),
}

for fname in missing_related:
    path = os.path.join(articles_dir, fname)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    slug = fname.replace('(source).html', '')
    card3 = card3_map.get(slug, ('qiye-shuiwu-fengxian.html', '实操指南', '企业税务风险防控实务', '常见税务风险点及应对策略'))
    
    related_html = make_related_section(card3)
    
    # Insert before </article>
    old = '\n\n</article>'
    new = '\n\n' + related_html + '\n</article>'
    
    if old in content:
        content = content.replace(old, new, 1)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'  [延伸阅读+CTA] {fname}')
    else:
        print(f'  [延伸阅读+CTA] {fname}: WARNING - pattern not found')

# ===== Part 3: Add 3rd card to 6 articles with only 2 =====
add_3rd_card = {
    '专精特新企业税收优惠政策深度解读(source).html': ('gaoxin-qiye-shuiwu.html', '关联专题', '高新技术企业税务全攻略', '高新技术企业认定的税务优惠体系详解'),
    '企业减资撤资全套税务处理指南(source).html': ('guquan-jiagou-shuiwu-chouhua.html', '深度分析', '股权架构全解析与税务规划', '不同持股模式下的税务影响与优化方案'),
    '家族财富传承税务考量与规划(source).html': ('guquan-zhuantang-geren-suodeshui.html', '股权税务', '股权转让个人所得税处理实务', '股权转让个税的计算与申报'),
    '对赌协议税务处理全解析(source).html': ('guquan-jiagou-shuiwu-chouhua.html', '深度分析', '股权架构全解析与税务规划', '不同持股模式下的税务影响与优化方案'),
    '平台经济灵活用工的税务合规(source).html': ('geren-suodeshui-huisuan-qingjiao.html', '个税指南', '个人所得税汇算清缴实务指南', '年度汇算清缴操作要点与技巧'),
    '新公司法注册资本实缴的税务影响(source).html': ('guquan-jiagou-shuiwu-chouhua.html', '深度分析', '股权架构全解析与税务规划', '不同持股模式下的税务影响与优化方案'),
}

for fname, (url, cat, title, excerpt) in add_3rd_card.items():
    path = os.path.join(articles_dir, fname)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    third_card = f'''      <a href="{url}" class="related-card">
        <span class="related-cat">{cat}</span>
        <div class="related-info">
          <h4>{title}</h4>
          <p>{excerpt}</p>
        </div>
        <span class="related-arrow"><i class="fas fa-arrow-right"></i></span>
      </a>\n    </div>'''
    
    # Find the 2nd card's closing </a> before </div> (closing related-grid)
    # Pattern: 2nd card ends with </a>\n    </div>
    old = '</a>\n    </div>'
    
    if old in content:
        content = content.replace(old, third_card, 1)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'  [3rd card] {fname}')
    else:
        print(f'  [3rd card] {fname}: WARNING - pattern not found')

print('\nDone!')
