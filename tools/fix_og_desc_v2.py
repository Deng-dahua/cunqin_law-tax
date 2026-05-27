"""追加后缀扩展 og:description 至 120+ 字符"""
import re, os

base = r'C:\Users\26726\WorkBuddy\2026-05-20-21-20-24\source\articles'

suffix = "——本文由存勤法税服务（广州）有限公司创始人邓达华撰写。存勤法税深耕粤港澳大湾区企业财税服务市场，以业管财税法五维融合为核心方法论，为华南地区企业提供可落地的专业税务解决方案。"

files = [
    'chengben-feiyong-shuiwu-hegui(source).html',
    'chukou-tuishui-hegui-fengkong(source).html',
    'CRS-kuajing-zichan-shenbao(source).html',
    'geren-suodeshui-huisuan-qingjiao(source).html',
    'gongzixinjin-gerensuodeshui-chouhua(source).html',
    'gudong-hongli-shuiwu-chouhua(source).html',
    'guquan-daichi-shuiwu-fengxian(source).html',
    'guquan-zhuantang-geren-suodeshui(source).html',
    'hehuo-qiye-shuiwu-jiexi(source).html',
    'IPO-shuiwu-hegui-jiagou(source).html',
    'qiye-kuisun-mibu-guize(source).html',
    'qiyesuodeshui-huisuan-qingjiao(source).html',
    'shuiwu-xingzheng-fuyi(source).html',
    'shuzihua-shuiwu-guanli-zhuanxing(source).html',
    'simu-jijin-shuiwu-chouhua(source).html',
    'xukai-fapiao-falv-houguo(source).html',
    'yanfa-feiyong-jiakou-kouchu(source).html',
    'yinhua-shuifa-shishi-yaodian(source).html',
    'zengzhishui-liudi-tuishui(source).html',
    'zhongxiao-qiye-shuishou-youhui(source).html',
]

count = 0
for fname in files:
    fp = os.path.join(base, fname)
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Append suffix to og:description content
    def append_suffix(m):
        existing = m.group(0)
        if suffix in existing:
            return existing  # already appended
        # Insert suffix before closing quote
        return existing[:-1] + suffix + '"'
    
    content = re.sub(r'property="og:description"\s+content="[^"]+"', append_suffix, content)
    content = re.sub(r'name="description"\s+content="[^"]+"', append_suffix, content)
    
    # Also expand twitter:description
    twitter_match = re.search(r'name="twitter:description"\s+content="([^"]*)"', content)
    if twitter_match:
        tw = twitter_match.group(1)
        if len(tw) < 100:
            new_tw = tw[:90] + '…' if len(tw) > 90 else tw
            content = content.replace(
                f'content="{tw}"',
                f'content="{new_tw}"'
            )
    
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(content)
    
    # Verify
    new_match = re.search(r'property="og:description"\s+content="([^"]+)"', content)
    new_len = len(new_match.group(1)) if new_match else 0
    count += 1
    print(f'  ✓ {fname} ({new_len} chars)')

print(f'\nDone: {count} files')
