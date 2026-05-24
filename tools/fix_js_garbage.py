#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量删除 HTML 文件中 JS 模板字符串残留的垃圾行：
  '}).join('')}
});
也处理变体：
  }).join('');
以及末尾多余的 }); 等。
"""

import os
import re

SOURCE_DIR = "C:/Users/26726/WorkBuddy/2026-05-20-21-20-24/source"

def fix_file(fpath):
    with open(fpath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    original_len = len(lines)
    cleaned = []
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # 匹配垃圾行模式
        # 模式1: '}).join('')}
        # 模式2: }).join('');
        # 模式3: 单独的 '}); 或 });
        # 模式4: 单独的 '}).join('')} 变体
        is_trash = False

        # 检查行内容
        if re.match(r"^'}\)\.join\('.*'\)}$", stripped):
            is_trash = True
        elif re.match(r"^}\)\.join\('.*'\);?\s*$", stripped):
            is_trash = True
        elif stripped in ("'}).join('')}", "});", "});", "')"):
            is_trash = True
        # 检查行是否包含在 <script> 标签外的裸 JS 代码
        elif stripped.startswith("'}).join") or stripped.startswith("}).join"):
            is_trash = True

        if is_trash:
            print(f"    删除行 {i+1}: {stripped[:60]}")
            i += 1
            continue

        cleaned.append(line)
        i += 1

    if len(cleaned) < original_len:
        with open(fpath, "w", encoding="utf-8") as f:
            f.writelines(cleaned)
        return original_len - len(cleaned)
    return 0


def main():
    total_fixed = 0
    files_checked = 0

    for root, dirs, files in os.walk(SOURCE_DIR):
        # 跳过 tools 目录
        if "tools" in root:
            continue
        for fname in files:
            if not fname.endswith(".html"):
                continue
            fpath = os.path.join(root, fname)
            files_checked += 1
            removed = fix_file(fpath)
            if removed > 0:
                print(f"  ✅ {os.path.relpath(fpath, SOURCE_DIR)}: 删除 {removed} 行")
                total_fixed += 1

    print(f"\n完成！检查 {files_checked} 个文件，修复 {total_fixed} 个文件")


if __name__ == "__main__":
    main()
