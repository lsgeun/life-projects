import os

path = "/Users/isgeun/Library/Mobile Documents/iCloud~md~obsidian/Documents/NOTE/4 아카이브"

dir_names = os.listdir(f"{path}")
dir_names = [_ for _ in dir_names if _.find("1학년 1학기") == -1]
dir_names = [_ for _ in dir_names if _.find(".") == -1]

print(dir_names)

for _ in dir_names:
    os.system(f"touch '{path}/{_}/0 {_}.md'")
