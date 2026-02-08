import calendar as cal
import datetime as dt
import os
import re
# ^ python version: 3.11.6 64bit

# ^ 아래 코드를 통해 제목 1 패턴을 얻을 수 있고 이를 통해 원하는 제목을 원하는 위치에 넣을 수 있다.
# heading_1_pattern = re.compile(r""" ^\#[ ](.*?)(\n|\Z) # heading 이름
#                                 (.|\n)*?           # heading 내용
#                                 (?=(\#[ ]|\Z))     # heading 끝
#                                 """, re.MULTILINE | re.VERBOSE)

# for 문에서 FROM, TO로 가독성을 높히기 위함
FROM = 0; TO = 1
# str.find() 함수의 반환값에 대한 이해도를 높히기 위함
NOT_FOUND = -1

# date_note_directory
date_note_directory = "/Users/isgeun/Library/Mobile Documents/iCloud~md~obsidian/Documents/NOTE-iCloud_Drive/2 Areas/Date Note"

# yearly_note
yearly_note = "2026"
# 현재 연도
current_year = int(yearly_note[0:4])
# 이전 연도
previous_year = current_year - 1
# 다음 연도
next_year = current_year + 1
# 현재 연도 디렉토리
current_year_directory = f"{date_note_directory}/{current_year}"
# 이전 연도 디렉토리
previous_year_directory = f"{date_note_directory}/{previous_year}"
# 다음 연도 디렉토리
next_year_directory = f"{date_note_directory}/{next_year}"

def insert_icon(file_path, icon):
    with open(file_path, "r") as file:
        file_content = file.readlines(); file_content = "".join(file_content)
    
    # * 폴더 파일에 아이콘 넣기
    # properties pattern
    properties_pattern = re.compile(r"\A(---\n(?:.+?\n)+?)(---)")
    # properties_match
    properties_match = properties_pattern.search(file_content)
    # 폴더 파일에 아이콘 추가하기
    ## * properties가 없다면 properties를 만들고 아이콘 추가
    if properties_match == None:
        if icon == "":
            # properties를 만들지 않음.
            pass
        else:
            file_content = f"---\nicon: {icon}\n---\n" + file_content
    ## * properties가 있을 때, 기존 property들을 유지한 채 icon property가 없다면  icon property를 추가, icon property가 있다면 icon property를 변경
    else:
        # properties 문자열
        properties = properties_match.group(0)
        # icon property pattern
        icon_property_pattern = re.compile(r"icon: (.+?)(?=\n)")
        # icon property match
        icon_property_match = icon_property_pattern.search(properties)
        # icon property가 없다면 icon property를 추가
        if icon_property_match == None:
            if icon == "":
                # properties를 만들지 않음.
                pass
            else:
                file_content = file_content[:properties_match.end(1)] + f"icon: {icon}\n" + file_content[properties_match.start(2):]
        # icon property가 있다면 icon property를 변경
        else: 
            if icon == "":
                # properties를 만들지 않음.
                file_content = file_content[:properties_match.start(0) + icon_property_match.start(0)] + file_content[properties_match.start(0) + icon_property_match.end(0)+1:] # 1을 추가하는 이유는 '\n'까지 삭제해야 하기 때문
            else:
                file_content = file_content[:properties_match.start(0) + icon_property_match.start(1)] + f"{icon}" + file_content[properties_match.start(0) + icon_property_match.end(1):]
    
    with open(file_path, "w") as file:
        file.writelines(file_content)

def add_to_note_heading(file_content, string):
    note_heading = "# Note\n"
    note_heading_start_index = file_content.find(note_heading)
    note_heading_end_index = note_heading_start_index + len(note_heading)
    if note_heading_start_index == NOT_FOUND:
        properties_pattern = re.compile(r"\A---\n(?:.+?\n)+?---\n")
        properties_match = properties_pattern.search(file_content)
        
        if properties_match == None:
            file_content =  note_heading +\
                            string + \
                            file_content
        else:
            file_content = file_content[:properties_match.end(0)] +\
                                        note_heading +\
                                        string +\
                                        file_content[properties_match.end(0):]
    else:
        file_content = file_content[:note_heading_end_index] +\
                                    string +\
                                    file_content[note_heading_end_index:]
    
    return file_content

# ^ date_note_in_year_directory에 date_note 넣기
## * 연도 디렉토리의 date_note 만들기
date_note_in_year_directory = {}

## * yearly_note 넣기
date_note_in_year_directory[yearly_note] = {}

## * quarterly_note 넣기
for quarter in range(FROM + 1, TO + 4):
    # quarterly_note
    quarterly_note = f"{current_year}-Q{quarter}"
    date_note_in_year_directory[yearly_note][quarterly_note] = {}

## * monthly_note 넣기
for quarterly_note in date_note_in_year_directory[yearly_note]:
    quarter = int(quarterly_note[-1])
    
    for month in range(FROM + 3*quarter-2, TO + 3*quarter):
        # monthly_note
        monthly_note = f"{current_year}-{str(month).zfill(2)}"
        date_note_in_year_directory[yearly_note][quarterly_note][monthly_note] = {}

## * weekly_note, daily_note 넣기
for quarterly_note in date_note_in_year_directory[yearly_note]:
    quarter = int(quarterly_note[-1])
    
    for monthly_note in date_note_in_year_directory[yearly_note][quarterly_note]:
        month = int(monthly_note[-2:])
        # 연-월의 전체 일 수
        day_count_in_month = cal.monthrange(current_year, month)[1] # [해당 연-월의 첫 번째 일의 요일, 해당 연-월의 전체 일수]를 반환
        
        for day in range(FROM + 1, TO + day_count_in_month):
            # 연-월-일의 isocalendar
            daily_note_isocalendar = dt.datetime(current_year, month, day).isocalendar() # [해당 연-월-일의 연, 해당 연-월-일의 주, 해당 연-월-일의 요일]을 반환
            
            ### * weekly_note 넣기
            # weekly_note의 연도는 이전 연도, 현재 연도, 다음 연도 일 수 있음
            weekly_note_year = daily_note_isocalendar[0]
            # week_included_daily_note를 포함하는 weekly_note의 week
            week_included_daily_note = daily_note_isocalendar[1]
            # weekly_note
            weekly_note = f"{weekly_note_year}-W{str(week_included_daily_note).zfill(2)}"
            
            if weekly_note not in date_note_in_year_directory[yearly_note][quarterly_note][monthly_note]:
                date_note_in_year_directory[yearly_note][quarterly_note][monthly_note][weekly_note] = {}
            
            ### * daily_note 넣기
            # daily_note
            daily_note = f"{current_year}-{str(month).zfill(2)}-{str(day).zfill(2)}"
            # daily_note의 요일
            daily_note_weekday = daily_note_isocalendar[2]
            
            date_note_in_year_directory[yearly_note][quarterly_note][monthly_note][weekly_note][daily_note] = daily_note_weekday

