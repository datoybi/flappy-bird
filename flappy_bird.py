# py -m pip install -U pygame --user
import pygame 
from pygame.locals import *
import random

pygame.init()

clock = pygame.time.Clock()
fps = 60
screen_width = 864 
screen_height = 936

screen = pygame.display.set_mode((screen_width, screen_height)) # width, height 설정
pygame.display.set_caption('Flappy Bird') # title 설정

# define font 
font = pygame.font.SysFont('Bauhaus 93', 60)

# define colors
white = (255, 255, 255)

# 변수 선언
ground_scroll = 0
scroll_speed = 4
flying = False
game_over = False
pipe_gap = 150
pipe_frequency = 1500 # milliseconds
last_pipe = pygame.time.get_ticks() - pipe_frequency
score = 0
pass_pipe = False

# load images
bg = pygame.image.load('images/bg.png')
ground_img = pygame.image.load('images/ground.png')

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

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

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/pipe.png')
        self.rect = self.image.get_rect()
        # position 1 is from the top, -1 is from the bottom
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True) # 파이프 flip하기 - x좌표는 false, y좌표만 flip
            self.rect.bottomleft = [x, y - int(pipe_gap / 2)]
        if position == -1:
            self.rect.topleft = [x, y + int(pipe_gap / 2)]

    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()

bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()
flappy = Bird(100, int(screen_height / 2)) 
bird_group.add(flappy)

# loop 설정
run = True
while run:
    clock.tick(fps)

    screen.blit(bg, (0,0)) # 백그라운드 그리기
    bird_group.draw(screen)
    bird_group.update() 
    pipe_group.draw(screen)
    screen.blit(ground_img, (ground_scroll, 768)) # 땅 그리기

    # check the score
    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
            and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
            and pass_pipe == False:
            pass_pipe = True

        if pass_pipe == True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                pass_pipe = False

    draw_text(str(score), font, white, int(screen_width / 2), 20)

    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0: # 파이프에 닿으면 게임오바
        game_over = True

    if flappy.rect.bottom >= 768: # 새가 땅에 닿았는지 체크
        game_over = True
        flying = False

    if game_over == False and flying == True: 
        time_now = pygame.time.get_ticks() # 새로운 파이프 생성 시간 계산
        if time_now - last_pipe > pipe_frequency:
            pipe_height = random.randint(-100, 100)
            btm_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, -1)
            top_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now

        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 35: # 땅 이미지 반복되게 하기위해
            ground_scroll = 0
        pipe_group.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT: # 창의 x를 누르면
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False: # 마우스 클릭시 게임 시작
            flying = True
    pygame.display.update()

pygame.quit()