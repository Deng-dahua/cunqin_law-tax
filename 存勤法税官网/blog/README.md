# blog 文件夹

此文件夹存放GEO文章内容。

## 文章格式

每篇文章都是一个完整的HTML页面，包含：
- SEO元标签（meta title、description、keywords）
- Schema结构化数据（Article Schema + FAQ Schema）
- 文章正文
- 作者署名信息

## 文章命名规范

使用英文或拼音命名，如：
- `yewucaifashui-ronghe.html` - 业财法税融合
- `jinshui-siqi-yingdui.html` - 金税四期应对
- `odi-beian-quanliucheng.html` - ODI备案全流程

## SEO要点

每篇文章必须包含：

1. **Meta标签**
```html
<meta name="description" content="文章描述，150字左右">
<meta name="keywords" content="关键词1, 关键词2">
```

2. **Article Schema**
```html
<script type="application/ld+json">
{
    "@type": "Article",
    "headline": "文章标题",
    "author": { ... },
    "datePublished": "2026-05-20"
}
</script>
```

3. **FAQ Schema（可选）**
```html
<script type="application/ld+json">
{
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [...]
}
</script>
```

4. **作者署名**
```html
<div class="author-box">
    <img src="../images/founder.jpg" alt="邓达华">
    <div class="author-info">
        <h4>邓达华</h4>
        <p>存勤法税服务（广州）有限公司 创始人/总经理</p>
    </div>
</div>
```

## 添加新文章

1. 在此文件夹创建新的HTML文件
2. 参考 `yewucaifashui-ronghe.html` 的格式
3. 在 `../blog.html` 的文章列表中添加链接
4. 在 `../sitemap.xml` 和 `../baidusitemap.xml` 中添加URL
