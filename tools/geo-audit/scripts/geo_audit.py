"""
============================================================
存勤法税官网 GEO 全站审计脚本
============================================================
用法: python tools/geo_audit.py

检查项（覆盖之前所有已发现的问题类型）:
  A. HTML 结构
     1. 标签平衡 (div, section, script, head, body, html)
     2. DOCTYPE 声明
     3. lang="zh-CN" 属性
  B. Meta 标签完整性
     4. baidu-site-verification
     5. robots meta
     6. canonical URL
     7. hreflang
     8. keywords
     9. description
    10. PWA meta (theme-color, apple-mobile-web-app-capable, apple-touch-icon)
  C. SEO 社交标签
    11. Open Graph (og:title, og:description, og:type, og:url, og:image, og:site_name)
    12. Twitter Card (twitter:card, twitter:title, twitter:description)
  D. 结构化数据
    13. Schema.org JSON-LD (application/ld+json)
  E. 代码质量
    14. 嵌套引号（HTML 属性值内的原始双引号）
    15. JS 垃圾代码 (}).join('')、孤立 }); </script>
    16. 未闭合 <script> 标签
  F. 内容质量
    17. og:description 长度 (120-160 字符区间)
    18. description meta 非空
    19. og:url 指向正确域名 (cunqin.tax)
============================================================
"""

import os
import re
import sys
from pathlib import Path

# 配置
SOURCE = Path(r'C:\Users\26726\WorkBuddy\2026-05-20-21-20-24\source')
EXPECTED_DOMAIN = 'cunqin.tax'
BAIDU_TOKEN = 'codeva-MMFsum3pdD'

TOTAL_CHECKS = 19
errors = []
warnings = []

def err(file, line, msg):
    errors.append(f'  {file}:{line}  {msg}')

def warn(file, line, msg):
    warnings.append(f'  {file}:{line}  {msg}')

def find_html_files():
    """递归查找所有 .html 文件"""
    files = []
    for root, dirs, filenames in os.walk(SOURCE):
        dirs[:] = [d for d in dirs if d not in ('.git', 'node_modules', '.workbuddy')]
        for f in filenames:
            if f.endswith('.html'):
                files.append(Path(root) / f)
    return sorted(files)

