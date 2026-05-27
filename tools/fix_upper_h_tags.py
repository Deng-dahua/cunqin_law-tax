"""Fix uppercase H tags to lowercase for SEO""".
import re, os, glob

files = sorted(glob.glob('source/articles/*.html'))

upper_files = []
for fp in files:
    with open(fp, "r", encoding="utf-8") as f:
        c = f.read()
    if re.search(r"<H[1-4]", c):
        upper_files.append(fp)

print(f"Need fix: {len(upper_files)} files")

count = 0
for fp in upper_files:
    with open(fp, "r", encoding="utf-8") as f:
        c = f.read()
    original = c
    c = re.sub(r"<(/?)H([1-4])([^>]*)>", r"<h>", c)
    if c != original:
        with open(fp, "w", encoding="utf-8") as f:
            f.write(c)
        count += 1
        print(f"  OK {os.path.basename(fp)}")

print(f"Done: {count} files fixed")
