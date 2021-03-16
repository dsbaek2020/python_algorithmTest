'''
by : chasujin, dsbaek
'''

import math
from time import sleep


class rocketSim(object):

  def __init__(self, g,dt, v, id):
    self.g = g  # [m/s^2]
    self.v=  v  # [m/s]
    self.vx = 0   # [m/s]
    self.vy = 0   # [m/s]
    self.x =0     # [m]
    self.y =0     # [m]
    self.dt = dt
    self.angle = 0.0  #degree
    self.name = id
    self.final_Distance =0
    self.status = 'normal'


  def diplayData(self, externalData):
    print('g=', self.g)
    print('ex data = ', externalData)

  def __str__(self):
    return self.name+"="+"("+str(round(self.x,2))+","+str(round(self.y,2))+")"

  def inputAngle(self):
    self.angle= float(input(self.name+'로켓의 발사 각도[deg]를 입력하세요:')) 
    self.calcVxVy_TimeZero()
    

  def calcVxVy_TimeZero(self):
    radTh=math.radians(self.angle)
    self.vx=self.v*math.cos(radTh)
    self.vy=self.v*math.sin(radTh)

  def moveRocket(self):
    self.vy = self.vy +  self.g*self.dt
    self.x  = self.x  + self.vx*self.dt  
    self.y  = self.y  + self.vy*self.dt   
    sleep(self.dt)

  def set_finalDistance(self):
    self.final_Distance = self.x
    self.status = 'simulation end'

    

rocketA = rocketSim(-9.8,0.1, 10, '대한민국')
rocketB = rocketSim(-9.8,0.1, 10, '미국')


rocketA.inputAngle()
rocketB.inputAngle()

print('Start simulation')
while rocketA.status != 'simulation end'  or rocketB.status != 'simulation end':

  if rocketA.y <0:
    rocketA.set_finalDistance()
  else:
    rocketA.moveRocket()
    print(rocketA)

  if rocketB.y <0:
    rocketB.set_finalDistance()
  else:
    rocketB.moveRocket()
    print(rocketB)


print('End simulation')


print('---시뮬레이션 결과----------------------------')
print('---비행시간---')
print(rocketA.name,'로켓의 비행시간=', rocketA.x/rocketA.vx)
print(rocketB.name,'로켓의 비행시간=', rocketB.x/rocketB.vx)

print('---이동거리---')
print(rocketA.name,'로켓의 이동거리=', round(rocketA.final_Distance,1))
print(rocketB.name,'로켓의 이동거리=', round(rocketB.final_Distance,2))





'''
non-class type code 

g = -9.8  # [m/s^2]
v= 10.0  # [m/s]
vx = 0   # [m/s]
vy = 0   # [m/s]
x =0     # [m]
y =0     # [m]
dt = 0.1

angle = float(input('발사 각도[deg]를 입력하세요:')) 
radTh = math.radians(angle)
vx = v*math.cos(radTh)
vy = v*math.sin(radTh)

print('vx=',vx)

while y >= 0:
  vy = vy + g*dt

  x = x + vx*dt
  y = y + vy*dt

  print('vy=',vy, 'xy=',x,y )
  sleep(dt)


print('xy=',x,y)
print('비행시간=', x/vx)

'''
