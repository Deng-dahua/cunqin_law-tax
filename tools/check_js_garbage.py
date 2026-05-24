#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查 source/ 目录下所有 HTML 文件中，页脚结束后是否有多余的 JS 垃圾代码。
垃圾代码特征（在 </div></body></html> 之前的某个位置）：
  1. 独立一行的 ; 
  2. 独立一行的 })();
  3. 独立一行的 </script>
这些行不在正常的 <script> 块内，是之前修复 JS 时残留的。
"""

import os
import re

SOURCE_DIR = r'C:\Users\26726\WorkBuddy\2026-05-20-21-20-24\source'

def has_bad_lines(lines):
    """返回有问题的行号列表"""
    bad = []
    in_script = False
    script_depth = 0
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        # 追踪是否在 <script> 块内
        if '<script' in stripped and '>' in stripped:
            in_script = True
        if '</script>' in stripped:
            in_script = False
        
        # 垃圾特征：不在 <script> 块内，却是独立 JS 语法
        if not in_script:
            if stripped in (';', '});', '})();'):
                bad.append(i+1)
            # 检查是否是 '}.join('')} 这种模板字符串泄漏
            if "'}.join('" in stripped or '"}.join("' in stripped:
                bad.append(i+1)
    
    return bad

def main():
    problem_files = []
    
    for root, dirs, files in os.walk(SOURCE_DIR):
        dirs[:] = [d for d in dirs if d not in ('.git', 'node_modules', '.workbuddy')]
        for fname in files:
            if not fname.endswith('.html'):
                continue
            fpath = os.path.join(root, fname)
            try:
                with open(fpath, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
            except:
                continue
            
            bad_lines = has_bad_lines(lines)
            if bad_lines:
                relpath = os.path.relpath(fpath, SOURCE_DIR)
                problem_files.append((relpath, bad_lines))
    
    if problem_files:
        print(f'❌ 发现 {len(problem_files)} 个文件有 JS 垃圾代码：\n')
        for relpath, lines in problem_files:
            print(f'  📄 {relpath}')
            for ln in lines[:5]:  # 最多显示5个
                print(f'    第 {ln} 行')
            if len(lines) > 5:
                print(f'    ... 还有 {len(lines)-5} 处')
            print()
    else:
        print('✅ 所有文件检查完毕，未发现 JS 垃圾代码')

if __name__ == '__main__':
    main()
