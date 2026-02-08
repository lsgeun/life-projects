import os
from datetime import datetime

data = """

"""

# 절대 경로만 추출
paths = [p for p in data.split("\n") if p.strip()]

i = 0
for p in paths:
    if not os.path.isfile(p):
        print(f"❌ 파일 없음: {p}")
        continue

    i += 1
    # 파일 생성일 (macOS)
    stat = os.stat(p)
    creation_date = datetime.fromtimestamp(stat.st_birthtime).strftime("%Y-%m-%d")

    folder, filename = os.path.split(p)
    name, ext = os.path.splitext(filename)
    new_name = f"{name}_{creation_date}{ext}"
    new_path = os.path.join(folder, new_name)

    os.rename(p, new_path)
    print(f"✅ {filename} → {new_name}")

print(i)
