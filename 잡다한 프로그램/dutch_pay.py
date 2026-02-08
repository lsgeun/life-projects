persons = input("사람을 입력하세요:").split()
# payments[i][j]는 i가 j에게 줘야하는 돈을 의미함.
# 참고로 열과 행이 같은 경우 항상 0임.
print("person:", persons, sep='')

payments = []
for i in range(len(persons)):
    payment_row = []
    for j in range(len(persons)):
        payment_row.append(0)
    payments.append(payment_row)

payment_info = ""
print("지불 정보를 입력한 후 입력이 끝난 후 end를 입력하세요.")
print("예를 들어, 홍길동 23000 -철수 혹은 영희 15000")
while True :
    payment_info = input().split()
    payment_info_length = payment_info.__len__()

    if payment_info == ["end"] :
        print("지불 정보 입력이 종료됩니다.")
        break

    if payment_info_length == 2 and\
        payment_info[0] in persons and\
        payment_info[1].isdigit():
        
        receiver = persons.index(payment_info[0])
        givers = [ giver for giver in range(persons.__len__()) ]
        for giver in givers:
            if giver != receiver:
                payments[giver][receiver] += float(payment_info[1]) / givers.__len__()
            else: # giver == receiver:
                pass # 주는 사람과 받는 사람이 같으므로 아무런 동작을 하지 않아도 됨.
    elif payment_info_length >= 3 and\
        payment_info[0] in persons and\
        payment_info[1].isdigit():
        
        is_error = False
        for i in range(2,payment_info_length):
             # - 이후에 문자가 없으면 에러가 나므로 try, catch를 쓰지 않기 위해
             # - 이후 문자가 있다는 것을 if문 첫번째 조건식에서 확인해야함.
             # 항상 payment_info[i].__len__() >= 1을 만족함.
            if payment_info[i].__len__() == 1 or\
                payment_info[i][0] != "-" or\
                payment_info[i][1:] not in persons:
            
                print(payment_info[i].__len__(), payment_info[i][0], payment_info[i][1:])
                is_error = True
                print("입력이 잘못되었습니다.")
                print("다음과 같은 방식으로 입력해주세요. 홍길동 23000 -철수 혹은 영희 15000")
                break
        
        if is_error == False:
            receiver = persons.index(payment_info[0])
            givers = [ giver for giver in range(persons.__len__()) ]

            for i in range(2, payment_info_length):
                givers.remove(persons.index(payment_info[i][1:]))
            
            for giver in givers:
                if giver != receiver:
                    payments[giver][receiver] += float(payment_info[1]) / givers.__len__()
                else: # giver == receiver:
                    pass # 주는 사람과 받는 사람이 같으므로 아무런 동작을 하지 않아도 됨.
    else:
        print("입력이 잘못되었습니다.")
        print("다음과 같은 방식으로 입력해주세요. 홍길동 23000 -철수 혹은 영희 15000")

    print(payment_info)
    
print("payments:")
for i in range(persons.__len__()):
    for j in range(persons.__len__()):
        if payments[i][j] % 100 >= 50:
            payments[i][j] = int((payments[i][j] // 100)*100 + 100)
        else:
            payments[i][j] = int((payments[i][j] // 100)*100)
        print(payments[i][j], "\t", sep ='', end=' ')
    print()

for first_person in range(persons.__len__()):
    for second_person in range(first_person+1, persons.__len__()):
        if payments[first_person][second_person] > payments[second_person][first_person]:
            print(f"{persons[first_person]}->{persons[second_person]}: {payments[first_person][second_person] - payments[second_person][first_person]}원")
        elif payments[first_person][second_person] < payments[second_person][first_person]:
            print(f"{persons[second_person]}->{persons[first_person]}: {payments[second_person][first_person] - payments[first_person][second_person]}원")
        else:
            pass # 주고 받을 돈이 같을 경우 아무 동작도 하지 않음.
