from time import sleep

class Planet :  # Make planet class
    def __init__(self, iName, iRad, iM, iDist, iC) :
        self.__name = iName
        self.__radius = iRad
        self.__mass = iM
        self.__distance = iDist
        self.__x = self.__distance
        self.__y = 0
        self.__color = iC
        

        self.__pTurtle = turtle.Turtle()

        self.__pTurtle.color(self.__color)
        self.__pTurtle.shape("circle")

        self.__pTurtle.up()
        self.__pTurtle.goto(self.__x, self.__y)
        self.__pTurtle.down()

    def getName(self) :
         return self.__name

    def getRadius(self) :
         return self.__radius

    def getMass(self) :
         return self.__mass

    def getDistance(self) :
         return self.__distance

    def getVolume(self) :
         import math
         v = 4/3 * math.pi *self.__radius**3
         return v

    def getSurfaceArea(self) :
         import math
         sa = 4 * math.pi * self.__radius**2

    def getDensity(self) :
         d = self.__mass / self.getVolume()
         return d

    def setName(self, newName) :
        self.__name = newName

    def __str__(self) :
        return self.__name

    def __lt__(self, otherPlanet) :
        return self.__distance < otherPlanet.__distance

    def __gt__(self, otherPlanet) :
        return self.__distance > otherPlanet.__distance

    def getXPos(self) :
        return self.__x

    def getYPos(self) :
        return self.__y

class Sun : # Make sun class
    def __init__(self, iName, iRad, iM, iTemp) :
       self.__name = iName
       self.__radius = iRad
       self.__mass = iM
       self.__temp = iTemp
       self.__x = 0
       self.__y = 0

       self.__sTurtle = turtle.Turtle()
       self.__sTurtle.shape("circle")
       self.__sTurtle.color("orange")

    def getMass(self) :
        return self.__mass

    def __str__(self) :
        return self.__name
    def getXPos(self) :
        return self.__x

    def getYPos(self) :
        return self.__y
    
class SolarSystem : # Make solar class
    def __init__(self,width, height) : # make constructor 
        self.__theSun = None
        self.__planets = []
        self.__ssTurtle = turtle.Turtle()
        self.__ssTurtle.hideturtle()
        self.__ssScreen = turtle.Screen()
        self.__ssScreen.setworldcoordinates(-width/2.0, -height/2.0, width/2.0, height/2.0)

    def addPlanet(self, aPlanet) :
        self.__planets.append(aPlanet)

    def addSun(self, aSun) :
        self. __theSun = aSun

    def showPlanets(self) :
        for aPlanet in self.__planets:
            print(aPlanet)

    def freeze(self) :
        self.__ssScreen.exitonclick()

 
import turtle
ss = SolarSystem(2, 2)

sun = Sun("Sun", 5000, 10, 5800)
ss.addSun(sun)

m = Planet("Mercury", 19.5, 1000, .25, "sky blue")
ss.addPlanet(m)

m = Planet("Earth", 47.5, 5000, 0.3, "blue")
ss.addPlanet(m)

m = Planet("Mars", 50, 9000, 0.5, "red")
ss.addPlanet(m)

m = Planet("Jupiter", 100, 49000, 0.7, "brown")
ss.addPlanet(m)

ss.freeze()