import os
import re
import time
import datetime

# timemator csv 파일 경로
csv_file_path = "/Users/isgeun/Library/Mobile Documents/iCloud~md~obsidian/Documents/NOTE-iCloud_Drive/0 Inbox/Timemator Export 2024-01-02 08.58.14.csv"

def get_date(kst):
    year = int(kst[0:4]); month = int(kst[4:6]); day = int(kst[6:8]); hour = int(kst[9:11]); minute = int(kst[11:13]); second = int(kst[13:15]); 
    date = datetime.datetime(year, month, day, hour, minute, second)
    
    return date

# timemator csv 파일 불러오기
csv_file_content = None
with open(csv_file_path, "r") as f:
    csv_file_content = f.readlines(); csv_file_content = csv_file_content[1:]; csv_file_content = "".join(csv_file_content); 

# 시작 시간, 종료 시간, 제목 정규식 pattern
start_end_heading_pattern = re.compile(r"(.+?),(.+?),.+?,.+?,.+?,\".*?\",\"(.+?)\",(?:.+?,){4}(?:.*?,){3}\"(.*?)\"")
# 시작 시간, 종료 시간, 제목 찾기
start_end_heading_match = start_end_heading_pattern.search(csv_file_content)

# * time_entries의 키(제목)에 [시작 시간, 종료 시간]을 저장하기
time_entries = {}
while start_end_heading_match != None:
    # 시작 시간, 종료 시간, 제목 정규식 변수에 저장
    ## 시작 시간
    start_micro_second = int(start_end_heading_match.group(1))
    start_date = time.localtime(start_micro_second)
    start_KST = str(start_date.tm_year) + str(start_date.tm_mon).zfill(2) + str(start_date.tm_mday).zfill(2) + "T" + str(start_date.tm_hour).zfill(2) + str(start_date.tm_min).zfill(2) + str(start_date.tm_sec).zfill(2)
    ## 종료 시간
    end_micro_second = int(start_end_heading_match.group(2))
    end_date = time.localtime(end_micro_second)
    end_KST = str(end_date.tm_year) + str(end_date.tm_mon).zfill(2) + str(end_date.tm_mday).zfill(2) + "T" + str(end_date.tm_hour).zfill(2) + str(end_date.tm_min).zfill(2) + str(end_date.tm_sec).zfill(2)
    ## 제목
    heading = start_end_heading_match.group(3)
    ## 노트
    note = start_end_heading_match.group(4)
    # time_entries에 이름이 [제목]인 키가 없다면 이름이 [제목]인 키를 추가한 후 빈 배열 할당
    if heading not in time_entries.keys():
        time_entries[heading] = []
    
    time_entries[heading].append([start_KST, end_KST, note])
    
    # 시작 시간, 종료 시간, 제목 찾기
    start_end_heading_match = start_end_heading_pattern.search(csv_file_content, start_end_heading_match.end(0))

# ^ 연속된 time entry가 5분 미만으로 차이 나면 하나의 time entry 합침
for heading in time_entries.keys():
    # 현재 인덱스
    current_index = 0
    # 현재 인덱스가 마지막 원소를 가리키지 않을 동안 반복
    while current_index != len(time_entries[heading])-1:
        # 현재 start_KST, end_KST, end_KST_date
        current_start_KST = time_entries[heading][current_index][0]
        current_end_KST = time_entries[heading][current_index][1]
        current_end_KST_date = get_date(current_end_KST)
        # 다음 인덱스 start_KST, end_KST, start_KST_date
        next_start_KST = time_entries[heading][current_index+1][0]
        next_end_KST = time_entries[heading][current_index+1][1]
        next_note = time_entries[heading][current_index+1][2]
        next_start_KST_date = get_date(next_start_KST)
        # 연속된 time entry가 5분 미만으로 차이 나면 하나의 time entry 합침
        if (next_start_KST_date - current_end_KST_date).seconds < 5 * 60:
            time_entries[heading][current_index] = [current_start_KST, next_end_KST, next_note]
            time_entries[heading].pop(current_index+1)
        else:
            current_index += 1

# ^ time entry의 시작 시간과 종료 시간이 2분보다 작은 작게 차이 나면 time entry를 삭제함
for heading in time_entries.keys():
    current_index = 0
    while current_index != len(time_entries[heading]):
        # 현재 start_KST, start_KST_date, end_KST, end_KST_date
        current_start_KST = time_entries[heading][current_index][0]
        current_start_KST_date = get_date(current_start_KST)
        current_end_KST = time_entries[heading][current_index][1]
        current_end_KST_date = get_date(current_end_KST)
        
        if (current_end_KST_date - current_start_KST_date).seconds < 2 * 60:
            time_entries[heading].pop(current_index)
        else:
            current_index += 1

# csv 파일 현재 디렉토리
csv_file_directory = os.path.dirname(csv_file_path)
# csv 파일 이름
csv_file_name = os.path.basename(csv_file_path)[:-4]
# csv 파일 넣을 디렉토리 생성
if not os.path.isdir(f"{csv_file_directory}/{csv_file_name}"):
    os.system(f"mkdir \"{csv_file_directory}/{csv_file_name}\"")
# * csv 파일 현재 디렉토리에 [제목].ics 파일 생성하기
for heading in time_entries.keys():
    ics_file_content = "BEGIN:VCALENDAR\n"
    for start_KST, end_KST, note in time_entries[heading]:
        ics_file_content += "BEGIN:VEVENT\n"
        ics_file_content += f"SUMMARY:{heading}\n"
        ics_file_content += f"DTSTART:{start_KST}\n"
        ics_file_content += f"DTEND:{end_KST}\n"
        ics_file_content += f"DESCRIPTION:{note}\n"
        ics_file_content += "END:VEVENT\n"
    ics_file_content += "END:VCALENDAR"
    
    with open(f"{csv_file_directory}/{csv_file_name}/{heading} {csv_file_name}.ics", "w") as f:
        f.writelines(ics_file_content)

# * csv 파일 현재 디렉토리에 All.ics 파일 생성하기
ics_file_content = "BEGIN:VCALENDAR\n"
for heading in time_entries.keys():
    for start_KST, end_KST, note in time_entries[heading]:
        ics_file_content += "BEGIN:VEVENT\n"
        ics_file_content += f"SUMMARY:{heading}\n"
        ics_file_content += f"DTSTART:{start_KST}\n"
        ics_file_content += f"DTEND:{end_KST}\n"
        ics_file_content += f"DESCRIPTION:{note}\n"
        ics_file_content += "END:VEVENT\n"
ics_file_content += "END:VCALENDAR"

with open(f"{csv_file_directory}/{csv_file_name}/All {csv_file_name}.ics", "w") as f:
    f.writelines(ics_file_content)
