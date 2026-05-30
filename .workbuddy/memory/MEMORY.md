# 存勤法税项目长期记忆

## ⚠️ URL 列表铁律（2026-05-24）
- **给用户列 URL 之前，必须先读 `source/sitemap.xml` 核对**——凭记忆列 URL 必然出错
- **文章 URL 用拼音 slug**（如 `jinshui-siqi-yingdui.html`），不是中文文件名
- **服务子页**：`services/s01-xxx.html` 至 `s11-xxx.html`（11项）
- **禁止凭记忆/推理列 URL**，sitemap 是唯一事实来源

## ⚠️ 阅读量实时计数铁律（2026-05-30，取代静态base方案）
- **全站77篇文章使用 countapi.xyz 实时计数**：`fetch('https://api.countapi.xyz/hit/cunqin-tax/' + slug)`
- **namespace**：`cunqin-tax`，**key**：文章 slug
- **兜底机制**：API 不可用时显示 `0`，不做虚假本地递增
- **验证**：`grep -r 'countapi.xyz' source/articles/ | wc -l` 应等于 77
- **严禁**手动修改阅读量
- **home-insights.json**：views 字段=0（排序参考），实际数值由线上 API 返回
- **本地 file:// 协议**：fetch 跨域可能失败，显示 0 属正常兜底

## ⚠️ 未完成任务（方案A三步）
- **Task #410**：77篇文章加 countapi.xyz hit 计数（in_progress，实际未完成）
- **Task #411**：首页JS用 countapi.xyz get 替代静态 views（pending）
- **Task #412**：法税洞察页JS用 countapi.xyz get 替代 localStorage（pending）
- **Task #368**：P0-2 添加社会证明板块（关于我们页 Logo墙+量化数据+行业认可）（pending）

## ⚠️ JS 搜索代码完整性检查（2026-05-24）
- **每次修改文章JS后必须检查**：`highlightInElement` 完整、`jumpToMatch` 存在、`doArticleSearch` forEach 闭合
- **检查**：`grep -c 'jumpToMatch' source/articles/*.html` 应为 4（全站 77×4=308）
- **检查**：`grep -c 'while (node = walker.nextNode())' source/articles/*.html` 应为 1（全站 77）

## ⚠️ 文章格式铁律（2026-05-27）
- **参考模板**：`source/articles/企业税务风险管控(source).html`
- **延伸阅读 H3 必须闭合**：`<h3 id="延伸阅读" class="related-heading"><span>延伸阅读</span></h3>`
- **延伸阅读卡片数 ≥ 3**
- **related-cta 必须含大湾区提示**：`对于广州及粤港澳大湾区企业而言，提前做好税务合规布局，是在复杂监管环境下稳健经营的关键。`
- **标准 Skill**：`.workbuddy/skills/cunqin-article-standard/`，验证：`validate_article.py --all`
- **每次操作后必须运行验证**，确保 jumpToMatch=4、createTreeWalker=1、Article≥1、FAQPage≥1

## ⚠️ 触发词：-成交-（2026-05-27）
- 立即恢复 P0 成交转化：P0-1 sameAs外链（Task #367已完成）+ P0-2 社会证明（Task #368待完成）

## ⚠️ GEO 合规要求（2026-05-27）
- **每次修改后必须跑 `python tools/geo_audit.py`，确认 0 ERROR 0 WARNING**
- **og:description 120-160 字符**：客观、信息丰富、含关键词，不带营销腔
- **meta description 与 og:description 保持一致**
- **twitter:description ≤100 字符**
- **baidu-site-verification token**：`codeva-9SPpSVW5X6`（非 `codeva-MMFsum3pdD`）
- **排除模板文件**：`_article_list_generated.html`、`_article_list_new.html`
- **keywords 格式**：`存勤法税 + 邓达华 + 业管财税法 + 财税顾问 + 税务筹划`（品牌词5件套）+ 主题词3-5个 + 地域词1-2个

## ⚠️ 文章库存管理（2026-05-30）
- **全站共 77 篇**，法税洞察页显示 77 篇
- **home-insights.json**：77篇元数据，views 全为 0，按 views 降序排列
- **search-index.json**：114 条（含非文章页）
- **新增文章后必须同步更新**：法税洞察页 + home-insights.json + search-index.json + sitemap.xml + atom.xml
- **atom.xml**：目前仅 8 条，待更新至 77 篇

