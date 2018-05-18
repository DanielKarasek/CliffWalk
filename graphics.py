from tkinter import *
from math import * 
import numpy as np
import time

def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
Canvas.create_circle = _create_circle

class Graphics:

    def __init__(self,grid,agent):
        self.grid = np.array(grid)
        self.agent = agent
        self.back,self.factor,self.resolution = self.createBack()
        self.drawMap()
        
    
    def polar2Cart(self,angle,length):
        angle = angle *(pi/180)
        x = cos(angle) * length 
        y = sin(angle) * length 
        return np.array([x,y])


    def triangle(self,point1,sideLen,rotation,color = "red"):
        firstAngle = -135-rotation
        secondAngle = -270-rotation

        
        point1 = np.asarray(point1)
        point2 = np.asarray(point1 + self.polar2Cart(firstAngle,sideLen))
        point3 = np.asarray(point2 + self.polar2Cart(secondAngle,sideLen *sqrt(2)))
        x1,y1 = point1
        x2,y2 = point2
        x3,y3 = point3
        
        self.back.create_polygon(x1,y1,x2,y2,x3,y3,fill = color,outline = "black")



    def getHexa(self,value):
        hexaInStr = str(hex(int(value)))
        hexaInStr = hexaInStr[-2:]
        return hexaInStr if hexaInStr[0] != "x" else "0"+hexaInStr[1]

    def getRG(self,value,maximum,minimum):
        factorRG = self.factor
        value -= (maximum+minimum)/2
        newMaxMin = maximum-(maximum+minimum)/2
        factorRG = 255/newMaxMin
        value = -newMaxMin if value<-newMaxMin else newMaxMin if value>newMaxMin else value
        value *= self.factor
        other = 255-abs(value)

        
        strVal = "ff"
        strOther = self.getHexa(other)
       
        if value < 0:
            return "#"+strVal+ 2* strOther
        else:
            return "#"+ strOther + strVal + strOther
        
    

    def drawQTriangle(self,values,position):
        #-90 90 0 180 == up,down,left,right
        position = np.array(position)
        rotations = [-90,90,0,180]
        halfFactor = self.factor/2 +2
        origin = (position * self.factor) + halfFactor


        tmp = origin [0]
        origin[0] = origin[1]
        origin[1] = tmp
        
        for value,rotation in zip(values,rotations):
            color = self.getRG(value,1,-1)
            self.triangle(origin,self.factor/sqrt(2),rotation,color)

        origin = (position * self.factor)+2
        
        diffY = self.factor/5
        diffX = self.factor/5
        startY = self.factor/2
        startX = self.factor/2
        
        self.back.create_text(origin[1]+startX,origin[0]+diffY,font = "Palatino 12 bold",text = round(values[0],2))
        self.back.create_text(origin[1]+startX,origin[0]+self.factor-diffY,font = "Palatino 12 bold",text = round(values[1],2))
        self.back.create_text(origin[1]+diffX,origin[0]+startY,font = "Palatino 12 bold",text = round(values[2],2))
        self.back.create_text(origin[1]+self.factor - diffX,origin[0]+startY,font = "Palatino 12 bold",text = round(values[3],2))
            
    def drawAgent(self,position):
        y = position[0] * self.factor + self.factor/2 + 2
        x = position[1] * self.factor + self.factor/2 + 2
        self.back.create_circle(x,y,self.factor * 0.1,fill = "#0000ff")

    def drawMap(self):
        shape = self.grid.shape

        self.back.delete("all")
        
        step = self.factor
        beginning = 2
        for x in range(shape[1]+1):
            self.back.create_line(beginning,0,beginning,self.resolution[1])
            beginning += step
        
        beginning = 2
        for x in range(shape[0]+1):
            self.back.create_line(0,beginning,self.resolution[0],beginning)
            beginning += step

        borderIndices = np.where(self.grid == 1)
        borderIndices = np.column_stack(borderIndices)

        for position in borderIndices:
            posY = (position[0])*self.factor+2
            posX = (position[1])*self.factor+2
            posYPlus = (position[0]+1)*self.factor+2
            posXPlus = (position[1]+1)*self.factor+2
            self.back.create_rectangle(posX,posY,posXPlus,posYPlus,fill = "gray")
        

        spaceIndices = np.where(self.grid != 1)
        spaceIndices = np.column_stack(spaceIndices)
        
        for position in spaceIndices:

            values = self.agent.getValues(position)
            self.drawQTriangle(values,position)
        
    def update(self):
        self.root.update()


    def createBack(self):
        
        shape = self.grid.shape
        pixelCount = shape[0]*shape[1]*12000
        factor = int(sqrt(pixelCount/(shape[0]*shape[1])))
        
        self.root = Tk()

        
        sizeY = shape[0]*factor
        sizeX = shape[1]*factor
        
        background = Canvas(self.root,width = sizeX, height = sizeY)
        
        background.pack()
        

        return background,factor,[sizeX,sizeY]



