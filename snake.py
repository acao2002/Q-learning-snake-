import pygame
import random 

pygame.init()


white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
dis_height = 600
dis_width = 800

dis=pygame.display.set_mode((dis_width,dis_height))
pygame.display.update()
pygame.display.set_caption('Snake game by Andrew')

game_over=False

x1 = dis_width/2
y1 = dis_height/2
 
x1_change = 0       
y1_change = 0
snake_block = 10

foodx = round(random.randrange(0, dis_width - 10) / 10.0) * 10.0
foody = round(random.randrange(0, dis_width - 10) / 10.0) * 10.0
clock = pygame.time.Clock()



while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x1_change = -10
                y1_change = 0
            elif event.key == pygame.K_RIGHT:
                x1_change = 10
                y1_change = 0
            elif event.key == pygame.K_UP:
                y1_change = -10
                x1_change = 0
            elif event.key == pygame.K_DOWN:
                y1_change = 10
                x1_change = 0
   

    if x1>800:
        x1 = 10;

    if x1 < 0:
        x1 = 790;

    if y1>600:
        y1 = 10;

    if y1 < 0:
        y1 = 790; 
     
     
    x1 += x1_change
    y1 += y1_change
    if x1 == foodx and y1 == foody:
        foodx = round(random.randrange(10, dis_width - snake_block) / 10.0) * 10.0
        foody = round(random.randrange(10, dis_width - snake_block) / 10.0) * 10.0

    dis.fill(white)
    pygame.draw.rect(dis, black, [x1, y1, 10, 10])
    pygame.draw.rect(dis, red, [foodx, foody, 10, 10])
    pygame.display.update()
 
    clock.tick(30)
 
pygame.quit()
quit()