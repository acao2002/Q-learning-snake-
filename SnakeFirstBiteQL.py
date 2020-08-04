import pygame
import time
import random
from snakeClass import Snake 
from snakeClass import Food
import numpy as np

LEARNING_RATE = 0.1

DISCOUNT = 0.95
EPISODES = 100
SHOW_EVERY = 5

DISCRETE_OS_SIZE = [30, 20, 30, 20]
discrete_os_win_size = 10

q_table = np.random.uniform(low = -1, high = 1, size = (DISCRETE_OS_SIZE + [4]))

def get_discrete_state(snake, food):
    combine = (snake + food)
    discrete_state = tuple( t/10 for t in combine)
    return discrete_state

epsilon = 1  # not a constant, qoing to be decayed
START_EPSILON_DECAYING = 1
END_EPSILON_DECAYING = EPISODES//2
epsilon_decay_value = epsilon/(END_EPSILON_DECAYING - START_EPSILON_DECAYING)

pygame.init()
 
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
 
dis_width = 300
dis_height = 200
 
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game by An Cao')
 
clock = pygame.time.Clock()
 
snake_block = 10
snake_speed = 15
 
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

reward = 0


def gameLoop():
    snake = Snake(black, snake_block)
    food = Food(green, snake_block)
   
    for episode in range(EPISODES):
        current_state = get_discrete_state(snake.position, food.position)
        game_over = False
        while not game_over: 
            global reward

            if np.random.random() > epsilon:
                # Get action from Q table
                act = np.argmax(q_table[discrete_state])
            else:
                # Get random action
                act = np.random.randint(0, 3)
            
            print(act)
            snake.move(act)
            snake.updateposition()
            new_state = get_discrete_state(snake.position, food.position)
           
            if snake.checkposition():     
                reward = -1
                snake.reset()
                game_over = True
                

            if snake.x1 == food.foodx and snake.y1 == food.foody:
                reward = 1
                snake.reset()
                game_over = True
                
            dis.fill(white)
            snake.start()
            food.start()
            if episode % SHOW_EVERY == 0:
                pygame.display.update()
                print(current_state)
                print(new_state)
            clock.tick(snake_speed)
        
    pygame.quit()
    quit()
 

gameLoop()