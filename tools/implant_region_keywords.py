"""P0-1: 为文章正文植入地域关键词（广州/大湾区/华南）
策略：P3概述段落后+结尾段落后，各插入一句自然地域引用
"""
import re, os, glob, random

articles_dir = 'source/articles'
files = sorted(glob.glob(f'{articles_dir}/*.html'))

# 地域短语池
mid_phrases = [
    "对于广州地区的企业而言，这一问题的现实紧迫性尤为突出。",
    "在广州及粤港澳大湾区，企业对此类税务问题的关注度持续走高。",
    "粤港澳大湾区企业在这一领域的合规需求正快速增长。",
    "从华南地区企业的实际运营来看，此类税务风险不容忽视。",
    "广州作为华南经济中心，企业面临的涉税监管环境日趋严格。",
]

end_phrases = [
    "对于广州及粤港澳大湾区企业而言，提前做好税务合规布局，是在复杂监管环境下稳健经营的关键。",
    "广州作为华南经济中心，企业面临的税务监管环境日趋严格。存勤法税立足广州，服务粤港澳大湾区，以18年实战经验助力企业筑牢财税合规防线。",
    "在粤港澳大湾区高质量发展的时代背景下，存勤法税（广州）愿以业管财税法五维融合方法论，助力华南企业行稳致远。",
    "大湾区企业正站在新一轮发展的起点，财税合规是可持续发展的基石。存勤法税，立足广州，以18年专业积累服务大湾区企业。",
    "华南地区企业正面临前所未有的税务合规挑战。存勤法税（广州）以实战经验为依托，为粤港澳大湾区企业保驾护航。",
]

def needs_keywords(content):
    """检查 article-body 正文是否已有地域关键词"""
    m = re.search(r'<article class="article-body">(.*?)</article>', content, re.DOTALL)
    if not m:
        return False  # 安全起见跳过
    body_text = re.sub(r'<[^>]+>', ' ', m.group(1))
    for kw in ['广州', '广东', '大湾区', '华南', '粤港澳']:
        if kw in body_text:
            return False
    return True

def insert_phrases(content):
    """在 article-body 中插入地域短语，返回修改后内容"""
    m = re.search(r'(<article class="article-body">.*?</article>)', content, re.DOTALL)
    if not m:
        return content
    body_block = m.group(1)
    body_start = m.start(1)
    
    # 找到所有 <p>...</p>
    ps = list(re.finditer(r'<p[^>]*>.*?</p>', body_block, re.DOTALL))
    if len(ps) < 3:
        return content
    
    # 找到 P3 的结束位置（在原始content中）
    p3_end_abs = body_start + ps[2].end()
    last_p_end_abs = body_start + ps[-1].end()
    
    modified = content
    
    # 插入1：P3后加地域过渡句
    mid = random.choice(mid_phrases)
    modified = modified[:p3_end_abs] + '\n<p>' + mid + '</p>\n' + modified[p3_end_abs:]
    
    # 插入2：最后一段后加结尾地域句（需要重新计算位置，因为上面插入改变了偏移）
    offset = len('\n<p>' + mid + '</p>\n')
    modified = modified[:last_p_end_abs + offset] + '\n<p>' + random.choice(end_phrases) + '</p>\n' + modified[last_p_end_abs + offset:]
    
    return modified

count = 0
skipped = []

for fp in files:
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if not needs_keywords(content):
        skipped.append(os.path.basename(fp).replace('(source).html', ''))
        continue
    
    modified = insert_phrases(content)
    if modified != content:
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(modified)
        count += 1
        print(f'  ✅ {os.path.basename(fp)}')

print(f'\n完成：{count}篇植入, {len(skipped)}篇跳过（已有地域词）')
