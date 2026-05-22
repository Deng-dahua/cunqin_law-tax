#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""给所有含 CTA 区块的页面添加微信二维码"""
import os
import re

# 页面列表（根据之前搜索结果）
pages = [
    'source/about/关于我们(source).html',
    'source/archives/法税洞察(source).html',
    'source/articles/ODI境外投资备案全流程(source).html',
    'source/articles/业管财税法五维融合(source).html',
    'source/articles/企业税务风险管控(source).html',
    'source/articles/企业重组税务规划(source).html',
    'source/articles/甲乙双视角税务顾问(source).html',
    'source/articles/跨境电商税务合规(source).html',
    'source/articles/金税四期全面解读(source).html',
    'source/articles/高新技术企业税务规划(source).html',
    'source/cases/客户案例(source).html',
    'source/contact/联系我们(source).html',
    'source/services/企业重组与重大交易税务规划(source).html',
    'source/services/全面预算管理体系建设(source).html',
    'source/services/利润增长体系建设(source).html',
    'source/services/十大核心服务(source).html',
    'source/services/涉税风险检查(source).html',
    'source/services/税务危机应对与争议解决(source).html',
    'source/services/营收增长战略咨询(source).html',
    'source/services/财税内控体系建设(source).html',
    'source/services/财税内训课程定制(source).html',
    'source/services/跨境投资与并购(source).html',
    'source/services/跨境法律及税务规划(source).html',
    'source/首页(source).html',
]

print(f'共 {len(pages)} 个页面\n')

for path in pages:
    if not os.path.exists(path):
        print(f'  ✗ 文件不存在：{path}')
        continue

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 检查是否已有二维码
    if 'cta-qrcode' in content:
        print(f'  ⊙ 已有二维码，跳过：{path}')
        continue

    # 检查是否有 CTA 区块
    if '<!-- CTA' not in content and '<section class="cta-section">' not in content:
        print(f'  ✗ 无 CTA 区块：{path}')
        continue

    # 判断图片路径
    if 'source/articles/' in path or 'source/archives/' in path:
        img = '../../images/wechat-qrcode.png'
    elif 'source/' in path and '/' in path.replace('source/', ''):
        img = '../images/wechat-qrcode.png'
    else:
        img = 'images/wechat-qrcode.png'

    # 二维码 HTML
    qrcode = f'''      <!-- 微信二维码 -->
      <div class="cta-qrcode" style="position: absolute; right: 4.7rem; top: 50%; transform: translateY(-50%); text-align: center;">
        <img src="{img}" alt="微信二维码" style="width: 120px; height: 120px; border-radius: 8px; background: #fff; padding: 6px; box-shadow: 0 4px 16px rgba(0,0,0,0.15);">
        <p style="font-size: 0.85rem; margin-top: 0.5rem; opacity: 0.88; color: #fff;">扫码添加微信</p>
      </div>
'''

    # 在 CTA 区块的 </section> 前插入二维码
    # 找 <!-- CTA ... </section>
    pattern = r'(<!-- CTA.*?)</section>'
    m = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
    if not m:
        # 尝试找 <section class="cta-section"> ... </section>
        pattern = r'(<section class="cta-section">.*?)</section>'
        m = re.search(pattern, content, re.DOTALL | re.IGNORECASE)

    if m:
        old = m.group(1)
        new = old + qrcode
        content = content.replace(old, new, 1)

        # 给 .cta-section 加 position: relative
        if '.cta-section {' in content:
            content = content.replace(
                '.cta-section {\n',
                '.cta-section {\n  position: relative;\n',
                1
            )

        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'  ✓ 已添加：{path}')
    else:
        print(f'  ✗ 未找到 CTA 区块：{path}')

print('\n完成！')
