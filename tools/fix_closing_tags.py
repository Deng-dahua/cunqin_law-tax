#!/usr/bin/env python3
"""为8篇旧文章添加缺失的 </script></body></html> 闭合标签"""
import os
import re

ARTICLES_DIR = r'C:\Users\26726\WorkBuddy\2026-05-20-21-20-24\source\articles'

# Old articles (not generated today)
OLD_ARTICLES = [
    'ODI境外投资备案全流程(source).html',
    '业管财税法五维融合(source).html',
    '企业税务风险管控(source).html',
    '企业重组税务规划(source).html',
    '甲乙双视角税务顾问(source).html',
    '跨境电商税务合规(source).html',
    '金税四期全面解读(source).html',
    '高新技术企业税务规划(source).html',
]

for fname in OLD_ARTICLES:
    filepath = os.path.join(ARTICLES_DIR, fname)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already has closing tags
    if content.rstrip().endswith('</html>'):
        print(f'  ⏭️  {fname}: already has closing tags')
        continue
    
    # Check if the file ends with jumpToMatch function (no closing script tag)
    if 'jumpToMatch' in content:
        # The search JS at the end needs </script>
        # The file should end with </script>\n</body>\n</html>
        content = content.rstrip()
        
        # Add closing tags
        if not content.endswith('</script>'):
            if not content.endswith('</html>'):
                content += '\n</script>\n</body>\n</html>\n'
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Verify
        with open(filepath, 'r', encoding='utf-8') as f:
            new_content = f.read()
        script_open = new_content.count('<script')
        script_close = new_content.count('</script>')
        has_html_close = new_content.rstrip().endswith('</html>')
        
        status = '✅' if (script_open == script_close and has_html_close) else '⚠️'
        print(f'  {status} {fname}: script {script_open}/{script_close}, html_closed={has_html_close}')
    else:
        print(f'  ❌ {fname}: jumpToMatch not found!')

print('\nDone!')
