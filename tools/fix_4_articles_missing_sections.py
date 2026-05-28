#!/usr/bin/env python3
"""Fix 4 articles missing 延伸阅读 h3 + cards + related-cta block"""
import os, sys, re
sys.stdout.reconfigure(encoding='utf-8')

BASE = r'C:\Users\26726\WorkBuddy\2026-05-20-21-20-24'
ARTICLES = os.path.join(BASE, 'source', 'articles')

# Define related readings for each article
# Format: (slug, category, title, excerpt)
RELATED = {
    'qishui-zhengce-jiedu': [
        ('tudi-zengzhishui-qingsuan-chouhua', '税务实务', '土地增值税清算实务与筹划策略：应纳税额计算、扣除项目与税收优惠', '土地增值税清算的触发条件、扣除项目的认定标准、不同清算方式的税负比较，以及清算中的常见争议与合规要点'),
        ('fangdichan-qiye-shuiwu-chouhua', '税务筹划', '房地产企业全流程税务筹划：从拿地到清算的节税方案', '房地产企业在拿地、开发、预售、竣工和清算各阶段的税务成本管控与筹划要点'),
        ('qiye-zhongzu-shuiwu', '企业重组', '企业重组与重大交易中的税务规划要点', '资产收购、股权收购、合并分立等重组交易中企业所得税、增值税、契税和土地增值税的优惠处理')
    ],
    'qiye-fenli-shuiwu-chuli': [
        ('qiye-zhongzu-shuiwu', '企业重组', '企业重组与重大交易中的税务规划要点', '资产收购、股权收购、合并分立等重组交易中企业所得税、增值税、契税和土地增值税的优惠处理'),
        ('guquan-jiagou-shuiwu-chouhua', '股权架构', '企业股权架构全解析与税务规划：四种持股方式的税负对比', '自然人直接持股、有限公司持股、合伙企业持股、信托持股的股息红利和股权转让税负对比'),
        ('fei-huobi-zichan-touzi-shuiwu', '税务实务', '非货币性资产投资的税务处理：作价评估、递延纳税与风险防范', '以股权、不动产、无形资产等非货币性资产出资的增值税、企业所得税和个人所得税处理')
    ],
    'xiaofeishui-shuiwu-guihua': [
        ('zengzhishuifa-shishi-yingdui', '增值税', '增值税法正式实施后的企业影响与应对要点', '增值税法正式实施带来的主要变化、企业需要调整的合同管理和发票处理要点'),
        ('jianyi-jinshui-vs-yiban-jinshui', '增值税', '简易计税与一般计税方法的选择策略：不同行业的税负比较', '建筑业、房地产业、劳务派遣等特殊行业简易计税与一般计税的税负比较和适用条件'),
        ('zhizaoye-shuiwu-chouhua', '税务筹划', '制造业企业税务筹划全案：研发优惠、加速折旧与全流程节税策略', '高新技术企业认定维护、研发费用加计扣除、固定资产加速折旧和先进制造业增值税加计抵减')
    ],
    'ziyuanshui-huanbao-shuiwu': [
        ('zhizaoye-shuiwu-chouhua', '税务筹划', '制造业企业税务筹划全案：研发优惠、加速折旧与全流程节税策略', '高新技术企业认定维护、研发费用加计扣除、固定资产加速折旧和先进制造业增值税加计抵减'),
        ('tan-guan-shui-cbam-chukou', '国际税收', '碳关税CBAM对中国出口企业的税务影响与应对策略', '欧盟碳边境调节机制的核算方法、报告义务，以及中国出口企业碳排放数据管理和税务应对'),
        ('zengzhishuifa-shishi-yingdui', '增值税', '增值税法正式实施后的企业影响与应对要点', '增值税法正式实施带来的主要变化、企业需要调整的合同管理和发票处理要点')
    ]
}

# CTA template
CTA_TEMPLATE = '''  <div class="related-cta">
    <p><em>如需了解更多相关内容，欢迎联系存勤法税获取专业咨询。</em></p>
    <p>📞 <strong>咨询热线</strong>：13556116691（微信同号）</p>
<p>对于广州及粤港澳大湾区企业而言，提前做好税务合规布局，是在复杂监管环境下稳健经营的关键。</p>

  </div>'''

def build_related_section(slug):
    """Build the 延伸阅读 HTML for a given article"""
    cards = RELATED.get(slug, [])
    card_html = ''
    for s, cat, title, excerpt in cards:
        card_html += f'''      <a href="{s}.html" class="related-card">
        <span class="related-cat">{cat}</span>
        <div class="related-info">
          <h4>{title}</h4>
          <p>{excerpt}</p>
        </div>
        <span class="related-arrow"><i class="fas fa-arrow-right"></i></span>
      </a>
'''
    
    section = f'''<div class="related-reading">
    <h3 id="延伸阅读" class="related-heading"><span>延伸阅读</span></h3>
    <div class="related-grid">
{card_html}    </div>
  </div>
{CTA_TEMPLATE}'''
    return section

def fix_article(slug):
    """Fix one article by inserting 延伸阅读 before </article>"""
    # Find the source file
    found = False
    for fname in os.listdir(ARTICLES):
        if '(source).html' not in fname:
            continue
        path = os.path.join(ARTICLES, fname)
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        if f'permalink: /articles/{slug}.html' not in content:
            continue
        
        found = True
        
        # Check if already has 延伸阅读 h3
        if '<h3 id="延伸阅读"' in content:
            print(f'  [SKIP] {slug} already has 延伸阅读 h3')
            return True
        
        # Find the </article> tag near the end
        # The pattern is: 结语 content ends, then </article>
        # We need to insert before </article>
        
        # Strategy: find the last </article> that appears before <!-- ===== 文章声明 -->
        article_end_marker = '<!-- ===== 文章声明 ===== -->'
        article_end_pos = content.rfind(article_end_marker)
        if article_end_pos < 0:
            article_end_pos = content.rfind('</article>')
            if article_end_pos < 0:
                print(f'  [FAIL] {slug}: cannot find </article> or 文章声明')
                return False
            # Insert before </article>
            insert_pos = article_end_pos
        else:
            # Find the </article> right before 文章声明
            before_decl = content[:article_end_pos]
            last_article = before_decl.rfind('</article>')
            if last_article < 0:
                print(f'  [FAIL] {slug}: cannot find </article> before 文章声明')
                return False
            insert_pos = last_article
        
        # Build the section to insert
        section_html = build_related_section(slug)
        
        # Insert
        new_content = content[:insert_pos] + '\n' + section_html + '\n' + content[insert_pos:]
        
        # Write back
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f'  [FIXED] {slug}')
        return True
    
    if not found:
        print(f'  [FAIL] {slug}: source file not found')
        return False

def main():
    slugs = ['qishui-zhengce-jiedu', 'qiye-fenli-shuiwu-chuli', 
             'xiaofeishui-shuiwu-guihua', 'ziyuanshui-huanbao-shuiwu']
    
    fixed = 0
    for slug in slugs:
        if fix_article(slug):
            fixed += 1
    
    print(f'\nFixed {fixed}/{len(slugs)} articles')

if __name__ == '__main__':
    main()
