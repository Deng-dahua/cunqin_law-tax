#!/usr/bin/env python3
"""Inject article body into geo_articles_batch1.json"""
import json, sys

JSON_PATH = r'C:\Users\26726\WorkBuddy\2026-05-20-21-20-24\tools\geo_articles_batch1.json'

def set_body(slug, body_html):
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    for a in data:
        if a['slug'] == slug:
            a['body'] = body_html
            break
    else:
        print(f'ERROR: slug {slug} not found')
        return
    with open(JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f'Body set for {slug} ({len(body_html)} chars)')

if __name__ == '__main__':
    if len(sys.argv) >= 3:
        set_body(sys.argv[1], sys.argv[2])
    else:
        print('Usage: add_article_body.py <slug> "<html>"')
