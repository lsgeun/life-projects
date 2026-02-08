import re

INPUT_FILE = "/Users/isgeun/Library/Mobile Documents/iCloud~md~obsidian/Documents/memo/03_life/프린트/출력한 이미지 프린트물/아빠 사진.md"
OUTPUT_FILE = "/Users/isgeun/Library/Mobile Documents/iCloud~md~obsidian/Documents/memo/03_life/프린트/출력한 이미지 프린트물/아빠 사진 복사본.md"

# 파일 읽기
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    text = f.read()

# 이미지 링크 추출
links = re.findall(r'!\[[^]]*?\]\([^)]+?\)', text)
n = len(links)
if n == 0:
    print("이미지 링크가 없습니다.")
    exit()

# 4등분
k = 4
chunk_size = (n + k - 1) // k
chunks = [links[i:i + chunk_size] for i in range(0, n, chunk_size)]

# Markdown 구조 생성
new_lines = []
for part in chunks:
    new_lines.append("- ")
    for link in part:
        new_lines.append(f"    - {link}")

new_text = "\n".join(new_lines) + "\n"

# 파일에 덮어쓰기
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(new_text)

print(f"✅ {n}개의 이미지 링크를 4등분하여 '{OUTPUT_FILE}'에 저장했습니다.")
