#!/usr/bin/env python3
"""同步新文章的索引：sitemap.xml, home-insights.json, search-index.json, 法税洞察页"""
import json, os, re
from datetime import date

ARTICLES = [
    {
        "slug": "xiaofeishui-shuiwu-guihua",
        "title": "消费税税务规划：从征税范围到纳税筹划的全流程指南",
        "date": "2026-05-27",
        "category": "行业洞察",
        "excerpt": "全面解读消费税征税范围、税率结构及纳税筹划策略，涵盖烟酒、化妆品、汽车、成品油、高档手表等15类应税消费品。",
        "views": 380,
    },
    {
        "slug": "qishui-zhengce-jiedu",
        "title": "契税政策全面解读：征税范围、税率优惠与实务操作",
        "date": "2026-05-27",
        "category": "政策解读",
        "excerpt": "全面解读契税法核心制度：土地使用权出让与转让、房屋买卖赠与互换的征税规则、法定税率与优惠税率适用条件。",
        "views": 410,
    },
    {
        "slug": "ziyuanshui-huanbao-shuiwu",
        "title": "资源税与环境保护税实务指南：征税规则与企业合规要点",
        "date": "2026-05-27",
        "category": "政策解读",
        "excerpt": "系统讲解资源税与环境保护税两大绿色税种：资源税的征税范围、从价与从量计征规则；环境保护税的四大应税污染物。",
        "views": 360,
    },
    {
        "slug": "qiye-fenli-shuiwu-chuli",
        "title": "企业分立的税务处理全攻略：所得税、增值税、契税与印花税",
        "date": "2026-05-27",
        "category": "财税咨询",
        "excerpt": "全面解析企业分立的税务处理规则：两种分立形式、企业所得税特殊性税务处理适用条件、增值税及契税免税规则。",
        "views": 450,
    },
]

def update_sitemap():
    spath = "source/sitemap.xml"
    with open(spath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Add missing closing tag if absent
    if not content.strip().endswith("</urlset>"):
        if "</url>" in content:
            # Find last </url> and insert </urlset> after it
            last_url_close = content.rfind("</url>")
            content = content[:last_url_close + 6] + "\n</urlset>\n"
            print("  [FIX] 补上缺失的 </urlset> 闭合标签")
        else:
            print("ERROR: sitemap has no </url> tags!")
            return False
    
    # Find </urlset> and insert before it
    insert_pos = content.rfind("</urlset>")
    if insert_pos == -1:
        print("ERROR: Could not find </urlset> in sitemap!")
        return False
    
    new_urls = ""
    for a in ARTICLES:
        url = f"""  <url>
    <loc>https://cunqin.tax/articles/{a["slug"]}.html</loc>
    <lastmod>{a["date"]}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.6</priority>
    <xhtml:link rel="alternate" hreflang="zh-CN" href="https://cunqin.tax/articles/{a["slug"]}.html"/>
  </url>
"""
        new_urls += url
    
    new_content = content[:insert_pos] + new_urls + content[insert_pos:]
    with open(spath, "w", encoding="utf-8") as f:
        f.write(new_content)
    
    count = content[:insert_pos].count("<url>") + len(ARTICLES)
    print(f"  [OK] sitemap.xml：新增 {len(ARTICLES)} 条 URL，共 {count} 条")
    return True

def update_home_insights():
    fpath = "source/home-insights.json"
    with open(fpath, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # Handle both list and dict formats
    if isinstance(data, dict):
        articles = data.get("articles", [])
    else:
        articles = data
    
    existing_slugs = set()
    for a in articles:
        if "url" in a:
            existing_slugs.add(a["url"].split("/")[-1].replace(".html", ""))
        elif "slug" in a:
            existing_slugs.add(a["slug"])
    
    added = 0
    for a in reversed(ARTICLES):  # reverse so first in list appears first
        if a["slug"] in existing_slugs:
            continue
        entry = {
            "title": a["title"],
            "url": f"articles/{a['slug']}.html",
            "date": a["date"],
            "category": a["category"],
            "views": a["views"],
            "excerpt": a["excerpt"],
        }
        articles.insert(0, entry)
        added += 1
    
    # Sort by views desc
    articles.sort(key=lambda x: x["views"], reverse=True)
    
    # Write back preserving dict structure
    if isinstance(data, dict):
        data["total"] = len(articles)
        data["articles"] = articles
        output = data
    else:
        output = articles
    
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"  [OK] home-insights.json：新增 {added} 条，共 {len(articles)} 条")
    return True

def update_search_index():
    fpath = "source/search-index.json"
    with open(fpath, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    existing_urls = {item["url"] for item in data}
    
    added = 0
    for a in ARTICLES:
        url = f"/articles/{a['slug']}.html"
        if url in existing_urls:
            continue
        entry = {
            "title": a["title"],
            "url": url,
            "text": a["excerpt"],
            "category": a["category"],
            "date": a["date"],
        }
        data.append(entry)
        added += 1
    
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"  [OK] search-index.json：新增 {added} 条，共 {len(data)} 条")
    return True

def update_archives_page():
    # Try both possible paths
    candidates = ["source/archives/法税洞察(source).html", "source/archives/index.html"]
    fpath = None
    for c in candidates:
        if os.path.exists(c):
            fpath = c
            break
    if not fpath:
        print("  [SKIP] 法税洞察页不存在")
        return True
    
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()
    
    added = 0
    for a in reversed(ARTICLES):
        # Check if already exists
        if f'''href="{a['slug']}.html"''' in content:
            continue
        
        # Build article card HTML
        card = f'''      <div class="article-item" data-category="{a['category']}" data-date="{a['date']}">
        <div class="article-meta">
          <span class="article-cat">{a['category']}</span>
          <time datetime="{a['date']}">{a['date']}</time>
        </div>
        <h3><a href="articles/{a['slug']}.html">{a['title']}</a></h3>
        <p>{a['excerpt']}</p>
      </div>
'''
        # Insert before </div> <!-- end articles-list -->
        marker = '  </div> <!-- end articles-list -->'
        if marker in content:
            content = content.replace(marker, card + marker, 1)
            added += 1
    
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"  [OK] 法税洞察页：新增 {added} 个文章卡片")
    return True

if __name__ == "__main__":
    print("=" * 50)
    print("同步索引文件（4 篇 GEO 文章）")
    print("=" * 50)
    
    update_sitemap()
    update_home_insights()
    update_search_index()
    update_archives_page()
    
    print("\n✅ 全部索引同步完成！")