# ^ date_note 생성
## * current_year_directory 생성
if not os.path.isdir(current_year_directory):
    os.system(f"mkdir \"{current_year_directory}\"")

## * yearly_note 생성
os.system(f"touch \"{current_year_directory}/{yearly_note}.md\"")

## * quarterly_note, monthly_note, weekly_note, daily_note 생성
for quarterly_note in date_note_in_year_directory[yearly_note]:
    ### * quarterly_note 생성
    os.system(f"touch \"{current_year_directory}/{quarterly_note}.md\"")
    
    for monthly_note in date_note_in_year_directory[yearly_note][quarterly_note]:
        ### * monthly_note 생성
        os.system(f"touch \"{current_year_directory}/{monthly_note}.md\"")
        
        for weekly_note in date_note_in_year_directory[yearly_note][quarterly_note][monthly_note]:
            ### * weekly_note 생성
            # weekly_note의 year
            weekly_note_year = int(weekly_note[0:4])
            
            # weekly_note_year가 현재 연도일 경우 current_year_directory에 weekly_note_year 생성
            if weekly_note_year == current_year:
                os.system(f"touch \"{current_year_directory}/{weekly_note}.md\"")
            # weekly_note_year가 이전 연도일 경우 previous_year_directory 생성 후 previous_year_directory에 weekly_note_year 생성
            elif weekly_note_year == previous_year:
                if not os.path.isdir(previous_year_directory):
                    os.system(f"mkdir \"{previous_year_directory}\"")
                os.system(f"touch \"{previous_year_directory}/{weekly_note}.md\"")
            # weekly_note_year가 다음 연도일 경우 next_year_directory 생성 후 next_year_directory에 weekly_note_year 생성
            elif weekly_note_year == next_year:
                if not os.path.isdir(next_year_directory):
                    os.system(f"mkdir \"{next_year_directory}\"")
                os.system(f"touch \"{next_year_directory}/{weekly_note}.md\"")
            # 예외일 경우 프로그램 종료
            else:
                print("weekly_note 생성 에러")
                exit(0)
            
            for daily_note in date_note_in_year_directory[yearly_note][quarterly_note][monthly_note][weekly_note]:
                ### * daily_note 생성
                os.system(f"touch \"{current_year_directory}/{daily_note}.md\"")

# ^ date_note에 link_table 생성
## * yearly_note
### * yearly_note에 아이콘 추가
insert_icon(f"{current_year_directory}/{yearly_note}.md", "FarCalendar")

### * yearly_note_file_content에 link_table 추가
# yearly_note_file_content
with open(f"{current_year_directory}/{yearly_note}.md", "r") as yearly_note_file:
    yearly_note_file_content = yearly_note_file.readlines(); yearly_note_file_content = "".join(yearly_note_file_content)

# link_table
link_table = "\n\n"

## root_directory_file
root_directory_name = os.path.basename(date_note_directory); root_directory_file = "0 " + root_directory_name
### 1행
link_table += "|"
link_table += " "*10 + f"{root_directory_name}" + " "*11 + "|"
link_table += "\n"
### 2행
link_table += "|"
link_table += " " + "-"*21 + " " + "|"
link_table += "\n"
### 3행
link_table += "|"
link_table += " " + f"[{root_directory_file}](../{root_directory_file.replace(' ', '%20')}.md)" + " " + "|"

link_table += "\n\n"

## previous_yearly_note, next_yearly_note
### 1행
link_table += "|"
link_table += " "*10 + "지난 연도" + " "*11 + "|"
link_table += " "*10 + "다음 연도" + " "*11 + "|"
link_table += "\n"
### 2행
link_table += "|"
link_table += " " + "-"*21 + " " + "|"
link_table += " " + "-"*21 + " " + "|"
link_table += "\n"
### 3행
previous_yearly_note = f"{previous_year}"
next_yearly_note = f"{next_year}"

link_table += "|"
link_table += " " + f"[{previous_yearly_note}](../{previous_year}/{previous_yearly_note}.md)" + " " + "|"
link_table += " " + f"[{next_yearly_note}](../{next_year}/{next_yearly_note}.md)" + " " + "|"

link_table += "\n\n"

## quarterly_note, monthly_note
### 1행
link_table += "|"
link_table += " "*10 + "분기" + " "*11 + "|"
link_table += " "*11 + "월" + " "*11 + "|"
for _ in range(4 - 2):
    link_table += " "*23 + "|"
link_table += "\n"
### 2행
link_table += "|"
for _ in range(4):
    link_table += " " + "-"*21 + " " + "|"
link_table += "\n"
### quarterly_note행
for quarterly_note in date_note_in_year_directory[yearly_note]:
    link_table += "|"
    link_table += " " + f"[{quarterly_note}]({quarterly_note}.md)" + " " + "|"
    for monthly_note in date_note_in_year_directory[yearly_note][quarterly_note]:
        link_table += " " + f"[{monthly_note}]({monthly_note}.md)" + " " + "|"
    link_table += "\n"

link_table += "\n"

