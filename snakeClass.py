import pygame
import time
import random
 
pygame.init()
 
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
 
dis_width = 600
dis_height = 400
 
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game by Edureka')
 
clock = pygame.time.Clock()
 
snake_block = 10
snake_speed = 15
 
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

reward = 0
class Snake:
    x1 = dis_width/2
    y1 = dis_height/2
    x1_change = 0
    y1_change = 0

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
    
    def checkposition(self):
        if self.x1 >= dis_width or self.x1 < 0 or self.y1 >= dis_height or self.y1 < 0:
            return True
        else: 
            return False
class Food:
     foodx = round(random.randrange(0, dis_width - 10) / 10.0) * 10.0
     foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

     def __init__(self, color, size):
        self.color = color
        self.size = size 
        self.step = size
    
     def start(self):
        pygame.draw.rect(dis, self.color, [self.foodx, self.foody, self.size, self.size])

def gameLoop():
    game_over = False
    snake = Snake(black, snake_block)
    food = Food(green, snake_block)
   
    
    while not game_over:  
        global reward
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:   
                if event.key == pygame.K_LEFT:
                    snake.left()
                if event.key == pygame.K_RIGHT:
                    snake.right()
                if event.key == pygame.K_UP:
                    snake.up()
                if event.key == pygame.K_DOWN:
                    snake.down()

        if snake.checkposition():     
            reward = 0
            print(reward) 
            gameLoop()
            

        if snake.x1 == food.foodx and snake.y1 == food.foody:
            reward = 1
            print(reward) 
            gameLoop()
             
        dis.fill(white)
        snake.updateposition()
        snake.start()
        food.start()
        pygame.display.update()
 
        clock.tick(snake_speed)
    
    pygame.quit()
    quit()
 

gameLoop()