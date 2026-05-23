# 存勤法税项目长期记忆

## ⚠️ 批量编辑铁律（2026-05-22）
- **严禁用 PowerShell 批量编辑含中文的 UTF-8 文件**——会导致中文乱码
- 需要批量编辑时，用 Python 脚本（`encoding="utf-8"`），绝不用 PowerShell

## ⚠️ CSS 布局修改铁律（2026-05-23）
- **改一个值，检查连锁影响**：修改 gap/margin/padding/font-size 时，必须同时检查容器宽度是否兜得住、相邻元素是否错位、响应式是否崩
- **心算校验**：改动前先估算 `容器宽度 < 内容宽度 + 间距总和` 是否成立，不成立就同时调整容器
- **一改到底**：不要等用户提醒"放不下了"才改容器宽度，一次性做完关联修改
- **视觉效果先于执行**：每次布局修改前先问自己——改完好看吗？比例协调吗？留白舒服吗？主动建议优化，不只是机械执行数值变更

## ⚠️ JS fetch/跳转路径铁律（2026-05-23 确立）
- **JS 中 fetch() 和 window.location.href 必须用站内绝对路径**：`/cunqin_law-tax/xxx.json` 或 `/cunqin_law-tax/about/`
- **严禁在 JS 中用 `./` 相对路径**：`new URL('./x.json', location.href)` 和 `window.location.href = './x/'` 在子目录页面会解析到错误路径
- **HTML `src`/`href` 属性中的 `../` 是正确且必要的**（浏览器原生解析），不要混淆

## ⚠️ 固定宽度拼图法（2026-05-23 确立）
水平排列多项内容时的标准方法，**严禁用 flex gap / justify-content 凭感觉调间距**：
1. **选锚点**：以中间项为基准，左右对称放置
2. **定容器固定宽度**：每个信息区设统一的 `width`（如 10rem），不用弹性值
3. **内部三要素等式**：`padding-left + 内容宽度 + 剩余空白 = 容器宽度`，三个数加起来正好填满
4. **gap = 0 紧挨排列**：项与项之间 gap 设为 0，间距全靠各容器固定宽度自然产生
5. **先裸后穿**：先摆纯图标定位置确认间距，再逐层加文字内容

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
- 图片路径：`source/images/` 现有 4 个：
  - `nav-logo.png`（导航栏 LOGO）
  - `footer-logo.png`（页脚 LOGO）
  - `company-logo.png`（公司 LOGO）
  - `founder-new.png`（创始人照片，2026-05-22 添加）
- 微信二维码图片：`source/images/wechat-qrcode.png`（透明PNG，125×125px），用于首页和联系我们页
- 导航栏统一使用 `nav-logo.png`，页脚统一使用 `footer-logo.png`

## ⚠️ 导航链接铁律（2026-05-22）
- **严禁在非首页使用绝对路径**：GitHub Pages 托管在 `deng-dahua.github.io/cunqin_law-tax/` 子目录下
- 首页（`source/` 根）：使用相对路径如 `about/`、`services/`、`contact/`
- 深度 1 页面（`source/about/`、`source/services/` 等）：使用 `../about/`、`../services/`、`../`（首页）
- 深度 2 页面（`source/articles/`）：使用 `../../about/`、`../../services/`、`../../`（首页）
- 绝对路径 `/about/` 会被解析为 `deng-dahua.github.io/about/` → 404

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
6. **自动部署铁律**：修改完代码后自动 `git add source/ && git commit && git push`，不询问用户
7. **Hexo permalink 陷阱**：`:title` token 使用完整文件名（含日期前缀）作为 slug，不是仅文件名的标题部分。若文件名含 `YYYY-MM-DD-slug.md` 格式，`:title` 会输出 `YYYY-MM-DD-slug`。修正方法：在每篇 post frontmatter 中显式指定 `permalink`（优先级最高）

## 文章写作规范（2026-05-22 确立）
- **深度优先**：每篇文章必须有实质性的专业深度，不下于2000字
- 避免浅尝辄止的介绍性内容，要涵盖政策背景、实操要点、风险提示、案例分析
- 结构要清晰：至少包含 3-4 个 H2 章节，每个章节下设 H3 子节
- 面向企业主/财务总监的实际需求，提供可操作的指导

## 服务详情页结构（2026-05-23 确立，以人为本8板块）
每个核心服务详情页采用"人心逻辑"8板块结构：
1. **核心痛点** — 以"你"视角共情，每页独有
2. **服务理念** — 核心理念（共享板块，10页一致）
3. **服务内容** — 服务流程与内容清单，每页独有
4. **专业团队** — 团队介绍（共享板块，10页一致）
5. **交付成果** — 交付物描述，每页独有
6. **服务保障** — 信任建设（共享板块，10页一致）
7. **适用场景** — 自我诊断，每页独有
8. **立即咨询** — 定制CTA（板块⑧无独立h2标题，直接为CTA区块）

- 共享板块（2/4/6）跨页面完全一致，修改时需同步更新
- 每页独有板块（1/3/5/7/8）各有定制的痛点、流程、交付物、自检场景和CTA文案

## 全站搜索功能（2026-05-23）
- 搜索弹窗支持"全网站"/"本页面"双范围切换
- **search-index.json**：位于 `source/`，含全部24页的标题、URL、文本摘要，由 fetch 加载
- **全网站模式**：匹配标题+正文，按相关性排序，点击结果跳转至目标页面
- **本页面模式**：按原有逻辑搜索当前页 section 元素
- **URL格式**：统一使用 `./` 开头的站点相对路径（与 permalink frontmatter 对齐）
- 涉及24个HTML文件 + 1个JSON索引文件

## 待办事项
- [ ] 替换所有不存在的banner图片（取消注释对应配置行并放入实际图片）
- [ ] 配置百度统计ID
- [ ] 配置Google Analytics ID
- [ ] 修改备案号（当前为占位符）
- [ ] 提交sitemap到百度搜索资源平台和Google Search Console
- [ ] 持续发布GEO文章（已规划15篇）
