# 프로젝트 설명

- [csv\_to\_ics\_sleep](csv_to_ics_sleep.py)는 애플 건강 앱에 내보낸 수면 데이터(csv 파일)를 비수면, 깊은 수면, 얕은 수면, 수면 시간 등의 정보를 담은 ics 파일로 만든다.
- [csv\_to\_ics 파일\_timemator](csv_to_ics_timemator.py)는 timemator 앱에서 내보낸 세션 데이터(csv 파일)를 세션의 시간 등의 정보를 담은 ics 파일로 만든다.
- [csv\_to\_ics 파일\_walking](csv_to_ics_walking.py)는 건강 앱에 내보낸 걷기 데이터(csv 파일)를 걸은 거리, 걸은 시간 등의 정보를 담은 ics 파일로 만든다.

# 에러

- 위 파일들에서 만든 ics 파일은 공통적으로 애플 캘린더에서 오류로 인식된다. 소스 코드 수정, ics 공부 등을 통해 에러를 고치면 좋다.
- [HKCategoryTypeIdentifierSleepAnalysis\_2023-12-351\_17-16-51\_SimpleHealthExportCSV](HKCategoryTypeIdentifierSleepAnalysis_2023-12-351_17-16-51_SimpleHealthExportCSV.csv)는 애플 건강 앱에 내보낸 수면 데이터(csv 파일)의 예이다.
