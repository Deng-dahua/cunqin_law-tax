"""批量移除页脚 margin-left: -3cm，实现水平居中"""
import os, glob

base = r'C:\Users\26726\WorkBuddy\2026-05-20-21-20-24\source'
files = glob.glob(os.path.join(base, '*.html')) + glob.glob(os.path.join(base, '*', '*.html'))

count = 0
for fp in files:
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 移除 .footer-links-dt { margin-left: -3cm; }
    new_content = content.replace(
        '.footer-links-dt { margin-left: -3cm; }',
        '.footer-links-dt { }'
    )
    
    if new_content != content:
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(new_content)
        count += 1
        print(f'  ✓ {os.path.basename(fp)}')

print(f'\nDone: {count} files updated')
