import pygame
import time
import random
from CompleteSnakeClass import Snake 
from CompleteSnakeClass import Food
import numpy as np
import pickle
import math 

LEARNING_RATE = 0.5

DISCOUNT = 0.95
EPISODES = 10
SHOW_EVERY = 1
snake_block = 10
snake_speed = 10

epsilon = 0  # not a constant, qoing to be decayed
START_EPSILON_DECAYING = 1
END_EPSILON_DECAYING = EPISODES
epsilon_decay_value = epsilon/(END_EPSILON_DECAYING - START_EPSILON_DECAYING)

DISCRETE_OS_SIZE = [15, 10]
discrete_os_win_size = 10

file = open("QlearningCompleteSnake/SnakeQtable.pkl",'rb')
q_table = pickle.load(file)
file.close()
'''
q_table = {}
for i in range(-15, 15):
    for ii in range(-10, 10):
        for iii in range(-15,15):
            for iiii in range(-10,10):
                q_table[(i, ii), (iii, iiii)] = [np.random.uniform(-3, 0) for i in range(4)]
'''

def get_discrete_state(snake, food, centerofmass):
    discrete_state = (int((food[0]-snake[0])/10), int((food[1]-snake[1])/10))
    return (tuple(discrete_state), centerofmass)

def caldistance(snake,food):
    distance = math.sqrt((snake[0]-food[0])**2 + (snake[1]-food[1])**2)
    return float(distance) 



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
 

 
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

reward = 0


def gameLoop():
    snake = Snake(black, snake_block, 1)
    food = Food(green, snake_block)
    for episode in range(EPISODES):
        global epsilon
        current_state = get_discrete_state(snake.position, food.position, snake.centerofmass())
        game_over = False
        current_distance = caldistance(snake.position, food.position)
        while not game_over:
            r1 = 0 
            r2 = 0 
            r3 = 0
            global reward

            if np.random.random() > epsilon:
                # Get action from Q table
                action = np.argmax(q_table[current_state])
            else:
                # Get random action
                action = np.random.randint(0, 4)
            
            
            snake.move(action)
            snake.updateposition()
            new_state = get_discrete_state(snake.position, food.position, snake.centerofmass())
            new_distance = caldistance(snake.position, food.position)

            
            if new_distance == 0:
                r1 = 50
                food.restart()
                snake.length +=1 
                print('point')

            else: 
                r1 = 0
            if new_distance > current_distance:
                r2 = -1
            elif new_distance < current_distance:
                r2 = 1
            
            if snake.checksuicide():
                r3 = -50
                reward = r1 + r2 + r3 
                max_future_q = np.max(q_table[new_state])

                # Current Q value (for current state and performed action)
                current_q = q_table[current_state][action]

                # And here's our equation for a new Q value for current state and action
                new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT * max_future_q)

                # Update Q table with new Q value
                q_table[current_state][action] = new_q
                
                current_distance = new_distance
                
                current_state = new_state
                snake.reset()
                game_over = True
            else: 
                r3 = 0
            reward = r1 + r2 + r3 
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
            current_distance = new_distance
            current_state = new_state
            
        
        if END_EPSILON_DECAYING >= episode >= START_EPSILON_DECAYING:
            epsilon -= epsilon_decay_value
        print(episode)
    output = open('QlearningCompleteSnake/SnakeQtable.pkl', 'wb')
    pickle.dump(q_table, output)
    output.close()
    pygame.quit()
    quit()
 

gameLoop()