# 存勤法税服务（广州）有限公司官网

> 业财法税管五维融合 | 甲乙双视角实战派

## 网站简介

存勤法税服务（广州）有限公司官方网站，基于Hexo静态网站生成器构建，采用Fluid主题，支持GitHub Pages自动部署。

## 技术栈

- **静态网站生成器**：Hexo
- **主题**：Fluid
- **部署平台**：GitHub Pages
- **自动部署**：GitHub Actions
- **SEO优化**：Schema结构化数据、Open Graph、Twitter Card

## 本地开发

### 环境要求

- Node.js 18及以上
- npm 8及以上

### 安装依赖

```bash
# 安装项目依赖
npm install

# 全局安装Hexo CLI（如未安装）
npm install -g hexo-cli
```

### 本地预览

```bash
# 启动本地服务器
hexo server

# 生成静态文件
hexo generate

# 清理生成文件
hexo clean
```

## 内容管理

### 目录结构

```
├── source/               # 源文件目录
│   ├── _posts/          # 博客文章
│   ├── about/           # 关于我们页面
│   ├── services/        # 十大核心服务页面
│   ├── cases/           # 客户案例页面
│   └── contact/         # 联系我们页面
├── themes/              # 主题目录
│   └── fluid/          # Fluid主题
├── .github/             # GitHub相关配置
│   └── workflows/      # GitHub Actions工作流
├── _config.yml          # Hexo主配置文件
└── package.json         # 项目依赖配置
```

### 添加新文章

在 `source/_posts/` 目录下创建新的Markdown文件，文件名格式为 `YYYY-MM-DD-文章标题.md`。

文章头部需要包含Front-matter：

```yaml
---
title: 文章标题
date: 2024-01-01 10:00:00
tags:
  - 标签1
  - 标签2
categories:
  - 分类1
description: 文章摘要，用于SEO
---
```

### 发布新文章

1. 将新文章添加到Git仓库
2. 提交并推送到GitHub
3. GitHub Actions将自动构建并部署网站

## 部署说明

### 自动部署

当代码推送到 `main` 或 `master` 分支时，GitHub Actions会自动执行以下操作：

1. 检出代码
2. 安装Node.js环境
3. 安装项目依赖
4. 使用Hexo生成静态网站
5. 部署到GitHub Pages

### 手动部署

如果需要手动部署：

```bash
# 生成静态文件
hexo generate

# 部署到GitHub Pages（需要配置deploy参数）
hexo deploy
```

## SEO配置

### 主配置文件 `_config.yml`

```yaml
# Site
title: 存勤法税服务（广州）有限公司
subtitle: 业财法税管五维融合 | 甲乙双视角实战派
description: 专注为企业提供涉税风险检查、税务危机应对、ODI备案、企业重组税务规划等专业服务
keywords: 业财法税融合, 财税顾问, 税务筹划, 金税四期应对, ODI备案, 企业重组, 跨境电商税务
author: 邓达华
language: zh-CN
timezone: Asia/Shanghai

# URL
url: https://dengdahua.github.io/cunqin_law-tax
root: /cunqin_law-tax/
```

### 文章SEO优化

每篇文章应包含：

1. **明确的标题**：包含核心关键词
2. **详细的摘要**：在Front-matter中设置description
3. **合理的标签**：反映文章主题
4. **正确的分类**：便于内容归档
5. **内部链接**：链接到相关文章

## 统计代码配置

### 百度统计

1. 登录百度统计，获取统计代码ID
2. 在 `themes/fluid/_config.yml` 中配置：

```yaml
seo:
  baidu_tongji_id: "您的百度统计ID"
```

### Google Analytics

1. 登录Google Analytics，获取跟踪ID
2. 在 `themes/fluid/_config.yml` 中配置：

```yaml
seo:
  google_analytics_id: "G-XXXXXXXXXX"
```

## 自定义域名（可选）

如果需要使用自定义域名：

1. 在域名服务商处添加CNAME记录，指向 `dengdahua.github.io`
2. 在 `source/` 目录下创建 `CNAME` 文件，内容为您的域名
3. 在GitHub仓库设置中启用自定义域名

## 故障排除

### 常见问题

1. **本地预览无法访问**
   - 检查端口是否被占用（默认4000）
   - 尝试使用 `hexo server -p 5000` 更换端口

2. **文章不显示**
   - 检查Front-matter格式是否正确
   - 运行 `hexo clean && hexo generate` 重新生成

3. **部署失败**
   - 检查GitHub Actions日志
   - 确认分支名称是否正确
   - 检查仓库的Pages设置

## 项目维护

### 定期更新

- 每月检查依赖包更新：`npm outdated`
- 更新依赖包：`npm update`
- 更新Hexo：`npm install hexo@latest`

### 内容更新

- **每月至少发布2篇原创文章**
- **每季度更新服务案例**
- **每年更新公司动态**

## 联系我们

- **电话/微信**：13556116691
- **邮箱**：contact@cunqin.cn
- **地址**：广州市

## 许可证

© 2024-2026 存勤法税服务（广州）有限公司。保留所有权利。
