import random
import pygame
 
dis_width = 250
dis_height = 200
snake_block = 10
dis = pygame.display.set_mode((dis_width, dis_height))
class Snake:
    x1 = dis_width/2
    y1 = dis_height/2
    x1_change = 0
    y1_change = 0
    position = (x1,y1)
    def __init__(self, color, size):
        self.color = color
        self.size = size 
        self.step = size
    
    def start(self):
        pygame.draw.rect(dis, self.color, [self.x1, self.y1, self.size, self.size])

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
    
    def checkposition(self):
        if self.x1 >= dis_width or self.x1 < 0 or self.y1 >= dis_height or self.y1 < 0:
            return True
        else: 
            return False
    def reset(self):
        self.x1 = dis_width/2
        self.y1 = dis_height/2
        self.x1_change = 0
        self.y1_change = 0
        self.position = (self.x1,self.y1)

    def move(self, action):
        if action == 0:
            self.left()
        if action == 1:
            self.right()
        if action == 2:
            self.up()
        if action == 3:
            self.down()
     

class Food:
     foodx = 120
     foody = 20
     position = (foodx,foody)
     def __init__(self, color, size):
        self.color = color
        self.size = size 
        self.step = size
    
     def start(self):
        pygame.draw.rect(dis, self.color, [self.foodx, self.foody, self.size, self.size])

     def restart(self): 
        self.foodx = round(random.randrange(0, dis_width - 10) / 10.0) * 10.0
        self.foody = round(random.randrange(0, dis_height - 10) / 10.0) * 10.0
        self.position = (self.foodx, self.foody)

