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
flying = False
game_over = False

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
        self.vel = 0 # gravity 처리 변수
        self.clicked = False # 꾹 누르고 있을때 효과 처리

    def update(self):
        if flying == True:
            # gravity
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < 768:
                self.rect.y += int(self.vel) # 시간이 지날수록 y값을 더 많이 해서 아래로 가게끔

        if game_over == False:
            # jump
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False: # 오른쪽 버튼을 눌렀을 때
                self.clicked = True
                self.vel = -10
            if pygame.mouse.get_pressed()[0] == 0: 
                self.clicked = False
        
            # 에니메이션 동작
            self.counter += 1
            flap_cooldown = 5

            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index] 

            # rotate the bird
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2) # 새가 떨어질때 살짝 기울임 효과
        else: # 게임오버면
            self.image = pygame.transform.rotate(self.images[self.index], -90) # -90로테이트 하면 새 얼굴이 땅을 바라보게끔 효과


bird_group = pygame.sprite.Group()
flappy = Bird(100, int(screen_height / 2)) 
bird_group.add(flappy)

# loop 설정
run = True
while run:
    clock.tick(fps)

    screen.blit(bg, (0,0)) # 백그라운드 그리기
    bird_group.draw(screen)
    bird_group.update() 
    screen.blit(ground_img, (ground_scroll, 768)) # 땅 그리기

    if flappy.rect.bottom > 768: # 새가 땅에 닿았는지 체크
        game_over = True
        flying = False

    if game_over == False:  
        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 35: # 땅 이미지 반복되게 하기위해
            ground_scroll = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT: # 창의 x를 누르면
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False: # 마우스 클릭시 게임 시작
            flying = True
    pygame.display.update()

pygame.quit()