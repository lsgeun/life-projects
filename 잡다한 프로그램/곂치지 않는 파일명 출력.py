from collections import Counter

with open(
    "/Users/isgeun/Library/Mobile Documents/iCloud~md~obsidian/Documents/memo/01_inbox/a.txt",
    "r",
) as f:
    content_a = f.readlines()
    content_a = [_.replace("\n", "") for _ in content_a]

with open(
    "/Users/isgeun/Library/Mobile Documents/iCloud~md~obsidian/Documents/memo/01_inbox/c.txt",
    "r",
) as f:
    content_b = f.readlines()
    content_b = [_.replace("\n", "") for _ in content_b]

set_a = set(content_a)
set_b = set(content_b)

a_minus_b = list(set_a - set_b)
b_minus_a = list(set_b - set_a)

print("a에 있지만, b에 없는 파일명")
for _ in a_minus_b:
    print(_)
print()
print("b에 있지만, a에 없는 파일명")
for _ in b_minus_a:
    print(_)

counter_a = Counter(content_a)
duplicates_a = [_ for _, count in counter_a.items() if count > 1]

counter_b = Counter(content_b)
duplicates_b = [_ for _, count in counter_b.items() if count > 1]

print("a에서 중복된 파일명")
for _ in duplicates_a:
    print(_)
print()
print("b에서 중복된 파일명")
for _ in duplicates_b:
    print(_)
