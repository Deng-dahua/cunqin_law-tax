#!/usr/bin/env python
"""批量给77篇文章添加 countapi.xyz 实时阅读量计数。"""
import re, os, sys

ARTICLES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'source', 'articles')

VIEW_SPAN = '<span><i class="fas fa-eye"></i> <span id="articleViewCount">...</span> 次阅读</span>'

COUNTAPI_JS_TEMPLATE = '''\x3Cscript>
(function(){
  var viewEl = document.getElementById('articleViewCount');
  if (!viewEl) return;
  var path = window.location.pathname;
  var slug = path.split('/').filter(Boolean).pop().replace('.html','');
  if (!slug) { viewEl.textContent = '0'; return; }
  // hit: increment counter
  fetch('https://api.countapi.xyz/hit/cunqin-tax/' + encodeURIComponent(slug))
    .then(function(r){ return r.json(); })
    .then(function(d){ viewEl.textContent = (d && d.value) ? d.value : '0'; })
    .catch(function(){ viewEl.textContent = '0'; });
})();
\x3C/script>'''

def process_article(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract slug from permalink frontmatter
    m = re.search(r'permalink:\s*/articles/([^\s]+)\.html', content)
    if not m:
        print(f'  SKIP: no permalink found in {os.path.basename(filepath)}')
        return False
    slug = m.group(1)
    base = os.path.basename(filepath)

    # Check if already has countapi
    if 'countapi.xyz' in content:
        print(f'  SKIP: already has countapi in {base}')
        return False

    # Check if already has articleViewCount
    if 'articleViewCount' in content:
        print(f'  SKIP: already has articleViewCount in {base}')
        return False

    # 1. Add view count span in hero meta area (<div class="art-meta">)
    # Look for the hero meta div and add view span after the author span
    # Pattern: <span><i class="fas fa-user-edit"></i> ... </span>    </div>
    meta_pattern = r'(<span><i class="fas fa-user-edit"></i> [^<]+</span>\s*)</div>'
    
    if not re.search(meta_pattern, content):
        # Try alternative pattern
        meta_pattern = r'(<span><i class="fas fa-user-edit"></i>[^<]*</span>\s*)</div>'
    
    if re.search(meta_pattern, content):
        content = re.sub(meta_pattern, r'\1' + VIEW_SPAN + '\n    </div>', content, count=1)
    else:
        print(f'  WARN: cannot find hero meta insertion point in {base}')
        return False

    # 2. Add countapi JS before </body>
    body_pattern = r'(</body>)'
    content = re.sub(body_pattern, COUNTAPI_JS_TEMPLATE + '\n\n\\1', content, count=1)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f'  OK: {base} (slug={slug})')
    return True

def main():
    files = sorted([f for f in os.listdir(ARTICLES_DIR) if f.endswith('(source).html')])
    print(f'Found {len(files)} article source files.\n')

    ok = 0
    for f in files:
        filepath = os.path.join(ARTICLES_DIR, f)
        if process_article(filepath):
            ok += 1

    print(f'\nDone: {ok}/{len(files)} processed successfully.')

if __name__ == '__main__':
    main()
