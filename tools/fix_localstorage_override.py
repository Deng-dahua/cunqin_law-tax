#!/usr/bin/env python3
"""修复 localStorage 覆盖 base 的 bug：当 base > localStorage 旧值时，优先使用 base"""

import os
import re
import glob

WORKSPACE = r"C:\Users\26726\WorkBuddy\2026-05-20-21-20-24"
SRC_DIR = os.path.join(WORKSPACE, "source", "articles")

# 匹配的模式
OLD_PATTERN = "var count = stored ? parseInt(stored, 10) : base;"
NEW_LINE = "var count = stored ? Math.max(base, parseInt(stored, 10)) : base;"

fixed = 0
skipped = 0
errors = []

for filepath in glob.glob(os.path.join(SRC_DIR, "*(source).html")):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    if OLD_PATTERN in content:
        new_content = content.replace(OLD_PATTERN, NEW_LINE)
        with open(filepath, "w", encoding="utf-8", newline="") as f:
            f.write(new_content)
        fixed += 1
    else:
        skipped += 1
        if "var count = stored" in content:
            errors.append(os.path.basename(filepath))

print(f"修复完成: {fixed} 篇")
print(f"跳过: {skipped} 篇")
if errors:
    print(f"警告 - 有 alternate 模式的文件: {errors}")
