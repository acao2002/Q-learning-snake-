import pickle 
import pygame
import time
import random
from CompleteSnakeClass import Snake 
from CompleteSnakeClass import Food
import numpy as np


pkl_file = open("QlearningCompleteSnake/SnakeQtable.pkl",'rb')

q_table = pickle.load(pkl_file)

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
snake_speed = 5

def get_discrete_state(snake, food, centerofmass):
    discrete_state = (int((food[0]-snake[0])/10), int((food[1]-snake[1])/10))
    return (tuple(discrete_state), centerofmass)

def gameLoop():
    snake = Snake(black, snake_block, 1)
    food = Food(green, snake_block)
    current_state = get_discrete_state(snake.position, food.position, snake.centerofmass())
    game_over = False
    while not game_over: 
            action = np.argmax(q_table[current_state])
            snake.move(action)
            snake.updateposition()     
            new_state = get_discrete_state(snake.position, food.position, snake.centerofmass())     
            if snake.position == food.position:       
                food.restart()
                snake.length += 1
            CenterSnake = snake.centerofmass()
            if snake.checksuicide():
                game_over = True
            if snake.checkposition():     
                game_over = True
                
            dis.fill(white)
            snake.start()
            food.start()
            pygame.display.update()
            clock.tick(snake_speed)
            current_state = new_state
gameLoop()