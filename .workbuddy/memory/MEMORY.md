# 存勤法税项目长期记忆

## 项目概览
- **公司**：存勤法税服务（广州）有限公司
- **创始人**：邓达华，18年财税法实战经验（14年甲方+4年乙方）
- **官网**：https://deng-dahua.github.io/cunqin_law-tax/
- **GitHub**：Deng-dahua/cunqin_law-tax
- **仓库路径**：`C:/Users/26726/WorkBuddy/2026-05-20-21-20-24/`

## 技术栈
- **静态网站生成器**：Hexo
- **主题**：hexo-theme-fluid（npm安装）
- **部署**：GitHub Actions（自动部署到GitHub Pages）
- **推送方式**：SSH（国内网络更稳定）

## SEO/GEO 配置
- **Base URL**: `https://deng-dahua.github.io/cunqin_law-tax`
- **全站 24 页均已配置**: Schema.org JSON-LD, Open Graph, Canonical URL, Twitter Card, Meta Keywords, hreflang, Apple Touch Icon, PWA Meta, time datetime
- **Sitemap**: `source/sitemap.xml` (24 URLs), `source/robots.txt` 已引用
- **Atom Feed**: `source/atom.xml` (8 entries)
- **Schema 类型分布**: Homepage(WebSite+Organization), Articles(Article+BreadcrumbList+FAQPage), Services(Service), About(AboutPage+Person), Contact(ContactPage), Archives/Cases(CollectionPage)

## 文件管理铁律（2026-05-22 确立）
- **相同文件只保留最新版**：功能相同的文件（如多个版本的二维码 `wechat-qrcode.png` / `wechat-qrcode-white.png` / `wechat-qrcode-final.png`），只保留最终使用的那个，旧版、中间版全部删除
- **唯一性优先**：`source/images/` 中每个用途只存 1 个文件，不得有多版本共存
- **冗余即删**：备份文件（如 `_posts-backup/`）、空目录、未引用的资源文件，一律清除
- **每次变更后自查**：确认没有残留旧版本文件

## 关键配置
- `_config.yml`：Hexo主配置（站点信息、URL、插件）
- `_config.fluid.yml`：Fluid主题配置（根目录放置，Hexo 5+标准）
- `.github/workflows/deploy.yml`：部署工作流（已精简，仅保留首页覆盖+CSS重命名）
- 图片路径：`source/images/` 现有 1 个：`nav-logo.png`（导航栏 LOGO，197KB）
- 微信二维码图片全部删除（2026-05-22），CTA 区块不再展示二维码
- 页脚 LOGO（footer-logo.png）已删除，用户将重新提供新 LOGO
- 导航栏统一使用 `nav-logo.png`

## 文件命名规则（2026-05-22 确立）
- **source/ 源文件**：中文描述名 + `(source)` 后缀，如 `首页(source).html`、`高新技术企业税务规划(source).html`
- **public/ 产物**：中文描述名，无后缀，如 `首页.html`
- **URL 保持不变**：所有 source HTML 通过 `permalink` + `layout: false` frontmatter 指定目标 URL
- **目录结构对齐**：about/archives/cases/contact/services 子目录在 source 和 public 中一一对应
- **skip_render 规则**：`source/` 中任何需要 Hexo 处理 permalink 的 HTML 文件，必须从 `_config.yml` 的 `skip_render` 中移除（含通配符模式）

## 部署注意事项
1. 必须设置GitHub Pages Source为 **GitHub Actions**（不是Deploy from a branch）
2. 使用 `npm install` 而不是 `npm ci`（避免lock文件版本问题）
3. `db.json` 已加入 `.gitignore`，不应提交
4. `_config.fluid.yml` 中的图片引用如果文件不存在必须注释掉，否则破图
5. `source/images/` 目录下不要放 `README.md` 等非图片文件（Hexo会尝试处理）
6. **Hexo permalink 陷阱**：`:title` token 使用完整文件名（含日期前缀）作为 slug，不是仅文件名的标题部分。若文件名含 `YYYY-MM-DD-slug.md` 格式，`:title` 会输出 `YYYY-MM-DD-slug`。修正方法：在每篇 post frontmatter 中显式指定 `permalink`（优先级最高）

## 待办事项
- [ ] 替换所有不存在的banner图片（取消注释对应配置行并放入实际图片）
- [ ] 配置百度统计ID
- [ ] 配置Google Analytics ID
- [ ] 修改备案号（当前为占位符）
- [ ] 提交sitemap到百度搜索资源平台和Google Search Console
- [ ] 持续发布GEO文章（已规划15篇）
