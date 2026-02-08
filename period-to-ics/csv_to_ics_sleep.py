import os
import datetime
import math

# TODO 1일에 가까운 기간을 가진 캘린더들 없애기

# * csv_file 내용을 배열로 불러오기
# csv_file 경로
csv_file_path = "/Users/isgeun/Library/Mobile Documents/iCloud~md~obsidian/Documents/NOTE-iCloud_Drive/0 Inbox/HKCategoryTypeIdentifierSleepAnalysis_2024-01-02_09-02-48_SimpleHealthExportCSV.csv"
# csv_file 디렉토리
csv_file_directory = os.path.dirname(csv_file_path)
# csv_file 파일 이름
CSV_FILE_EXTENSION_LENGTH = 4
csv_file_name  = os.path.basename(csv_file_path)[:-CSV_FILE_EXTENSION_LENGTH]
# csv_file 내용
csv_file_content = None
with open(f"{csv_file_path}", "r") as f:
    csv_file_content = f.readlines(); csv_file_content.pop(0)

# * source_name, start_date, end_date, sleep_type의 index 설정
NOT_FOUND = -1
source_name_index = NOT_FOUND
start_date_index = NOT_FOUND
end_date_index = NOT_FOUND
sleep_type_index = NOT_FOUND
# sleep_attributes
sleep_attributes = csv_file_content.pop(0); sleep_attributes = sleep_attributes.split(",")
for sleep_attribute_index, sleep_attribute in enumerate(sleep_attributes):
    if sleep_attribute == "sourceName":
        source_name_index = sleep_attribute_index
    elif sleep_attribute == "startDate":
        start_date_index = sleep_attribute_index
    elif sleep_attribute == "endDate":
        end_date_index = sleep_attribute_index
    elif sleep_attribute == "value":
        sleep_type_index = sleep_attribute_index
    else:
        pass

def convert_csv_date(utc):
    '''
    # * YYYY-MM-DD hh:mm:ss \+\d\d\d\d 형태로 된 데이터에서 연, 월, 일, 시, 분, 초 데이터를 뽑아 이를 이용해 datetime.datetime 변수를 만들어 반환한다.
    '''
    year = int(utc[0:4]); month = int(utc[5:7]); day = int(utc[8:10]); hour = int(utc[11:13]); minute = int(utc[14:16]); second = int(utc[17:19])
    return datetime.datetime(year, month, day, hour, minute, second)

def get_sleep_attribute_value(file_line, sleep_attribute_index):
    '''
    # * 파일의 한 라인(file_line)에서 인덱스(sleep_attribute_index)에 해당하는 sleep_attribute_value 값을 반환한다.
    '''
    sleep_attribute_values = (file_line.split(','))
    current_index = 0 
    while 0 <= current_index <= len(sleep_attribute_values)-1:
        # 첫 번째 쌍따옴표를 발견하지 못했다면 다음 current_sleep_attribute_value 탐색
        first_double_quote_index = NOT_FOUND
        first_double_quote_index = sleep_attribute_values[current_index].find("\"")
        if first_double_quote_index == NOT_FOUND:
            current_index += 1
            continue
        
        # 두 번째 쌍따옴표를 발견하지 못했다면 현재 current_sleep_attribute_value에 "," + 다음 current_sleep_attribute_value를 추가
        second_double_quote_index = NOT_FOUND
        second_double_quote_index = sleep_attribute_values[current_index].find("\"", first_double_quote_index+1)
        while second_double_quote_index == NOT_FOUND:
            sleep_attribute_values[current_index] = sleep_attribute_values[current_index] + "," + sleep_attribute_values[current_index+1]
            sleep_attribute_values.pop(current_index+1)
            
            second_double_quote_index = sleep_attribute_values[current_index].find("\"", first_double_quote_index+1)
        
        current_index += 1
    return sleep_attribute_values[sleep_attribute_index]

