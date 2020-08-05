import pygame
import time
import random
from snakeClass import Snake 
from snakeClass import Food
import numpy as np
import pickle
import math 

LEARNING_RATE = 0.1

DISCOUNT = 0.95
EPISODES = 200
SHOW_EVERY = 1

DISCRETE_OS_SIZE = [15, 10]
discrete_os_win_size = 10

q_table = {}

for i in range(-14, 15):
    for ii in range(-9, 10):
        q_table[(i, ii)] = [np.random.uniform(-3, 0) for i in range(4)]


def get_discrete_state(snake, food):
    discrete_state = (int((food[0]-snake[0])/10), int((food[1]-snake[1])/10))
    return tuple(discrete_state)

def caldistance(snake,food):
    distance = math.sqrt((snake[0]-food[0])**2 + (snake[1]-food[1])**2)
    return float(distance) 

epsilon = 1  # not a constant, qoing to be decayed
START_EPSILON_DECAYING = 1
END_EPSILON_DECAYING = EPISODES
epsilon_decay_value = epsilon/(END_EPSILON_DECAYING - START_EPSILON_DECAYING)

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
    snake = Snake(black, snake_block)
    food = Food(green, snake_block)
   
    for episode in range(EPISODES):
        global epsilon
        current_state = get_discrete_state(snake.position, food.position)
        game_over = False
        current_distance = caldistance(snake.position, food.position)
        while not game_over:
            r1 = 0 
            r2 = 0 
            global reward

            if np.random.random() > epsilon:
                # Get action from Q table
                action = np.argmax(q_table[current_state])
            else:
                # Get random action
                action = np.random.randint(0, 4)
            
            
            snake.move(action)
            snake.updateposition()
            new_state = get_discrete_state(snake.position, food.position)
            new_distance = caldistance(snake.position, food.position)
            
            if snake.position == food.position:
                r1 = 5
                food.restart()
                print('point')
            else: 
                r1 = 0
            if new_distance > current_distance:
                r2 = -0.2
            elif new_distance < current_distance:
                r2 = 0.2
            
            reward = r1 + r2 

            if not game_over:

                max_future_q = np.max(q_table[new_state])

                # Current Q value (for current state and performed action)
                current_q = q_table[current_state][action]

                # And here's our equation for a new Q value for current state and action
                new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT * max_future_q)

                # Update Q table with new Q value
                q_table[current_state][action] = new_q

            if snake.checkposition():     
                snake.reset()
                game_over = True
                
            dis.fill(white)
            if episode % SHOW_EVERY == 0:
                snake.start()
                food.start()
                pygame.display.update()
            clock.tick(snake_speed)
            current_state = new_state
            new_distance = current_distance
        
        if END_EPSILON_DECAYING >= episode >= START_EPSILON_DECAYING:
            epsilon -= epsilon_decay_value
        print(episode)
    output = open('data.pkl', 'wb')
    pickle.dump(q_table, output)
    output.close()
    pygame.quit()
    quit()
 

gameLoop()