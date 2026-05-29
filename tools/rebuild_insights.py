#!/usr/bin/env python3
"""
综合修复脚本:
1. home-insights.json 去重 + 加入3篇CTA文章
2. 更新3篇CTA源文件的cat-tag (财税咨询->税务实务)
3. 重新生成法税洞察页文章列表 (article-tag = data-category)
4. 从footer移除3篇CTA文章
"""
import json
import re
import os
import copy

BASE = r'C:\Users\26726\WorkBuddy\2026-05-20-21-20-24'

# === 1. home-insights.json 去重 + 加3篇CTA ===
insights_path = os.path.join(BASE, 'source', 'home-insights.json')
with open(insights_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 去重 (保留首次出现的)
seen_urls = set()
unique_articles = []
for a in data['articles']:
    if a['url'] not in seen_urls:
        seen_urls.add(a['url'])
        unique_articles.append(a)

dup_count = len(data['articles']) - len(unique_articles)
print(f"[1] home-insights.json: {len(data['articles'])}条 -> 去重后 {len(unique_articles)}条 (移除{dup_count}条重复)")

# 加入3篇CTA文章
cta_articles = [
    {
        "title": "企业税务健康体检清单：30个指标自查你的公司有没有税务问题",
        "url": "articles/qiye-shuiwu-jiankang-tijian.html",
        "date": "2026-05-27",
        "category": "税务实务",
        "views": 280,
        "excerpt": "企业税务健康体检30项指标全面梳理：从增值税税负率、企业所得税贡献率到发票管理合规性，建立企业税务风险自查清单，帮助企业主动发现潜在税务问题，在大湾区日益严格的税务监管环境下做到防患于未然。"
    },
    {
        "title": "私户收款被查怎么办？金税四期下的补救窗口期与合规路径全解析",
        "url": "articles/sihu-shoukuan-bujiu-zhinan.html",
        "date": "2026-05-27",
        "category": "税务实务",
        "views": 350,
        "excerpt": "金税四期下私户收款被查的补救指南：深度解析银行流水与税务申报数据自动比对机制，梳理主动补申报的窗口期与从宽处理条件，为广州及大湾区企业主提供私户收款合规转化的实操路径与风险防范策略。"
    },
    {
        "title": "税务稽查应对实战手册：从收到稽查通知书到结案的每一步",
        "url": "articles/shuiwu-jicha-yingdui-shouce.html",
        "date": "2026-05-27",
        "category": "税务实务",
        "views": 320,
        "excerpt": "税务稽查应对全流程实战手册：从收到稽查通知书的第一时间应对策略、稽查期间的资料准备与沟通技巧、到稽查结论的异议处理与行政复议，为企业提供可操作的稽查应对方案，最大限度降低稽查风险与经济损失。"
    }
]

for cta in cta_articles:
    if cta['url'] not in seen_urls:
        seen_urls.add(cta['url'])
        unique_articles.append(cta)

# 按views降序排列
unique_articles.sort(key=lambda x: x['views'], reverse=True)

data['articles'] = unique_articles
data['total'] = len(unique_articles)

with open(insights_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"[1] 加入3篇CTA后: {data['total']}篇, 已保存")

# === 2. 更新3篇CTA源文件的cat-tag ===
cta_sources = [
    '企业税务健康体检30项(source).html',
    '私户收款被查补救指南(source).html',
    '税务稽查应对实战手册(source).html',
]

for src_name in cta_sources:
    src_path = os.path.join(BASE, 'source', 'articles', src_name)
    if not os.path.exists(src_path):
        print(f"[2] WARNING: {src_name} 不存在, 跳过")
        continue
    with open(src_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 替换 cat-tag
    old = '<span class="cat-tag">财税咨询</span>'
    new = '<span class="cat-tag">税务实务</span>'
    if old in content:
        content = content.replace(old, new)
        with open(src_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"[2] 已更新 cat-tag: {src_name} (财税咨询 -> 税务实务)")
    else:
        print(f"[2] WARNING: {src_name} 中未找到 cat-tag '财税咨询'")

# === 3. 重新生成法税洞察页文章列表 ===
archives_path = os.path.join(BASE, 'source', 'archives', '法税洞察(source).html')
with open(archives_path, 'r', encoding='utf-8') as f:
    html = f.read()

# 从home-insights.json获取文章列表(已去重+排序)
articles_sorted = data['articles']  # already sorted by views desc

def date_to_display(date_str):
    """2026-05-27 -> 2026.05.27"""
    return date_str.replace('-', '.')

def generate_article_item(a):
    """生成单篇文章的HTML"""
    title = a['title']
    url = a['url']  # articles/xxx.html
    date = a['date']
    category = a['category']
    views = a['views']
    excerpt = a.get('excerpt', '')
    
    # 截断excerpt (约100字)
    if len(excerpt) > 120:
        excerpt = excerpt[:117] + '...'
    
    display_date = date_to_display(date)
    
    return f"""      <a href="../{url}" class="article-item" data-date="{date}" data-category="{category}" data-views="{views}">
        <div class="article-content">
          <h3>{title}</h3>
          <p>{excerpt}</p>
          <div class="article-meta-row">
            <span class="article-tag">{category}</span>
            <span class="article-date-text"><i class="fas fa-calendar-alt"></i> {display_date}</span>
            <span class="article-views"><i class="fas fa-eye"></i> {views}</span>
          </div>
        </div>
        <div class="article-arrow"><i class="fas fa-chevron-right"></i></div>
      </a>"""

# 生成新文章列表HTML
new_article_items = '\n'.join(generate_article_item(a) for a in articles_sorted)

# 找到 articleList 的起始和结束位置
list_start_marker = '<div class="article-list" id="articleList">'
list_end_marker = '\n\n<!-- ===== CTA ===== -->'

list_start = html.find(list_start_marker)
list_end = html.find(list_end_marker)

if list_start == -1:
    print("[3] ERROR: 找不到 articleList 起始标记!")
    exit(1)
if list_end == -1:
    print("[3] ERROR: 找不到 CTA 区块标记!")
    exit(1)

# 找到 articleList div 内第一个 <a 的位置(新文章起始)
first_a = html.find('<a ', list_start + len(list_start_marker))
if first_a == -1 or first_a >= list_end:
    print("[3] ERROR: 找不到列表中的第一篇文章!")
    exit(1)

# 替换
before_list = html[:first_a]
after_list = html[list_end:]

new_html = before_list + '\n' + new_article_items + '\n    </div>\n  </div>\n</section>\n' + after_list

html = new_html

# === 4. 从footer移除3篇CTA文章 ===
# 移除footer中的CTA文章节点 (位于 <div class="footer-service-items"> 内的最后3个 <a> 标签)
cta_urls = [
    '../../articles/qiye-shuiwu-jiankang-tijian.html',
    '../../articles/sihu-shoukuan-bujiu-zhinan.html',
    '../../articles/shuiwu-jicha-yingdui-shouce.html',
]

for cta_url in cta_urls:
    # 查找这个URL在footer中的位置
    pos = html.find(cta_url)
    if pos == -1:
        print(f"[4] WARNING: footer中找不到 {cta_url}")
        continue
    
    # 向前找到所在 <a 标签的开始
    # 这个CTA节点格式: <a href="URL" class="article-item">...</a>
    a_start = html.rfind('<a href="', 0, pos)
    if a_start == -1:
        print(f"[4] WARNING: 找不到 {cta_url} 的 <a> 开始标签")
        continue
    
    # 找到匹配的 </a>
    depth = 0
    a_end = a_start
    for i in range(a_start, len(html)):
        if html[i:i+2] == '<a':
            depth += 1
        elif html[i:i+3] == '</a':
            depth -= 1
            if depth == 0:
                a_end = i + 4
                break
    
    if a_end == a_start:
        print(f"[4] WARNING: 找不到 {cta_url} 的 </a> 结束标签")
        continue
    
    # 找到节点前后的换行和空白
    # 向前扩展至前一个换行
    before = a_start
    while before > 0 and html[before-1] in (' ', '\t'):
        before -= 1
    if before > 0 and html[before-1] == '\n':
        before -= 1
    
    # 向后扩展至后一个换行
    after = a_end
    while after < len(html) and html[after] in (' ', '\t'):
        after += 1
    if after < len(html) and html[after] == '\n':
        after += 1
    
    html = html[:before] + html[after:]
    print(f"[4] 已移除footer CTA: {cta_url.split('/')[-1]}")

# 写回
with open(archives_path, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"[3-4] 法税洞察页已更新: {len(articles_sorted)}篇文章, article-tag=data-category, 3篇CTA已移入列表并从footer移除")

# === 5. 统计验证 ===
cats = {}
for a in articles_sorted:
    cats[a['category']] = cats.get(a['category'], 0) + 1
print(f"\n[5] 最终分类统计 ({len(articles_sorted)}篇):")
for cat, cnt in sorted(cats.items(), key=lambda x: -x[1]):
    print(f"  {cat}: {cnt}篇")

print("\nDone!")
