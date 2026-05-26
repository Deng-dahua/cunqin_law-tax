"""从 archives 页面提取所有文章数据，生成 home-insights.json"""
import re, json

with open('source/archives/法税洞察(source).html', 'r', encoding='utf-8') as f:
    content = f.read()

# 提取每个 article-item
pattern = r'<a href="([^"]+)" class="article-item" data-date="([^"]+)" data-category="([^"]+)" data-views="(\d+)">\s*<div class="article-content">\s*<h3>(.+?)</h3>\s*<p>(.+?)</p>'
matches = re.findall(pattern, content, re.DOTALL)

articles = []
for url, date, category, views, title, excerpt in matches:
    # URL: ../articles/xxx.html → articles/xxx.html (relative to homepage)
    clean_url = url.replace('../articles/', 'articles/')
    # Clean excerpt: remove HTML tags if any, trim
    excerpt = re.sub(r'<[^>]+>', '', excerpt).strip()
    articles.append({
        'title': title.strip(),
        'url': clean_url,
        'date': date,
        'category': category,
        'views': int(views),
        'excerpt': excerpt
    })

# Sort by views descending
articles.sort(key=lambda x: x['views'], reverse=True)

# Output
output = {
    'total': len(articles),
    'articles': articles
}

with open('source/home-insights.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f'✅ 提取 {len(articles)} 篇文章 → source/home-insights.json')
print(f'   Top 5:')
for a in articles[:5]:
    print(f'   {a["views"]:>5}  {a["title"][:40]}')
