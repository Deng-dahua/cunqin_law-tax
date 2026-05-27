"""P0-2: 为全站17个有 Organization Schema 的页面添加 openingHours + priceRange"""
import re, glob

files = [
    'source/首页(source).html',
    'source/about/关于我们(source).html',
    'source/archives/法税洞察(source).html',
    'source/cases/客户案例(source).html',
    'source/contact/联系我们(source).html',
    'source/services/企业重组与重大交易税务规划(source).html',
    'source/services/全面预算管理体系建设(source).html',
    'source/services/利润增长体系建设(source).html',
    'source/services/十大核心服务(source).html',
    'source/services/常年法税顾问(source).html',
    'source/services/涉税风险检查(source).html',
    'source/services/税务危机应对与争议解决(source).html',
    'source/services/营收增长战略咨询(source).html',
    'source/services/财税内控体系建设(source).html',
    'source/services/财税内训课程定制(source).html',
    'source/services/跨境投资与并购(source).html',
    'source/services/跨境法律及税务规划(source).html',
]

# 要插入的Schema字段（放在 telephone 之前）
new_fields = '''    "openingHours": "Mo-Fr 09:00-18:00",
    "priceRange": "\u00A5\u00A5",
'''

pattern = r'(    "telephone": "13556116691")'
replacement = new_fields + r'\1'

count = 0
for fp in files:
    try:
        with open(fp, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'openingHours' in content:
            print(f'  ⏭️ {fp} (已有openingHours)')
            continue
        
        new_content = re.sub(pattern, replacement, content)
        if new_content != content:
            with open(fp, 'w', encoding='utf-8') as f:
                f.write(new_content)
            count += 1
            short = fp.replace('source/', '').replace('(source).html', '')
            print(f'  ✅ {short}')
    except FileNotFoundError:
        print(f'  ❌ {fp} 不存在')

print(f'\n完成：{count}页添加 openingHours + priceRange')
