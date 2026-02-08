from note_content_in_year_folder import *
import os
import calendar as cal
import datetime
import sys

saveDir = sys.argv[1]
linkDir = saveDir.replace("/Users/isgeun/Library/Mobile Documents/iCloud~md~obsidian/Documents/NOTE-iCloud_Drive/", "").replace(" ", "%20")
yearInt = int(sys.argv[2])
# Year Directory
yearDir = f'{saveDir}/{yearInt}' # path라고 생각되면 ' '을 '\ '로 바꿔주는가 봄
# Year Note
with open(f'{yearDir}/{yearInt}.md', 'w') as f:
    f.write(yearNoteContent(f'{yearInt}', linkDir))
# Quarter Note
for quarterLastNumber in range(1, 4+1):
    with open(f'{yearDir}/{yearInt}-Q{quarterLastNumber}.md', 'w') as f:
        f.write(quarterNoteContent(f'{yearInt}-Q{quarterLastNumber}', linkDir))
# Month Note
for monthLastNumber in range(1, 12+1):
    if monthLastNumber <= 9:
        with open(f'{yearDir}/{yearInt}-0{monthLastNumber}.md', 'w') as f:
            f.write(monthNoteContent(f'{yearInt}-0{monthLastNumber}', linkDir))
    else:
        with open(f'{yearDir}/{yearInt}-{monthLastNumber}.md', 'w') as f:
            f.write(monthNoteContent(f'{yearInt}-{monthLastNumber}', linkDir))
# Week Note, ISO 기준 1년에 53주임
weekLastNumbersInDecMonthInt = set()
for day in range(1, 31+1):
    isoCalendar = datetime.datetime(yearInt, 12, day).isocalendar()
    weekLastNumbersInDecMonthInt.add(isoCalendar[1])
weekLastNumbersInDecMonthInt = sorted(list(weekLastNumbersInDecMonthInt))
maxWeekLastNumberInDecMonthInt = weekLastNumbersInDecMonthInt[-1]

for weekLastNumber in range(1, maxWeekLastNumberInDecMonthInt+1):
    if weekLastNumber <= 9:
        with open(f'{yearDir}/{yearInt}-W0{weekLastNumber}.md', 'w') as f:
            f.write(weekNoteContent(f'{yearInt}-W0{weekLastNumber}', linkDir))
    else:
        with open(f'{yearDir}/{yearInt}-W{weekLastNumber}.md', 'w') as f:
            f.write(weekNoteContent(f'{yearInt}-W{weekLastNumber}', linkDir))
# Day Note
dayAddedInYear = int(cal.isleap(yearInt))
monthDaysOfYear = [(1,31), (2,28 + dayAddedInYear), (3,31), (4,30), (5,31), (6,30), (7,31), (8,31), (9,30), (10,31), (11,30), (12,31)]
for month, days in monthDaysOfYear:
    if month <= 9:
        monthStr = f'0{month}'
    else:
        monthStr = f'{month}'
    for day in range(1, days+1):
        if day <= 9:
            with open(f'{yearDir}/{yearInt}-{monthStr}-0{day}.md', 'w') as f:
                f.write(dayNoteContent(f'{yearInt}-{monthStr}-0{day}', linkDir))
        else:
            with open(f'{yearDir}/{yearInt}-{monthStr}-{day}.md', 'w') as f:
                f.write(dayNoteContent(f'{yearInt}-{monthStr}-{day}', linkDir))
