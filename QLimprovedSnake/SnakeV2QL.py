import pygame
import time
import random
from V2SnakeClass import Snake 
from V2SnakeClass import Food
import numpy as np
import pickle
import math 


LEARNING_RATE = 0.3
DISCOUNT = 0.93
EPISODES = 10000
SHOW_EVERY = 5000
snake_block = 10
snake_speed = 100000
snake_speedshow = 30

epsilon = 1 # not a constant, qoing to be decayed
START_EPSILON_DECAYING = 1
END_EPSILON_DECAYING = EPISODES
epsilon_decay_value = epsilon/(END_EPSILON_DECAYING - START_EPSILON_DECAYING)

DISCRETE_OS_SIZE = [15, 10]
discrete_os_win_size = 10

file = open("QlimprovedSnake/SnakeQtable.pkl",'rb')
q_table = pickle.load(file) #load exisiting qtable
file.close()

#train snake from initialized q table

# q_table = {}
# for i in range(0, 2):
#     for ii in range(0, 2):
#         for iii in range(0,2):
#             for iiii in range(0,2):
#                 for iiiii in range(0,8):
#                     q_table[(i, ii,iii,iiii), (iiiii)] = [np.random.uniform(-5, 0) for i in range(4)]

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

def get_discrete_state(snake, food, surrounding):
    state = findRelativeP(snake,food)
    return (surrounding, state)

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
screen_height = 400 
dis_width = 450
dis_height = 300
 
dis = pygame.display.set_mode((dis_width, screen_height))
pygame.display.set_caption('Snake Game by An Cao')
 
clock = pygame.time.Clock()
 
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 20)

reward = 0


def gameLoop():
    snake = Snake(black, snake_block, 1)
    food = Food(green, snake_block)
    scores = [] 
    count = 0 
    for episode in range(EPISODES):
        global epsilon
        current_state = get_discrete_state(snake, food, snake.checksurrounding())
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
            new_state = get_discrete_state(snake, food, snake.checksurrounding())
            new_distance = caldistance(snake.position, food.position)

            
            if new_distance == 0:
                r1 = 50
                food.restart()
                snake.length +=1 
                #print('point')

            else: 
                r1 = 0
            if new_distance > current_distance:
                r2 = -1
            elif new_distance < current_distance:
                r2 = 1
            
            if snake.checkposition():
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
                if count % 10 == 0:
                    scores.append(snake.length)
                #scores keep track of snake performance overtime
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
            
            dis.fill(white)
            if episode % SHOW_EVERY == 0:
                pygame.draw.rect(dis, black, (0, 0, 450, 300), 3) 
                textsurface = myfont.render(('generation: '+ (str(episode))), False, (0, 0, 0))  
                score = myfont.render(('score: '+ (str(snake.length))), False, (0, 0, 0))  
                dis.blit(textsurface,(20,320))
                dis.blit(score, (300,320))
                snake.start()
                food.start()
                pygame.display.update()
                clock.tick(snake_speedshow)
            else:
                clock.tick(snake_speed)
            current_distance = new_distance
            current_state = new_state
               
        count +=1
 
        if count % 500 == 0:
            print(scores)
        if END_EPSILON_DECAYING >= episode >= START_EPSILON_DECAYING:
            epsilon -= epsilon_decay_value
        print(episode)
       
    output = open('QlimprovedSnake/SnakeQtable.pkl', 'wb')
    pickle.dump(q_table, output)
    output.close()
    pygame.quit()
    quit()

 

gameLoop()