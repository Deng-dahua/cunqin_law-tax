# 存勤法税官网 - 部署说明

## 📁 文件夹结构

```
cunqin_law-tax/
├── index.html          # 首页
├── about.html          # 关于我们
├── services.html       # 核心服务（十大服务详情）
├── cases.html          # 客户案例
├── blog.html           # GEO文章列表
├── contact.html        # 联系我们
├── robots.txt          # 爬虫规则
├── sitemap.xml         # Google/通用站点地图
├── baidusitemap.xml    # 百度专用站点地图
├── css/
│   └── style.css       # 样式文件
├── js/
│   └── main.js         # JavaScript文件
├── images/
│   ├── README.md        # 图片说明
│   ├── logo.png         # Logo（请替换）
│   ├── wechat-qrcode.jpg # 微信二维码（请替换）
│   └── founder.jpg      # 创始人照片（请替换）
└── blog/
    ├── README.md        # 文章文件夹说明
    ├── yewucaifashui-ronghe.html    # 文章示例1
    ├── jinshui-siqi-yingdui.html    # 文章示例2
    └── odi-beian-quanliucheng.html  # 文章示例3
```

## 🚀 部署步骤

### 方式一：直接上传到GitHub Pages仓库

1. **上传所有文件**
   - 将整个文件夹内容上传到您的GitHub Pages仓库根目录

2. **提交更改**
   ```bash
   git add .
   git commit -m "部署存勤法税官网 v1.0"
   git push
   ```

3. **等待部署**
   - GitHub Pages会自动构建，约1-2分钟后生效

### 方式二：上传到现有仓库

1. **复制文件**
   - 将所有HTML、CSS、JS文件复制到您的仓库

2. **确保images文件夹存在**
   - 包含必要的图片文件

3. **提交并推送**

## 📝 必须完成的配置

### 1. 替换图片文件

在 `images/` 文件夹中替换以下文件：

| 文件名 | 说明 | 建议尺寸 |
|--------|------|----------|
| `logo.png` | 公司Logo | 200x200px，透明背景 |
| `wechat-qrcode.jpg` | 微信二维码 | 300x300px |
| `founder.jpg` | 创始人照片 | 400x400px |

### 2. 配置百度统计

编辑 `index.html`，替换百度统计ID：

```html
<!-- 找到这行，替换为您的统计ID -->
hm.src = "https://hm.baidu.com/hm.js?您的百度统计ID";
```

### 3. 配置Google Analytics

编辑 `index.html`，替换GA4测量ID：

```html
<!-- 找到这行，替换为您的测量ID -->
gtag('config', 'G-XXXXXXXXXX');
```

### 4. 配置备案号

编辑 `index.html`，找到并替换备案号：

```html
<a href="https://beian.miit.gov.cn/">粤ICP备XXXXXXXX号</a>
```

## 🔍 提交站点地图

### 提交到Google Search Console
1. 访问 https://search.google.com/search-console
2. 添加网站属性
3. 验证所有权
4. 提交 `sitemap.xml`

### 提交到百度搜索资源平台
1. 访问 https://ziyuan.baidu.com
2. 添加网站
3. 验证所有权
4. 提交 `baidusitemap.xml`

## 📄 SEO检查清单

- [ ] 替换Logo图片
- [ ] 替换微信二维码
- [ ] 替换创始人照片
- [ ] 配置百度统计ID
- [ ] 配置Google Analytics ID
- [ ] 修改备案号
- [ ] 提交sitemap到Google
- [ ] 提交sitemap到百度
- [ ] 验证网站可访问性

## 📝 添加新文章

1. 在 `blog/` 文件夹创建新HTML文件
2. 参考现有文章格式
3. 在 `blog.html` 中添加链接
4. 在 `sitemap.xml` 和 `baidusitemap.xml` 中添加URL

## 🆘 常见问题

### Q: 网站显示异常？
A: 检查控制台错误，确保所有CSS/JS文件路径正确。

### Q: 图片无法显示？
A: 确保images文件夹已上传，路径正确。

### Q: 百度统计不生效？
A: 确保ID正确，且代码在</body>标签前。

## 📞 联系方式

如有问题，请联系：
- 电话：13556116691
- 微信：13556116691

---

*最后更新：2026-05-20*
