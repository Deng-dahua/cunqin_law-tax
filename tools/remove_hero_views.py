"""删除所有文章页 Hero 区的阅读量信息（art-view-counter）"""
import re, os, glob, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

SRC = r'source/articles'
files = sorted(glob.glob(os.path.join(SRC, '*(source).html')))

modified = 0
for fp in files:
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()

    orig = content

    # 1. 删除 HTML: <span class="art-view-counter" ...>...</span> (整行)
    content = re.sub(
        r'\s*<span class="art-view-counter"[^>]*>.*?</span>\n',
        '',
        content,
        flags=re.DOTALL
    )

    # 2. 删除 CSS: .art-view-counter 样式块
    content = re.sub(
        r'\.art-view-counter\s*\{[^}]*\}\n?',
        '',
        content
    )

    # 3. 删除 JS: countapi.xyz 实时计数代码块
    #    匹配从注释开始到 })(); 结束
    content = re.sub(
        r'\s*/\* ===== 实时阅读量统计.*?\*/\s*\(\s*function\s*\(\)\s*\{.*?\}\s*\)\s*;\s*',
        '',
        content,
        flags=re.DOTALL
    )

    if content != orig:
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(content)
        modified += 1
        print(f'  OK {os.path.basename(fp)}')

print(f'\nDone: {modified} files modified')