# 기존의 link_table 삭제
link_table_pattern = re.compile(r"""
                            (?:
                                # root_folder_file
                                \|(?:[^\|\n]++\|)\n                   ## 1행
                                \|(?:[ ]*+:?+-++:?+[ ]*+\|)\n         ## 2행
                                \|[^\|\n]++\|                         ## 3행
                            |
                                # previous_yearly_note, next_yearly_note
                                \|(?:[^\|\n]++\|){2}\n                ## 1행
                                \|(?:[ ]*+:?+-++:?+[ ]*+\|){2}\n      ## 2행
                                ## 3행
                                \|
                                (?:
                                    [ ]*+
                                    \[
                                    \d\d\d\d ### yearly_note
                                    \]
                                    \(
                                    (?:\.\./\d\d\d\d/)?+ ### year_directory
                                    \d\d\d\d ### yearly_note
                                    \.md
                                    \)
                                    [ ]*+
                                    \|
                                ) {2} # 2열 반복
                            |
                                # quarterly_note, monthly_note
                                \|(?:[^\|\n]++\|){4}\n                ## 1행
                                \|(?:[ ]*+:?+-++:?+[ ]*+\|){4}      ## 2행
                                ## quarterly_note행
                                (?:
                                    \n
                                    \|
                                    (?:
                                        [ ]*+
                                        \[
                                        \d\d\d\d-
                                            (Q[1-4]| ### quarterly_note
                                            0[1-9]|1[0-2]) ### monthly_note
                                        \]
                                        \(
                                        (?:\.\./\d\d\d\d/)?+ ### year_directory
                                        \d\d\d\d-
                                            (Q[1-4]| ### quarterly_note
                                            0[1-9]|1[0-2]) ### monthly_note
                                        \.md
                                        \)
                                        [ ]*+
                                        \|
                                    ) {4} # 4열 반복
                                ) {4} # 4행 반복
                            )
                            """, re.VERBOSE)
link_table_match = link_table_pattern.search(yearly_note_file_content)

while link_table_match != None:
    yearly_note_file_content = yearly_note_file_content[:link_table_match.start(0)] + "\n\n" + yearly_note_file_content[link_table_match.end(0):]
    link_table_match = link_table_pattern.search(yearly_note_file_content)

# yearly_note_file_content에 note_heading에 link_table 추가
yearly_note_file_content = add_to_note_heading(yearly_note_file_content, link_table)

### * 3번 이상 띄어쓰기 한 것 삭제
while re.search(r"\n{3}", yearly_note_file_content) != None:
    yearly_note_file_content = re.sub(r"\n{3}", "\n\n", yearly_note_file_content)

### * yearly_note_file에 yearly_note_file_content 반영
with open(f"{current_year_directory}/{yearly_note}.md", "w") as yearly_note_file:
    yearly_note_file.writelines(yearly_note_file_content)

