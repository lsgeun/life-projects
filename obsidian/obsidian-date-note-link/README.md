# 프로젝트 설명
## 빈 날짜 노트 생성
- [create\_empty\_note\_in\_year\_folder](create_empty_note_in_year_folder.py) 명령에 '저장 경로', '연도'를 입력하면 연도 폴더에 연도에 속한 빈 날짜 노트들을 생성한다.

## 날짜 노트에 관련 링크를 포함한 템플릿 삽입
- 막 코딩을 하며 아이디어를 얻은 후 이 아이디어들을 코드에 바로 활용할 수 있도록 [note\_content\_in\_year\_folder](note_content_in_year_folder.py)에 함수 형태로 잘 정리해두었다.
- [note\_content\_in\_year\_folder](note_content_in_year_folder.py)에 있는 함수를 활용하여 [insert\_template\_to\_note\_in\_year\_folder](insert_template_to_note_in_year_folder.py) 명령에 '저장 경로', '옵시디언 링크 경로', '연도'를 입력하면 연도 폴더에 있는 날짜 노트에 날짜 관련 링크를 포함한 템플릿 삽입한다. 즉, 연도 폴더에 있는 날짜 노트를 링크로 연결하고, 날짜 노트마다 있어야 하는 노트 템플릿을 작성한다.

## 연도 폴더에 날짜 노트 생성 및 링크 걸기
- [create\_empty\_note\_in\_year\_folder](create_empty_note_in_year_folder.py), [insert\_template\_to\_note\_in\_year\_folder](insert_template_to_note_in_year_folder.py) 순으로 파일을 실행하면 연도 폴더를 생성한 후 관련 날짜 노트를 모두 생성하고, 생성된 날짜 노트에 필요한 템플릿을 작성한 후 날짜 노트 간에 링크를 건다.

## 매개 변수 일치
- 위 두 파이썬 파일에 공통적으로 들어가는 '저장 경로'와 '연도'가 동일해야 한다. [insert\_template\_to\_note\_in\_year\_folder](insert_template_to_note_in_year_folder.py)의 매개변수인 '옵시디언 링크 경로'는 '저장 경로'가 옵시디언에서 링크로 사용될 때 쓰이는 경로이다.

# 모르는 개념을 익히기 위한 파일
    - [practice.ipynb](practice.ipynb), [monthly\_note\_test\_in\_year\_folder](monthly_note_test_in_year_folder.py)는 잡다한 코드들을 연습하기 위한 파이썬 파일이다.

# 달력
- [ISO 8601 - 위키백과, 우리 모두의 백과사전](https://ko.wikipedia.org/wiki/ISO_8601#Week_Dates)

## 한국 달력
- 한국 달력 주차 계산은 KS x ISO-8601을 따름
- 월요일이 주의 첫째 요일이다.
- 매월 첫째 주나 매년 첫째 주는 목요일을 포함한 주이다.
- 좀 더 일반화하여 표현하자면 어떤 년도의 날들이 해당 주에 4일 이상이 포함되면 그 주는 어떤 년도의 주이다. 비슷하게 어떤 달의 날들이 해당 주에 4일 이상이 포함되면 그 주는 어떤 달의 주이다.

## 미국 달력
- 미국 달력 주차 계산은 ANSI INCITS 30-1997 (R2008) and NIST FIPS PUB 4-2을 따른다고 함.
- 아마도 아래의 규칙인 거 같다.
    - 일요일이 주의 첫째 요일이다.
    - 어떤 년도의 날들이 해당 주에 포함하고 다음 년도의 1월 1일이 해당 주에 포함되지 않으면 그 주는 어떤 년도의 주이다.
    - 어떤 달의 날들이 해당 주에 포함하고 다음 달의 1일이 해당 주에 포함되지 않으면 그 주는 어떤 달의 주이다.
    - 어떤 년도의 주나 어떤 달의 주에 대한 설명은 추측이고 확실하지 않다.

# 그 밖에
- ISO 기준 1주가 월요일부터 시작하는 경우도 있기 때문에 일요일부터 시작하는 일반적인 1주와 다르다. 따라서, Periodic Note에서 ==ISO week인 WW== 말고 ==normal한 week인 ww==를 쓰는게 더 적합하다.
- [monthly note UI](monthly%20note%20UI.md)는 월간 노트에 있는 링크 템플릿을 임시로 적어본 거다.
