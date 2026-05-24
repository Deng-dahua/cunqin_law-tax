#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
重新生成 search-index.json，text 字段只保留文章正文摘要（前 200 字），
去除导航栏/footer/搜索栏等噪音文字。
"""

import json
import re
import os

SOURCE_DIR = "C:/Users/26726/WorkBuddy/2026-05-20-21-20-24/source"
OUTPUT_PATH = os.path.join(SOURCE_DIR, "search-index.json")

def find_article_html_by_url(url):
    """根据 URL 找到对应的 source HTML 文件"""
    articles_dir = os.path.join(SOURCE_DIR, "articles")
    # url 形如 /articles/jinshui-siqi-yingdui.html
    # 需要从文件 frontmatter 里的 permalink 匹配
    for fname in os.listdir(articles_dir):
        if not fname.endswith("(source).html"):
            continue
        fpath = os.path.join(articles_dir, fname)
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()
        # 检查 frontmatter 中的 permalink
        pm_match = re.search(r'^permalink:\s*(.+)$', content, re.MULTILINE)
        if pm_match:
            pm_url = pm_match.group(1).strip()
            # 去掉引号
            pm_url = pm_url.strip("'\"")
            if pm_url == url:
                return fpath
    return None

def extract_article_summary(html_path):
    """从文章 HTML 中提取正文摘要（前 200 个中文字符）"""
    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 策略：找 article-body 的起始位置，然后提取里面的纯文本
    body_match = re.search(r'class="article-body"', content)
    if not body_match:
        return ""

    # 从 article-body div 开始，找到对应的结束 tag
    start_pos = body_match.start()
    # 找到 article-body 的 > 结束位置
    gt_pos = content.find(">", start_pos)
    if gt_pos == -1:
        return ""
    text_start = gt_pos + 1

    # 取一段 HTML（足够 200 字）
    html_fragment = content[text_start: text_start + 5000]

    # 去掉所有 HTML 标签
    text = re.sub(r'<[^>]+>', ' ', html_fragment)
    # 去掉 HTML 实体
    text = re.sub(r'&[a-z]+;', '', text)
    text = re.sub(r'&[a-z]+', '', text)  # 不完整的实体
    # 去掉多余空白和空行
    text = re.sub(r'\s+', ' ', text).strip()
    # 去掉开头的"前言"（如果有）
    text = re.sub(r'^[\s　]*前言[\s　]*', '', text)
    # 取前 200 个字
    return text[:200]

def clean_text_field(text):
    """清理 text 字段，去除明显的噪音模式"""
    if not text:
        return ""
    noise_patterns = [
        r'了解服务\s*联系我们',
        r'法税洞察专业视角.*?新范式',
        r'共\s*\d+\s*篇文章',
        r'排序：.*?最热',
        r'文章分类：.*?行业洞察',
        r'首页\s*>.*?法税洞察\s*>',
        r'目录\s*首页.*?新范式',
        r'真实服务经验.*?专业价值',
        r'留下您的需求.*?严格保密',
        r'135\d{8}.*?广州市天河区',
        r'扫码添加微信咨询.*?紧急咨询',
        r'十大核心服务.*?财税内训课程定制',
        r'「业管财税法」五维融合.*?实战派',
        r'18\s*年.*?行业经验.*?企业信赖',
        r'客户案例.*?典型案例',
    ]
    cleaned = text
    for pattern in noise_patterns:
        cleaned = re.sub(pattern, ' ', cleaned, flags=re.DOTALL)
    # 去掉多余空白
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned

# 读取现有 search-index.json
with open(OUTPUT_PATH, "r", encoding="utf-8") as f:
    index = json.load(f)

updated = 0
for entry in index:
    url = entry.get("url", "")
    # 只处理文章页
    if not url.startswith("/articles/"):
        # 非文章页做噪音清理
        cleaned = clean_text_field(entry.get("text", ""))
        if cleaned != entry.get("text", ""):
            entry["text"] = cleaned
            updated += 1
            print(f"  🔄 非文章页清理: {url}")
        continue

    # 找对应的 source 文件
    html_file = find_article_html_by_url(url)
    if not html_file:
        print(f"  ⚠ 找不到对应文件: {url}")
        # fallback: 清理现有 text
        cleaned = clean_text_field(entry.get("text", ""))
        entry["text"] = cleaned
        updated += 1
        continue

    # 提取正文摘要
    summary = extract_article_summary(html_file)
    if summary and len(summary) > 20:
        entry["text"] = summary
        updated += 1
        print(f"  ✅ {url} -> {len(summary)} 字摘要")
    else:
        print(f"  ⚠ 摘要提取失败: {url}")
        cleaned = clean_text_field(entry.get("text", ""))
        entry["text"] = cleaned
        updated += 1

# 写回
with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(index, f, ensure_ascii=False, indent=2)

print(f"\n完成！共更新 {updated} 条")
