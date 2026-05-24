import os

fpath = r'C:\Users\26726\WorkBuddy\2026-05-20-21-20-24\.workbuddy\memory\2026-05-24.md'
with open(fpath, 'a', encoding='utf-8') as f:
    f.write('\n## 自定义域名切换 cunqin.tax（07:44）\n')
    f.write('- _config.yml: url 改为 https://cunqin.tax，root 改为 /\n')
    f.write('- 创建 source/CNAME（GitHub Pages 自动配置 HTTPS）\n')
    f.write('- 全站 24 个 HTML 文件：canonical/og:url/og:image/twitter:image/Schema.org JSON-LD\n')
    f.write('  全部从 https://deng-dahua.github.io/cunqin_law-tax/ 改为 https://cunqin.tax/\n')
    f.write('- search-index.json: 24 条 url 从 /cunqin_law-tax/xxx 改为 /xxx\n')
    f.write('- sitemap.xml / robots.txt: 全部 <loc> 和 Sitemap URL 更新为新域名\n')
    f.write('- search.html: scopePrefixes 从 /cunqin_law-tax/articles/ 改为 /articles/\n')
    f.write('- 修正旧域名拼写混乱（deng-dahua 三个 a / deng-dahua 两个 a），replace_domain.py 同时覆盖两种拼写\n')
    f.write('- tools/replace_domain.py: 域名替换脚本（已移出 source/）\n')
    f.write('- 本地 hexo generate 成功，31 个文件已推送，GitHub Actions 构建中\n')
print('写入成功')
