---
name: geo-audit
description: "GEO and SEO full-site audit tool for cunqin.tax website. Triggers when user asks to check GEO optimization, SEO audit, or full-site check. Must run before any GEO work."
---

# GEO 全站审计 Skill

## 概述

此 skill 提供 `tools/geo_audit.py` 脚本，对 cunqin.tax 全站（25 个 HTML 文件）执行 19 项 GEO/SEO 检查。

**核心原则：凡涉及 GEO 优化的事项，必须先跑审计，全部通过才验收。**

## 何时使用此 Skill

- 用户要求"全站 GEO 检查"、"SEO 审计"
- 用户完成一批 GEO 修改后，要求验证
- 用户提到"检查全站有没有问题"
- 任何涉及 meta 标签、Schema、OG/Twitter 标签的修改之后

## 使用方法

### 运行审计

```bash
cd /c/Users/26726/WorkBuddy/2026-05-20-21-20-24
python tools/geo_audit.py
```

### 解读结果

```
扫描 25 个 HTML 文件...
============================================================
检查项: 19 | 文件: 25
ERROR:   0
WARNING: 0
============================================================
✅ 全站 GEO 审计通过 — 0 错误 0 警告
```

- **0 ERROR + 0 WARNING** = 通过，可以验收
- **有 ERROR** = 必须修复，不可验收
- **有 WARNING** = 建议修复（og:description 过短等）

### 19 项检查内容

| # | 类别 | 检查项 |
|---|------|---------|
| 1-3 | HTML 结构 | 标签平衡(div/section/script/head/body/html)、DOCTYPE、lang 属性 |
| 4-10 | Meta 完整性 | baidu-verify、robots、canonical、hreflang、keywords、description、PWA meta |
| 11-12 | 社交标签 | Open Graph(6项)、Twitter Card(3项) |
| 13 | 结构化数据 | Schema.org JSON-LD |
| 14-16 | 代码质量 | 嵌套引号、JS 垃圾代码、未闭合 script 标签 |
| 17-19 | 内容质量 | og:description 长度(120-160)、description 非空、og:url 域名正确 |

## 修改后验证流程

1. 完成一批 GEO 修改
2. **立即运行** `python tools/geo_audit.py`
3. 确认 0 ERROR 0 WARNING 才推送
4. 若有 ERROR，先修复再推送

## 常见错误及修复

| 错误 | 原因 | 修复方法 |
|------|------|---------|
| 标签不平衡 | 未闭合的 div 或 script 标签 | 用 Python 脚本精确匹配并补全 |
| 缺少 baidu-verify | 仅首页有，其余 24 页缺失 | 批量在 `msvalidate.01` 后插入 |
| og:description 过短 | 描述只有 50-100 字符 | 扩展到 120-160 字符，包含关键词 |
| 嵌套引号 | `content=".."引号.."` | 将内部引号改为 `&quot;` |
| JS 垃圾代码 | 旧模板残留 `}); })();` | 用 Python 脚本精确删除 |

## 参考资料

- 百度搜索资源平台：https://ziyuan.baidu.com/
- Open Graph 协议：https://ogp.me/
- Schema.org：https://schema.org/
- Google Search Central：https://developers.google.com/search/docs