## * quarterly_note
for quarterly_note in date_note_in_year_directory[yearly_note]:
    ### * quarterly_note에 아이콘 추가
    insert_icon(f"{current_year_directory}/{quarterly_note}.md", "FarCalendar")
    
    ### * quarterly_note_content에 link_table 추가
    # quarterly_note_file_content
    with open(f"{current_year_directory}/{quarterly_note}.md", "r") as quarterly_note_file:
        quarterly_note_file_content = quarterly_note_file.readlines(); quarterly_note_file_content = "".join(quarterly_note_file_content)
    
    # link_table
    ## 각 monthly_note의 weekly_note 개수의 최대 값
    maximum_weekly_note_count = 0
    for monthly_note in date_note_in_year_directory[yearly_note][quarterly_note]:
        if maximum_weekly_note_count < len(date_note_in_year_directory[yearly_note][quarterly_note][monthly_note].keys()):
            maximum_weekly_note_count = len(date_note_in_year_directory[yearly_note][quarterly_note][monthly_note].keys())
    ## maximum_column_count_for_monthly_row
    maximum_column_count_for_monthly_row = 1 + maximum_weekly_note_count
    
    link_table = "\n\n"
    
    ## this_yearly_note
    ### 1행
    link_table += "|"
    link_table += " "*9 + "이번 연도" + " "*9 + "|"
    link_table += "\n"
    ### 2행
    link_table += "|"
    link_table += " " + "-"*21 + " " + "|"
    link_table += "\n"
    ### 3행
    link_table += "|"
    link_table += " " + f"[{yearly_note}]({yearly_note}.md)" + " " + "|"
    
    link_table += "\n\n"
    
    ## previous_quarterly_note, next_quarterly_note
    ### 1행
    link_table += "|"
    link_table += " "*9 + "지난 분기" + " "*9 + "|"
    link_table += " "*9 + "다음 분기" + " "*9 + "|"
    link_table += "\n"
    ### 2행
    link_table += "|"
    link_table += " " + "-"*21 + " " + "|"
    link_table += " " + "-"*21 + " " + "|"
    link_table += "\n"
    ### 3행
    quarterly_note_year = int(quarterly_note[0:4]); quarterly_note_quarter = int(quarterly_note[-1])
    
    previous_quarterly_note_year = quarterly_note_year; previous_quarterly_note_quarter = quarterly_note_quarter - 1
    if previous_quarterly_note_quarter == 0:
        previous_quarterly_note_quarter = 4
        previous_quarterly_note_year -= 1
    previous_quarterly_note = f"{previous_quarterly_note_year}-Q{previous_quarterly_note_quarter}"
    
    next_quarterly_note_year = quarterly_note_year; next_quarterly_note_quarter = quarterly_note_quarter + 1
    if next_quarterly_note_quarter == 5:
        next_quarterly_note_quarter = 1
        next_quarterly_note_year += 1
    next_quarterly_note = f"{next_quarterly_note_year}-Q{next_quarterly_note_quarter}"
    
    link_table += "|"
    if previous_quarterly_note_year != quarterly_note_year:
        link_table += " " + f"[{previous_quarterly_note}](../{previous_quarterly_note_year}/{previous_quarterly_note}.md)" + " " + "|"
    else:
        link_table += " " + f"[{previous_quarterly_note}]({previous_quarterly_note}.md)" + " " + "|"
    if next_quarterly_note_year != quarterly_note_year:
        link_table += " " + f"[{next_quarterly_note}](../{next_quarterly_note_year}/{next_quarterly_note}.md)" + " " + "|"
    else:
        link_table += " " + f"[{next_quarterly_note}]({next_quarterly_note}.md)" + " " + "|"
    
    link_table += "\n\n"
    
    ## monthly_note, weekly_note
    ### 1행
    link_table += "|"
    link_table += " "*11 + "월" + " "*11 + "|"
    link_table += " "*11 + "주" + " "*11 + "|"
    for _ in range(maximum_column_count_for_monthly_row - 2):
        link_table += " "*23 + "|"
    link_table += "\n"
    ### 2행
    link_table += "|"
    for _ in range(maximum_column_count_for_monthly_row):
        link_table += " " + "-"*21 + " " + "|"
    link_table += "\n"
    ### monthly_note행
    for monthly_note in date_note_in_year_directory[yearly_note][quarterly_note]:
        link_table += "|"
        link_table += " " + f"[{monthly_note}]({monthly_note}.md)" + " " + "|"
        
        current_weekly_note_count = 0
        for weekly_note in date_note_in_year_directory[yearly_note][quarterly_note][monthly_note]:
            weekly_note_year = int(weekly_note[0:4])
            if weekly_note_year == previous_year:
                link_table += " " + f"[{weekly_note}](../{previous_year}/{weekly_note}.md)" + " " + "|"
            elif weekly_note_year == current_year:
                link_table += " " + f"[{weekly_note}]({weekly_note}.md)" + " " + "|"
            elif weekly_note_year == next_year:
                link_table += " " + f"[{weekly_note}](../{next_year}/{weekly_note}.md)" + " " + "|"
            else:
                pass
            current_weekly_note_count += 1
        
        ### empty_cell 개수만큼 빈 셀 만들기
        empty_cell_count = maximum_column_count_for_monthly_row - current_weekly_note_count - 1
        for _ in range(empty_cell_count):
            link_table += " "*23 + "|"

        link_table += "\n"
    
    link_table += "\n"
    
    # 기존의 link_table 삭제
    link_table_pattern = re.compile(r"""
                                (?:
                                    # this_yearly_note
                                    \|(?:[^\|\n]++\|)\n                              ## 1행
                                    \|(?:[ ]*+:?+-++:?+[ ]*+\|)\n                    ## 2행
                                    ## 3행
                                    \|
                                    [ ]*+
                                    \[
                                    \d\d\d\d ### yearly_note
                                    \]
                                    \(
                                    (?:\.\./\d\d\d\d/)?+ ### year_directory
                                    \d\d\d\d ### yearly_note
                                    \.md
                                    \)
                                    [ ]*+
                                    \|
                                |
                                    # previous_quarterly_note, next_quarterly_note
                                    \|(?:[^\|\n]++\|){2}\n                          ## 1행
                                    \|(?:[ ]*+:?+-++:?+[ ]*+\|){2}\n                ## 2행
                                    ## 3행
                                    \|
                                    (?:
                                        [ ]*+
                                        \[
                                        \d\d\d\d-Q[1-4] ### quarterly_note
                                        \]
                                        \(
                                        (?:\.\./\d\d\d\d/)?+ ### year_directory
                                        \d\d\d\d-Q[1-4] ### quarterly_note
                                        \.md
                                        \)
                                        [ ]*+
                                        \|
                                    ) {2} # 2열 반복
                                |
                                    # monthly_note, weekly_note
                                    \|(?:[^\|\n]++\|){4,}\n                ## 1행
                                    \|(?:[ ]*+:?+-++:?+[ ]*+\|){4,}        ## 2행
                                    ## monthly_note행
                                    (?:
                                        \n
                                        \|
                                        (?:
                                            [ ]*+
                                            \[
                                            \d\d\d\d-
                                                (0[1-9]|1[0-2]| ### monthly_note
                                                W5[0-3]|W[1-4][0-9]|W0[1-9]) ### weekly_note
                                            \]
                                            \(
                                            (?:\.\./\d\d\d\d/)?+ ### year_directory
                                            \d\d\d\d-
                                                (0[1-9]|1[0-2]| ### monthly_note
                                                W5[0-3]|W[1-4][0-9]|W0[1-9]) ### weekly_note
                                            \.md
                                            \)
                                            [ ]*+
                                            \|
                                            |
                                            [^\|\n]++
                                            \|
                                        ) {4,} # 4열 이상 반복
                                    ) {3} # 3행 반복
                                )
                                """, re.VERBOSE)
    link_table_match = link_table_pattern.search(quarterly_note_file_content)

    while link_table_match != None:
        quarterly_note_file_content = quarterly_note_file_content[:link_table_match.start(0)] + "\n\n" + quarterly_note_file_content[link_table_match.end(0):]
        link_table_match = link_table_pattern.search(quarterly_note_file_content)
    
    # quarterly_note_file_content에 note_heading에 link_table 추가
    quarterly_note_file_content = add_to_note_heading(quarterly_note_file_content, link_table)

    ### * 3번 이상 띄어쓰기 한 것 삭제
    while re.search(r"\n{3}", quarterly_note_file_content) != None:
        quarterly_note_file_content = re.sub(r"\n{3}", "\n\n", quarterly_note_file_content)

    ### * quarterly_note_file에 quarterly_note_file_content 반영
    with open(f"{current_year_directory}/{quarterly_note}.md", "w") as quarterly_note_file:
        quarterly_note_file.writelines(quarterly_note_file_content)

