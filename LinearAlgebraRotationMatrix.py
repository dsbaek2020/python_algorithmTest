#회전행렬을 이용한 이미지데이터 회전하기
#준비물:
   #라즈베리파이 + SenseHat Board
#만든사람: KYL, BDS
#아직 라즈베리파 센스햇에 되지 않습니다. (알고리즘 만들 있는중)
  
import math

print('hello')
b = (0, 0, 0)
r = (100, 0, 0)

figIn = [[b, b, b, b, b, b, b, b], 
         [b, b, b, b, b, b, b, b],
         [b, b, b, b, b, b, b, b], 
         [b, b, r, r, r, b, b, b],
         [b, b, r, r, r, b, b, b], 
         [b, b, r, r, r, b, b, b],
         [b, b, b, b, b, b, b, b], 
         [b, b, b, b, b, b, b, b]]
figOut = [[]]

th = 45

i = 0
j = 0

color = figIn[i][j]

x = j-3
y = -i+3



v = np.array([[x],[y]])

v1x = math.cos(math.radians(th))
v1y = math.sin(math.radians(th))
v2x = -1 * math.sin(math.radians(th))
v2y = math.cos(math.radians(th))

M = np.array([[v1x, v2x], [v1y, v2y]])

v_out = M.dot(v)
print (v)

print (v_out)
