"""批量修复文章目录TOC: 跳过结语, 延伸阅读列为顶层项"""
import os, re

articles_dir = 'source/articles'

# 旧代码段（精确匹配）
old_block = '''    headings.forEach(function(h, i) {
      if (!h.id) { h.id = 'section-' + i; }
      var li = document.createElement('li');
      li.className = 'article-toc-item' + (h.tagName === 'H3' ? ' toc-sub' : '');
      var a = document.createElement('a');
      a.href = '#' + h.id;
      a.className = 'article-toc-link' + (h.tagName === 'H3' ? ' toc-h3' : '');
      a.textContent = h.textContent.replace(/^\\d+\\.?\\s*/, '');'''

# 新代码段
new_block = '''    headings.forEach(function(h, i) {
      if (!h.id) { h.id = 'section-' + i; }
      var text = h.textContent.replace(/^\\d+\\.?\\s*/, '');
      // 跳过结语章节
      if (h.id === '结语' || text === '结语') return;
      var isH3 = h.tagName === 'H3';
      var isRelated = h.classList.contains('related-heading');
      var li = document.createElement('li');
      li.className = 'article-toc-item' + (isH3 && !isRelated ? ' toc-sub' : '');
      var a = document.createElement('a');
      a.href = '#' + h.id;
      a.className = 'article-toc-link' + (isH3 && !isRelated ? ' toc-h3' : '');
      a.textContent = text;'''

files = sorted([f for f in os.listdir(articles_dir) if f.endswith('.html')])

count = 0
for fname in files:
    path = os.path.join(articles_dir, fname)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if old_block not in content:
        print(f'  ⚠ {fname}: 未匹配到TOC代码块')
        continue
    
    new_content = content.replace(old_block, new_block)
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    count += 1
    print(f'  ✓ {fname}')

print(f'\n成功修复 {count}/{len(files)} 个文件')