## * monthly_note
for quarterly_note in date_note_in_year_directory[yearly_note]:
    for monthly_note in date_note_in_year_directory[yearly_note][quarterly_note]:
        ### * monthly_note에 아이콘 추가
        insert_icon(f"{current_year_directory}/{monthly_note}.md", "FarCalendar")
        
        ### * monthly_note_content에 link_table 추가
        # monthly_note_content
        with open(f"{current_year_directory}/{monthly_note}.md", "r") as monthly_note_file:
            monthly_note_file_content = monthly_note_file.readlines(); monthly_note_file_content = "".join(monthly_note_file_content)
        
        # link_table
        link_table = "\n\n"
        
        ## this_quarterly_note
        ### 1행
        link_table += "|"
        link_table += " "*9 + "이번 분기" + " "*9 + "|"
        link_table += "\n"
        ### 2행
        link_table += "|"
        link_table += " " + "-"*21 + " " + "|"
        link_table += "\n"
        ### 3행
        link_table += "|"
        link_table += " " + f"[{quarterly_note}]({quarterly_note}.md)" + " " + "|"
        
        link_table += "\n\n"
        
        ## previous_monthly_note, next_monthly_note
        ### 1행
        link_table += "|"
        link_table += " "*9 + "지난 달" + " "*10 + "|"
        link_table += " "*9 + "다음 달" + " "*10 + "|"
        link_table += "\n"
        ### 2행
        link_table += "|"
        link_table += " " + "-"*21 + " " + "|"
        link_table += " " + "-"*21 + " " + "|"
        link_table += "\n"
        ### 3행
        monthly_note_year = int(monthly_note[0:4]); monthly_note_month = int(monthly_note[-2:])
        
        previous_monthly_note_year = monthly_note_year; previous_monthly_note_month = monthly_note_month - 1
        if previous_monthly_note_month == 0:
            previous_monthly_note_month = 12
            previous_monthly_note_year -= 1
        previous_monthly_note = f"{previous_monthly_note_year}-{str(previous_monthly_note_month).zfill(2)}"
        
        next_monthly_note_year = monthly_note_year; next_monthly_note_month = monthly_note_month + 1
        if next_monthly_note_month == 13:
            next_monthly_note_month = 1
            next_monthly_note_year += 1
        next_monthly_note = f"{next_monthly_note_year}-{str(next_monthly_note_month).zfill(2)}"
        
        link_table += "|"
        if previous_monthly_note_year != monthly_note_year:
            link_table += " " + f"[{previous_monthly_note}](../{previous_monthly_note_year}/{previous_monthly_note}.md)" + " " + "|"
        else:
            link_table += " " + f"[{previous_monthly_note}]({previous_monthly_note}.md)" + " " + "|"
        if next_monthly_note_year != monthly_note_year:
            link_table += " " + f"[{next_monthly_note}](../{next_monthly_note_year}/{next_monthly_note}.md)" + " " + "|"
        else:
            link_table += " " + f"[{next_monthly_note}]({next_monthly_note}.md)" + " " + "|"
        
        link_table += "\n\n"
        
        ## weekly_note, daily_note
        ### 1행
        link_table += "|"
        link_table += " "*11 + "주" + " "*11 + "|"
        weekdays = ["월", "화", "수", "목", "금", "토", "일"]
        for weekday in weekdays:
            link_table += " "*11 + weekday + " "*11 + "|"
        link_table += "\n"
        ### 2행
        link_table += "|"
        for _ in range(8):
            link_table += " " + "-"*21 + " " + "|"
        link_table += "\n"
        ### weekly_note행
        for i, weekly_note in enumerate(date_note_in_year_directory[yearly_note][quarterly_note][monthly_note]):
            link_table += "|"
            
            weekly_note_year = int(weekly_note[0:4])
            if weekly_note_year == previous_year:
                link_table += " " + f"[{weekly_note}](../{previous_year}/{weekly_note}.md)" + " " + "|"
            elif weekly_note_year == current_year:
                link_table += " " + f"[{weekly_note}]({weekly_note}.md)" + " " + "|"
            elif weekly_note_year == next_year:
                link_table += " " + f"[{weekly_note}](../{next_year}/{weekly_note}.md)" + " " + "|"
            else:
                pass
            
            if i == 0:
                current_daily_note_count = 0
                for daily_note in date_note_in_year_directory[yearly_note][quarterly_note][monthly_note][weekly_note]:
                    current_daily_note_count += 1
                
                empty_cell_count = 7 - current_daily_note_count
                
                for _ in range(empty_cell_count):
                    link_table += " "*23 + "|"
                
                for daily_note in date_note_in_year_directory[yearly_note][quarterly_note][monthly_note][weekly_note]:
                    link_table += " " + f"[{daily_note}]({daily_note}.md)" + " " + "|"
                
                link_table += "\n"
                
            else:
                current_daily_note_count = 0
                for daily_note in date_note_in_year_directory[yearly_note][quarterly_note][monthly_note][weekly_note]:
                    link_table += " " + f"[{daily_note}]({daily_note}.md)" + " " + "|"
                    current_daily_note_count += 1
                
                empty_cell_count = 7 - current_daily_note_count
                for _ in range(empty_cell_count):
                    link_table += " "*23 + "|"
                
                link_table += "\n"
        
        link_table += "\n"
        
        # 기존의 link_table 삭제
        link_table_pattern = re.compile(r"""
                                    (?:
                                        # this_quarterly_note
                                        \|(?:[^\|\n]++\|)\n                              ## 1행
                                        \|(?:[ ]*+:?+-++:?+[ ]*+\|)\n                    ## 2행
                                        ## 3행
                                        \|
                                        [ ]*+
                                        \[
                                        \d\d\d\d-Q[1-4] ### quarterly_note
                                        \]
                                        \(
                                        (?:\.\./\d\d\d\d/)?+ ### year_directory
                                        \d\d\d\d-Q[1-4] ### quarterly_note
                                        \.md
                                        \)
                                        [ ]*+
                                        \|
                                    |
                                        # previous_monthly_note, next_monthly_note
                                        \|(?:[^\|\n]++\|){2}\n                          ## 1행
                                        \|(?:[ ]*+:?+-++:?+[ ]*+\|){2}\n                ## 2행
                                        ## 3행
                                        \|
                                        (?:
                                            [ ]*+
                                            \[
                                            \d\d\d\d-(?:0[1-9]|1[0-2]) ### monthly_note
                                            \]
                                            \(
                                            (?:\.\./\d\d\d\d/)?+ ### year_directory
                                            \d\d\d\d-(?:0[1-9]|1[0-2]) ### monthly_note
                                            \.md
                                            \)
                                            [ ]*+
                                            \|
                                        ) {2} # 2열 반복
                                    |
                                        # weekly_note, daily_note
                                        \|(?:[^\|\n]++\|){8}\n                          ## 1행
                                        \|(?:[ ]*+:?+-++:?+[ ]*+\|){8}                  ## 2행
                                        ## weekly_note행
                                        (?:
                                            \n
                                            \|
                                            (?:
                                                [ ]*+
                                                \[
                                                \d\d\d\d-
                                                    (W5[0-3]|W[1-4][0-9]|W0[1-9]| ### weekly_note
                                                    ((0[1-9]|1[0-2])-(0[1-9]|1[0-9]|2[0-9]|3[0-1]))) ### daily_note
                                                \]
                                                \(
                                                (?:\.\./\d\d\d\d/)?+ ### year_directory
                                                \d\d\d\d-
                                                    (W5[0-3]|W[1-4][0-9]|W0[1-9]| ### weekly_note
                                                    ((0[1-9]|1[0-2])-(0[1-9]|1[0-9]|2[0-9]|3[0-1]))) ### daily_note
                                                \.md
                                                \)
                                                [ ]*+
                                                \|
                                                |
                                                [ ]*+ ### empty_cell
                                                \|
                                            ) {8} # 8열 반복
                                        ) {4,} # 4행 이상 반복
                                    )
                                    """, re.VERBOSE)
        link_table_match = link_table_pattern.search(monthly_note_file_content)
        
        while link_table_match != None:
            monthly_note_file_content = monthly_note_file_content[:link_table_match.start(0)] + "\n\n" + monthly_note_file_content[link_table_match.end(0):]
            link_table_match = link_table_pattern.search(monthly_note_file_content)
        
        # monthly_note_file_content note_heading에 link_table 추가
        monthly_note_file_content = add_to_note_heading(monthly_note_file_content, link_table)
        
        ### * 3번 이상 띄어쓰기 한 것 삭제
        while re.search(r"\n{3}", monthly_note_file_content) != None:
            monthly_note_file_content = re.sub(r"\n{3}", "\n\n", monthly_note_file_content)

        ### * monthly_note_file에 monthly_note_file_content 반영
        with open(f"{current_year_directory}/{monthly_note}.md", "w") as monthly_note_file:
            monthly_note_file.writelines(monthly_note_file_content)

