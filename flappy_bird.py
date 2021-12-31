# py -m pip install -U pygame --user
import pygame 
from pygame.locals import *

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 864 
screen_height = 936

screen = pygame.display.set_mode((screen_width, screen_height)) # width, height 설정
pygame.display.set_caption('Flappy Bird') # title 설정

# load images
bg = pygame.image.load('images/bg.png')
ground_img = pygame.image.load('images/ground.png')

# 변수 선언
ground_scroll = 0
scroll_speed = 4

# loop 설정
run = True
while run:
    clock.tick(fps)

    screen.blit(bg, (0,0)) # 백그라운드 그리기
    screen.blit(ground_img, (ground_scroll, 768)) # 땅 그리기
    ground_scroll -= scroll_speed

    if abs(ground_scroll) > 35: # 땅 이미지 반복되게 하기위해
        ground_scroll = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT: # 창의 x를 누르면
            run = False
    pygame.display.update()

pygame.quit()