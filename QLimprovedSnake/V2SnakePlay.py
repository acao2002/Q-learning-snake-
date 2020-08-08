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
 
dis_width = 750
dis_height = 300
 
dis = pygame.display.set_mode((dis_width, dis_height))
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
            checkfood(snake,food)
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
            pygame.display.update()
            clock.tick(snake_speed)
            current_state = new_state
gameLoop()