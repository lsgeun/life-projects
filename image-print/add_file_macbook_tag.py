import os
import subprocess
import unicodedata

data = """

"""

# 절대 경로만 추출
paths = data.split("\n")[1:-1]

for p in paths:
    # ! 파일 경로명과 태그명 잘 확인하기!
    # * 올바른 문자 비교를 위해서 unicode를 NFC(완성형)으로 바꿈.
    # 추가할 태그 이름
    tag_name = "SSD5/프린터한 거"
    tag_name = unicodedata.normalize("NFC", tag_name)
    # 현재 태그 목록 가져오기
    file_tags = subprocess.run(["tag", "-l", p], capture_output=True, text=True)
    file_tags = unicodedata.normalize("NFC", file_tags.stdout)
    # 태그를 정확히 비교하기 위해 아래 2줄 씀.
    # 부분적으로 일치하면 false, 완전히 일치해야 true.
    file_tags = file_tags.split("\t")[-1].split(",")
    if tag_name in file_tags:
        print("✅ 이미 태그 있음:", p)
        continue

    # homebrew로 설치한 tag 명령을 이용
    # * 맥북 태그를 붙이는 것임. =윈도우, 안드로이드에서 인식 못함. 근데 거의 안 써서 상관 없음.
    subprocess.run(["tag", "-a", tag_name, p])
    print("태그 추가:", p)
