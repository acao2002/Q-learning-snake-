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

dis_width = 150
dis_height = 100

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

        snake.updateposition()
        print(snake.position)
        print(food.position)
        if snake.checkposition():     
            reward = 0
            print(reward) 
            snake.reset()

        
        if snake.position == food.position:
            reward = 1
            food.restart()

        dis.fill(white)
        snake.start()
        food.start()
        pygame.display.update()
        
        clock.tick(snake_speed)

    pygame.quit()
    quit()


gameLoop() 