def find_sleep_attribute_values(content, search_index, source_name_, sleep_type_):
    # * search_index 인덱스가 범위를 벗어난다면 None 반환
    if not(0 <= search_index and search_index <= len(content)-1):
        return None
    
    # * content에서 index위치부터 시작해 source_name이 [source_name_]을 포함하고 sleep_type이 [sleep_type]인 content_line을 찾을 때까지 반복, 찾았다면 반복문 탈출
    for offset, content_line in enumerate(content[search_index:]):
        # source_name
        source_name = get_sleep_attribute_value(content_line, source_name_index)
        source_name_is_valid = (source_name.find(source_name_) >= 0)
        # sleep_type
        sleep_type = get_sleep_attribute_value(content_line, sleep_type_index)
        sleep_type_is_valid = (sleep_type == sleep_type_)
        # content_line_is_valid
        content_line_is_valid = source_name_is_valid and sleep_type_is_valid
        
        if content_line_is_valid:
            break
        
    # * 위의 content_line을 찾았다면 sleep_attribute_values 반환
    if content_line_is_valid:
        # start_date_KST
        start_date = get_sleep_attribute_value(content_line, start_date_index); start_date_KST = convert_csv_date(start_date) + datetime.timedelta(hours=9)
        # end_date_KST
        end_date = get_sleep_attribute_value(content_line, end_date_index); end_date_KST = convert_csv_date(end_date) + datetime.timedelta(hours=9)
        return {"source_name": source_name, "start_date_KST": start_date_KST, "end_date_KST": end_date_KST, "sleep_type": sleep_type, "index": search_index + offset}
    # * 위의 content_line을 찾지 못했다면 None 반환
    else:
        return None

def convert_ics_date(KST):
    return str(KST.year) + str(KST.month).zfill(2) + str(KST.day).zfill(2) + "T" + str(KST.hour).zfill(2) + str(KST.minute).zfill(2) + str(KST.second).zfill(2)

# * csv_file_content를 valid_content, invalid_content로 분할
valid_content = []
invalid_content = []

current_index = 0 
while 0 <= current_index <= len(csv_file_content)-1:
    current_source_name = get_sleep_attribute_value(csv_file_content[current_index], source_name_index)
    # AutoSleep, iPhone, Apple Watch
    if current_source_name == "AutoSleep" or current_source_name.find("iPhone") >= 0 or current_source_name.find("Apple Watch") >= 0:
        valid_content.append(csv_file_content[current_index])
    # 그 밖에
    else:
        invalid_content.append(csv_file_content[current_index])
    
    current_index += 1

# * sleep_session을 나누는 인덱스 찾기
# sleep_session을 나누는 인덱스
sleep_session_separator_indexes = []

# 현재 sleep_attribute_values_included_inbed_for_iphone 찾기
current_sleep_attribute_values_included_inbed_for_iphone = find_sleep_attribute_values(valid_content, 0, source_name_="iPhone", sleep_type_="inBed")
current_index = current_sleep_attribute_values_included_inbed_for_iphone["index"]
# 다음 sleep_attribute_values_included_inbed_for_iphone 찾기
next_sleep_attribute_values_included_inbed_for_iphone = find_sleep_attribute_values(valid_content, current_index+1, source_name_="iPhone", sleep_type_="inBed")
next_index = next_sleep_attribute_values_included_inbed_for_iphone["index"]

sleep_session_separator_indexes.append(0)

while True:
    # * 다음 sleep_attribute_values_included_inbed_for_iphone의 시작 시간과 현재 sleep_attribute_values_included_inbed_for_iphone의 종료 시간의 차이가 1시간보다 클 경우 next_index를 sleep_session_separator_indexes에 append
    if (next_sleep_attribute_values_included_inbed_for_iphone["start_date_KST"] - current_sleep_attribute_values_included_inbed_for_iphone["end_date_KST"]).total_seconds() > 1 * 60 * 60:
        sleep_session_separator_indexes.append(next_index)
    
    # 현재 sleep_attribute_values_included_inbed_for_iphone 찾기
    current_sleep_attribute_values_included_inbed_for_iphone = next_sleep_attribute_values_included_inbed_for_iphone
    current_index = next_index
    # 다음 sleep_attribute_values_included_inbed_for_iphone 찾기
    next_sleep_attribute_values_included_inbed_for_iphone = find_sleep_attribute_values(valid_content, current_index+1, source_name_="iPhone", sleep_type_="inBed")
    ## 다음 sleep_attribute_values_included_inbed_for_iphone 없다면 반복분 종료
    if next_sleep_attribute_values_included_inbed_for_iphone == None:
        break
    next_index = next_sleep_attribute_values_included_inbed_for_iphone["index"]

