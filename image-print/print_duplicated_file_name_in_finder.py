import os
import subprocess
from collections import defaultdict

# 설정
TARGET_DIR = "_check_duplication"
os.makedirs(TARGET_DIR, exist_ok=True)
md_path = os.path.join(TARGET_DIR, "duplicate_files.md")
root_dir = '/Volumes/My Passport_ssd_sg5/SSD/사진'

# 1. 모든 파일 경로 수집
all_files = []
for root, dirs, files in os.walk(root_dir):
    for f in files:
        all_files.append(os.path.join(root, f))

# 2. 파일 이름별 경로 매핑
files_by_name = defaultdict(list)
for path in all_files:
    name = os.path.basename(path)
    files_by_name[name].append(path)

# 3. 중복 이름만 필터링
duplicates = {name: paths for name, paths in files_by_name.items() if len(paths) > 1}

# 4. Markdown 작성
with open(md_path, "w", encoding="utf-8") as md:
    md.write("# 중복 파일 목록\n\n")

    if not duplicates:
        md.write("✅ 중복된 파일 이름이 없습니다.\n")
    else:
        for name in sorted(duplicates.keys()):
            if name == ".DS_Store":
                continue
            
            md.write(f"### {name}\n")
            for path in duplicates[name]:
                md.write(path + "\n")
            md.write("\n")

print(f"✅ 완료: {md_path}")
