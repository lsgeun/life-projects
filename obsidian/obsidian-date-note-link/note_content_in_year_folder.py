import calendar as cal
import datetime

right = '→'; left = '←'; up = '↑'; down = '↓'

body = "# Goal\n\n\n# Note\n##아침\n\n##점심\n\n##저녁\n\n"

def wrapLink(time, linkDir):
    year = time.split('-')[0]; yeardir = f'{linkDir}/{year}'
    return f'[{time}]({yeardir}/{time}.md)'

def yearNoteContent(year, linkDir):
    pastYear = str(int(year)-1); curYear = year; nextYear = str(int(year)+1)
    quarters = [f'{curYear}-Q{i+1}' for i in range(4)]
    
    header = '\n\n'
    header += f'{wrapLink(pastYear, linkDir)} {left} {curYear} {right} {wrapLink(nextYear, linkDir)}\n'
    header += f'{down} '
    for i, quarter in enumerate(quarters):
        header += wrapLink(quarter, linkDir)
        if (i+1) == 4:
            header += '\n'
        else:
            header += ', '
    header += '\n'
    
    return header + body

def quarterNoteContent(quarter, linkDir):
    curYear = quarter.split('-')[0]
    
    curQuarterLastNumberInt = int(quarter[-1])
    pastQuarterLastNumberInt = curQuarterLastNumberInt-1
    if pastQuarterLastNumberInt == 0:
        pastQuarterLastNumberInt = 4
        pastYearInt = int(curYear) - 1
    else:
        pastYearInt = int(curYear)
        
    nextQuarterLastNumberInt = curQuarterLastNumberInt+1
    if nextQuarterLastNumberInt == 5:
        nextQuarterLastNumberInt = 1
        nextYearInt = int(curYear) + 1
    else:
        nextYearInt = int(curYear)
    pastQuarter = f'{pastYearInt}-Q{pastQuarterLastNumberInt}'; curQuarter = quarter; nextQuarter = f'{nextYearInt}-Q{nextQuarterLastNumberInt}'
    
    header = "\n"
    header += f'{up} {wrapLink(curYear, linkDir)}\n'
    header += f'{wrapLink(pastQuarter, linkDir)} {left} {curQuarter} {right} {wrapLink(nextQuarter, linkDir)}\n'
    header += f'{down} '
    
    monthLastNumberInts = [(3*curQuarterLastNumberInt-2)+i for i in range(3)]
    months = []
    for monthLastNumberInt in monthLastNumberInts:
        if monthLastNumberInt <= 9:
            months.append(f'{curYear}-0{monthLastNumberInt}')
        else:
            months.append(f'{curYear}-{monthLastNumberInt}')
            
    for i, month in enumerate(months):
        header += wrapLink(month, linkDir)
        if (i+1) == 3:
            header += '\n'
        else:
            header += ', '
    header += '\n'
    
    return header + body

