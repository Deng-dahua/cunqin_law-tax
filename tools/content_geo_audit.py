"""#176 内容层面 GEO 审计 + 修复（大写H标签 + 结构审计）"""
import re, os, glob, json

articles_dir = 'source/articles'
files = sorted(glob.glob(f'{articles_dir}/*.html'))

issues = {
    'upper_h_tags': [],   # H2/H3 大写标签
    'short_content': [],   # <1500字
    'few_h2': [],
    'few_h3': [],
    'no_toc': [],
    'weak_intro': [],
}

for fp in files:
    with open(fp, 'r', encoding='utf-8') as f:
        c = f.read()
    
    name = os.path.basename(fp).replace('(source).html', '')
    short = name[:20]
    
    # 1. 大写 H 标签检查
    upper_h = re.findall(r'<(H[1-4])[^>]*>', c)
    if upper_h:
        issues['upper_h_tags'].append((short, [t for t in upper_h]))
    
    # 2. 正文内容字数
    m = re.search(r'<article class="article-body">(.*?)</article>', c, re.DOTALL)
    if m:
        text = re.sub(r'<[^>]+>', ' ', m.group(1))
        text = re.sub(r'\s+', ' ', text).strip()
        word_count = len(text)
        if word_count < 1500:
            issues['short_content'].append((short, word_count))
        
        # 3. H2/H3 数量
        h2_count = len(re.findall(r'<h2', m.group(1)))
        h3_count = len(re.findall(r'<h3', m.group(1)))
        if h2_count < 3:
            issues['few_h2'].append((short, h2_count))
        if h3_count < 3:
            issues['few_h3'].append((short, h3_count))
    else:
        issues['short_content'].append((short, 0))
    
    # 4. 是否有目录（article-toc）
    has_toc = 'article-toc' in c
    if not has_toc:
        issues['no_toc'].append(short)
    
    # 5. 前言/引言段落质量（前200字是否含"本文"或概述性语句）
    if m:
        first_200 = text[:200]
        if '本文' not in first_200 and '引言' not in first_200 and '前言' not in first_200:
            issues['weak_intro'].append(short)

# ========== 输出审计报告 ==========
print('=' * 60)
print('内容层面 GEO 审计报告')
print('=' * 60)

print(f'\n【P0】大写 H 标签（SEO价值≈0）：{len(issues["upper_h_tags"])}篇')
for name, tags in issues['upper_h_tags'][:10]:
    print(f'  - {name}: {tags}')
if len(issues['upper_h_tags']) > 10:
    print(f'  ... 还有{len(issues["upper_h_tags"])-10}篇')

print(f'\n【P1】字数<1500：{len(issues["short_content"])}篇')
for name, wc in sorted(issues['short_content'], key=lambda x: x[1])[:10]:
    print(f'  - {name}: {wc}字')

print(f'\n【P1】H2<3：{len(issues["few_h2"])}篇')
for name, cnt in issues['few_h2'][:10]:
    print(f'  - {name}: H2={cnt}')

print(f'\n【P2】H3<3：{len(issues["few_h3"])}篇')
for name, cnt in issues['few_h3'][:10]:
    print(f'  - {name}: H3={cnt}')

print(f'\n【P2】无目录（article-toc）：{len(issues["no_toc"])}篇')
if issues['no_toc']:
    for n in issues['no_toc'][:5]:
        print(f'  - {n}')

print(f'\n【P2】前言/引言弱：{len(issues["weak_intro"])}篇')
for n in issues['weak_intro'][:5]:
    print(f'  - {n}')

print('\n' + '=' * 60)
print('摘要统计')
print('=' * 60)
print(f'  大写H标签(P0): {len(issues["upper_h_tags"])}篇 ← 优先修复')
print(f'  字数<1500(P1): {len(issues["short_content"])}篇')
print(f'  H2<3(P1):      {len(issues["few_h2"])}篇')
print(f'  H3<3(P2):      {len(issues["few_h3"])}篇')
print(f'  无目录(P2):       {len(issues["no_toc"])}篇')
print(f'  弱前言(P2):       {len(issues["weak_intro"])}篇')
