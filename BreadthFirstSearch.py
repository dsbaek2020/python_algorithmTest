#kimHY
#jelly coding

#이코드는 아래의 도서를 참고하여 완성하였습니다.
#제목: 그림으로 개념을 이해하는 알고리즘, 
   #  다디트야 바르가바(저), 김도형(역), 한빛미디어 출판사

from collections import deque
from time import sleep
checkList = deque()

friend = {} #딕셔너리 선언
friend['me'] = ['Kim Byung-ji', 'ParkJisung','Lee Eul-yong']
friend['ParkJisung'] = ['Park Na-rae', 'Huh Jae' ]
friend['Lee Eul-yong'] = ['Gomass', 'Backcom' ]
friend['Kim Byung-ji'] = ['Park Na-rae','Hong Myung-bo']
friend['Park Na-rae'] = []
friend['Huh Jae'] = []
friend['Gomass'] = []
friend['Backcom'] = []
friend['Hong Myung-bo'] = []

checkedList = []
 
# 6.망고판매상이 아닌 사람을 따로 분류한다 
# 7.망고판매상인지 확인하기 전에 망고판매상이 아닌 분류에 있는지 확인한다
#   7.1밍고판매상이 아닌 분류에 없으면 계속 진행한다
#   7.2망고판매사이 아닌 분류에 있으면 2번으로 돌아간다 

def checkMangoMen(name):
   if name[-1] == 'm':
     return True
   else: 
     return False


#무한반복한다.
# 1. 차트에 친구를 추가한다.
# 2. 차트(큐)에서 첫번째 사람의 이름을 빼낸다
# 3. 망고 판매상인지 확인다. 
# 4. 만약 망고 판매상이라면, 망고판매상임을 알려주고 프로그램을 종료한다.
#   4.1 망고판매상을 찾았다고 알려주고 그 친구 이름을 출력한다. 
#   4.2 braek 명령으로 무한반복에서 탈출한다. 
# 5. 아니면, 1번으로 돌아간다.  

person = 'me'
while True:

  checkList += friend[person]
  person = checkList.popleft()
   
  try:
    num = checkedList.index(person)
    print(person,'은 이미 확인한 사람입니다.', '그리고', num,'번째에 있습니다.')
  except:
    print ('지금',person,'검사','중','입니다' )
    if checkMangoMen(person) == True:
      print('망고판매상을 찾았습니다. 그사람이름은',person, '입니다.')
      break
    else:
      
      checkedList.append(person)
      sleep (0.75)

#outdata = a.get()
#print(outdata)

#while True:
  #if outdata < 10:
    #outdata = a.get()
    #print (outdata)
    #q = outdata + 1 
    #a.put (q)
  #else:
      #break
