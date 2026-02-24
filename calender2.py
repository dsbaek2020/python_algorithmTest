# 간단한 달력 출력 프로그램
# - 사용자로부터 년도와 월을 입력받아 해당 달의 달력을 콘솔에 출력합니다.
# - Python의 datetime 모듈로 해당 달의 첫 요일을 계산합니다.
# - 윤년 여부를 판단하여 2월의 일수를 자동으로 조정합니다.

import datetime

# 각 달의 기본 일수 목록 (평년 기준). 인덱스 0이 1월, 11이 12월을 의미합니다.
month_days_list = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

# 월 약어 목록. 출력 시 가독성을 위해 사용합니다.
month_abbr_list = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', \
                   'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

# 요일에 따른 첫 주에 출력해야 할 칸 수를 정의합니다.
# 예: 'sun': 7 은 첫날이 일요일이면 첫 주에 7칸(일~토)을 채운다는 의미입니다.
firstWeekDays = {"sun": 7,
                 "mon": 6,
                 "tue": 5,
                 "wed": 4,
                 "thu": 3,
                 "fri": 2,
                 "sat": 1}

# 사용자로부터 년도와 월을 입력받습니다. 문자열 입력을 정수로 변환합니다.
years = int(input("Enter year (e.g., 2026): "))
month = int(input("Enter month (1-12): "))

# 윤년 판별 로직
# - 4로 나누어떨어지고 100으로 나누어떨어지지 않으면 윤년
# - 또는 400으로 나누어떨어지면 윤년
# 윤년인 경우 2월의 일수를 29일로 설정합니다.
if (years % 4 == 0 and years % 100 != 0) or (years % 400 == 0):
    month_days_list[1] = 29
else:
    month_days_list[1] = 28

# 입력된 년/월의 1일 날짜 객체를 생성하고, 해당 요일을 구합니다.
first_day_of_month = datetime.date(years, month, 1)
weekday_int = first_day_of_month.weekday() # 월요일=0, 일요일=6의 정수 값

# datetime.weekday()가 반환하는 정수(0~6)를 요일 문자열로 매핑합니다.
weekdays_map = {
    0: "mon",
    1: "tue",
    2: "wed",
    3: "thu",
    4: "fri",
    5: "sat",
    6: "sun"
}

# 해당 달 1일의 요일 문자열(예: 'mon', 'tue')
one_day = weekdays_map[weekday_int]

# 첫 주에서 1일 앞에 필요한 공백 칸 수를 계산합니다.
# (일~토 7칸 중, 첫날 요일에 따라 앞쪽 빈 칸을 채움)
firstWeek_space = 7 - firstWeekDays[one_day]

# 출력 루프를 위한 주(week)와 일(day) 카운터 초기화
week = 1
day = 1

# 공백 칸(n개)을 출력하는 보조 함수. 각 칸은 4칸 폭으로 맞춥니다.
def printSpace(n):
  for i in range(n):
    print("    ", end="")

# 달력 헤더 출력 (년도와 월)
print(f"{years} {month_abbr_list[month-1]}")

# 요일 행 출력 (일~토). 이 스크립트는 일요일 시작 형식을 사용합니다.
print("sun mon tue wed thu fri sat")

# 첫 주 시작 전에 필요한 공백 칸을 먼저 출력합니다.
printSpace(firstWeek_space)

# 해당 월의 마지막 날까지 주 단위로 줄바꿈하며 날짜를 출력합니다.
while day <= month_days_list[month-1]:
  # 첫 주는 첫날의 요일에 맞는 칸 수만큼만 출력하고,
  # 이후 주부터는 항상 7칸(일~토)을 출력합니다.
  if week == 1:
    day_of_week = firstWeekDays[one_day]
  else:
    day_of_week = 7

  for i in range(day_of_week):
    # 한 자리 수와 두 자리 수의 폭을 맞추기 위해 언더스코어로 패딩합니다.
    if day<10:
      print(f"{day}___", end="")
    else:
      print(f"{day}__", end="")

    day = day + 1
    # 해당 월의 마지막 날짜를 넘으면 루프를 종료합니다.
    if day > month_days_list[month-1]:
      break

  # 다음 주로 넘어가며 줄바꿈
  week = week + 1
  print()

