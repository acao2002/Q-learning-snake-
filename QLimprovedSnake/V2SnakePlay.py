import pickle 
import pygame
import time
import random
from V2SnakeClass import Snake 
from V2SnakeClass import Food
import numpy as np


pkl_file = open("QlimprovedSnake/SnakeQtable.pkl",'rb')

q_table = pickle.load(pkl_file)

pygame.init()
 
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
screen_height = 400 
dis_width = 450
dis_height = 300
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 20)
 
dis = pygame.display.set_mode((dis_width, screen_height))
pygame.display.set_caption('Snake Game by An Cao')
 
clock = pygame.time.Clock()
 
snake_block = 10
snake_speed = 20

def findRelativeP(snake, food):
    state = 0 
    if snake.x1 < food.x1 and snake.y1 < food.y1:
        state = 0
    if snake.x1 == food.x1 and snake.y1 < food.y1:
        state = 1
    if snake.x1 > food.x1 and snake.y1 < food.y1:
        state = 2
    if snake.x1 > food.x1 and snake.y1 == food.y1:
        state = 3 
    if snake.x1 > food.x1 and snake.y1 > food.y1:
        state = 4
    if snake.x1 == food.x1 and snake.y1 > food.y1:
        state = 5
    if snake.x1 < food.x1 and snake.y1 > food.y1:
        state = 6 
    if snake.x1 < food.x1 and  snake.y1 == food.y1:
        state = 7 
    return state

def checkfoodP(snake,food):
    for x in snake.snakelist: 
        if x == food.position:
            food.restart()
            checkfoodP(snake,food)
        else:
            pass

def get_discrete_state(snake, food, surrounding):
    state = findRelativeP(snake,food)
    return (surrounding, state)
def gameLoop():
    snake = Snake(black, snake_block, 1)
    food = Food(green, snake_block)
    current_state = get_discrete_state(snake, food, snake.checksurrounding())
    game_over = False
    
    while not game_over: 
            action = np.argmax(q_table[current_state])
            snake.move(action)
            snake.updateposition()     
            new_state = get_discrete_state(snake, food, snake.checksurrounding())  
            if snake.position == food.position:       
                food.restart()
                checkfoodP(snake,food)
                snake.length += 1
            if snake.checkposition():     
                game_over = True 
            dis.fill(white)
            snake.start()
            food.start()
            pygame.draw.rect(dis, black, (0, 0, 450, 300), 3) 
            textsurface = myfont.render(('generation: 10000 '), False, (0, 0, 0))  
            score = myfont.render(('score: '+ (str(snake.length))), False, (0, 0, 0))  
            dis.blit(textsurface,(20,320))
            dis.blit(score, (300,320))
            pygame.display.update()
            clock.tick(snake_speed)
            current_state = new_state
gameLoop()