#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复 source/ 目录下所有 HTML 文件中 footer 结束后多余的 JS 垃圾代码：
  ';\n})();\n</script>'
这些行出现在 </div></body></html> 之前，是之前 JS 修复残留的。
"""

import os
import re

SOURCE_DIR = r'C:\Users\26726\WorkBuddy\2026-05-20-21-20-24\source'

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_len = len(content)

    # 修复1：页脚 </div> 之后、<!-- ============ 置顶/置底按钮 ============ --> 之前的多余 JS 垃圾
    # 特征：空行 + ; + })(); + </script> + 空行 + 置顶按钮注释
    pattern1 = r'\n\n;\n}\)\(\);\n</script>\n'
    content = content.replace(pattern1, '\n')

    # 修复2：变体——可能没有空行
    pattern2 = r'\n;\n}\)\(\);\n</script>\n'
    content = content.replace(pattern2, '\n')

    # 修复3：更宽泛的匹配——footer-copyright 结束 </div> 后到置顶按钮注释之间的垃圾
    # 匹配：</div>\n\n</div>\n\n;\n})();\n</script>\n<!-- ============ 置顶
    pattern3 = re.compile(r'(</div>\s*\n\s*</div>\s*\n)\s*;\s*\n\s*}\) \(\);\s*\n\s*</script>\s*\n\s*<!-- ============ 置顶', re.DOTALL)
    content = pattern3.sub(r'\1<!-- ============ 置顶', content)

    if len(content) != original_len:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True, filepath
    return False, filepath

def main():
    fixed = []
    for root, dirs, files in os.walk(SOURCE_DIR):
        # 跳过 .git 和 node_modules
        dirs[:] = [d for d in dirs if d not in ('.git', 'node_modules', '.workbuddy')]
        for fname in files:
            if fname.endswith('.html'):
                fpath = os.path.join(root, fname)
                was_fixed, _ = fix_file(fpath)
                if was_fixed:
                    fixed.append(fpath.replace(SOURCE_DIR, '').lstrip('\\'))

    if fixed:
        print(f'✅ 修复了 {len(fixed)} 个文件：')
        for f in fixed:
            print(f'  - {f}')
    else:
        print('✅ 没有发现需要修复的垃圾代码')

if __name__ == '__main__':
    main()
