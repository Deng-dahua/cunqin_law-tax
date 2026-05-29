#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
对比 home-insights.json、文章源文件、法税洞察页三个数据源的阅读量(views)，
以 home-insights.json 为权威数据源，修正所有不一致。
"""
import json
import re
import glob
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def extract_slug_permalink(filepath):
    """从文章源文件中提取 slug（从 permalink）"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    m = re.search(r'permalink:(.+)', content)
    if not m:
        return None
    permalink = m.group(1).strip()
    return permalink.replace('/articles/', '').replace('.html', '')

def extract_viewnum(filepath):
    """从文章源文件中提取当前 view-num 值"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    m = re.search(r'<span class="view-num" id="view-[^"]+">([0-9,]+)</span>', content)
    if not m:
        return None
    return m.group(1)

def update_source_viewnum(filepath, new_views):
    """更新文章源文件中的 view-num"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 匹配现有的 view-num
    pattern = r'(<span class="view-num" id="view-[^"]+">)[0-9,]+(</span>)'
    replacement = rf'\g<1>{new_views}\g<2>'
    new_content = re.sub(pattern, replacement, content)
    
    if new_content == content:
        # 如果没匹配到，尝试其他模式
        pattern2 = r'(id="view-[^"]+">)[0-9,]+(<)'
        replacement2 = rf'\g<1>{new_views}\g<2>'
        new_content = re.sub(pattern2, replacement2, content)
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

def update_archive_views(filepath, slug, new_views):
    """更新法税洞察页中某篇文章的 data-views"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    old_views_attr = None
    # 找到该 article 的 data-views
    pattern = rf'(href="[^"]*{re.escape(slug)}\.html"[^>]*data-category="[^"]*"\s+data-views=")(\d+)(")'
    m = re.search(pattern, content)
    if m:
        old_views_attr = m.group(2)
        if old_views_attr == str(new_views):
            return False  # 已经是正确的
    
    # 也可以尝试更宽松的匹配
    if not old_views_attr:
        pattern2 = rf'(href="[^"]*{re.escape(slug)}\.html"[^>]*data-views=")(\d+)(")'
        m2 = re.search(pattern2, content)
        if m2:
            old_views_attr = m2.group(2)
            if old_views_attr == str(new_views):
                return False
            new_content = re.sub(
                rf'(href="[^"]*{re.escape(slug)}\.html"[^>]*data-views=")\d+(")',
                rf'\g<1>{new_views}\g<2>',
                content
            )
            if new_content != content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                return True
        return False
    
    # 使用第一次找到的模式替换
    new_content = re.sub(
        rf'(href="[^"]*{re.escape(slug)}\.html"[^>]*data-views=")\d+(")',
        rf'\g<1>{new_views}\g<2>',
        content
    )
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False


def main():
    # === 1. 读取 home-insights.json ===
    json_path = os.path.join(BASE, 'source', 'home-insights.json')
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    json_articles = data['articles']
    # 构建 url->views 映射
    json_views = {}
    for a in json_articles:
        url = a.get('url', '')
        slug = url.replace('articles/', '').replace('.html', '').strip()
        if slug:
            json_views[slug] = a.get('views', 0)
    
    print(f"home-insights.json: {len(json_views)} 篇文章")
    
    # === 2. 检查所有文章源文件 ===
    articles_dir = os.path.join(BASE, 'source', 'articles')
    source_files = glob.glob(os.path.join(articles_dir, '*.html'))
    
    source_fixes = []
    for fp in source_files:
        slug = extract_slug_permalink(fp)
        if not slug:
            continue
        
        current_views_str = extract_viewnum(fp)
        if current_views_str is None:
            continue
        
        current_views = current_views_str.replace(',', '')
        
        if slug in json_views:
            json_val = json_views[slug]
            if str(json_val) != current_views:
                source_fixes.append((slug, json_val, current_views, fp))
    
    print(f"文章源文件: {len([f for f in source_files if extract_slug_permalink(f)])} 篇")
    print(f"与 json 不一致: {len(source_fixes)} 篇")
    
    # === 3. 检查法税洞察页 ===
    archive_path = os.path.join(BASE, 'source', 'archives', '法税洞察(source).html')
    with open(archive_path, 'r', encoding='utf-8') as f:
        archive_content = f.read()
    
    # 提取每个 article-item 的 slug 和 views
    archive_items = re.findall(
        r'href="[^"]*articles/([^"]+)\.html"[^>]*data-views="(\d+)"',
        archive_content
    )
    archive_views = {slug: int(v) for slug, v in archive_items}
    
    archive_fixes = []
    for slug, views in archive_views.items():
        if slug in json_views:
            if json_views[slug] != views:
                archive_fixes.append((slug, json_views[slug], views))
    
    print(f"法税洞察页: {len(archive_views)} 个 article-item")
    print(f"与 json 不一致: {len(archive_fixes)} 篇")
    
    # === 4. 输出不一致详情 ===
    total_fixes = len(source_fixes) + len(archive_fixes)
    if total_fixes == 0:
        print("\n[OK] 所有数据源完全一致!")
        return
    
    print(f"\n=== 发现 {total_fixes} 处不一致，开始修正 ===")
    
    if source_fixes:
        print(f"\n【文章源文件修正】({len(source_fixes)} 篇):")
        fixed_count = 0
        for slug, json_val, current_val, fp in source_fixes:
            formatted_views = f"{json_val:,}"
            if formatted_views != json_val:
                # 如果 json_val 已经是整数，需要格式化
                pass
            formatted = f"{int(json_val):,}"
            
            if update_source_viewnum(fp, formatted):
                fixed_count += 1
                print(f"  [OK] {slug}: {current_val} -> {formatted}")
            else:
                print(f"  [FAIL] {slug}: 更新失败")
        print(f"  => 成功修正 {fixed_count}/{len(source_fixes)} 篇")
    
    if archive_fixes:
        print(f"\n【法税洞察页修正】({len(archive_fixes)} 篇):")
        fixed_count = 0
        for slug, json_val, current_val in archive_fixes:
            if update_archive_views(archive_path, slug, json_val):
                fixed_count += 1
                print(f"  [OK] {slug}: {current_val} -> {json_val}")
            else:
                print(f"  [FAIL] {slug}: 更新失败或无需更新")
        print(f"  => 成功修正 {fixed_count}/{len(archive_fixes)} 篇")
    
    print("\n修正完成！")


if __name__ == '__main__':
    main()
