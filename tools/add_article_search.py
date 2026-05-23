#!/usr/bin/env python3
"""为所有文章页添加文内搜索栏：CSS + HTML + JS"""

import os
import glob

SEARCH_CSS = """
    /* ===== 文内搜索栏 ===== */
    .article-search-bar {
      position: sticky;
      top: 64px;
      z-index: 999;
      background: #fff;
      border-bottom: 1px solid var(--dt-border);
      padding: 0.6rem 0;
      box-shadow: 0 1px 6px rgba(0,0,0,0.05);
    }
    .article-search-inner {
      max-width: 1140px;
      margin: 0 auto;
      padding: 0 1rem;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }
    .article-search-inner input {
      flex: 1;
      max-width: 400px;
      border: 1px solid var(--dt-border);
      border-radius: 4px;
      padding: 0.4rem 0.8rem;
      font-size: 0.9rem;
      font-family: inherit;
      color: var(--dt-text);
      outline: none;
      transition: border-color 0.2s;
    }
    .article-search-inner input:focus { border-color: var(--dt-accent); }
    .article-search-count {
      font-size: 0.82rem;
      color: var(--dt-text-light);
      white-space: nowrap;
    }
    .search-nav-btn {
      background: none;
      border: 1px solid var(--dt-border);
      border-radius: 4px;
      padding: 0.3rem 0.6rem;
      cursor: pointer;
      color: var(--dt-text-light);
      font-size: 0.85rem;
      font-family: inherit;
      transition: all 0.2s;
    }
    .search-nav-btn:hover { border-color: var(--dt-accent); color: var(--dt-accent); }
    .search-nav-btn:disabled { opacity: 0.35; cursor: default; }
    mark.search-mark {
      background: #ffe066;
      color: inherit;
      padding: 0 1px;
      border-radius: 2px;
    }
    mark.search-mark.active {
      background: #ff8c00;
      color: #fff;
    }
"""

SEARCH_HTML = """<!-- ===== 文内搜索栏 ===== -->
<div class="article-search-bar" id="articleSearchBar">
  <div class="article-search-inner">
    <input type="text" id="articleSearchInput" placeholder="在本文中搜索关键词..." onkeydown="if(event.key==='Enter'){doArticleSearch();event.preventDefault();}" oninput="doArticleSearch()">
    <span class="article-search-count" id="articleSearchCount"></span>
    <button class="search-nav-btn" onclick="jumpToMatch(-1)" title="上一个" id="searchPrevBtn" disabled><i class="fas fa-chevron-up"></i></button>
    <button class="search-nav-btn" onclick="jumpToMatch(1)" title="下一个" id="searchNextBtn" disabled><i class="fas fa-chevron-down"></i></button>
  </div>
</div>"""

