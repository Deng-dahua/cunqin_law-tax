"""检查所有 source HTML 文件中 content 属性内的嵌套引号问题"""
import os, re

SOURCE = r'C:\Users\26726\WorkBuddy\2026-05-20-21-20-24\source'
issues = []

for root, dirs, files in os.walk(SOURCE):
    dirs[:] = [d for d in dirs if d not in ('.git', 'node_modules', '.workbuddy')]
    for f in files:
        if not f.endswith('.html'):
            continue
        fpath = os.path.join(root, f)
        with open(fpath, 'r', encoding='utf-8') as fp:
            lines = fp.readlines()
        for i, line in enumerate(lines, 1):
            # 找 content="... 后面还有非 > 的内容（说明 content 里有未转义的引号）
            m = re.search(r'content="([^"]*)"([^>]*)', line)
            if m:
                after_content = m.group(2).strip()
                if after_content and not after_content.startswith('/'):
                    rel_path = fpath.replace(SOURCE, '').lstrip('\\')
                    issues.append(f'  Line {i}: {rel_path}')
                    snippet = line.strip()[:120]
                    issues.append(f'    → {snippet}')
                    break  # 每个文件只报一次

print(f'发现 {len(issues)//2} 个文件有嵌套引号问题:')
for iss in issues:
    print(iss)
if not issues:
    print('No issues found - all clear')
