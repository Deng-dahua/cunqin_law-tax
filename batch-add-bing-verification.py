#!/usr/bin/env python3
"""
Batch add Bing verification meta tag to all HTML files in source/
"""
import os
import re

SOURCE_DIR = "C:/Users/26726/WorkBuddy/2026-05-20-21-20-24/source"
BING_TAG = '  <meta name="msvalidate.01" content="643F9F9C5376BCE8168CB8533417070C" />\n'

def add_bing_verification(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'msvalidate.01' in content:
        print(f"  ⚠️  已存在: {file_path}")
        return False

    # Insert after <head> tag
    new_content = content.replace('<head>\n', '<head>\n' + BING_TAG, 1)
    if new_content == content:
        # Try <head> without newline
        new_content = content.replace('<head>', '<head>\n' + BING_TAG, 1)

    if new_content == content:
        print(f"  ❌ 未找到 <head>: {file_path}")
        return False

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"  ✅ 已添加: {file_path}")
    return True

def main():
    html_files = []
    for root, dirs, files in os.walk(SOURCE_DIR):
        for f in files:
            if f.endswith('.html'):
                html_files.append(os.path.join(root, f))

    html_files.sort()
    print(f"找到 {len(html_files)} 个 HTML 文件\n")

    count = 0
    for f in html_files:
        if add_bing_verification(f):
            count += 1

    print(f"\n总共修改了 {count} 个文件")

if __name__ == '__main__':
    main()
