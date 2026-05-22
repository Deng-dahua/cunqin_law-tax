#!/usr/bin/env python3
"""Batch update: replace wechat-qrcode.png with wechat-qrcode-orange.png in all CTA QR code blocks."""
import os
import re

SOURCE_DIR = r"C:\Users\26726\WorkBuddy\2026-05-20-21-20-24\source"

# All HTML files to process
files = []
for root, dirs, fnames in os.walk(SOURCE_DIR):
    # Skip .workbuddy
    if ".workbuddy" in root:
        continue
    for f in fnames:
        if f.endswith(".html"):
            files.append(os.path.join(root, f))

print(f"Found {len(files)} HTML files")

updated = 0
for fpath in files:
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()
    
    if "wechat-qrcode.png" not in content and "wechat-qrcode-orange.png" not in content:
        continue
    
    original = content
    
    # Replace wechat-qrcode.png with wechat-qrcode-orange.png (only in cta-qrcode context or any context)
    content = content.replace("wechat-qrcode.png", "wechat-qrcode-orange.png")
    
    if content != original:
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(content)
        updated += 1
        print(f"  ✓ Updated: {os.path.relpath(fpath, SOURCE_DIR)}")

print(f"\nTotal updated: {updated} files")