## * weekly_note
for quarterly_note in date_note_in_year_directory[yearly_note]:
    for monthly_note in date_note_in_year_directory[yearly_note][quarterly_note]:
        for weekly_note in date_note_in_year_directory[yearly_note][quarterly_note][monthly_note]:
            # weekly_note_year_directory
            weekly_note_year = int(weekly_note[0:4])
            if weekly_note_year == previous_year:
                weekly_note_year_directory = previous_year_directory
            elif weekly_note_year == current_year:
                weekly_note_year_directory = current_year_directory
            elif weekly_note_year == next_year:
                weekly_note_year_directory = next_year_directory
            else:
                pass
            
            ### * weekly_note 아이콘 추가
            insert_icon(f"{weekly_note_year_directory}/{weekly_note}.md", "FarCalendar")
            
            ### * weekly_note_content에 link_table 추가
            # weekly_note_content
            with open(f"{weekly_note_year_directory}/{weekly_note}.md", "r") as weekly_note_file:
                weekly_note_file_content = weekly_note_file.readlines(); weekly_note_file_content = "".join(weekly_note_file_content)
            
            # link_table            
            one_daily_note = list(date_note_in_year_directory[yearly_note][quarterly_note][monthly_note][weekly_note].keys())[0]
            one_daily_note_year = int(one_daily_note[0:4]); one_daily_note_month = int(one_daily_note[5:7]); one_daily_note_day = int(one_daily_note[8:10])
            one_daily_note_date = dt.datetime(one_daily_note_year, one_daily_note_month, one_daily_note_day)
            
            link_table = "\n\n"
            
            ## this_monthly_note
            one_daily_note_isocalendar_date = one_daily_note_date.isocalendar(); one_daily_note_weekday = one_daily_note_isocalendar_date[2]
            
            leftmost_daily_note_date = one_daily_note_date + dt.timedelta(days = -one_daily_note_weekday + 1); leftmost_daily_note_monthly_note = f"{leftmost_daily_note_date.year}-{str(leftmost_daily_note_date.month).zfill(2)}"; rightmost_daily_note_date = one_daily_note_date + dt.timedelta(days = 7 - one_daily_note_weekday); rightmost_daily_note_monthly_note = f"{rightmost_daily_note_date.year}-{str(rightmost_daily_note_date.month).zfill(2)}"
            
            this_monthly_note_set = set([leftmost_daily_note_monthly_note, rightmost_daily_note_monthly_note])
            
            ### 1행
            link_table += "|"
            link_table += " "*9 + "이번 달" + " "*10 + "|"
            if len(this_monthly_note_set) == 2:
                link_table += " "*23 + "|"
            link_table += "\n"
            ### 2행
            link_table += "|"
            link_table += " " + "-"*21 + " " + "|"
            if len(this_monthly_note_set) == 2:
                link_table += " " + "-"*21 + " " + "|"
            link_table += "\n"
            ### 3행
            link_table += "|"
            this_monthly_note_list = sorted(list(this_monthly_note_set))
            for this_monthly_note in this_monthly_note_list:
                this_monthly_note_year = int(this_monthly_note[0:4])
                if this_monthly_note_year != weekly_note_year:
                    link_table += " " + f"[{this_monthly_note}](../{this_monthly_note_year}/{this_monthly_note}.md)" + " " + "|"
                else:
                    link_table += " " + f"[{this_monthly_note}]({this_monthly_note}.md)" + " " + "|"
            
            link_table += "\n\n"
            
            ## previous_weekly_note, next_weekly_note
            ### 1행
            link_table += "|"
            link_table += " "*9 + "지난 주" + " "*10 + "|"
            link_table += " "*9 + "다음 주" + " "*10 + "|"
            link_table += "\n"
            ### 2행
            link_table += "|"
            link_table += " " + "-"*21 + " " + "|"
            link_table += " " + "-"*21 + " " + "|"
            link_table += "\n"
            ### 3행
            before_a_week_one_daily_note_date = one_daily_note_date + dt.timedelta(weeks = -1); before_a_week_one_daily_note_isocalendar_date = before_a_week_one_daily_note_date.isocalendar()
            previous_weekly_note_year = before_a_week_one_daily_note_isocalendar_date[0]; previous_weekly_note_week = before_a_week_one_daily_note_isocalendar_date[1]; previous_weekly_note = f"{previous_weekly_note_year}-W{str(previous_weekly_note_week).zfill(2)}"
            after_a_week_one_daily_note_date = one_daily_note_date + dt.timedelta(weeks = +1); after_a_week_one_daily_note_isocalendar_date = after_a_week_one_daily_note_date.isocalendar()
            next_weekly_note_year = after_a_week_one_daily_note_isocalendar_date[0]; next_weekly_note_week = after_a_week_one_daily_note_isocalendar_date[1]
            next_weekly_note = f"{next_weekly_note_year}-W{str(next_weekly_note_week).zfill(2)}"
            
            link_table += "|"
            if previous_weekly_note_year != weekly_note_year:
                link_table += " " + f"[{previous_weekly_note}](../{previous_weekly_note_year}/{previous_weekly_note}.md)" + " " + "|"
            else:
                link_table += " " + f"[{previous_weekly_note}]({previous_weekly_note}.md)" + " " + "|"
            if next_weekly_note_year != weekly_note_year:
                link_table += " " + f"[{next_weekly_note}](../{next_weekly_note_year}/{next_weekly_note}.md)" + " " + "|"
            else:
                link_table += " " + f"[{next_weekly_note}]({next_weekly_note}.md)" + " " + "|"
            
            link_table += "\n\n"
            
            ## daily_note
            ### 1행
            link_table += "|"
            weekdays = ["월", "화", "수", "목", "금", "토", "일"]
            for weekday in weekdays:
                link_table += " "*11 + weekday + " "*11 + "|"
            link_table += "\n"
            ### 2행
            link_table += "|"
            for _ in range(7):
                link_table += " " + "-"*21 + " " + "|"
            link_table += "\n"
            ### 3행
            link_table += "|"
            
            one_daily_note = list(date_note_in_year_directory[yearly_note][quarterly_note][monthly_note][weekly_note].keys())[0]
            one_daily_note_year = int(one_daily_note[0:4]); one_daily_note_month = int(one_daily_note[5:7]); one_daily_note_day = int(one_daily_note[8:10])
            one_daily_note_date = dt.datetime(one_daily_note_year, one_daily_note_month, one_daily_note_day); one_daily_note_isocalendar_date = one_daily_note_date.isocalendar(); one_daily_note_weekday =  one_daily_note_isocalendar_date[2]
            
            daily_note_count = one_daily_note_weekday - 1; daily_note_date = one_daily_note_date; daily_note_date += dt.timedelta(days = -daily_note_count - 1)
            
            for _ in range(7):
                daily_note_date += dt.timedelta(days = +1); daily_note = str(daily_note_date)[0:10]; daily_note_year = int(daily_note[0:4])
                if daily_note_year != weekly_note_year:
                    link_table += " " + f"[{daily_note}](../{daily_note_year}/{daily_note}.md)" + " " + "|"
                else:
                    link_table += " " + f"[{daily_note}]({daily_note}.md)" + " " + "|"
            
            link_table += "\n\n"
            
            # 기존의 link_table 삭제
            link_table_pattern = re.compile(r"""
                                        (?:
                                            # this_monthly_note
                                            \|(?:[^\|\n]++\|){1,2}\n                    ## 1행
                                            \|(?:[ ]*+:?+-++:?+[ ]*+\|){1,2}\n          ## 2행
                                            ## 3행
                                            \|
                                            (?:
                                                [ ]*+
                                                \[
                                                \d\d\d\d-(0[1-9]|1[0-2]) ### monthly_note
                                                \]
                                                \(
                                                (?:\.\./\d\d\d\d/)?+ ### year_directory
                                                \d\d\d\d-(0[1-9]|1[0-2]) ### monthly_note
                                                \.md
                                                \)
                                                [ ]*+
                                                \|
                                            ){1,2}  # 1~2열 반복
                                        |
                                            # previous_weekly_note, next_weekly_note
                                            \|(?:[^\|\n]++\|){2}\n                        ## 1행
                                            \|(?:[ ]*+:?+-++:?+[ ]*+\|){2}\n              ## 2행
                                            ## 3행
                                            \|
                                            (?:
                                                [ ]*+
                                                \[
                                                \d\d\d\d-W(?:0[1-9]|[1-4][0-9]|5[0-3]) ### weekly_note
                                                \]
                                                \(
                                                (?:\.\./\d\d\d\d/)?+ ### year_directory
                                                \d\d\d\d-W(?:0[1-9]|[1-4][0-9]|5[0-3]) ### weekly_note
                                                \.md
                                                \)
                                                [ ]*+
                                                \|
                                            ) {2} # 2열 반복
                                        |
                                            # daily_note
                                            \|(?:[^\|\n]++\|){7}\n                      ## 1행
                                            \|(?:[ ]*+:?+-++:?+[ ]*+\|){7}\n            ## 2행
                                            ## 3행
                                            \|
                                            (?:
                                                [ ]*+
                                                \[
                                                \d\d\d\d-(?:0[1-9]|1[0-2])-(?:0[1-9]|1[0-9]|2[0-9]|3[0-1]) ### daily_note
                                                \]
                                                \(
                                                (?:\.\./\d\d\d\d/)?+ ### year_directory
                                                \d\d\d\d-(?:0[1-9]|1[0-2])-(?:0[1-9]|1[0-9]|2[0-9]|3[0-1]) ### daily_note
                                                \.md
                                                \)
                                                [ ]*+
                                                \|
                                            ) {7} # 7열 반복
                                        )
                                        """, re.VERBOSE)
            link_table_match = link_table_pattern.search(weekly_note_file_content)

            while link_table_match != None:
                weekly_note_file_content = weekly_note_file_content[:link_table_match.start(0)] + "\n\n" + weekly_note_file_content[link_table_match.end(0):]
                link_table_match = link_table_pattern.search(weekly_note_file_content)
    
            # weekly_note_file_content note_heading에 link_table 추가
            weekly_note_file_content = add_to_note_heading(weekly_note_file_content, link_table)

            ### * 3번 이상 띄어쓰기 한 것 삭제
            while re.search(r"\n{3}", weekly_note_file_content) != None:
                weekly_note_file_content = re.sub(r"\n{3}", "\n\n", weekly_note_file_content)

            # ### * weekly_note_file에 weekly_note_file_content 반영
            with open(f"{weekly_note_year_directory}/{weekly_note}.md", "w") as weekly_note_file:
                weekly_note_file.writelines(weekly_note_file_content)

