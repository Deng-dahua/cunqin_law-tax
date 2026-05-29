"""
============================================================
重置全站阅读量为0，并实现 countapi.xyz 实时阅读量抓取
============================================================
操作：
1. 77篇文章: 替换旧的静态base计数JS → countapi.xyz实时计数JS
2. home-insights.json: 全部views→0，按日期降序排列
3. 验证: 确认旧模式已清零、新模式已覆盖
"""
import os, re, json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(ROOT, 'source', 'articles')
HI_PATH = os.path.join(ROOT, 'source', 'home-insights.json')

# 新的实时计数JS模板（countapi.xyz + 本地兜底）
NEW_COUNTER_TEMPLATE = """<script>
  /* ===== 实时阅读量统计（countapi.xyz） ===== */
  (function(){
    var slug = '__SLUG__';
    var el = document.getElementById('view-' + slug);
    if (!el) return;
    el.textContent = '0';
    fetch('https://api.countapi.xyz/hit/cunqin-tax/' + slug)
      .then(function(r){ return r.json(); })
      .then(function(d){ el.textContent = d.value.toLocaleString(); })
      .catch(function(){});
  })();
</script>
"""

# ===========================
# Part 1: 替换所有文章的JS
# ===========================

MARKER = '/* ===== 动态阅读量计数 ===== */'
MARKER_V2 = '/* ===== 实时阅读量统计（countapi.xyz） ===== */'

updated = 0
skipped = 0
errors = []

for fname in sorted(os.listdir(SRC_DIR)):
    if not fname.endswith('(source).html'):
        continue
    fpath = os.path.join(SRC_DIR, fname)

    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 检查是否已经是新模式
    if MARKER_V2 in content:
        print(f'  SKIP (already new): {fname}')
        skipped += 1
        continue

    # 找到旧标记位置
    start = content.find(MARKER)
    if start == -1:
        print(f'  SKIP (no marker): {fname}')
        skipped += 1
        continue

    # 找到包围的 <script> 和 </script>
    script_open = content.rfind('<script>', 0, start)
    script_close = content.find('</script>', start)
    if script_open == -1 or script_close == -1:
        errors.append(f'{fname}: malformed script block')
        print(f'  ERROR (malformed): {fname}')
        continue

    old_block = content[script_open:script_close + len('</script>')]

    # 提取 slug
    sm = re.search(r"var slug = '([^']+)';", old_block)
    if not sm:
        errors.append(f'{fname}: no slug found')
        print(f'  ERROR (no slug): {fname}')
        continue

    slug = sm.group(1)
    new_block = NEW_COUNTER_TEMPLATE.replace('__SLUG__', slug)

    content = content.replace(old_block, new_block)
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)

    updated += 1
    print(f'  OK: {fname}  slug={slug}')

print(f'\n=== Part 1 Done: {updated} updated, {skipped} skipped, {len(errors)} errors ===')

# ===========================
# Part 2: home-insights.json 清零
# ===========================

with open(HI_PATH, 'r', encoding='utf-8') as f:
    hi = json.load(f)

arts = hi['articles']
for a in arts:
    a['views'] = 0

# 按日期降序排列（所有views=0时的合理排序）
arts.sort(key=lambda a: a.get('date', '2020-01-01'), reverse=True)
hi['articles'] = arts

with open(HI_PATH, 'w', encoding='utf-8') as f:
    json.dump(hi, f, ensure_ascii=False, indent=2)

print(f'\n=== Part 2 Done: home-insights.json {len(arts)} articles, all views=0 ===')

# ===========================
# Part 3: 验证
# ===========================

print('\n=== Part 3: Verification ===')

# 检查旧模式残留
old_remaining = 0
new_found = 0
for fname in sorted(os.listdir(SRC_DIR)):
    if not fname.endswith('(source).html'):
        continue
    fpath = os.path.join(SRC_DIR, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    if MARKER in content:
        old_remaining += 1
        print(f'  OLD MARKER STILL PRESENT: {fname}')
    if MARKER_V2 in content:
        new_found += 1

print(f'Old marker remaining: {old_remaining} (should be 0)')
print(f'New marker found: {new_found} (should be 77)')

# 检查 home-insights.json
with open(HI_PATH, 'r', encoding='utf-8') as f:
    hi = json.load(f)
non_zero = sum(1 for a in hi['articles'] if a.get('views', 0) != 0)
print(f'home-insights.json non-zero views: {non_zero} (should be 0)')

print('\n=== All Done ===')
