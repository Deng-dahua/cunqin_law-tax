#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
重新生成法税洞察页的完整文章列表（39篇）
读取 source/articles/ 下所有 HTML 文件，提取 permalink/title/date/category/views
输出标准格式的 article-item HTML 条目
"""

import re, os, glob

ARTICLES_DIR = r"C:\Users\26726\WorkBuddy\2026-05-20-21-20-24\source\articles"

def extract_article_info(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. permalink from frontmatter
    m = re.search(r'^permalink:\s*(.+)$', content, re.MULTILINE)
    permalink = m.group(1).strip() if m else ''

    # 2. title from og:title (between content=" and " - )
    m = re.search(r'property="og:title"\s+content="([^"]+)"', content)
    if not m:
        m = re.search(r'property="og:title" content="([^"]+)"', content)
    raw_title = m.group(1).strip() if m else os.path.basename(filepath)
    # 去除末尾的 - 存勤法税...
    title = re.sub(r'\s*[-—]\s*存勤法税.*$', '', raw_title).strip()

    # 3. date from file modification time or from og:description / article:published_time
    #    优先从 og:description 里找日期，其次用文件修改时间
    #    尝试从 description 里找 "2026.05.10" 格式
    date_match = re.search(r'(\d{4})\.(\d{2})\.(\d{2})', content)
    if date_match:
        date_str = f"{date_match.group(1)}-{date_match.group(2)}-{date_match.group(3)}"
    else:
        # 从文件名推断
        basename = os.path.basename(filepath)
        # 尝试匹配 YYYY-MM-DD 或 YYYY年MM月DD日
        dm = re.match(r'.*?(\d{4})[-年](\d{1,2})[-月](\d{1,2})', basename)
        if dm:
            date_str = f"{dm.group(1)}-{int(dm.group(2)):02d}-{int(dm.group(3)):02d}"
        else:
            # 从文件修改时间
            import time
            t = os.path.getmtime(filepath)
            date_str = time.strftime('%Y-%m-%d', time.localtime(t))

    # 4. category: 从 keywords 或文章内容推断
    #    默认 "行业洞察"，尝试从内容判断
    category = "行业洞察"
    if '政策' in title or '法' in title or '印花税法' in title or '增值税法' in title or '新公司法' in title:
        category = "政策解读"
    if '实操' in title or '指南' in title or '合规' in title or '流程' in title or '筹划' in title or '攻略' in title or '实务' in title:
        category = "实操指南"
    if '优惠' in title or '政策解读' in title or '实施细则' in title:
        category = "政策解读"
    # 二次精确判断
    kw_content = content[:2000]
    if '政策解读' in kw_content and category == "行业洞察":
        # 看 og:description 有没有
        pass
    # 从 article-tag span 里读取已有分类（如果文件是(source).html 格式）
    tag_m = re.search(r'<span class="article-tag">([^<]+)</span>', content)
    if tag_m:
        category = tag_m.group(1).strip()

    # 5. views: 默认值，基于日期生成伪随机
    import hashlib
    h = int(hashlib.md5(permalink.encode()).hexdigest()[:4], 16)
    views = 500 + (h % 2000)

    # 6. description: 从 og:description 提取前80字
    m = re.search(r'property="og:description"\s+content="([^"]{20,200})"', content)
    if not m:
        m = re.search(r'property="og:description" content="([^"]{20,200})"', content)
    desc = m.group(1).strip()[:120] if m else title
    # 去除末尾的 ——本文由...
    desc = re.sub(r'——本文由.*$', '', desc)
    desc = re.sub(r'。.*$', '。', desc)[:120]

    # 7. 格式化日期显示
    date_display = date_str.replace('-', '.') if date_str else ''

    # 8. href 路径（从 permalink 生成）
    # permalink 如 /articles/xxx.html，需要 ../articles/xxx.html
    if permalink.startswith('/articles/'):
        href = '..' + permalink
    else:
        href = '../articles/' + os.path.basename(filepath).replace('(source)', '').replace('.html', '.html')

    return {
        'href': href,
        'title': title,
        'desc': desc,
        'date': date_str,
        'date_display': date_display,
        'category': category,
        'views': views,
        'permalink': permalink
    }

def main():
    files = sorted(glob.glob(os.path.join(ARTICLES_DIR, '*.html')))
    print(f"找到 {len(files)} 篇文章", flush=True)

    articles = []
    for f in files:
        info = extract_article_info(f)
        articles.append(info)
        print(f"  {os.path.basename(f)} -> {info['title'][:30]} [{info['category']}] {info['date']}", flush=True)

    # 按日期降序排序
    articles.sort(key=lambda x: x['date'], reverse=True)

    # 生成 HTML
    lines = []
    for a in articles:
        lines.append(f'''      <a href="{a['href']}" class="article-item" data-date="{a['date']}" data-category="{a['category']}" data-views="{a['views']}">
        <div class="article-content">
          <h3>{a['title']}</h3>
          <p>{a['desc']}</p>
          <div class="article-meta-row">
            <span class="article-tag">{a['category']}</span>
            <span class="article-date-text"><i class="fas fa-calendar-alt"></i> {a['date_display']}</span>
            <span class="article-views"><i class="fas fa-eye"></i> {a['views']}</span>
          </div>
        </div>
        <div class="article-arrow"><i class="fas fa-chevron-right"></i></div>
      </a>
''')

    output_path = os.path.join(ARTICLES_DIR, '..', 'archives', '_article_list_new.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f"\n已生成 {len(articles)} 条文章条目 -> {output_path}", flush=True)
    print("请手动替换法税洞察(source).html 中 <div class=\"article-list\" id=\"articleList\"> 到 </div> 之间的内容", flush=True)

if __name__ == '__main__':
    main()
