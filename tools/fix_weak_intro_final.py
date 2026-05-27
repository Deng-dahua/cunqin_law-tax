"""修复3篇弱前言文章：在首段后插入一句概述"""
import re, os

fixes = {
    'source/articles/专精特新企业税收优惠政策深度解读(source).html': {
        'after_paragraph': 1,
        'insert': '<p>本文从政策沿革、核心优惠、适用条件、留存备查、合规风险五个维度，为专精特新企业提供一套可落地的税收优惠实操指南。</p>'
    },
    'source/articles/企业减资撤资全套税务处理指南(source).html': {
        'after_paragraph': 1,
        'insert': '<p>本文围绕新公司法认缴期限收紧背景，系统梳理企业减资、撤资、清算退出三类场景的全流程税务处理，帮助企业避免补税滞纳金罚款的连锁风险。</p>'
    },
    'source/articles/家族财富传承税务考量与规划(source).html': {
        'after_paragraph': 1,
        'insert': '<p>本文从股权架构、不动产持有、家族信托、跨境资产配置四个维度，为中国高净值家庭提供一套合法合规可落地的家族财富传承税务规划框架。</p>'
    },
}

count = 0
for fp, cfg in fixes.items():
    try:
        with open(fp, 'r', encoding='utf-8') as f:
            c = f.read()
        m = re.search(r'(<article class="article-body">.*?</article>)', c, re.DOTALL)
        if not m:
            print(f'  SKIP {os.path.basename(fp)} (无article-body)')
            continue
        body = m.group(1)
        ps = list(re.finditer(r'<p[^>]*>.*?</p>', body, re.DOTALL))
        if len(ps) < cfg['after_paragraph']:
            print(f'  SKIP {os.path.basename(fp)} (段落不足)')
            continue
        # 第N段的绝对结束位置
        target_p = ps[cfg['after_paragraph'] - 1]
        abs_pos = m.start(1) + target_p.end()
        new_c = c[:abs_pos] + '\n' + cfg['insert'] + '\n' + c[abs_pos:]
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(new_c)
        count += 1
        print(f'  OK {os.path.basename(fp).replace("(source).html","")}')
    except Exception as e:
        print(f'  ERR {fp}: {e}')

print(f'\n完成：{count}篇前言已增强')