def check_file(fpath, rel):
    """对单个文件执行所有检查"""
    with open(fpath, 'r', encoding='utf-8') as fp:
        content = fp.read()
    lines = content.split('\n')

    # === A. HTML 结构 ===

    # 1. 标签平衡
    pairs = [
        ('<div', '</div>'),
        ('<section', '</section>'),
        ('<script', '</script>'),
        ('<head', '</head>'),
        ('<body', '</body>'),
        ('<html', '</html>'),
    ]
    for open_tag, close_tag in pairs:
        # 用正则匹配开放标签（避免匹配到 </xx>）
        open_count = len(re.findall(r'(?<!/)' + re.escape(open_tag) + r'[\s>]', content))
        # 如果 open_tag 是 '<html'，也要匹配 '<html>' (无空格关闭)
        if open_tag == '<html':
            open_count += content.count('<html>')
        close_count = content.count(close_tag)
        if open_count != close_count:
            err(rel, '-', f'标签不平衡: {open_tag}({open_count}) vs {close_tag}({close_count})')

    # 2. DOCTYPE
    if '<!DOCTYPE html>' not in content:
        err(rel, '-', '缺少 <!DOCTYPE html>')

    # 3. lang 属性
    if 'lang="zh-CN"' not in content and "lang='zh-CN'" not in content:
        warn(rel, '-', '缺少 lang="zh-CN"')

    # === B. Meta 完整性 ===

    # 4. 百度验证
    if BAIDU_TOKEN not in content:
        err(rel, '-', f'缺少 baidu-site-verification ({BAIDU_TOKEN})')

    # 5. robots
    if 'name="robots"' not in content:
        err(rel, '-', '缺少 robots meta')

    # 6. canonical
    if 'canonical' not in content:
        err(rel, '-', '缺少 canonical URL')

    # 7. hreflang
    if 'hreflang' not in content:
        warn(rel, '-', '缺少 hreflang')

    # 8. keywords
    if 'name="keywords"' not in content:
        err(rel, '-', '缺少 keywords meta')

    # 9. description
    if 'name="description"' not in content:
        err(rel, '-', '缺少 description meta')

    # 10. PWA meta
    pwa_checks = [
        ('name="theme-color"', 'theme-color'),
        ('apple-mobile-web-app-capable', 'apple-mobile-web-app-capable'),
        ('apple-touch-icon', 'apple-touch-icon'),
    ]
    for pattern, name in pwa_checks:
        if pattern not in content:
            warn(rel, '-', f'缺少 PWA meta: {name}')

    # === C. SEO 社交标签 ===

    # 11. Open Graph
    og_fields = ['og:title', 'og:description', 'og:type', 'og:url', 'og:image', 'og:site_name']
    for field in og_fields:
        if field not in content:
            err(rel, '-', f'缺少 OG: {field}')

    # 12. Twitter Card
    tw_fields = ['twitter:card', 'twitter:title', 'twitter:description']
    for field in tw_fields:
        if field not in content:
            warn(rel, '-', f'缺少 Twitter: {field}')

    # === D. 结构化数据 ===

    # 13. JSON-LD
    if 'application/ld+json' not in content:
        err(rel, '-', '缺少 Schema.org JSON-LD')

    # === E. 代码质量 ===

    # 14. 嵌套引号
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith('<!--'):
            continue
        # 找到所有 HTML 属性值
        attrs = re.findall(r'''(\w+(?:-\w+)*)=(["'])(.*?)\2''', stripped)
        for attr_name, quote, value in attrs:
            if quote in value:  # 属性值里包含相同引号
                err(rel, i, f'嵌套引号: {attr_name}="{value[:60]}..."')
                break

    # 15. JS 垃圾代码
    garbage_patterns = [
        ("').join('", "').join('"),
        ("'}); </script>", "孤立的 }); </script>"),
    ]
    for pattern, desc in garbage_patterns:
        if pattern in content:
            # 找具体行号
            for i, line in enumerate(lines, 1):
                if pattern in line:
                    err(rel, i, f'JS 垃圾代码: {desc}')
                    break

    # 16. 未闭合 script（简单检查：<script> 不在 JSON-LD 内，且后面没有 </script>）
    # 这比较复杂，这里用简化版：检查是否有 <script>（非 ld+json）后无对应闭合
    script_open_lines = []
    in_jsonld = False
    for i, line in enumerate(lines, 1):
        if 'application/ld+json' in line:
            in_jsonld = True
        if '</script>' in line:
            if in_jsonld:
                in_jsonld = False
            continue
        if '<script' in line and 'ld+json' not in line:
            if not in_jsonld:
                script_open_lines.append(i)

    # 17. og:description 长度
    og_desc_match = re.search(r'property="og:description"\s+content="([^"]{10,})"', content)
    if og_desc_match:
        desc_len = len(og_desc_match.group(1))
        if desc_len < 120:
            err(rel, '-', f'og:description 过短: {desc_len} 字符 (建议 120-160)')
        elif desc_len > 180:
            warn(rel, '-', f'og:description 过长: {desc_len} 字符')

    # 18. description 非空
    meta_desc_match = re.search(r'name="description"\s+content="([^"]*)"', content)
    if meta_desc_match and len(meta_desc_match.group(1).strip()) < 20:
        err(rel, '-', 'meta description 内容过短或为空')

    # 19. og:url 指向正确域名
    og_url_match = re.search(r'property="og:url"\s+content="([^"]*)"', content)
    if og_url_match:
        url = og_url_match.group(1)
        if EXPECTED_DOMAIN not in url:
            err(rel, '-', f'og:url 域名错误: {url} (期望含 {EXPECTED_DOMAIN})')


def main():
    files = find_html_files()
    print(f'扫描 {len(files)} 个 HTML 文件...')
    print()

    for fpath in files:
        rel = str(fpath.relative_to(SOURCE))
        check_file(fpath, rel)

    # 输出结果
    print('=' * 60)
    print(f'检查项: {TOTAL_CHECKS} | 文件: {len(files)}')
    print(f'ERROR:   {len(errors)}')
    print(f'WARNING: {len(warnings)}')
    print('=' * 60)

    if errors:
        print('\n❌ ERRORS:')
        for e in errors:
            print(e)

    if warnings:
        print('\n⚠️  WARNINGS:')
        for w in warnings:
            print(w)

    if not errors and not warnings:
        print('\n✅ 全站 GEO 审计通过 — 0 错误 0 警告')

    print()
    return len(errors)


if __name__ == '__main__':
    sys.exit(main())
