#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量修复 source/ 目录下 HTML 文件中页脚结束后多余的 JS 垃圾代码：
  
  [页脚结束</div>]
  ;
  })();
  </script>
  <!-- ============ 置顶/置底按钮 ============ -->

需要删除中间3行（; })(); </script>），保留页脚</div>和注释之间的干净过渡。
"""

import os
import re

SOURCE_DIR = r'C:\Users\26726\WorkBuddy\2026-05-20-21-20-24\source'

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # 模式1：标准垃圾代码（空行 + ; + })(); + </script> + 空行 + 置顶注释）
    pattern1 = r'\n\n;\n}\)\(\);\n</script>\n\n<!-- ============ 置顶'
    replacement1 = r'\n\n<!-- ============ 置顶'
    content = re.sub(pattern1, replacement1, content)
    
    # 模式2：没有前面的空行
    pattern2 = r'\n;\n}\)\(\);\n</script>\n\n<!-- ============ 置顶'
    replacement2 = r'\n\n<!-- ============ 置顶'
    content = re.sub(pattern2, replacement2, content)
    
    # 模式3：垃圾代码后面是中文 置顶/置底
    pattern3 = r'\n;\n}\)\(\);\n</script>\n<!-- ============ 置顶'
    replacement3 = r'\n<!-- ============ 置顶'
    content = re.sub(pattern3, replacement3, content)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    fixed = []
    for root, dirs, files in os.walk(SOURCE_DIR):
        dirs[:] = [d for d in dirs if d not in ('.git', 'node_modules', '.workbuddy')]
        for fname in files:
            if not fname.endswith('.html'):
                continue
            fpath = os.path.join(root, fname)
            try:
                if fix_file(fpath):
                    rel = os.path.relpath(fpath, SOURCE_DIR)
                    fixed.append(rel)
            except Exception as e:
                print(f'❌ 修复失败 {fpath}: {e}')
    
    if fixed:
        print(f'✅ 修复了 {len(fixed)} 个文件：\n')
        for f in fixed:
            print(f'  - {f}')
    else:
        print('✅ 没有发现需要修复的垃圾代码')

if __name__ == '__main__':
    main()
