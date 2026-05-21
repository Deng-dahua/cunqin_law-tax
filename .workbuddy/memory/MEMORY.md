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

## 关键配置
- `_config.yml`：Hexo主配置（站点信息、URL、插件）
- `_config.fluid.yml`：Fluid主题配置（根目录放置，Hexo 5+标准）
- `.github/workflows/deploy.yml`：部署工作流
- 图片路径：`source/images/`（logo.png, founder.jpg, wechat-qrcode.png（透明背景））

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
