"""
GEO批量修复脚本
1. 批量添加 baidu-site-verification (codeva-9SPpSVW5X6)
2. 修复 og:description 过短的文章
3. 排除辅助文件
"""
import sys, re, glob, os
sys.stdout.reconfigure(encoding='utf-8')

BASE = r'C:\Users\26726\WorkBuddy\2026-05-20-21-20-24\source'
BAIDU_TOKEN = 'codeva-9SPpSVW5X6'
BAIDU_META = f'<meta name="baidu-site-verification" content="{BAIDU_TOKEN}" />'

def fix_baidu_verification():
    """批量补全 baidu-site-verification"""
    # Exclude template/generated files
    exclude = [
        '_article_list_generated.html',
        '_article_list_new.html',
        'search.html',
    ]
    
    # Find all HTML files that need fix
    files = []
    for root, dirs, filenames in os.walk(BASE):
        dirs[:] = [d for d in dirs if d not in ('.git',)]
        for fn in filenames:
            if fn.endswith('.html') and fn not in exclude:
                files.append(os.path.join(root, fn))
    
    fixed = 0
    for fp in files:
        with open(fp, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if BAIDU_TOKEN in content:
            continue  # Already has it
        
        if 'baidu-site-verification' in content:
            # Has old/wrong token - replace
            content = re.sub(
                r'<meta name="baidu-site-verification" content="[^"]*" />',
                BAIDU_META,
                content
            )
        else:
            # Completely missing - add after msvalidate or charset
            if '<meta name="msvalidate.01"' in content:
                content = content.replace(
                    '<meta name="msvalidate.01"',
                    f'{BAIDU_META}\n  <meta name="msvalidate.01"'
                )
            elif '<meta charset=' in content:
                content = content.replace(
                    '<meta charset=',
                    f'{BAIDU_META}\n  <meta charset='
                )
            else:
                # Add after <head>
                content = content.replace('<head>', f'<head>\n  {BAIDU_META}')
        
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(content)
        rel = os.path.relpath(fp, BASE)
        print(f'  [OK] {rel}')
        fixed += 1
    
    print(f'\nBaidu verification fixed: {fixed} files')
    return fixed

def fix_og_description_short():
    """修复 og:description 过短的文章 (需要手动扩展)"""
    short_files = [
        ('公司注销清算的税务处理全流程(source).html', 41),
        ('关联方借款的税务风险与合规处理(source).html', 38),
        ('土地增值税清算实务与筹划策略(source).html', 29),
        ('房地产企业税务筹划(source).html', 104),
        ('税收协定待遇申请实务指南(source).html', 35),
        ('股东借款税务风险(source).html', 107),
        ('非货币性资产投资的税务处理(source).html', 30),
    ]
    
    articles_dir = os.path.join(BASE, 'articles')
    fixed = 0
    for fn, cur_len in short_files:
        fp = os.path.join(articles_dir, fn)
        if not os.path.exists(fp):
            print(f'  [MISS] {fn}')
            continue
        
        with open(fp, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find current og:description
        m = re.search(r'(<meta property="og:description"\s+content=")([^"]*)(")', content)
        if not m:
            print(f'  [NO_OG] {fn}')
            continue
        
        cur_desc = m.group(2)
        if len(cur_desc) >= 120:
            print(f'  [SKIP] {fn} - already {len(cur_desc)} chars')
            continue
        
        # Extract page keyword context to extend
        h1_m = re.search(r'<h1[^>]*>(.*?)</h1>', content)
        h1 = h1_m.group(1) if h1_m else fn
        
        print(f'  [TODO] {fn}: {cur_len} chars -> need {120-cur_len} more. H1: {h1[:50]}')
        
    return fixed

if __name__ == '__main__':
    print("=== 1. 批量修复 baidu-site-verification ===")
    fix_baidu_verification()
    print("\n=== 2. 修复 og:description 过短 ===")
    fix_og_description_short()
