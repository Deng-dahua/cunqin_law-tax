#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""给所有含 CTA 区块的页面添加微信二维码"""
import re
import os
import glob

os.chdir(r'C:\Users\26726\WorkBuddy\2026-05-20-21-20-24')

# 二维码 HTML 模板
QRCODE_TPL = '''      <!-- 微信二维码 -->
      <div class="cta-qrcode" style="position: absolute; right: 4.7rem; top: 50%; transform: translateY(-50%); text-align: center;">
        <img src="{img_path}" alt="微信二维码" style="width: 120px; height: 120px; border-radius: 8px; background: #fff; padding: 6px; box-shadow: 0 4px 16px rgba(0,0,0,0.15);">
        <p style="font-size: 0.85rem; margin-top: 0.5rem; opacity: 0.88; color: #fff;">扫码添加微信</p>
      </div>
'''

# 找所有含 CTA 区块的页面
pages = []
for f in glob.glob('source/**/*.html', recursive=True):
    with open(f, 'r', encoding='utf-8') as fp:
        if 'cta-section' in fp.read():
            pages.append(f)

print(f'找到 {len(pages)} 个含 CTA 的页面\n')

for path in pages:
    with open(path, 'r', encoding='utf-8') as fp:
        content = fp.read()

    # 跳过已有二维码的
    if 'cta-qrcode' in content:
        print(f'  已有二维码，跳过：{path}')
        continue

    # 判断图片路径
    if '/articles/' in path or '/archives/' in path:
        img_path = '../../images/wechat-qrcode.png'
    elif '/' in path.replace('source/', ''):
        img_path = '../images/wechat-qrcode.png'
    else:
        img_path = 'images/wechat-qrcode.png'

    qrcode_html = QRCODE_TPL.format(img_path=img_path)

    # 1. 给 .cta-section 加 position: relative
    if '.cta-section {' in content:
        # 找第一个 .cta-section { ... } 块
        idx = content.index('.cta-section {')
        block = content[idx:content.index('}', idx)]
        if 'position:' not in block:
            content = content.replace(
                '.cta-section {\n',
                '.cta-section {\n  position: relative;\n',
                1
            )

    # 2. 在 CTA 区块的 </section> 前插入二维码
    # 找 <!-- CTA --> ... </section> 或 <section class="cta-section"> ... </section>
    pattern = r'(<!-- CTA.*?)</section>'
    m = re.search(pattern, content, re.DOTALL)
    if not m:
        pattern = r'(<section class="cta-section">.*?)</section>'
        m = re.search(pattern, content, re.DOTALL)

    if m:
        old_block = m.group(1)
        new_block = old_block + qrcode_html
        content = content.replace(old_block, new_block, 1)
        with open(path, 'w', encoding='utf-8') as fp:
            fp.write(content)
        print(f'  ✓ 已添加：{path}')
    else:
        print(f'  ✗ 未找到 CTA 区块：{path}')

print('\n完成！')
