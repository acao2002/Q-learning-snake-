import random
import pygame
import math
dis_width = 450
dis_height = 300
snake_block = 10
dis = pygame.display.set_mode((dis_width, dis_height))
class Snake:
    x1 = 350
    y1 = 150
    x1_change = 0
    y1_change = 0
    position = (x1,y1)
    leftP = (x1-10,y1)
    rightP = (x1+10,y1)
    upP = (x1,y1+10)
    downP =(x1, y1-10)  
    def __init__(self, color, size, initiallength):
        self.color = color
        self.size = size 
        self.step = size
        self.initallength = initiallength
        self.length = self.initallength
        self.snakelist = [self.position]
    
    def start(self):
        for i in self.snakelist:
            pygame.draw.rect(dis, self.color, [i[0], i[1], self.size, self.size])

    def left(self): 
        self.x1_change = -self.step
        self.y1_change = 0
    
    def right(self): 
        self.x1_change = self.step
        self.y1_change = 0
    
    def up(self): 
        self.y1_change = -self.step
        self.x1_change = 0
    
    def down(self): 
        self.y1_change = self.step
        self.x1_change = 0
    
    def updateposition(self):
        self.x1 += self.x1_change
        self.y1 += self.y1_change
        self.position =(self.x1,self.y1)
        self.snakelist.append(self.position)
        if len(self.snakelist) > self.length:
            del(self.snakelist[0])

        self.leftP = (self.x1-10,self.y1)
        self.rightP = (self.x1+10,self.y1)
        self.upP = (self.x1,self.y1+10)
        self.downP =(self.x1, self.y1-10)
    
    def checkposition(self):
        check = False 
        for x in self.snakelist[:-1]:
            if x == self.position:
                check = True
        if self.x1 >= dis_width or self.x1 < 0 or self.y1 >= dis_height or self.y1 < 0 or check:
            return True
        else: 
            return False

    def reset(self):
        self.x1 = 350
        self.y1 = 150
        self.x1_change = 0
        self.y1_change = 0
        self.position = (self.x1,self.y1)
        self.length = self.initallength
        self.snakelist=[self.position]
        self.leftP = (self.x1-10,self.y1)
        self.rightP = (self.x1+10,self.y1)
        self.upP = (self.x1,self.y1+10)
        self.downP =(self.x1, self.y1-10)

    def move(self, action):
        if action == 0:
            self.left()
        if action == 1:
            self.right()
        if action == 2:
            self.up()
        if action == 3:
            self.down()
    
    def checksurrounding(self):
        l = 0
        r = 0 
        t = 0 
        d = 0 
        for x in self.snakelist[:-1]:
            if x == self.leftP:
                l = 1 
            if x == self.rightP:
                r = 1
            if x == self.upP:
                t = 1
            if x == self.downP:
                d = 1
        if self.rightP[0] >= dis_width:
            r = 1 
        if self.leftP[0] < 0:
            l = 1
        if self.upP[1] >= dis_height:
            t = 1
        if self.downP[1] < 0:
            d = 0

        return(l,r,t,d)

class Food:
     x1 = round(random.randrange(0, dis_width - 20) / 10.0) * 10.0
     y1 = round(random.randrange(0, dis_height - 20) / 10.0) * 10.0
     position = (x1,y1)
     def __init__(self, color, size):
        self.color = color
        self.size = size 
        self.step = size
    
     def start(self):
        pygame.draw.rect(dis, self.color, [self.x1, self.y1, self.size, self.size])

     def restart(self): 
        self.x1 = round(random.randrange(0, dis_width - 20) / 10.0) * 10.0
        self.y1 = round(random.randrange(0, dis_height - 20) / 10.0) * 10.0
        self.position = (self.x1, self.y1)

