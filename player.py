import pygame
from setting import *

class player(pygame.sprite.Sprite):

    # 생성자
    def __init__(self, screen, x, y, crs, sprites):
        super().__init__()
        
        self.screen=screen
        
        self.sprites = sprites

        for i in range(len(self.sprites)):
            self.sprites[i] = pygame.transform.scale(self.sprites[i], (80,80))


        self.current_sprite = crs
        self.image = self.sprites[int(self.current_sprite)]
        self.rect = self.image.get_rect()
        self.rect.topleft = [x,y]
        
        


        # player 이미지 크기
        # self.image = pygame.transform.scale(self.image, (50, 60))
        self.sx, self.sy = self.image.get_size()
        
        # player 위치
        self.x = x
        self.y = y
        
        self.c_rect = pygame.Rect(self.x+15, self.y+30, 50, 50)
        
        # default
        self.move = 5   # 아이템에 따라 달라짐
        self.is_animating = False
        self.speed = 0.2   # 아이템에 따라 달라짐

	# 해당 player의 이미지를 screen의 어느 위치에 띄울지 정해주는 함수
    def show(self):
        self.screen.blit(self.image, (self.x,self.y))

    # 키보드 입력값에 따라 player의 위치를 바꿔주는 함수
    def change_location(self, left_go,right_go,up_go,down_go,obstacle_sprites):
        if left_go == True:
            self.x -= self.move
            self.c_rect = pygame.Rect(self.x+15, self.y+30, 50, 50)
            if self.current_sprite < 8:
                self.current_sprite = 8
            self.current_sprite+=self.speed    # 속도 조절하는 ㅅㄲ
            if self.current_sprite>11:
                self.current_sprite=8
                self.is_animating = False   # 이거 설정하면, 어떤 입력값이 들어왔을 때 애니메이션 동작을 한번만 수행. 이거 설정 안하면 애니메이션 동작은 영구적 수행.
            self.image = self.sprites[int(self.current_sprite)]
            if self.x <= -self.sx/2:
                self.x = -self.sx/2
            for sprite in obstacle_sprites:
                if sprite.rect.colliderect(self.c_rect): # moving left
                    self.x += self.move
            
        elif right_go == True:
            self.x += self.move
            self.c_rect = pygame.Rect(self.x+15, self.y+30, 50, 50)
            if self.current_sprite < 12:
                self.current_sprite = 12
            self.current_sprite+=self.speed    # 속도 조절하는 ㅅㄲ
            if self.current_sprite>15:
                self.current_sprite=12
                self.is_animating = False   # 이거 설정하면, 어떤 입력값이 들어왔을 때 애니메이션 동작을 한번만 수행. 이거 설정 안하면 애니메이션 동작은 영구적 수행.
            self.image = self.sprites[int(self.current_sprite)]
            if self.x >= size[0] - self.sx/2:
                self.x = size[0] - self.sx/2
            for sprite in obstacle_sprites:
                if sprite.rect.colliderect(self.c_rect): # moving left
                    self.x -= self.move
            
        elif up_go == True:
            self.y -= self.move
            self.c_rect = pygame.Rect(self.x+15, self.y+30, 50, 50)
            if self.current_sprite < 4:
                self.current_sprite = 4
            self.current_sprite+=self.speed    # 속도 조절하는 ㅅㄲ
            if self.current_sprite>7:
                self.current_sprite=4
                self.is_animating = False   # 이거 설정하면, 어떤 입력값이 들어왔을 때 애니메이션 동작을 한번만 수행. 이거 설정 안하면 애니메이션 동작은 영구적 수행.
            self.image = self.sprites[int(self.current_sprite)]
            if self.y <= -self.sy/2:
                self.y = -self.sy/2
            for sprite in obstacle_sprites:
                if sprite.rect.colliderect(self.c_rect): # moving left
                    self.y += self.move
            
        elif down_go == True:
            self.y += self.move
            self.c_rect = pygame.Rect(self.x+15, self.y+30, 50, 50)
            if self.current_sprite < 0:
                self.current_sprite = 0
            self.current_sprite+=self.speed    # 속도 조절하는 ㅅㄲ
            if self.current_sprite>3:
                self.current_sprite=0
                self.is_animating = False   # 이거 설정하면, 어떤 입력값이 들어왔을 때 애니메이션 동작을 한번만 수행. 이거 설정 안하면 애니메이션 동작은 영구적 수행.
            self.image = self.sprites[int(self.current_sprite)]
                
            if self.y >= size[1] - self.sy/2:
                self.y = size[1] - self.sy/2
            
            for sprite in obstacle_sprites:
                if sprite.rect.colliderect(self.c_rect): # moving left
                    self.y -= self.move
        print(self.x, self.y)
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.x,self.y]
