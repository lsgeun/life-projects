import os

# parent_path = "/Users/isgeun/Library/Mobile Documents/iCloud~md~obsidian/Documents/NOTE/1 프로젝트/웹 해킹"
# subdir_names = ["이것이 MySQL이다", "자바스크립트 완벽 가이드", "Do it HTML5 CSS3 웹 표준의 정석", "HTTP 완벽 가이드 - 웹은 어떻게 동작하는가", "JAVA의 정석", "윤성우의 열혈 TCP-IP 소켓 프로그래밍"]

# for _ in subdir_names:
#     path = f"{parent_path}/{_}"

path = "/Users/isgeun/Library/Mobile Documents/iCloud~md~obsidian/Documents/NOTE/2 영역/컴퓨터/후니의 쉽게 쓴 시스코 네트워킹"

index_depth1_md_file_names = os.listdir(f"{path}")
index_depth1_md_file_names = [_ for _ in index_depth1_md_file_names if _.find(".md") != -1]
index_depth1_md_file_names = [_ for _ in index_depth1_md_file_names if _[0] != '0' and _[0].isdigit() and (_[1] == ' ' or _[2] == ' ')]

dir_names = []
for _ in index_depth1_md_file_names:
    if _.find(" - ") == 1:
        dir_names.append(_[4:-3])
    elif _.find(" - ") == 2:
        dir_names.append(_[5:-3])
    elif _.find(" ") == 2:
        dir_names.append(_[3:-3])
    else:
        dir_names.append(_[2:-3])

index_depth1_md_file_names.sort()
dir_names.sort()

# print(index_depth1_md_file_names)
# print(dir_names)

for _ in dir_names:
    os.system(f"mkdir '{path}/{_}'")
