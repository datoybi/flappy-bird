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

# 변수 선언
ground_scroll = 0
scroll_speed = 4

# load images
bg = pygame.image.load('images/bg.png')
ground_img = pygame.image.load('images/ground.png')

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1, 4):
            img = pygame.image.load(f'images/bird{num}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
    
    def update(self):
        # 에니메이션 동작
        self.counter += 1
        flap_cooldown = 5

        if self.counter > flap_cooldown:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0
        self.image = self.images[self.index]

bird_group = pygame.sprite.Group()
flappy = Bird(100, int(screen_height / 2)) 
bird_group.add(flappy)

# loop 설정
run = True
while run:
    clock.tick(fps)

    screen.blit(bg, (0,0)) # 백그라운드 그리기
    screen.blit(ground_img, (ground_scroll, 768)) # 땅 그리기
    bird_group.draw(screen)
    bird_group.update()
    ground_scroll -= scroll_speed

    if abs(ground_scroll) > 35: # 땅 이미지 반복되게 하기위해
        ground_scroll = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT: # 창의 x를 누르면
            run = False
    pygame.display.update()

pygame.quit()