def monthNoteContent(month, linkDir):
    # 현재 연도
    curYear = month.split('-')[0]
    # 현재 월 마지막 정수
    curMonthLastNumberInt = int(month[-2:])
    # 현재 분기 마지막 정수
    curQuarterLastNumberInt = (curMonthLastNumberInt-1)//3 + 1
    # 현재 분기
    curQuarter = f'{curYear}-Q{curQuarterLastNumberInt}'
    # 이전 월 마지막 정수, 이전 연도 정수
    pastMonthLastNumberInt = curMonthLastNumberInt - 1
    if pastMonthLastNumberInt == 0:
        pastMonthLastNumberInt = 12
        pastYearInt = int(curYear)-1
    else:
        pastYearInt = int(curYear)
    pastMonthLastNumberStr = str(pastMonthLastNumberInt).zfill(2)
    # 다음 월 마지막 정수, 다음 연도 정수
    nextMonthLastNumberInt = curMonthLastNumberInt + 1
    if nextMonthLastNumberInt == 13:
        nextMonthLastNumberInt = 1
        nextYearInt = int(curYear)+1
    else:
        nextYearInt = int(curYear)
    nextMonthLastNumberStr = str(nextMonthLastNumberInt).zfill(2) 
    # 이전 월, 현재 월, 다음 월
    pastMonth = f'{pastYearInt}-{pastMonthLastNumberStr}'; curMonth = month; nextMonth = f'{nextYearInt}-{nextMonthLastNumberStr}'
    
    # 현재 연도 정수
    curYearInt = int(curYear)
    # 현재 연도 2월 달에 추가될 일 수
    dayAddedInYear = int(cal.isleap(curYearInt))
    # 현재 연도 각 월의 일 수
    monthDaysOfCurYear = [(1,31), (2,28 + dayAddedInYear), (3,31), (4,30), (5,31), (6,30), (7,31), (8,31), (9,30), (10,31), (11,30), (12,31)]
    # 월에 속한 주의 마지막 수들
    weekLastNumbersInMonthInt = set()
    
    for day in range(1, monthDaysOfCurYear[curMonthLastNumberInt-1][1]+1):
        isoCalendar = datetime.datetime(curYearInt, curMonthLastNumberInt, day).isocalendar()
        weekLastNumbersInMonthInt.add(isoCalendar[1])
        
    weekLastNumbersInMonthInt = sorted(list(weekLastNumbersInMonthInt))
    
    # 고립된 주의 마지막 수
    # 1월의 첫 주나, 12월의 마지막 주가 고립된 주에 해당함
    isolatedWeekLastNumerInt = 0
    if weekLastNumbersInMonthInt[1] - weekLastNumbersInMonthInt[0] != 1:
        isolatedWeekLastNumerInt = weekLastNumbersInMonthInt[0]
    if weekLastNumbersInMonthInt[-1] - weekLastNumbersInMonthInt[-2] != 1:
        isolatedWeekLastNumerInt = weekLastNumbersInMonthInt[-1]
    # 월에 속한 주의 마지막 수의 문자열들
    weekLastNumbersInMonthStr = []
    for weekLastNumberInMonthInt in weekLastNumbersInMonthInt:
        weekLastNumbersInMonthStr.append(str(weekLastNumberInMonthInt).zfill(2))
    
    # 현재 월의 모든 주차
    weeks = []
    for weekLastNumberInMonthStr in weekLastNumbersInMonthStr:
        if int(weekLastNumberInMonthStr) == isolatedWeekLastNumerInt:
            if weekLastNumberInMonthStr == '01':
                nextYear = str(nextYearInt + 1)
                week = f'{nextYear}-W{weekLastNumberInMonthStr}'
                weeks.append(week)
            elif weekLastNumberInMonthStr == '12':
                pastYear = str(pastYearInt - 1)
                week = f'{pastYear}-W{weekLastNumberInMonthStr}'
                weeks.append(week)
            else:
                pass
            
            continue
        
        week = f'{curYear}-W{weekLastNumberInMonthStr}'
        weeks.append(week)
        
    weeks = sorted(weeks)
    
    header = "\n"
    header += f'{up} {wrapLink(curQuarter, linkDir)}\n'
    header += f'{wrapLink(pastMonth, linkDir)} {left} {curMonth} {right} {wrapLink(nextMonth, linkDir)}\n'
    header += f'{down} '
    for i, week in enumerate(weeks):
        header += wrapLink(week, linkDir)
        if (i+1) == weeks.__len__():
            header += '\n'
        else:
            header += ', '
    header += '\n'
    
    return header + body

