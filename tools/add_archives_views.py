#!/usr/bin/env python
"""给法税洞察页所有文章条目添加 countapi.xyz 阅读量展示。使用块级匹配避免跨块回溯问题。"""
import re, os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILEPATH = os.path.join(BASE, 'source', 'archives', '法税洞察(source).html')

with open(FILEPATH, 'r', encoding='utf-8') as f:
    content = f.read()

# 策略：逐条匹配 article-item 块，从 <a href="..."> 中提取 slug，然后在其 article-meta-row 中注入阅读量 span
def process_article_block(match):
    block = match.group(0)
    href_m = re.search(r'href="\.\./articles/([^"]+)\.html"', block)
    if not href_m:
        return block
    slug = href_m.group(1)
    views_span = f'\n            <span class="article-views" data-slug="{slug}">—</span>'
    # 在 </span>\n            </div> (meta-row 结束) 前插入
    # 更精确：在 article-date-text span 之后，article-meta-row 的 </div> 之前
    block = block.replace(
        '</span>\n            </div>',
        '</span>' + views_span + '\n            </div>'
    )
    return block

# 匹配每个 <a href="../articles/..."> ... </a> 的 article-item 完整块
# 用非贪婪匹配到 </a>
count_before = len(re.findall(r'class="article-views"', content))
content = re.sub(
    r'<a href="\.\./articles/[^"]+\.html" class="article-item".*?</a>',
    process_article_block,
    content,
    flags=re.DOTALL
)
count_after = len(re.findall(r'class="article-views"', content))

print(f'Before: {count_before} views, After: {count_after} views')

# 验证 unknown 数量
unknown = len(re.findall(r'data-slug="unknown"', content))
print(f'Unknown slugs: {unknown}')

# 添加 countapi.xyz fetch JS，在 </body> 前
COUNTAPI_JS = '''\x3C!-- 实时阅读量（countapi.xyz） -->
<script>
(function(){
  var views = document.querySelectorAll('.article-views');
  views.forEach(function(v){
    var slug = v.getAttribute('data-slug');
    if (!slug) { v.textContent = '0'; return; }
    fetch('https://api.countapi.xyz/get/cunqin-tax/' + encodeURIComponent(slug))
      .then(function(r){ return r.json(); })
      .then(function(d){
        if (d && d.value !== undefined) { v.textContent = d.value + '次阅读'; }
      })
      .catch(function(){});
  });
})();
</script>
\x3C/body>'''

content = content.replace('</body>', COUNTAPI_JS)

with open(FILEPATH, 'w', encoding='utf-8') as f:
    f.write(content)

print('Done.')