## ⚠️ 批量编辑铁律（2026-05-22）
- **严禁用 PowerShell 批量编辑含中文的 UTF-8 文件**——会导致中文乱码
- 需要批量编辑时，用 Python 脚本（`encoding="utf-8"`）

## ⚠️ CSS 布局修改铁律（2026-05-23）
- **改一个值，检查连锁影响**：修改 gap/margin/padding/font-size 时同时检查容器宽度、相邻元素、响应式
- **一改到底**：不要等用户提醒才改容器宽度，一次性做完关联修改
- **视觉效果先于执行**：每次布局改动前先评估好看吗/比例协调吗/留白舒服吗

## ⚠️ JS fetch/跳转路径铁律（2026-05-26）
- **JS 中 fetch() 和 window.location.href 必须用站内绝对路径**：`/xxx.json` 或 `/about/`
- **严禁在 JS 中用 `./` 相对路径**（在子目录页面会解析错误）
- **HTML `src`/`href` 属性中的 `../` 是正确且必要的**，不要混淆

## 项目概览
- **公司**：存勤法税服务（广州）有限公司
- **创始人**：邓达华，18年财税法实战经验（14年甲方+4年乙方）
- **官网**：https://cunqin.tax
- **GitHub**：Deng-dahua/cunqin_law-tax
- **仓库路径**：`C:/Users/26726/WorkBuddy/2026-05-20-21-20-24/`
- **技术栈**：Hexo + hexo-theme-fluid，GitHub Actions 部署，SSH 推送

## 关键配置
- `_config.yml`：Hexo主配置；`_config.fluid.yml`：主题配置（根目录）
- `.github/workflows/deploy.yml`：部署工作流（首页覆盖+CSS重命名）
- 图片路径 `source/images/`：`nav-logo.png`、`footer-logo.png`、`company-logo.png`、`founder-new.png`、`wechat-qrcode.png`
- 文章JSON生成工具：`tools/generate_articles.py`
- 索引更新工具：`tools/update_indexes.py`
- 首页热门文章工具：`tools/build_home_insights.py`
- **skip_render 规则**：需要 Hexo 处理 permalink 的 HTML 文件，必须从 `_config.yml` skip_render 中移除

## SEO/GEO 配置
- **Base URL**: `https://cunqin.tax`
- **全站 24 页均已配置**: Schema.org JSON-LD, Open Graph, Canonical URL, Twitter Card, Meta Keywords, hreflang
- **Sitemap**: `source/sitemap.xml`，**robots.txt** 已引用
- **Schema 类型**：Homepage(WebSite+Organization), Articles(Article+BreadcrumbList+FAQPage), Services(Service), About(AboutPage+Person), Contact(ContactPage), Archives/Cases(CollectionPage)

## 搜索引擎收录状态（2026-05-24）
| 平台 | 验证 | Sitemap | URL推送 | 备注 |
|------|------|---------|---------|------|
| Bing | ✅ Meta标签 | ✅ 27 URLs | ✅ 24条已推送 | 国内可访问 |
| 百度 | ✅ Meta标签 `codeva-9SPpSVW5X6` | ❌ 无ICP备案 | ⚠️ 日限10条，剩14条待推 | API token: SWGy4vjzNfOGuuLt |
| GSC | ❌ | - | - | 需翻墙 |

## 导航链接铁律（2026-05-24）
- 首页（`source/` 根）：相对路径 `about/`、`services/`
- 深度 1 页面：`../about/`、`../`（首页）
- 深度 2 页面（articles/）：`../../about/`、`../../`（首页）
- **自动部署铁律**：修改完代码后自动 `git add source/ && git commit && git push`

## 文章写作规范
- **深度优先**：每篇不下于 2000 字，涵盖政策背景/实操要点/风险提示/案例分析
- 结构：至少 3-4 个 H2 章节，每章节设 H3 子节
- 面向企业主/财务总监，提供可操作指导

## 待办事项
- [ ] 百度：每日手动提交 10 条 URL（剩余 14 条）
- [ ] GSC：翻墙后添加站点 + 提交 sitemap
- [ ] ICP备案/国内CDN 方案决策（方案A/B/C）
- [ ] 更新 atom.xml（目前仅 8 条，应为 77 条）
- [ ] 完成方案A三步（Task #410/#411/#412）
- [ ] P0-2 社会证明板块（Task #368）