def weekNoteContent(week, linkDir):
    curYear = week.split('-')[0]; pastYear = str(int(curYear)-1); nextYear = str(int(curYear)+1)
            
    weeksOfMonths = []
    WEEK = 1
    # 이전 12 주
    weekLastNumbersOfMonth = set()
    for day in range(1, 31+1):
        dayIsoCalendar = datetime.datetime(int(pastYear), 12, day).isocalendar()
        weekLastNumbersOfMonth.add(dayIsoCalendar[WEEK])
    
    weekLastNumbersOfMonth = list(weekLastNumbersOfMonth)
    for i, weekLastNumber in enumerate(weekLastNumbersOfMonth):
        if weekLastNumber <= 9:
            weekLastNumbersOfMonth[i] = f'0{weekLastNumber}'
        else:
            weekLastNumbersOfMonth[i] = f'{weekLastNumber}'

    weeksOfMonth = []
    for weekLastNumber in weekLastNumbersOfMonth:
        if weekLastNumber == '01':
            weeksOfMonth.append(f'{curYear}-W{weekLastNumber}')
        else:
            weeksOfMonth.append(f'{pastYear}-W{weekLastNumber}')
    weeksOfMonth = sorted(weeksOfMonth)
    weeksOfMonths.append(weeksOfMonth)
    
    weekLastNumbersOfMonth = set()
    # 현재 1-12 주
    dayAddedInYear = int(cal.isleap(int(curYear)))
    monthDaysOfCurYear = [(1,31), (2,28 + dayAddedInYear), (3,31), (4,30), (5,31), (6,30), (7,31), (8,31), (9,30), (10,31), (11,30), (12,31)]
    DAYS = 1
    for monthLastNumber in range(1,12+1):
        for day in range(1, monthDaysOfCurYear[monthLastNumber-1][DAYS]+1):
            dayIsoCalendar = datetime.datetime(int(curYear), (monthLastNumber), day).isocalendar()
            weekLastNumbersOfMonth.add(dayIsoCalendar[WEEK])
            
        weekLastNumbersOfMonth = list(weekLastNumbersOfMonth)
        for i, weekLastNumber in enumerate(weekLastNumbersOfMonth):
            if weekLastNumber <= 9:
                weekLastNumbersOfMonth[i] = f'0{weekLastNumber}'
            else:
                weekLastNumbersOfMonth[i] = f'{weekLastNumber}'

        weeksOfMonth = []
        for weekLastNumber in weekLastNumbersOfMonth:
            if monthLastNumber == 12 and weekLastNumber == '01':
                weeksOfMonth.append(f'{nextYear}-W{weekLastNumber}')
            elif monthLastNumber == 1 and int(weekLastNumber) > 6:
                weeksOfMonth.append(f'{pastYear}-W{weekLastNumber}')
            else:
                weeksOfMonth.append(f'{curYear}-W{weekLastNumber}')
        weeksOfMonth = sorted(weeksOfMonth)
        weeksOfMonths.append(weeksOfMonth)
        
        weekLastNumbersOfMonth = set()
    # 다음 1 주
    for day in range(1, 31+1):
        dayIsoCalendar = datetime.datetime(int(nextYear), 1, day).isocalendar()
        weekLastNumbersOfMonth.add(dayIsoCalendar[WEEK])
    
    weekLastNumbersOfMonth = list(weekLastNumbersOfMonth)
    for i, weekLastNumber in enumerate(weekLastNumbersOfMonth):
        if weekLastNumber <= 9:
            weekLastNumbersOfMonth[i] = f'0{weekLastNumber}'
        else:
            weekLastNumbersOfMonth[i] = f'{weekLastNumber}'

    weeksOfMonth = []
    for weekLastNumber in weekLastNumbersOfMonth:
        if int(weekLastNumber) > 6:
            weeksOfMonth.append(f'{curYear}-W{weekLastNumber}')
        else:
            weeksOfMonth.append(f'{nextYear}-W{weekLastNumber}')
    weeksOfMonth = sorted(weeksOfMonth)
    weeksOfMonths.append(weeksOfMonth)
    
    weekLastNumbersOfMonth = set()
    # find current months
    monthsOfCurWeek = []; curWeekIndexs = []; curMonths = []
    for month, weeksOfMonth in enumerate(weeksOfMonths):
        for index, weekOfMonth in enumerate(weeksOfMonth):
            if weekOfMonth == week:
                monthsOfCurWeek.append(month)
                curWeekIndexs.append(index)
    for monthOfCurWeek in monthsOfCurWeek:
        if monthOfCurWeek == 0:
            curMonths.append(f'{pastYear}-12')
        elif monthOfCurWeek == 13:
            curMonths.append(f'{nextYear}-01')
        else:
            if monthOfCurWeek <= 9:
                curMonths.append(f'{curYear}-0{monthOfCurWeek}')
            else:
                curMonths.append(f'{curYear}-{monthOfCurWeek}')
    # find past, next week
    curWeek = weeksOfMonths[monthsOfCurWeek[0]][curWeekIndexs[0]]
    
    pastWeekIndex = curWeekIndexs[0]-1
    if pastWeekIndex < 0:
        pastWeekIndex = -1
        monthOfPastWeek = monthsOfCurWeek[0]-1
        if weeksOfMonths[monthOfPastWeek][pastWeekIndex] == curWeek:
            pastWeekIndex = -2
    else:
        monthOfPastWeek = monthsOfCurWeek[0]
    pastWeek = weeksOfMonths[monthOfPastWeek][pastWeekIndex]
    
    nextWeekIndex = curWeekIndexs[0]+1
    if nextWeekIndex > weeksOfMonths[monthsOfCurWeek[0]].__len__()-1:
        nextWeekIndex = 0
        monthOfNextWeek = monthsOfCurWeek[0]+1
        if weeksOfMonths[monthOfNextWeek][nextWeekIndex] == curWeek:
            nextWeekIndex = 1
    else:
        monthOfNextWeek = monthsOfCurWeek[0]
    nextWeek = weeksOfMonths[monthOfNextWeek][nextWeekIndex]
    # find days
    calendar = cal.Calendar()
    curMonths0LastNumberInt = int(curMonths[0][-2:])
    yearOfCurMonths0Int = int(curMonths[0].split('-')[0])
    weeksDaysOfCurMonth = calendar.monthdatescalendar(yearOfCurMonths0Int, curMonths0LastNumberInt)
    days = weeksDaysOfCurMonth[curWeekIndexs[0]]
    for i, day in enumerate(days):
        days[i] = str(day)
    # header
    header = "\n"
    header += f'{up}'
    for i, curMonth in enumerate(curMonths):
        if i == 0:
            header += f' {wrapLink(curMonth, linkDir)}'
        else:
            header += f', {wrapLink(curMonth, linkDir)}'
    header += '\n'
    header += f'{wrapLink(pastWeek, linkDir)} {left} {curWeek} {right} {wrapLink(nextWeek, linkDir)}\n'
    header += f'{down} '
    for i, day in enumerate(days):
        header += wrapLink(day, linkDir)
        if i == days.__len__()-1:
            header += '\n'
        else:
            header += ', '
    header += '\n'
    
    return header + body

