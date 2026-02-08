import os
import shutil
from datetime import datetime

# 원본 이미지 폴더
source_folder = "/Users/isgeun/임시 저장 폴더/아빠 사진 SSD로 정리 백업"
# 분류된 이미지를 저장할 루트 폴더
destination_root = "/Users/isgeun/임시 저장 폴더/분류한 사진"

# 이미지 확장자
image_extensions = {".jpg", ".jpeg", ".png", ".heic", ".gif", ".tiff", ".bmp"}

for filename in os.listdir(source_folder):
    file_path = os.path.join(source_folder, filename)
    
    if not os.path.isfile(file_path):
        continue
    
    ext = os.path.splitext(filename)[1].lower()
    if ext not in image_extensions:
        continue

    # macOS에서 파일 생성일 가져오기
    # * 윈도우나, 안드로이드에서 인식 못할 수도 있지만 거의 안 써서 상관 없음.
    stat = os.stat(file_path)
    creation_date = datetime.fromtimestamp(stat.st_birthtime)
    
    # yyyyMM__ 형식의 폴더명
    folder_name = creation_date.strftime("%Y%m__")
    dest_folder = os.path.join(destination_root, folder_name)
    os.makedirs(dest_folder, exist_ok=True)
    
    # 파일 이동
    shutil.move(file_path, os.path.join(dest_folder, filename))

print("이미지 분류 완료!")