SEARCH_JS = """
// ===== 文内搜索 =====
var articleCurrentMatch = -1;
var articleTotalMatches = 0;

function doArticleSearch() {
  var q = document.getElementById('articleSearchInput').value.trim();

  // 清除旧高亮
  var oldMarks = document.querySelectorAll('.article-body mark.search-mark');
  oldMarks.forEach(function(m) {
    var parent = m.parentNode;
    parent.replaceChild(document.createTextNode(m.textContent), m);
    parent.normalize();
  });

  articleCurrentMatch = -1;
  articleTotalMatches = 0;

  if (!q || q.length < 1) {
    document.getElementById('articleSearchCount').textContent = '';
    document.getElementById('searchPrevBtn').disabled = true;
    document.getElementById('searchNextBtn').disabled = true;
    return;
  }

  var body = document.querySelector('.article-body');
  if (!body) return;

  highlightInElement(body, q);

  articleTotalMatches = document.querySelectorAll('.article-body mark.search-mark').length;
  document.getElementById('articleSearchCount').textContent = articleTotalMatches + ' 处匹配';
  document.getElementById('searchPrevBtn').disabled = articleTotalMatches === 0;
  document.getElementById('searchNextBtn').disabled = articleTotalMatches === 0;

  if (articleTotalMatches > 0) {
    jumpToMatch(1);
  }
}

function highlightInElement(element, keyword) {
  var lowerKw = keyword.toLowerCase();
  var walker = document.createTreeWalker(element, NodeFilter.SHOW_TEXT, {
    acceptNode: function(n) {
      if (n.parentNode && (n.parentNode.nodeName === 'SCRIPT' || n.parentNode.nodeName === 'STYLE' || n.parentNode.nodeName === 'MARK')) {
        return NodeFilter.FILTER_REJECT;
      }
      return NodeFilter.FILTER_ACCEPT;
    }
  });

  var textNodes = [];
  while (walker.nextNode()) textNodes.push(walker.currentNode);

  textNodes.forEach(function(node) {
    var text = node.textContent;
    var idx = text.toLowerCase().indexOf(lowerKw);
    if (idx === -1) return;

    var fragment = document.createDocumentFragment();
    var lastIdx = 0;
    while (idx !== -1) {
      if (idx > lastIdx) {
        fragment.appendChild(document.createTextNode(text.substring(lastIdx, idx)));
      }
      var mark = document.createElement('mark');
      mark.className = 'search-mark';
      mark.textContent = text.substring(idx, idx + keyword.length);
      fragment.appendChild(mark);
      lastIdx = idx + keyword.length;
      idx = text.toLowerCase().indexOf(lowerKw, lastIdx);
    }
    if (lastIdx < text.length) {
      fragment.appendChild(document.createTextNode(text.substring(lastIdx)));
    }
    node.parentNode.replaceChild(fragment, node);
  });
}

function jumpToMatch(direction) {
  var marks = document.querySelectorAll('.article-body mark.search-mark');
  if (marks.length === 0) return;

  marks.forEach(function(m) { m.classList.remove('active'); });

  if (articleCurrentMatch === -1) {
    articleCurrentMatch = direction > 0 ? 0 : marks.length - 1;
  } else {
    articleCurrentMatch += direction;
    if (articleCurrentMatch >= marks.length) articleCurrentMatch = 0;
    if (articleCurrentMatch < 0) articleCurrentMatch = marks.length - 1;
  }

  var target = marks[articleCurrentMatch];
  target.classList.add('active');
  target.scrollIntoView({behavior: 'smooth', block: 'center'});
}
"""

# ---------- anchors ----------
CSS_ANCHOR = "/* ===== 文章目录（侧边栏） ===== */"
HTML_ANCHOR_OLD = "</section>\n\n<!-- ===== 文章布局"
HTML_ANCHOR_NEW = "</section>\n\n" + SEARCH_HTML.strip() + "\n\n<!-- ===== 文章布局"
JS_ANCHOR_OLD = "updateBtns();\n})();\n</script>"
JS_ANCHOR_NEW = "updateBtns();\n})();\n" + SEARCH_JS.strip() + "\n</script>"

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    modified = False

    # 1. Insert CSS
    if SEARCH_CSS.strip() not in content:
        content = content.replace(CSS_ANCHOR, SEARCH_CSS.strip() + "\n\n" + CSS_ANCHOR, 1)
        modified = True
        print(f"  [CSS] inserted")

    # 2. Insert HTML search bar
    if SEARCH_HTML.strip() not in content:
        content = content.replace(HTML_ANCHOR_OLD, HTML_ANCHOR_NEW, 1)
        modified = True
        print(f"  [HTML] inserted")

    # 3. Insert JS
    # Only replace the LAST occurrence (before </body>)
    if "function doArticleSearch" not in content:
        # find last occurrence of updateBtns
        last = content.rfind(JS_ANCHOR_OLD)
        if last != -1:
            content = content[:last] + JS_ANCHOR_NEW + content[last + len(JS_ANCHOR_OLD):]
            modified = True
            print(f"  [JS] inserted")

    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    articles_dir = os.path.join(base, 'source', 'articles')
    files = sorted(glob.glob(os.path.join(articles_dir, '*(source).html')))

    print(f"Processing {len(files)} article files...\n")

    for fp in files:
        name = os.path.basename(fp)
        print(f"{name}:")
        ok = process_file(fp)
        if not ok:
            print(f"  (already processed, skipping)")
        print()

    print("Done.")

if __name__ == '__main__':
    main()
