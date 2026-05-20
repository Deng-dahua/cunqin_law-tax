# 存勤法税官网部署指南

本指南将帮助您将存勤法税官网部署到GitHub Pages。

## 第一步：准备GitHub仓库

### 1. 创建GitHub仓库

1. 登录GitHub，点击右上角 `+` → `New repository`
2. 仓库名称填写：`cunqin_law-tax`
3. 选择 `Public`（私有仓库无法使用免费GitHub Pages）
4. 勾选 `Add a README file`
5. 点击 `Create repository`

### 2. 连接本地项目到GitHub

在本地项目目录运行：

```bash
# 进入项目目录
cd "C:/Users/26726/WorkBuddy/2026-05-20-21-20-24/"

# 初始化Git仓库
git init

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit: 存勤法税官网"

# 添加远程仓库（替换为您的GitHub用户名）
git remote add origin https://github.com/你的用户名/cunqin_law-tax.git

# 推送代码
git push -u origin main
```

## 第二步：配置GitHub Pages

### 1. 开启GitHub Pages

1. 进入您的GitHub仓库
2. 点击 `Settings` → `Pages`
3. 在 `Build and deployment` 部分：
   - Source 选择 `GitHub Actions`
4. 点击 `Save`

### 2. 配置仓库密钥（可选）

如果您需要使用Google Analytics等外部服务：

1. 在仓库 `Settings` → `Secrets and variables` → `Actions`
2. 点击 `New repository secret`
3. 添加以下密钥（如需要）：
   - `GITHUB_TOKEN`：GitHub自动提供，无需手动添加
   - `GEO_API_KEY`：如果有第三方API需要

## 第三步：推送代码触发部署

### 1. 推送代码

```bash
# 添加所有修改
git add .

# 提交修改
git commit -m "feat: 添加GEO文章和SEO优化"

# 推送到GitHub
git push origin main
```

### 2. 查看部署进度

1. 进入GitHub仓库
2. 点击 `Actions` 标签页
3. 您会看到部署工作流正在运行
4. 等待2-3分钟，部署完成后会显示绿色对勾

### 3. 访问网站

部署成功后，访问以下网址：

```
https://你的用户名.github.io/cunqin_law-tax/
```

## 第四步：添加图片文件

网站需要以下图片文件才能正常显示：

### 必需图片

| 文件名 | 建议尺寸 | 用途 |
|--------|------------|------|
| `logo.png` | 200×60px | 网站Logo |
| `favicon.ico` | 32×32px | 浏览器图标 |
| `og-image.jpg` | 1200×630px | 社交媒体分享图 |
| `founder.jpg` | 400×500px | 创始人照片 |
| `wechat-qrcode.jpg` | 200×200px | 微信二维码 |

### 添加图片步骤

1. 准备以上图片文件
2. 将图片复制到 `source/images/` 目录
3. 提交并推送代码：

```bash
git add source/images/
git commit -m "add: 添加网站图片"
git push origin main
```

## 第五步：配置统计代码（可选）

### 百度统计

1. 登录 [百度统计](https://tongji.baidu.com/)
2. 添加网站，获取统计代码ID
3. 编辑 `themes/fluid/_config.yml`，找到以下内容：

```yaml
seo:
  baidu_tongji_id: "您的百度统计ID"
```

4. 替换为您的实际ID
5. 提交并推送代码

### Google Analytics

1. 登录 [Google Analytics](https://analytics.google.com/)
2. 创建媒体资源，获取跟踪ID（格式：G-XXXXXXXXXX）
3. 编辑 `themes/fluid/_config.yml`，找到以下内容：

```yaml
seo:
  google_analytics_id: "G-XXXXXXXXXX"
```

4. 替换为您的实际ID
5. 提交并推送代码

## 第六步：自定义域名（可选）

如果您有自己的域名，可以配置自定义域名：

### 1. 添加CNAME文件

在 `source/` 目录下创建 `CNAME` 文件，内容为您的域名：

```
www.cunqin.com
```

### 2. 配置DNS解析

在您的域名服务商处添加CNAME记录：

| 记录类型 | 主机记录 | 记录值 |
|----------|----------|----------|
| CNAME | www | 你的用户名.github.io |

### 3. 开启HTTPS

1. 进入GitHub仓库 `Settings` → `Pages`
2. 勾选 `Enforce HTTPS`

## 日常更新指南

### 添加新文章

1. 在 `source/_posts/` 目录下创建新的Markdown文件
2. 文件名格式：`YYYY-MM-DD-文章标题.md`
3. 添加文章头部信息：

```yaml
---
title: 文章标题
date: 2024-06-20 10:00:00
tags:
  - 标签1
  - 标签2
categories:
  - 分类
description: 文章摘要，用于SEO
---
```

4. 编写文章内容（支持Markdown格式）
5. 提交并推送代码

### 修改网站信息

1. 编辑 `_config.yml` 修改网站标题、描述等
2. 编辑 `themes/fluid/_config.yml` 修改主题相关设置
3. 提交并推送代码

### 更新文章

1. 直接编辑 `source/_posts/` 目录下的文章文件
2. 提交并推送代码

## 常见问题

### Q1：网站访问显示404

**可能原因**：
- 仓库名称与 `baseurl` 不匹配
- GitHub Pages未正确开启

**解决方案**：
1. 检查 `_config.yml` 中的 `url` 和 `root` 配置
2. 确认GitHub Pages已设置为 `GitHub Actions` 模式

### Q2：文章不显示

**可能原因**：
- 文章文件名或路径错误
- Front-matter格式错误

**解决方案**：
1. 检查文件名格式是否正确
2. 检查Front-matter的YAML格式是否正确
3. 运行 `hexo clean && hexo generate` 本地测试

### Q3：图片不显示

**可能原因**：
- 图片文件路径错误
- 图片文件名大小写不匹配

**解决方案**：
1. 确认图片已放置在 `source/images/` 目录
2. 检查HTML中的图片路径是否正确
3. 注意GitHub文件名大小写敏感

### Q4：部署失败

**可能原因**：
- 依赖包安装失败
- Hexo版本不兼容

**解决方案**：
1. 查看GitHub Actions日志，定位错误
2. 尝试更新依赖包：`npm update`
3. 确保Node.js版本与GitHub Actions中配置的一致

## 技术支持

如果在部署过程中遇到问题，请联系存勤法税团队：

- **电话/微信**：13556116691
- **邮箱**：contact@cunqin.cn
- **服务时间**：周一至周五 9:00-18:00

---

**恭喜！您已成功部署存勤法税官网。现在可以开始添加内容，建立GEO内容矩阵，提升企业在搜索引擎中的影响力。**
