#!/usr/bin/env python3
"""批量删除除首页和联系我们页之外的所有 wechat-qrcode 引用"""
import re, os

KEEP = {
    os.path.join('contact', '联系我们(source).html'),
    '首页(source).html'
}

src = r'C:\Users\26726\WorkBuddy\2026-05-20-21-20-24\source'
count = 0

for root, dirs, files in os.walk(src):
    for fn in files:
        if not fn.endswith('.html'):
            continue
        rel = os.path.relpath(os.path.join(root, fn), src).replace('\\', '/')
        if rel in KEEP:
            continue
        fpath = os.path.join(root, fn)
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        if 'cta-qrcode' not in content:
            continue
        # 删除整个 cta-qrcode div（含换行）
        new_content = re.sub(
            r'\s*<div class="cta-qrcode"[^>]*>.*?</div>\s*</div>\s*</section>',
            '</section>',
            content,
            flags=re.DOTALL
        )
        if new_content == content:
            # 尝试更宽松的匹配
            new_content = re.sub(
                r'<div class="cta-qrcode"[^>]*>.*?</div>\s*</div>',
                '',
                content,
                flags=re.DOTALL
            )
        if new_content != content:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            count += 1
            print(f'已处理: {rel}')

print(f'\n共处理 {count} 个文件')