sleep_session_separator_indexes.append(len(valid_content))

# * ics_file_content에 valid_content에 대한 sleep_session_data들을 저장
ics_file_content = "BEGIN:VCALENDAR\n"

# current_index, current_sleep_session_separator_index
for current_index, current_sleep_session_separator_index in enumerate(sleep_session_separator_indexes):
    # * current_index가 마지막이라면 반복문 탈출
    if current_index == len(sleep_session_separator_indexes)-1:
        break
    
    # next_index, next_sleep_session_separator_index
    next_index = current_index+1
    next_sleep_session_separator_index = sleep_session_separator_indexes[next_index]
    
    # * sleep_session_data에 값 할당
    sleep_session_data = {}
    sleep_session_data["inBed"] = {}; sleep_session_data["inBed"]["start_date_KST"] = []; sleep_session_data["inBed"]["end_date_KST"] = []
    sleep_session_data["asleep"] = {}; sleep_session_data["asleep"]["start_date_KST"] = []; sleep_session_data["asleep"]["end_date_KST"] = []
    sleep_session_data["awake"] = {}; sleep_session_data["awake"]["start_date_KST"] = []; sleep_session_data["awake"]["end_date_KST"] = []
    sleep_session_data["asleepREM"] = {}; sleep_session_data["asleepREM"]["start_date_KST"] = []; sleep_session_data["asleepREM"]["end_date_KST"] = []
    sleep_session_data["asleepCore"] = {}; sleep_session_data["asleepCore"]["start_date_KST"] = []; sleep_session_data["asleepCore"]["end_date_KST"] = []
    sleep_session_data["asleepDeep"] = {}; sleep_session_data["asleepDeep"]["start_date_KST"] = []; sleep_session_data["asleepDeep"]["end_date_KST"] = []
    
    for valid_content_line in valid_content[current_sleep_session_separator_index:next_sleep_session_separator_index]:
        ## source_name
        source_name = get_sleep_attribute_value(valid_content_line, source_name_index)
        ## start_date_KST
        start_date = get_sleep_attribute_value(valid_content_line, start_date_index); start_date_KST = convert_csv_date(start_date) + datetime.timedelta(hours=9)
        ## end_date_KST
        end_date = get_sleep_attribute_value(valid_content_line, end_date_index); end_date_KST = convert_csv_date(end_date) + datetime.timedelta(hours=9)
        ## sleep_type
        sleep_type = get_sleep_attribute_value(valid_content_line, sleep_type_index)
        
        # * source_name이 "AutoSleep"이면 다음 valid_content_line 탐색
        # TODO 나중에 source_name이 "AutoSleep"인 sleep_attribute_values도 포함시켜 처리할 생각임. 아직은 무시.
        if source_name == "AutoSleep":
            continue
        
        # * sleep_session_data에 현재 sleep_attribute_value들을 배열로 저장
        sleep_session_data[sleep_type]["start_date_KST"].append(start_date_KST)
        sleep_session_data[sleep_type]["end_date_KST"].append(end_date_KST)
    
    # * ics_file_content에 valid_content에 대한 sleep_session_data들을 저장
    empty_dictionary_for_sleep_type = {"start_date_KST": [], "end_date_KST": []}
    
    ## * inBed만 존재
    if sleep_session_data["inBed"] != empty_dictionary_for_sleep_type and\
    sleep_session_data["asleep"] == empty_dictionary_for_sleep_type and\
    sleep_session_data["awake"] == empty_dictionary_for_sleep_type and\
    sleep_session_data["asleepREM"] == empty_dictionary_for_sleep_type and\
    sleep_session_data["asleepCore"] == empty_dictionary_for_sleep_type and\
    sleep_session_data["asleepDeep"] == empty_dictionary_for_sleep_type:
        # inBed
        minimum_start_date_KST_inbed = min(sleep_session_data["inBed"]["start_date_KST"]); minimum_start_date_KST_inbed_ics = convert_ics_date(minimum_start_date_KST_inbed)
        maximum_end_date_KST_inbed = max(sleep_session_data["inBed"]["end_date_KST"]); maximum_end_date_KST_inbed_ics = convert_ics_date(maximum_end_date_KST_inbed)
        inbed_time = maximum_end_date_KST_inbed - minimum_start_date_KST_inbed; inbed_time = str(inbed_time)[:-3]
        
        ics_file_content += "BEGIN:VEVENT\n"
        ics_file_content += "SUMMARY:취침\n"
        ics_file_content += f"DTSTART:{minimum_start_date_KST_inbed_ics}\n"
        ics_file_content += f"DTEND:{maximum_end_date_KST_inbed_ics}\n"
        ics_file_content += f"DESCRIPTION:취침: {inbed_time}\n"
        ics_file_content += "END:VEVENT\n"
    
    ## * asleep만 존재
    elif sleep_session_data["inBed"] == empty_dictionary_for_sleep_type and\
    sleep_session_data["asleep"] != empty_dictionary_for_sleep_type and\
    sleep_session_data["awake"] == empty_dictionary_for_sleep_type and\
    sleep_session_data["asleepREM"] == empty_dictionary_for_sleep_type and\
    sleep_session_data["asleepCore"] == empty_dictionary_for_sleep_type and\
    sleep_session_data["asleepDeep"] == empty_dictionary_for_sleep_type:
        # asleep
        minimum_start_date_KST_asleep = min(sleep_session_data["asleep"]["start_date_KST"]); minimum_start_date_KST_asleep_ics = convert_ics_date(minimum_start_date_KST_asleep)
        maximum_end_date_KST_asleep = max(sleep_session_data["asleep"]["end_date_KST"]); maximum_end_date_KST_asleep_ics = convert_ics_date(maximum_end_date_KST_asleep)
        asleep_time = maximum_end_date_KST_asleep - minimum_start_date_KST_asleep; asleep_time = str(asleep_time)[:-3]
        
        ics_file_content += "BEGIN:VEVENT\n"
        ics_file_content += "SUMMARY:수면\n"
        ics_file_content += f"DTSTART:{minimum_start_date_KST_asleep_ics}\n"
        ics_file_content += f"DTEND:{maximum_end_date_KST_asleep_ics}\n"
        ics_file_content += f"DESCRIPTION:수면: {asleep_time}\n"
        ics_file_content += "END:VEVENT\n"
    
    ## * inBed, asleep만 존재
    elif sleep_session_data["inBed"] != empty_dictionary_for_sleep_type and\
    sleep_session_data["asleep"] != empty_dictionary_for_sleep_type and\
    sleep_session_data["awake"] == empty_dictionary_for_sleep_type and\
    sleep_session_data["asleepREM"] == empty_dictionary_for_sleep_type and\
    sleep_session_data["asleepCore"] == empty_dictionary_for_sleep_type and\
    sleep_session_data["asleepDeep"] == empty_dictionary_for_sleep_type:
        # inBed
        minimum_start_date_KST_inbed = min(sleep_session_data["inBed"]["start_date_KST"]); minimum_start_date_KST_inbed_ics = convert_ics_date(minimum_start_date_KST_inbed)
        maximum_end_date_KST_inbed = max(sleep_session_data["inBed"]["end_date_KST"]); maximum_end_date_KST_inbed_ics = convert_ics_date(maximum_end_date_KST_inbed)
        inbed_time = maximum_end_date_KST_inbed - minimum_start_date_KST_inbed; inbed_time = str(inbed_time)[:-3]
        # asleep
        minimum_start_date_KST_asleep = min(sleep_session_data["asleep"]["start_date_KST"]); minimum_start_date_KST_asleep_ics = convert_ics_date(minimum_start_date_KST_asleep)
        maximum_end_date_KST_asleep = max(sleep_session_data["asleep"]["end_date_KST"]); maximum_end_date_KST_asleep_ics = convert_ics_date(maximum_end_date_KST_asleep)
        asleep_time = maximum_end_date_KST_asleep - minimum_start_date_KST_asleep; asleep_time = str(asleep_time)[:-3]
        
        ics_file_content += "BEGIN:VEVENT\n"
        ics_file_content += "SUMMARY:수면\n"
        ics_file_content += f"DTSTART:{minimum_start_date_KST_asleep_ics}\n"
        ics_file_content += f"DTEND:{maximum_end_date_KST_asleep_ics}\n"
        ics_file_content += f"DESCRIPTION:취침: {inbed_time}\\n수면: {asleep_time}\n"
        ics_file_content += "END:VEVENT\n"
    
    ## * inBed, asleep, awake만 존재
    elif sleep_session_data["inBed"] != empty_dictionary_for_sleep_type and\
    sleep_session_data["asleep"] != empty_dictionary_for_sleep_type and\
    sleep_session_data["awake"] != empty_dictionary_for_sleep_type and\
    sleep_session_data["asleepREM"] == empty_dictionary_for_sleep_type and\
    sleep_session_data["asleepCore"] == empty_dictionary_for_sleep_type and\
    sleep_session_data["asleepDeep"] == empty_dictionary_for_sleep_type:
        # inBed
        minimum_start_date_KST_inbed = min(sleep_session_data["inBed"]["start_date_KST"]); minimum_start_date_KST_inbed_ics = convert_ics_date(minimum_start_date_KST_inbed)
        maximum_end_date_KST_inbed = max(sleep_session_data["inBed"]["end_date_KST"]); maximum_end_date_KST_inbed_ics = convert_ics_date(maximum_end_date_KST_inbed)
        inbed_time = maximum_end_date_KST_inbed - minimum_start_date_KST_inbed; inbed_time = str(inbed_time)[:-3]
        # asleep
        minimum_start_date_KST_asleep = min(sleep_session_data["asleep"]["start_date_KST"]); minimum_start_date_KST_asleep_ics = convert_ics_date(minimum_start_date_KST_asleep)
        maximum_end_date_KST_asleep = max(sleep_session_data["asleep"]["end_date_KST"]); maximum_end_date_KST_asleep_ics = convert_ics_date(maximum_end_date_KST_asleep)
        asleep_time = maximum_end_date_KST_asleep - minimum_start_date_KST_asleep; asleep_time = str(asleep_time)[:-3]
        # awake
        awake_time = datetime.timedelta()
        for i in range(len(sleep_session_data["awake"]["start_date_KST"])):
            awake_time += sleep_session_data["awake"]["end_date_KST"][i] - sleep_session_data["awake"]["start_date_KST"][i]
        awake_time = str(awake_time)[:-3]
        
        ics_file_content += "BEGIN:VEVENT\n"
        ics_file_content += "SUMMARY:수면\n"
        ics_file_content += f"DTSTART:{minimum_start_date_KST_asleep_ics}\n"
        ics_file_content += f"DTEND:{maximum_end_date_KST_asleep_ics}\n"
        ics_file_content += f"DESCRIPTION:취침: {inbed_time}\\n수면: {asleep_time}\\n비수면: {awake_time}\n"
        ics_file_content += "END:VEVENT\n"
    
    ## * inBed, awake, asleepREM, asleepCore, asleepDeep만 존재
    elif sleep_session_data["inBed"] != empty_dictionary_for_sleep_type and\
    sleep_session_data["asleep"] == empty_dictionary_for_sleep_type and\
    (sleep_session_data["awake"] != empty_dictionary_for_sleep_type or\
    sleep_session_data["asleepREM"] != empty_dictionary_for_sleep_type or\
    sleep_session_data["asleepCore"] != empty_dictionary_for_sleep_type or\
    sleep_session_data["asleepDeep"] != empty_dictionary_for_sleep_type):
        # inBed
        minimum_start_date_KST_inbed = min(sleep_session_data["inBed"]["start_date_KST"]); minimum_start_date_KST_inbed_ics = convert_ics_date(minimum_start_date_KST_inbed)
        maximum_end_date_KST_inbed = max(sleep_session_data["inBed"]["end_date_KST"]); maximum_end_date_KST_inbed_ics = convert_ics_date(maximum_end_date_KST_inbed)
        inbed_time = maximum_end_date_KST_inbed - minimum_start_date_KST_inbed; inbed_time = str(inbed_time)[:-3]
        # awake
        awake_time = datetime.timedelta()
        for i in range(len(sleep_session_data["awake"]["start_date_KST"])):
            awake_time += sleep_session_data["awake"]["end_date_KST"][i] - sleep_session_data["awake"]["start_date_KST"][i]
        awake_time = str(awake_time)[:-3]
        # asleepREM
        asleepREM_time = datetime.timedelta()
        for i in range(len(sleep_session_data["asleepREM"]["start_date_KST"])):
            asleepREM_time += sleep_session_data["asleepREM"]["end_date_KST"][i] - sleep_session_data["asleepREM"]["start_date_KST"][i]
        asleepREM_time = str(asleepREM_time)[:-3]
        # asleepCore
        asleepCore_time = datetime.timedelta()
        for i in range(len(sleep_session_data["asleepCore"]["start_date_KST"])):
            asleepCore_time += sleep_session_data["asleepCore"]["end_date_KST"][i] - sleep_session_data["asleepCore"]["start_date_KST"][i]
        asleepCore_time = str(asleepCore_time)[:-3]
        # asleepDeep
        asleepDeep_time = datetime.timedelta()
        for i in range(len(sleep_session_data["asleepDeep"]["start_date_KST"])):
            asleepDeep_time += sleep_session_data["asleepDeep"]["end_date_KST"][i] - sleep_session_data["asleepDeep"]["start_date_KST"][i]
        asleepDeep_time = str(asleepDeep_time)[:-3]
        # asleep
        all_asleep_start_time_KST = [*sleep_session_data["awake"]["start_date_KST"], *sleep_session_data["asleepREM"]["start_date_KST"], *sleep_session_data["asleepCore"]["start_date_KST"], *sleep_session_data["asleepDeep"]["start_date_KST"]]; all_asleep_start_time_KST = set(all_asleep_start_time_KST); minimum_all_asleep_start_time_KST = min(all_asleep_start_time_KST)
        all_asleep_end_time_KST = [*sleep_session_data["awake"]["end_date_KST"], *sleep_session_data["asleepREM"]["end_date_KST"], *sleep_session_data["asleepCore"]["end_date_KST"], *sleep_session_data["asleepDeep"]["end_date_KST"]]; all_asleep_end_time_KST = set(all_asleep_end_time_KST); maximum_all_asleep_end_time_KST = max(all_asleep_end_time_KST)
        asleep_time = maximum_all_asleep_end_time_KST - minimum_all_asleep_start_time_KST
        asleep_time = str(asleep_time)[:-3]
        
        ics_file_content += "BEGIN:VEVENT\n"
        ics_file_content += "SUMMARY:수면\n"
        ics_file_content += f"DTSTART:{convert_ics_date(minimum_all_asleep_start_time_KST)}\n"
        ics_file_content += f"DTEND:{convert_ics_date(maximum_all_asleep_end_time_KST)}\n"
        ics_file_content += f"DESCRIPTION:취침: {inbed_time}\\n수면: {asleep_time}\\n비수면: {awake_time}\\nREM 수면: {asleepREM_time}\\n코어 수면: {asleepCore_time}\\n깊은 수면: {asleepDeep_time}\n"
        ics_file_content += "END:VEVENT\n"
    
    # * 예외
    else:
        print("sleep_attribute_values의 다른 패턴이 존재함\nsleep_session_data를 ics_file_content에 넣는 부분을 확인하면 됨")
        print(sleep_session_data, current_sleep_session_separator_index)
        exit(0)

ics_file_content += "END:VCALENDAR"

# * csv_file 디렉토리에 ics_file_content를 Sleep.ics 파일로 저장
with open(f"{csv_file_directory}/Sleep.ics", "w") as f:
    f.writelines(ics_file_content)
