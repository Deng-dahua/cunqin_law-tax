#!/usr/bin/env python3
"""Find all source HTML files and check git deployment status"""
import os, subprocess

os.chdir("C:/Users/26726/WorkBuddy/2026-05-20-21-20-24")

# Get all source HTML files
html_files = []
for root, dirs, files in os.walk("source"):
    for f in files:
        if f.endswith(".html"):
            html_files.append(os.path.join(root, f).replace("\\", "/"))

# Get all tracked + untracked
r1 = subprocess.run(["git", "ls-files", "--cached", "--others", "--exclude-standard"],
                     capture_output=True, text=True)
tracked = set(line.strip() for line in r1.stdout.splitlines() if line.strip())

# Get committed only
r2 = subprocess.run(["git", "ls-files", "--cached"], capture_output=True, text=True)
committed = set(line.strip() for line in r2.stdout.splitlines() if line.strip())

untracked = [f for f in html_files if f not in tracked]
not_committed = [f for f in html_files if f in tracked and f not in committed]

print("=== UNTRACKED (new files, not git added) ===")
for f in sorted(untracked):
    print(f"  [NEW] {f}")

print(f"\n=== NOT COMMITTED (added but not committed) ===")
for f in sorted(not_committed):
    print(f"  [MOD] {f}")

total = len(untracked) + len(not_committed)
print(f"\nTotal pending deploy: {len(untracked)} new + {len(not_committed)} modified = {total}")
