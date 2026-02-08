import os
import sys

saveDir = sys.argv[1]
saveDir = saveDir.replace(' ', '\ ')
linkDir = sys.argv[2]
linkDir = linkDir.replace(' ', '\ ')
yearInt = int(sys.argv[3])

os.system(f"python '/Users/isgeun/Library/Mobile Documents/iCloud~md~obsidian/Documents/NOTE/2 Areas/정기적인 기록/정기적인 기록 년도에 대한 메모 생성 소스 코드/create_empty_note.py' {saveDir} {yearInt}")
os.system(f"python '/Users/isgeun/Library/Mobile Documents/iCloud~md~obsidian/Documents/NOTE/2 Areas/정기적인 기록/정기적인 기록 년도에 대한 메모 생성 소스 코드/insert_template_to_note.py' {saveDir} {linkDir} {yearInt}")

