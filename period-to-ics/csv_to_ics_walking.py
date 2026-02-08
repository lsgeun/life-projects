import os
import datetime
import math

# csv 파일 경로
csv_file_path = "/Users/isgeun/Library/Mobile Documents/iCloud~md~obsidian/Documents/NOTE-iCloud_Drive/0 Inbox/HKWorkoutActivityTypeWalking_2024-01-02_09-03-25_SimpleHealthExportCSV.csv"

# * source_name, start_date, end_date, sleep_type의 index 설정
NOT_FOUND = -1
start_date_index = NOT_FOUND
end_date_index = NOT_FOUND
kilocalorie_index = NOT_FOUND
distance_index = NOT_FOUND
humidity_index = NOT_FOUND
temperature_index = NOT_FOUND
height_index = NOT_FOUND

# csv 파일을 변수에 저장
csv_file_content = None
with open(csv_file_path, "r") as f:
    csv_file_content = f.readlines(); csv_file_content.pop(0)

# sleep_attributes
sleep_attributes = csv_file_content.pop(0); sleep_attributes = sleep_attributes.split(",")
for sleep_attribute_index, sleep_attribute in enumerate(sleep_attributes):
    if sleep_attribute == "startDate":
        start_date_index = sleep_attribute_index
    elif sleep_attribute == "endDate":
        end_date_index = sleep_attribute_index
    elif sleep_attribute == "totalEnergyBurned":
        kilocalorie_index = sleep_attribute_index
    elif sleep_attribute == "totalDistance":
        distance_index = sleep_attribute_index
    elif sleep_attribute == "HKWeatherHumidity":
        humidity_index = sleep_attribute_index
    elif sleep_attribute == "HKWeatherTemperature":
        temperature_index = sleep_attribute_index
    elif sleep_attribute == "HKElevationAscended":
        height_index = sleep_attribute_index
    else:
        pass

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

def get_date(utc):
    year = int(utc[0:4]); month = int(utc[5:7]); day = int(utc[8:10]); hour = int(utc[11:13]); minute = int(utc[14:16]); second = int(utc[17:19])
    return datetime.datetime(year, month, day, hour, minute, second)

# * ics_file_content에 walking_data를 저장하기
ics_file_content = "BEGIN:VCALENDAR\n"
for csv_file_content_line in csv_file_content:
    # 시작 시간, 종료 시간, 칼로리, 거리, 고도, 습도, 온도 초기화
    ## 시작 시간
    start_UTC = get_sleep_attribute_value(csv_file_content_line, start_date_index); start_UTC_date = get_date(start_UTC); start_KST_date = start_UTC_date + datetime.timedelta(hours=9); start_KST = str(start_KST_date.year) + str(start_KST_date.month).zfill(2) + str(start_KST_date.day).zfill(2) + "T" + str(start_KST_date.hour).zfill(2) + str(start_KST_date.minute).zfill(2) + str(start_KST_date.second).zfill(2)
    ## 종료 시간
    end_UTC = get_sleep_attribute_value(csv_file_content_line, end_date_index); end_UTC_date = get_date(end_UTC); end_KST_date = end_UTC_date + datetime.timedelta(hours=9); end_KST = str(end_KST_date.year) + str(end_KST_date.month).zfill(2) + str(end_KST_date.day).zfill(2) + "T" + str(end_KST_date.hour).zfill(2) + str(end_KST_date.minute).zfill(2) + str(end_KST_date.second).zfill(2)
    ## 칼로리
    kcal = get_sleep_attribute_value(csv_file_content_line, kilocalorie_index); kcal = math.floor(float(kcal[:-5]))
    ## 거리
    distance = get_sleep_attribute_value(csv_file_content_line, distance_index); distance = round(float(distance[:-2])/1000, 2)
    ## 온도
    temperature = get_sleep_attribute_value(csv_file_content_line, temperature_index); temperature = round((float(temperature[:-5]) - 32) * 5/9) if temperature != "" else ""
    ## 습도
    humidity = get_sleep_attribute_value(csv_file_content_line, humidity_index); humidity = round(float(humidity[:-2])/100) if humidity != "" else ""
    ## 고도
    height = get_sleep_attribute_value(csv_file_content_line, height_index); height = 0 if height == "" else round(float(height[:-3])/100) if height != "" else ""
    # 시작 시간, 종료 시간, 칼로리, 거리, 고도, 습도, 온도로 이벤트 만들기
    ics_file_content += "BEGIN:VEVENT\n"
    ics_file_content += "SUMMARY:걷기\n"
    ics_file_content += f"DTSTART:{start_KST}\n"
    ics_file_content += f"DTEND:{end_KST}\n"
    ics_file_content += f"DESCRIPTION:칼로리:   {kcal}kcal\\n거리:      {distance}km\\n고도:      {height}m\\n습도:      {humidity}%\\n온도:      {temperature}°C\n"
    ics_file_content += "END:VEVENT\n"
    # walking_data 찾기
ics_file_content += "END:VCALENDAR"

# csv_file 디렉토리 경로
csv_file_directory = os.path.dirname(csv_file_path)
# csv_file 파일 이름
csv_file_name = os.path.basename(csv_file_path)[:-4]
# * csv_file 현재 디렉토리에 Walking.ics 파일 생성하기
with open(f"{csv_file_directory}/Walking {csv_file_name}.ics", "w") as f:
    f.writelines(ics_file_content)
