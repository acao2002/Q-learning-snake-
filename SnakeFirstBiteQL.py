import pygame
import time
import random
from snakeClass import Snake 
from snakeClass import Food
 
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
pygame.display.set_caption('Snake Game by An Cao')
 
clock = pygame.time.Clock()
 
snake_block = 10
snake_speed = 15
 
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

reward = 0


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
        print(snake.position)
        clock.tick(snake_speed)
    
    pygame.quit()
    quit()
 

gameLoop()