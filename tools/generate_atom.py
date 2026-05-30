#!/usr/bin/env python3
"""Generate atom.xml for cunqin.tax with all 77 articles."""
import re
import os
from datetime import datetime

ARTICLES_DIR = "source/articles"
OUTPUT_PATH = "source/atom.xml"
BASE_URL = "https://cunqin.tax"
FEED_ID = "tag:cunqin.tax,2026:feed"
SITE_TITLE = "存勤法税 — 业管财税法五维融合"
SITE_AUTHOR = "邓达华"
SITE_EMAIL = "contact@cunqin.tax"

def extract_metadata(filepath):
    """Extract title, slug, date, description from an article HTML file."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Frontmatter permalink -> slug
    slug_match = re.search(r'permalink:\s*/articles/(.+?)\.html', content)
    slug = slug_match.group(1) if slug_match else None

    # Title from <title> tag
    title_match = re.search(r'<title>(.+?)</title>', content)
    raw_title = title_match.group(1) if title_match else None
    # Strip site name suffix
    if raw_title:
        title = re.sub(r'\s*[-–|]\s*存勤法税.*$', '', raw_title).strip()
    else:
        title = None

    # Date from article:published_time
    date_match = re.search(r'article:published_time"\s+content="(\d{4}-\d{2}-\d{2})"', content)
    if not date_match:
        date_match = re.search(r'<time datetime="(\d{4}-\d{2}-\d{2})"', content)
    date_str = date_match.group(1) if date_match else "2026-05-24"
    # Convert to ISO 8601 datetime
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        iso_date = dt.strftime("%Y-%m-%dT00:00:00+08:00")
    except ValueError:
        iso_date = date_str + "T00:00:00+08:00"

    # Description from og:description or meta description
    desc_match = re.search(r'<meta\s+property="og:description"\s+content="(.+?)"', content)
    if not desc_match:
        desc_match = re.search(r'<meta\s+name="description"\s+content="(.+?)"', content)
    description = desc_match.group(1) if desc_match else ""
    # Clean HTML entities and truncate
    description = description.replace("&quot;", '"').replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
    if len(description) > 300:
        description = description[:297] + "..."

    return {
        "slug": slug,
        "title": title,
        "date": iso_date,
        "description": description,
    }

def main():
    articles = []
    files = sorted(os.listdir(ARTICLES_DIR))
    for fname in files:
        if not fname.endswith(".html"):
            continue
        filepath = os.path.join(ARTICLES_DIR, fname)
        meta = extract_metadata(filepath)
        if meta["slug"] and meta["title"]:
            articles.append(meta)
        else:
            print(f"  WARNING: Could not extract metadata from {fname}")

    # Sort by date descending
    articles.sort(key=lambda a: a["date"], reverse=True)

    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")

    xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom" xml:lang="zh-CN">
  <id>{FEED_ID}</id>
  <title>{SITE_TITLE}</title>
  <subtitle>存勤法税服务（广州）有限公司 — 专业法税洞察，助力企业合规经营</subtitle>
  <link href="{BASE_URL}/atom.xml" rel="self" type="application/atom+xml"/>
  <link href="{BASE_URL}/" rel="alternate" type="text/html"/>
  <updated>{now}</updated>
  <author>
    <name>{SITE_AUTHOR}</name>
    <email>{SITE_EMAIL}</email>
    <uri>{BASE_URL}/about/deng-dahua/</uri>
  </author>
  <rights>Copyright &amp;copy; {datetime.now().year} 存勤法税服务（广州）有限公司</rights>
  <generator uri="https://cunqin.tax">存勤法税 CMS</generator>
'''

    for a in articles:
        entry_id = f"tag:cunqin.tax,2026:article:{a['slug']}"
        url = f"{BASE_URL}/articles/{a['slug']}.html"
        # Escape XML special chars in title and description
        title_safe = a["title"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
        desc_safe = a["description"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

        xml += f'''  <entry>
    <id>{entry_id}</id>
    <title>{title_safe}</title>
    <link href="{url}" rel="alternate" type="text/html"/>
    <published>{a["date"]}</published>
    <updated>{a["date"]}</updated>
    <summary type="html">{desc_safe}</summary>
    <author>
      <name>{SITE_AUTHOR}</name>
    </author>
  </entry>
'''

    xml += "</feed>\n"

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(xml)

    print(f"Generated {OUTPUT_PATH} with {len(articles)} articles")
    print(f"Expected:        77 articles")
    if len(articles) < 77:
        print(f"WARNING: Missing {77 - len(articles)} articles!")

if __name__ == "__main__":
    main()