def dayNoteContent(day, linkDir):
    # current week
    daySplitByHyphen = day.split('-')
    curYearInt = int(daySplitByHyphen[0]); curMonthLastNumberInt = int(daySplitByHyphen[1]); curDayLastNumberInt = int(daySplitByHyphen[2])
    
    yearWeekWeekDayOfCurDay = datetime.datetime(curYearInt, curMonthLastNumberInt, curDayLastNumberInt).isocalendar()
    curWeekLastNumberInt = yearWeekWeekDayOfCurDay[1]
    curYearAsIsoInt = yearWeekWeekDayOfCurDay[0]
    if curWeekLastNumberInt <= 9:
        curWeek = f'{curYearAsIsoInt}-W0{curWeekLastNumberInt}'
    else:
        curWeek = f'{curYearAsIsoInt}-W{curWeekLastNumberInt}'
    # current day
    curDay = f'{day}'
    # past, next day
    dayAddedInYear = int(cal.isleap(curYearInt))
    monthDaysOfCurYear = [(1,31), (2,28 + dayAddedInYear), (3,31), (4,30), (5,31), (6,30), (7,31), (8,31), (9,30), (10,31), (11,30), (12,31)]
    
    pastDayLastNumberInt = curDayLastNumberInt - 1
    if pastDayLastNumberInt == 0:
        pastMonthLastNumberInt = curMonthLastNumberInt - 1
        if pastMonthLastNumberInt == 0:
            pastYearInt = curYearInt - 1
            pastMonthLastNumberInt = 12
            pastDayLastNumberInt = 31
        else:
            daysCountOfPastMonth = monthDaysOfCurYear[pastMonthLastNumberInt-1][1]
            pastYearInt = curYearInt
            pastDayLastNumberInt = daysCountOfPastMonth
    else:
        pastMonthLastNumberInt = curMonthLastNumberInt
        pastYearInt = curYearInt
    
    pastYearStr = str(pastYearInt)
    if pastMonthLastNumberInt <= 9:
        pastMonthLastNumberStr = f'0{pastMonthLastNumberInt}'
    else:
        pastMonthLastNumberStr = f'{pastMonthLastNumberInt}'
    if pastDayLastNumberInt <= 9:
        pastDayLastNumberStr = f'0{pastDayLastNumberInt}'
    else:
        pastDayLastNumberStr = f'{pastDayLastNumberInt}'
    pastDay = f'{pastYearStr}-{pastMonthLastNumberStr}-{pastDayLastNumberStr}'
    
    nextDayLastNumberInt = curDayLastNumberInt + 1
    daysCountOfCurMonth = monthDaysOfCurYear[curMonthLastNumberInt-1][1]
    if nextDayLastNumberInt > daysCountOfCurMonth:
        nextMonthLastNumberInt = curMonthLastNumberInt + 1
        nextDayLastNumberInt = 1
        if nextMonthLastNumberInt > 12:
            nextYearInt = curYearInt + 1
            nextMonthLastNumberInt = 1
        else:
            nextYearInt = curYearInt
    else:
        nextMonthLastNumberInt = curMonthLastNumberInt
        nextYearInt = curYearInt
        
    nextYearStr = str(nextYearInt)
    if nextMonthLastNumberInt <= 9:
        nextMonthLastNumberStr = f'0{nextMonthLastNumberInt}'
    else:
        nextMonthLastNumberStr = f'{nextMonthLastNumberInt}'
    if nextDayLastNumberInt <= 9:
        nextDayLastNumberStr = f'0{nextDayLastNumberInt}'
    else:
        nextDayLastNumberStr = f'{nextDayLastNumberInt}'
    nextDay = f'{nextYearStr}-{nextMonthLastNumberStr}-{nextDayLastNumberStr}'
    
    # header
    header = "\n"
    header += f'{up} {wrapLink(curWeek, linkDir)}'
    header += '\n'
    header += f'{wrapLink(pastDay, linkDir)} {left} {curDay} {right} {wrapLink(nextDay, linkDir)}\n'
    header += '\n\n'
    
    return header + body