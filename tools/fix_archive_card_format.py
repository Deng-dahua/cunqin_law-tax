"""修复 GEO 文章归档卡片格式：从 article-date 块格式 → 标准 article-meta-row 格式"""
import re

with open('source/archives/法税洞察(source).html', 'r', encoding='utf-8') as f:
    content = f.read()

count = 0

def transform_geo_card(match):
    global count
    block = match.group(0)
    
    # Extract <a> tag attributes
    a_tag_match = re.search(r'<a\s+href="([^"]+)"\s+class="article-item"\s+data-date="([^"]+)"\s+data-category="([^"]+)"\s+data-views="(\d+)"', block)
    if not a_tag_match:
        return block  # shouldn't happen
    
    href = a_tag_match.group(1)
    date_iso = a_tag_match.group(2)  # e.g., "2026-05-27"
    category = a_tag_match.group(3)
    views = a_tag_match.group(4)
    
    # Extract h3 title
    h3_match = re.search(r'<h3>(.+?)</h3>', block, re.DOTALL)
    title = h3_match.group(1).strip() if h3_match else ''
    
    # Extract <p> excerpt
    p_match = re.search(r'<p>(.+?)</p>', block, re.DOTALL)
    excerpt = p_match.group(1).strip() if p_match else ''
    
    # Convert date: "2026-05-27" → "2026.05.27"
    date_display = date_iso.replace('-', '.')
    
    # Determine indentation from original <a> tag
    indent_match = re.search(r'^(\s*)<a href="' + re.escape(href), block, re.MULTILINE)
    indent = indent_match.group(1) if indent_match else '      '
    inner_indent = indent + '  ' if indent else '        '
    
    # Build standard format (matching old articles exactly)
    new_block = f'''{indent}<a href="{href}" class="article-item" data-date="{date_iso}" data-category="{category}" data-views="{views}">
{inner_indent}<div class="article-content">
{inner_indent}  <h3>{title}</h3>
{inner_indent}  <p>{excerpt}</p>
{inner_indent}  <div class="article-meta-row">
{inner_indent}    <span class="article-tag">{category}</span>
{inner_indent}    <span class="article-date-text"><i class="fas fa-calendar-alt"></i> {date_display}</span>
{inner_indent}    <span class="article-views"><i class="fas fa-eye"></i> {views}</span>
{inner_indent}  </div>
{inner_indent}</div>
{inner_indent}<div class="article-arrow"><i class="fas fa-chevron-right"></i></div>
{indent}</a>'''
    
    count += 1
    print(f'  [{count}] {href.split("/")[-1].replace(".html","")} → {date_display} | {category} | {views}阅读')
    return new_block

# Pattern: match <a class="article-item" ...> containing <div class="article-date"> up to </a>
# This finds GEO articles (those with article-date div)
pattern = re.compile(
    r'<a\s+href="[^"]+"\s+class="article-item"\s+data-date="[^"]+"\s+data-category="[^"]+"\s+data-views="\d+">\s*'
    r'<div\s+class="article-date">.*?</div>\s*'
    r'<div\s+class="article-content">.*?</div>\s*'
    r'<div\s+class="article-arrow">.*?</div>\s*'
    r'</a>',
    re.DOTALL
)

print(f'Found {len(pattern.findall(content))} GEO-format cards to convert:')
new_content = pattern.sub(transform_geo_card, content)
print(f'\nConverted: {count} cards')

# Check the transformation didn't break anything
assert 'class="article-date"' not in new_content, 'ERROR: article-date blocks still exist!'
assert new_content.count('article-item') == content.count('article-item'), f'ERROR: article count changed! {new_content.count("article-item")} vs {content.count("article-item")}'

with open('source/archives/法税洞察(source).html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print('[OK] All GEO article cards converted to standard format')
