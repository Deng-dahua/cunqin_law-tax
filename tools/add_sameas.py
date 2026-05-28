#!/usr/bin/env python3
"""Add sameAs external links to all Schema.org JSON-LD blocks across source files"""
import os, re

BASE = "C:/Users/26726/WorkBuddy/2026-05-20-21-20-24"

# User-provided external links
QCC_URL = "https://www.qcc.com/firm/0154c65337aa7fba73076a16778295d0.html"
ZHIHU_URL = "https://www.zhihu.com/people/l2ylp9z"

# For Organization schemas, add QCC + Zhihu
ORG_SAMEAS = f'"sameAs": ["{QCC_URL}", "{ZHIHU_URL}"]'

# For Person schemas, add Zhihu
PERSON_SAMEAS = f'"sameAs": ["{ZHIHU_URL}"]'

files_to_patch = {
    # File path: (target sameAs value, search context to disambiguate)
    "source/首页(source).html": [
        (ORG_SAMEAS, "Organization"),
    ],
    "source/about/关于我们(source).html": [
        (ORG_SAMEAS, "存勤法税服务（广州）有限公司"),
        (ORG_SAMEAS, '"@id": "https://cunqin.tax/#org"'),
    ],
    "source/about/deng-dahua.html": [
        (PERSON_SAMEAS, "Person"),
    ],
}

count = 0
for fname, patches in files_to_patch.items():
    fpath = os.path.join(BASE, fname)
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()
    
    original = content
    for replacement, _ctx in patches:
        old = '"sameAs": []'
        new = replacement
        if old in content:
            content = content.replace(old, new, 1)
            count += 1
    
    if content != original:
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  [OK] {fname}")

print(f"\nDone! Patched {count} sameAs slots.")
