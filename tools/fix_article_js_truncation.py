#!/usr/bin/env python3
"""
修复所有8篇文章中截断的JS代码:
1. doArticleSearch 中 forEach 缺少 });
2. highlightInElement 函数体在 createTreeWalker 后截断
3. jumpToMatch 函数完全缺失
"""
import os
import re

ARTICLES_DIR = r'C:\Users\26726\WorkBuddy\2026-05-20-21-20-24\source\articles'

# 完整的 highlightInElement 函数（替换截断版）
COMPLETE_HIGHLIGHT = '''function highlightInElement(element, keyword) {
  var lowerKw = keyword.toLowerCase();
  var walker = document.createTreeWalker(element, NodeFilter.SHOW_TEXT, {
    acceptNode: function(n) {
      if (n.parentNode && (n.parentNode.nodeName === 'SCRIPT' || n.parentNode.nodeName === 'STYLE' || n.parentNode.nodeName === 'MARK')) {
        return NodeFilter.FILTER_REJECT;
      }
      return NodeFilter.FILTER_ACCEPT;
    }
  }, false);

  var textNodes = [];
  var node;
  while (node = walker.nextNode()) {
    if (node.nodeValue.toLowerCase().indexOf(lowerKw) >= 0) {
      textNodes.push(node);
    }
  }

  var escaped = keyword.replace(/[.*+?^${}()|[\\]\\\\]/g, '\\\\$&');
  var regex = new RegExp('(' + escaped + ')', 'gi');

  textNodes.forEach(function(textNode) {
    var frag = document.createDocumentFragment();
    var lastIdx = 0;
    var text = textNode.nodeValue;
    var match;
    while ((match = regex.exec(text)) !== null) {
      if (match.index > lastIdx) {
        frag.appendChild(document.createTextNode(text.substring(lastIdx, match.index)));
      }
      var mark = document.createElement('mark');
      mark.className = 'search-mark';
      mark.textContent = match[0];
      frag.appendChild(mark);
      lastIdx = regex.lastIndex;
    }
    if (lastIdx < text.length) {
      frag.appendChild(document.createTextNode(text.substring(lastIdx)));
    }
    textNode.parentNode.replaceChild(frag, textNode);
    regex.lastIndex = 0;
  });
}

function jumpToMatch(direction) {
  var marks = document.querySelectorAll('.article-body mark.search-mark');
  if (marks.length === 0) return;

  marks.forEach(function(m) { m.classList.remove('active'); });

  articleCurrentMatch += direction;
  if (articleCurrentMatch >= marks.length) articleCurrentMatch = 0;
  if (articleCurrentMatch < 0) articleCurrentMatch = marks.length - 1;

  var currentMark = marks[articleCurrentMatch];
  currentMark.classList.add('active');

  var offset = 120;
  var top = currentMark.getBoundingClientRect().top + window.pageYOffset - offset;
  window.scrollTo({ top: top, behavior: 'smooth' });

  document.getElementById('articleSearchCount').textContent = (articleCurrentMatch + 1) + '/' + articleTotalMatches + ' \\u5904\\u5339\\u914d';
}
'''

# 截断版的 highlightInElement 函数头（到 }, false); 结束）
TRUNCATED_PATTERN = re.compile(
    r'function highlightInElement\(element, keyword\) \{\s*'
    r'var lowerKw = keyword\.toLowerCase\(\);\s*'
    r'var walker = document\.createTreeWalker\(element, NodeFilter\.SHOW_TEXT, \{\s*'
    r'acceptNode: function\(n\) \{\s*'
    r'if \(n\.parentNode && \(n\.parentNode\.nodeName === .SCRIPT. \|\| n\.parentNode\.nodeName === .STYLE. \|\| n\.parentNode\.nodeName === .MARK.\)\) \{\s*'
    r'return NodeFilter\.FILTER_REJECT;\s*'
    r'\}\s*'
    r'return NodeFilter\.FILTER_ACCEPT;\s*'
    r'\}\s*'
    r'\}, false\);\s*$',
    re.DOTALL
)

# Fix 1: forEach 缺少 });
FOREACH_FIX_OLD = '''  oldMarks.forEach(function(m) {
    var parent = m.parentNode;
    parent.replaceChild(document.createTextNode(m.textContent), m);
    parent.normalize();

  articleCurrentMatch = -1;'''

FOREACH_FIX_NEW = '''  oldMarks.forEach(function(m) {
    var parent = m.parentNode;
    parent.replaceChild(document.createTextNode(m.textContent), m);
    parent.normalize();
  });

  articleCurrentMatch = -1;'''


def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    fixes = []

    # Fix 1: forEach missing });
    if FOREACH_FIX_OLD in content:
        content = content.replace(FOREACH_FIX_OLD, FOREACH_FIX_NEW)
        fixes.append('forEach });')

    # Fix 2: truncated highlightInElement -> complete version
    # Find the line "function highlightInElement(element, keyword) {" and everything after it
    truncated_start = content.find('function highlightInElement(element, keyword) {')
    if truncated_start >= 0:
        # Check if the function is incomplete (file ends shortly after)
        remaining = content[truncated_start:]
        if 'jumpToMatch' not in remaining:
            # Truncated! Replace from the function start with complete version
            # But we need to keep the scroll buttons code if it's before highlightInElement
            content = content[:truncated_start] + COMPLETE_HIGHLIGHT + '\n'
            fixes.append('highlightInElement+jumpToMatch')
        else:
            print(f'  WARNING: jumpToMatch already exists, skipping replacement')

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return fixes
    return []


def main():
    files = sorted([f for f in os.listdir(ARTICLES_DIR) if f.endswith('(source).html')])
    print(f'Found {len(files)} article files\n')

    total_fixes = 0
    for f in files:
        filepath = os.path.join(ARTICLES_DIR, f)
        fixes = fix_file(filepath)
        if fixes:
            print(f'  ✅ {f}: {", ".join(fixes)}')
            total_fixes += 1
        else:
            print(f'  ⏭️  {f}: no fixes needed (already correct)')

    print(f'\nDone. Fixed {total_fixes}/{len(files)} files.')


if __name__ == '__main__':
    main()
