import math

def mean_err():
    # 입력을 받은 후
    measure = input("측정값을 공백으로 구분하여 넣으세요.(ex: 14.53 24.52 45.21)")
    # 리스트의 원소를 실수로
    measure = list(map(float,measure.split()))

    # 측정회수 출력
    print('\n"측정회수"')
    print(len(measure))

    # 측정값 출력
    print()
    print('"측정값"')
    for i in range(len(measure)):
        if (i + 1) % 10 == 1:
            print("[",sep='',end='')
        print("x",i+1, "=",measure[i],sep='',end='')
        if ( (i + 1) % 10 != 0 ) and ( i != len(measure) - 1 ):
            print(", ",sep='',end='')
        if ( (i + 1) % 10 == 0 ) or ( i == len(measure) - 1 ):
            print("]")

    # 평균 계산
    mean = 0
    for i in range(len(measure)):
        mean += measure[i]
    mean /= len(measure)
    # 평균 출력
    print()
    print('"평균"')
    print('"(Σ(i:from ', 1, " to ", len(measure), ")xi) / ", len(measure), '"', sep='')
    print("(",sep='',end='')
    for i in range(len(measure)):
        if i != len(measure) - 1:
            print(measure[i],sep='',end=' + ')
        else:
            print(measure[i],sep='',end='')
    print(") / ", len(measure),sep='')
    print('"평균" => ', mean, sep='')

    # 편차 계산
    der = [measure[i] - mean for i in range(len(measure))]
    # 편차 출력
    print()
    print('"편차"')
    print('"평균 - xi", for all ', 1, " <= i <= ", len(measure), sep='')
    for i in range(len(measure)):
        print("[", i+1, "] x", i, " - mean = ", measure[i], " - ", mean, " = ", der[i], sep='')
    print('"편차" => ', der, sep='')

    # 표준편차 계산
    stdder = 0
    sqrder = [der[i] ** 2 for i in range(len(measure))]
    for i in range(len(measure)):
        stdder += der[i] ** 2

    # 표준편차 출력
    print()
    print('"표준편차"')
    print('"편차^2( = (평균 - xi)^2 )"')
    for i in range(len(measure)):
        print("[", i+1, "] (x", i, " - mean)^2 = (", measure[i], " - ", mean, ")^2 = ", der[i], "^2 = ", sqrder[i], sep='')
    print('"Σ(i:from ', 1, " to ", len(measure), ')(평균 - xi)^2"', sep='')
    stdder = sum(sqrder,0)
    print("=> ", sep='', end='')
    print(stdder)
    print('"root( Σ(i:from ', 1, " to ", len(measure), ')(평균 - xi)^2', ') / (', len(measure), " - 1", ') )"', sep='')
    stdder = math.sqrt( stdder / (len(measure) - 1) )
    print("=> ", sep='', end='')
    print(stdder)
    print('"표준편차"')
    print("=> ", stdder, sep='')
    # print("root( (Σ(i:from ", 1, " to ", len(measure), ")(평균 - xi)^2) / (", len(measure), "-1)", " )", sep='')
    # print("root( (Σ(i:from ", 1, " to ", len(measure), ")(평균 - xi)^2) / ", len(measure) - 1, " )", sep='')

    # 표준오차 계산
    stderr = 0
    stderr = stdder / math.sqrt( len(measure) )
    # 표준오차 출력
    print()
    print("<표준오차>")
    print("root( (Σ(i:from ", 1, " to ", len(measure), ")(평균 - xi)^2) / ", len(measure), " x (", len(measure), " - 1)", " )", sep='')
    # print("root( (Σ(i:from ", 1, " to ", len(measure), ")(평균 - xi)^2) / ", len(measure), "x", len(measure) - 1, " )", sep='')
    print('"표준오차"')
    print("=> ", stderr, sep='')

    print()
