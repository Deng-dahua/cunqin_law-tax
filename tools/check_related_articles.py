#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""检查所有文章延伸阅读链接的完整性"""

import os, re, glob

ARTICLES_DIR = r'source\articles'

def scan_related_links(filepath):
    """扫描单篇文章的延伸阅读链接"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    results = {'file': os.path.basename(filepath), 'links': []}

    # 找到 related-reading 区块
    m = re.search(r'<div class="related-reading">(.*?)</div>\s*<div class="related-cta">', content, re.DOTALL)
    if not m:
        results['status'] = 'NO_RELATED_SECTION'
        return results

    section = m.group(1)
    # 提取所有 a href
    links = re.findall(r'<a href="([^"]+)"', section)
    for link in links:
        # 提取 slug
        slug = link.split('/')[-1] if '/' in link else link
        results['links'].append({'href': link, 'slug': slug})

    results['status'] = 'OK'
    return results


def main():
    os.chdir(r'C:\Users\26726\WorkBuddy\2026-05-20-21-20-24')

    # 获取所有文章文件
    article_files = sorted(glob.glob(os.path.join(ARTICLES_DIR, '*(source).html')))
    print(f'文章总数: {len(article_files)}')

    # 获取所有存在的slug
    existing_slugs = set()
    for f in article_files:
        with open(f, 'r', encoding='utf-8') as fh:
            first_lines = ''.join(fh.readline() for _ in range(4))
        m = re.search(r'permalink:\s*/articles/([^\s]+)', first_lines)
        if m:
            existing_slugs.add(m.group(1))

    print(f'\n已存在的文章 slug ({len(existing_slugs)}):')
    for s in sorted(existing_slugs):
        print(f'  {s}')

    # 扫描每篇文章的延伸阅读
    print('\n' + '='*80)
    print('延伸阅读引用分析')
    print('='*80)

    all_referenced = set()
    missing_slugs = set()
    article_links_map = {}

    for af in article_files:
        result = scan_related_links(af)
        filename = result['file']

        if result['status'] == 'NO_RELATED_SECTION':
            print(f'\n[无延伸阅读] {filename}')
            continue

        print(f'\n[{filename}]')
        for link in result['links']:
            slug = link['slug']
            all_referenced.add(slug)
            exists = '[OK]' if slug in existing_slugs else '[MISSING]'
            print(f'  {exists} {link["href"]}')
            if slug not in existing_slugs:
                missing_slugs.add(slug)

        article_links_map[filename] = result['links']

    # 汇总报告
    print('\n' + '='*80)
    print(f'汇总报告')
    print('='*80)
    print(f'文章总数: {len(article_files)}')
    print(f'有延伸阅读的文章数: {len(article_links_map)}')
    print(f'被引用的唯一文章: {len(all_referenced)}')
    print(f'缺失的文章: {len(missing_slugs)}')

    if missing_slugs:
        print(f'\n[MISSING] 以下 {len(missing_slugs)} 篇文章被引用但不存在详情页:')
        for s in sorted(missing_slugs):
            # 找出是哪篇文章引用了它
            referencing = [f for f, links in article_links_map.items()
                          if any(l['slug'] == s for l in links)]
            print(f'  {s}  (被引用自: {", ".join(referencing)})')
    else:
        print('\n[OK] 所有延伸阅读引用的文章都存在')

    # 检查哪些文章没有被任何延伸阅读引用
    print(f'\n未被任何延伸阅读引用的文章:')
    referenced_slugs = {s for s in all_referenced if s in existing_slugs}
    unreferenced = existing_slugs - referenced_slugs
    for s in sorted(unreferenced):
        print(f'  {s}')


if __name__ == '__main__':
    main()
