"""批量替换所有文章详情页的"更多文章"区块为动态Top5版本"""
import os, re

articles_dir = 'source/articles'

# 新的"更多文章"HTML（不含CTA注释）
new_section = '''<!-- ===== 更多文章 ===== -->
<section class="more-section">
  <div class="container-dt">
    <div class="section-header-dt">
      <h2 id="更多文章">更多文章
      <p>阅读其他精彩内容</p>
    </div>
    <div class="more-list" id="more-list">
      <!-- 动态加载中... -->
    </div>
    <p style="text-align:center;font-size:0.85rem;color:var(--dt-text-light);margin-top:1.2rem;">共 <span id="more-total">0</span> 篇文章</p>
  </div>
</section>'''

# 动态加载JS
new_js = '''
<!-- ===== 更多文章动态加载 ===== -->
<script>
(function(){
  var list = document.getElementById('more-list');
  var totalEl = document.getElementById('more-total');
  var currentPath = window.location.pathname;
  var currentSlug = currentPath.split('/').pop();
  fetch('/cunqin_law-tax/home-insights.json')
    .then(function(r){ return r.json(); })
    .then(function(data){
      totalEl.textContent = data.total;
      var others = data.articles.filter(function(a){
        return !a.url.endsWith(currentSlug);
      });
      var top5 = others.slice(0, 5);
      var html = '';
      top5.forEach(function(a){
        var href = '/cunqin_law-tax/' + a.url;
        html += '<a href="' + href + '" class="more-item">';
        html += '<div class="more-cat">' + a.category + '</div>';
        html += '<div class="more-info">';
        html += '<h4>' + a.title + '</h4>';
        html += '<p>' + a.excerpt + '</p>';
        html += '</div>';
        html += '<div class="more-arrow"><i class="fas fa-chevron-right"></i></div>';
        html += '</a>';
      });
      list.innerHTML = html;
    })
    .catch(function(){
      list.innerHTML = '<p style="text-align:center;color:#999;">文章加载中，请稍候...</p>';
    });
})();
</script>
'''

# 正则：匹配"更多文章"区块 + JS + CTA注释尾部
# 替换目标: <!-- ===== 更多文章 ===== --> ... </section>\n\n<!-- ===== CTA ===== -->
old_pattern = re.compile(
    r'<!-- ===== 更多文章 ===== -->.*?</section>\s*\n\s*<!-- ===== CTA ===== -->',
    re.DOTALL
)

# 替换为: 新Section + JS + CTA注释
replacement = new_section + '\n' + new_js + '\n\n' + '<!-- ===== CTA ===== -->'

files = sorted([f for f in os.listdir(articles_dir) if f.endswith('.html')])
print(f'找到 {len(files)} 个文章文件\n')

count = 0
for fname in files:
    path = os.path.join(articles_dir, fname)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content, n = old_pattern.subn(replacement, content)
    
    if n == 0:
        print(f'  ⚠ {fname}: 未匹配到区块')
        continue
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    count += 1
    print(f'  ✓ {fname}')

print(f'\n成功替换 {count}/{len(files)} 个文件')
