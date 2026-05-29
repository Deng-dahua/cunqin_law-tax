#!/usr/bin/env python3
"""fix_article_base_views.py
修复所有文章页动态阅读量计数器的 base 值，使其与 home-insights.json 一致。
同时修正「数字化税务管理转型之路」的分类。
"""
import json
import re
import glob
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_PATH = os.path.join(BASE_DIR, 'source', 'home-insights.json')
ARTICLES_DIR = os.path.join(BASE_DIR, 'source', 'articles')

# 1. 读取 home-insights.json 构建 url -> views 映射
with open(JSON_PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)

url_views = {}
for a in data['articles']:
    # url 格式: articles/xxx.html
    url_views[a['url']] = a['views']

print(f"home-insights.json: {len(url_views)} articles")

# 2. 遍历所有文章源文件
articles = glob.glob(os.path.join(ARTICLES_DIR, '*(source).html'))
print(f"article source files: {len(articles)}")

fixed_base = 0
fixed_category = 0
errors = []
skipped = 0

for filepath in sorted(articles):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 提取 permalink
    pm = re.search(r'permalink:\s*(\S+)', content)
    if not pm:
        errors.append(f"{os.path.basename(filepath)}: no permalink found")
        continue
    permalink = pm.group(1)
    url_key = permalink.lstrip('/')  # articles/xxx.html

    # 提取当前的 base 值
    base_match = re.search(r'var base = (\d+);', content)
    current_base = int(base_match.group(1)) if base_match else None
    if current_base is None:
        errors.append(f"{os.path.basename(filepath)}: no var base found")
        continue

    # 提取当前的 cat-tag
    cat_match = re.search(r'<span class="cat-tag">([^<]+)</span>', content)
    current_cat = cat_match.group(1) if cat_match else None

    modified = False
    new_content = content

    # --- Fix 1: base 值 ---
    if url_key in url_views:
        target_views = url_views[url_key]
        if current_base != target_views:
            new_content = re.sub(
                r'var base = \d+;',
                f'var base = {target_views};',
                new_content
            )
            fixed_base += 1
            print(f"  base: {os.path.basename(filepath)[:50]:50s} {current_base:,} -> {target_views:,}")
    else:
        skipped += 1
        print(f"  SKIP: {os.path.basename(filepath)} not in home-insights.json")

    # --- Fix 2: 数字化税务管理 分类 ---
    if 'shuzihua-shuiwu-guanli-zhuanxing' in permalink and current_cat == '行业洞察':
        new_content = new_content.replace(
            '<span class="cat-tag">行业洞察</span>',
            '<span class="cat-tag">税务实务</span>'
        )
        fixed_category += 1
        print(f"  cat: {os.path.basename(filepath)} 行业洞察 -> 税务实务")

    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

print(f"\n=== Summary ===")
print(f"base fixed: {fixed_base}")
print(f"category fixed: {fixed_category}")
print(f"skipped: {skipped}")
print(f"errors: {len(errors)}")
for e in errors:
    print(f"  [ERR] {e}")