## * daily_note
for quarterly_note in date_note_in_year_directory[yearly_note]:
    for monthly_note in date_note_in_year_directory[yearly_note][quarterly_note]:
        for weekly_note in date_note_in_year_directory[yearly_note][quarterly_note][monthly_note]:            
            one_daily_note = list(date_note_in_year_directory[yearly_note][quarterly_note][monthly_note][weekly_note].keys())[0]
            one_daily_note_year = int(one_daily_note[0:4]); one_daily_note_month = int(one_daily_note[5:7]); one_daily_note_day = int(one_daily_note[8:10])
            one_daily_note_date = dt.datetime(one_daily_note_year, one_daily_note_month, one_daily_note_day); one_daily_note_isocalendar_date = one_daily_note_date.isocalendar()
            one_daily_note_weekday = one_daily_note_isocalendar_date[2]
            
            daily_note_count = one_daily_note_weekday - 1; daily_note_date = one_daily_note_date; daily_note_date += dt.timedelta(days = -daily_note_count - 1)
            
            for _ in range(7):
                daily_note_date += dt.timedelta(days = +1); daily_note = str(daily_note_date)[0:10]
                
                ## daily_note_year_directory
                daily_note_year = int(daily_note[0:4])
                if daily_note_year == previous_year:
                    daily_note_year_directory = previous_year_directory
                elif daily_note_year == current_year:
                    daily_note_year_directory = current_year_directory
                elif daily_note_year == next_year:
                    daily_note_year_directory = next_year_directory
                else:
                    pass
                
                #### * daily_note 생성
                if not os.path.isdir(daily_note_year_directory):
                    os.system(f"mkdir \"{daily_note_year_directory}\"")

                os.system(f"touch \"{daily_note_year_directory}/{daily_note}.md\"")
                
                #### * daily_note에 아이콘 생성
                insert_icon(f"{daily_note_year_directory}/{daily_note}.md", "FarCalendar")
                
                #### * daily_note에 link_table 추가
                with open(f"{daily_note_year_directory}/{daily_note}.md", "r") as daily_note_file:
                    daily_note_file_content = daily_note_file.readlines(); daily_note_file_content = "".join(daily_note_file_content)
                
                # link_table
                link_table = "\n\n"
                
                ## this_weekly_note
                ### 1행
                link_table += "|"
                link_table += " "*9 + "이번 주" + " "*10 + "|"
                link_table += "\n"
                ### 2행
                link_table += "|"
                link_table += " " + "-"*21 + " " + "|"
                link_table += "\n"
                ### 3행
                link_table += "|"
                this_weekly_note = weekly_note
                this_weekly_note_year = int(this_weekly_note[0:4])
                if this_weekly_note_year != daily_note_year:
                    link_table += " " + f"[{this_weekly_note}](../{this_weekly_note_year}/{this_weekly_note}.md)" + " " + "|"
                else:
                    link_table += " " + f"[{this_weekly_note}]({this_weekly_note}.md)" + " " + "|"
                
                link_table += "\n\n"
                
                ## previous_daily_note, next_daily_note
                ### 1행
                link_table += "|"
                link_table += " "*10 + "전 날" + " "*10 + "|"
                link_table += " "*9 + "다음 날" + " "*10 + "|"
                link_table += "\n"
                ### 2행
                link_table += "|"
                link_table += " " + "-"*21 + " " + "|"
                link_table += " " + "-"*21 + " " + "|"
                link_table += "\n"
                ### 3행
                previous_daily_note_date = daily_note_date + dt.timedelta(days = -1); previous_daily_note = str(previous_daily_note_date)[0:10]; previous_daily_note_year = int(previous_daily_note[0:4]); next_daily_note_date = daily_note_date + dt.timedelta(days = +1); next_daily_note = str(next_daily_note_date)[0:10]; next_daily_note_year = int(next_daily_note[0:4])
                
                link_table += "|"
                if previous_daily_note_year != daily_note_year:
                    link_table += " " + f"[{previous_daily_note}](../{previous_daily_note_year}/{previous_daily_note}.md)" + " " + "|"
                else:
                    link_table += " " + f"[{previous_daily_note}]({previous_daily_note}.md)" + " " + "|"
                if next_daily_note_year != daily_note_year:
                    link_table += " " + f"[{next_daily_note}](../{next_daily_note_year}/{next_daily_note}.md)" + " " + "|"
                else:
                    link_table += " " + f"[{next_daily_note}]({next_daily_note}.md)" + " " + "|"
                
                link_table += "\n\n"
                
                # 기존의 link_table 삭제
                link_table_pattern = re.compile(r"""
                                            (?:
                                                # this_weekly_note
                                                \|(?:[^\|\n]++\|)\n                     ## 1행
                                                \|(?:[ ]*+:?+-++:?+[ ]*+\|)\n           ## 2행
                                                ## 3행
                                                \|
                                                [ ]*+
                                                \[
                                                \d\d\d\d-W(?:0[1-9]|[1-4][0-9]|5[0-3]) ### weekly_note
                                                \]
                                                \(
                                                (?:\.\./\d\d\d\d/)?+ ### year_directory
                                                \d\d\d\d-W(?:0[1-9]|[1-4][0-9]|5[0-3]) ### weekly_note
                                                \.md
                                                \)
                                                [ ]*+
                                                \|
                                            |
                                                # previous_daily_note, next_daily_note
                                                \|(?:[^\|\n]++\|){2}\n                  ## 1행
                                                \|(?:[ ]*+:?+-++:?+[ ]*+\|){2}\n        ## 2행
                                                ## 3행
                                                \|
                                                (?:
                                                    [ ]*+
                                                    \[
                                                    \d\d\d\d-(?:0[1-9]|1[0-2])-(?:0[1-9]|1[0-9]|2[0-9]|3[0-1]) ### daily_note
                                                    \]
                                                    \(
                                                    (?:\.\./\d\d\d\d/)?+ ### year_directory
                                                    \d\d\d\d-(?:0[1-9]|1[0-2])-(?:0[1-9]|1[0-9]|2[0-9]|3[0-1]) ### daily_note
                                                    \.md
                                                    \)
                                                    [ ]*+
                                                    \|
                                                ) {2} # 2열 반복
                                            )
                                            """, re.VERBOSE)
                link_table_match = link_table_pattern.search(daily_note_file_content)
                
                while link_table_match != None:
                    daily_note_file_content = daily_note_file_content[:link_table_match.start(0)] + "\n\n" + daily_note_file_content[link_table_match.end(0):]
                    link_table_match = link_table_pattern.search(daily_note_file_content)
                daily_note_file_content = add_to_note_heading(daily_note_file_content, link_table)
                
                #### * 3번 이상 띄어쓰기 한 것 삭제
                while re.search(r"\n{3}", daily_note_file_content) != None:
                    daily_note_file_content = re.sub(r"\n{3}", "\n\n", daily_note_file_content)
                
                #### * daily_note_file에 daily_note_file_content 반영
                with open(f"{daily_note_year_directory}/{daily_note}.md", "w") as daily_note_file:
                    daily_note_file.writelines(daily_note_file_content)
            