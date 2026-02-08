import os
import calendar as cal
import datetime
import sys

saveDir = sys.argv[1]
saveDir = saveDir.replace(' ', '\ ')
yearInt = int(sys.argv[2])
# Year Directory
os.system(f'mkdir {saveDir}/{yearInt}')
# Year Note
os.system(f'touch {saveDir}/{yearInt}/{yearInt}.md')
# Quarter Note
for quarterLastNumber in range(1, 4+1):
    os.system(f'touch {saveDir}/{yearInt}/{yearInt}-Q{quarterLastNumber}.md')
# Month Note
for monthLastNumber in range(1, 12+1):
    if monthLastNumber <= 9:
        os.system(f'touch {saveDir}/{yearInt}/{yearInt}-0{monthLastNumber}.md')
    else:
        os.system(f'touch {saveDir}/{yearInt}/{yearInt}-{monthLastNumber}.md')
# Week Note, ISO 기준 1년에 53주임
weekLastNumbersInDecMonthInt = set()
for day in range(1, 31+1):
    isoCalendar = datetime.datetime(yearInt, 12, day).isocalendar()
    weekLastNumbersInDecMonthInt.add(isoCalendar[1])
weekLastNumbersInDecMonthInt = sorted(list(weekLastNumbersInDecMonthInt))
maxWeekLastNumberInDecMonthInt = weekLastNumbersInDecMonthInt[-1]

for weekLastNumber in range(1, maxWeekLastNumberInDecMonthInt+1):
    if weekLastNumber <= 9:
        os.system(f'touch {saveDir}/{yearInt}/{yearInt}-W0{weekLastNumber}.md')
    else:
        os.system(f'touch {saveDir}/{yearInt}/{yearInt}-W{weekLastNumber}.md')
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
            os.system(f'touch {saveDir}/{yearInt}/{yearInt}-{monthStr}-0{day}.md')
        else:
            os.system(f'touch {saveDir}/{yearInt}/{yearInt}-{monthStr}-{day}.md')
