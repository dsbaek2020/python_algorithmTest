


from turtle import Turtle
from random import randint
from time import sleep
from math import sqrt

r = 150

#pen = turtle.Turtle()

dart_arrow = Turtle()

dart_arrow.penup()
dart_arrow.goto(0,0)
#pen.goto(100,100)
#pen.dot(10, 'red')
#import random
#x = random.randrange(0, 151)
#y = random.randrange(0, 151)


#import math

t = sqrt(1)
'''
for i in range(100):
  x = randint(0, 150)
  y = randint(0, 150)
  dart_arrow.goto(x, y)
  dart_arrow.dot(10, 'red')
'''

totalDot = 100
i =0
while i<totalDot:
  x = randint(0, r)
  y = randint(0, r)
  distance = sqrt(x**2 + y**2)
  dart_arrow.goto(x, y)
  if distance <= r:
    dart_arrow.dot(10, 'red')

  else:
    dart_arrow.dot(10, 'green')
  i = i+1


