import pygame
from setting import *

class player(pygame.sprite.Sprite):

    # 생성자
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)
    
        
        self.sprites = []
        self.sprites.append(pygame.image.load('asset/character/down_1.png').convert_alpha())
        self.sprites.append(pygame.image.load('asset/character/down_2.png').convert_alpha())
        self.sprites.append(pygame.image.load('asset/character/down_3.png').convert_alpha())
        self.sprites.append(pygame.image.load('asset/character/down_4.png').convert_alpha())
        self.sprites.append(pygame.image.load('asset/character/up_1.png').convert_alpha())
        self.sprites.append(pygame.image.load('asset/character/up_2.png').convert_alpha())
        self.sprites.append(pygame.image.load('asset/character/up_3.png').convert_alpha())
        self.sprites.append(pygame.image.load('asset/character/up_4.png').convert_alpha())
        self.sprites.append(pygame.image.load('asset/character/left_1.png').convert_alpha())
        self.sprites.append(pygame.image.load('asset/character/left_2.png').convert_alpha())
        self.sprites.append(pygame.image.load('asset/character/left_3.png').convert_alpha())
        self.sprites.append(pygame.image.load('asset/character/left_4.png').convert_alpha())
        self.sprites.append(pygame.image.load('asset/character/right_1.png').convert_alpha())
        self.sprites.append(pygame.image.load('asset/character/right_2.png').convert_alpha())
        self.sprites.append(pygame.image.load('asset/character/right_3.png').convert_alpha())
        self.sprites.append(pygame.image.load('asset/character/right_4.png').convert_alpha())
        for i in range(len(self.sprites)):
            self.sprites[i] = pygame.transform.scale(self.sprites[i], (80,80))

        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        #self.rect = self.image.get_rect()
        #self.rect.topleft = (x,y)
        self.rect = self.image.get_rect(topleft = pos)
        self.c_rect = self.rect
        # player 이미지 크기
        # self.image = pygame.transform.scale(self.image, (50, 60))
        self.sx, self.sy = self.image.get_size()
        
        # player 위치
        # self.x = pos[0]
        # self.y = pos[1]
        
        # default
        self.move = 5   # 아이템에 따라 달라짐
        self.is_animating = False
        self.speed = 0.2   # 아이템에 따라 달라짐
        self.obstacle_sprites = obstacle_sprites
        self.direction = pygame.math.Vector2()

	# 해당 player의 이미지를 screen의 어느 위치에 띄울지 정해주는 함수
    # def show(self):
    #     self.screen.blit(self.image, (self.x,self.y))

    # 키보드 입력값에 따라 player의 위치를 바꿔주는 함수
    def change_location(self, left_go,right_go,up_go,down_go):
        if left_go == True:
            self.direction.x = -1
            #self.x -= self.move
            if self.current_sprite < 8:
                self.current_sprite = 8
            self.current_sprite+=self.speed    # 속도 조절하는 ㅅㄲ
            if self.current_sprite>11:
                self.current_sprite=8
                self.is_animating = False   # 이거 설정하면, 어떤 입력값이 들어왔을 때 애니메이션 동작을 한번만 수행. 이거 설정 안하면 애니메이션 동작은 영구적 수행.
            self.image = self.sprites[int(self.current_sprite)]
            if self.rect.x <= 0:
                # self.x = 0
                self.direction.x = 0


        elif right_go == True:
            self.direction.x = 1
            #self.x += self.move
            if self.current_sprite < 12:
                self.current_sprite = 12
            self.current_sprite+=self.speed    # 속도 조절하는 ㅅㄲ
            if self.current_sprite>15:
                self.current_sprite=12
                self.is_animating = False   # 이거 설정하면, 어떤 입력값이 들어왔을 때 애니메이션 동작을 한번만 수행. 이거 설정 안하면 애니메이션 동작은 영구적 수행.
            self.image = self.sprites[int(self.current_sprite)]
            if self.rect.x >= size[0] - self.sx:
                # self.x = size[0] - self.sx
                self.direction.x = 0

        elif up_go == True:
            self.direction.y = -1
            # self.y -= self.move
            if self.current_sprite < 4:
                self.current_sprite = 4
            self.current_sprite+=self.speed    # 속도 조절하는 ㅅㄲ
            if self.current_sprite>7:
                self.current_sprite=4
                self.is_animating = False   # 이거 설정하면, 어떤 입력값이 들어왔을 때 애니메이션 동작을 한번만 수행. 이거 설정 안하면 애니메이션 동작은 영구적 수행.
            self.image = self.sprites[int(self.current_sprite)]
            if self.rect.y <= 0:
                #self.y = 0
                self.direction.y=0

        elif down_go == True:
            self.direction.y = 1
            #self.y += self.move
            if self.current_sprite < 0:
                self.current_sprite = 0
            self.current_sprite+=self.speed    # 속도 조절하는 ㅅㄲ
            if self.current_sprite>3:
                self.current_sprite=0
                self.is_animating = False   # 이거 설정하면, 어떤 입력값이 들어왔을 때 애니메이션 동작을 한번만 수행. 이거 설정 안하면 애니메이션 동작은 영구적 수행.
            self.image = self.sprites[int(self.current_sprite)]    
            if self.rect.y >= size[1] - self.sy:
                #self.y = size[1] - self.sy
                self.direction.y=0
        

        
        self.rect.x += self.direction.x * 5
        self.c_rect = pygame.Rect(self.rect.x+15, self.rect.y+30, 50, 50)
        print(self.rect, self.c_rect)
        self.collision('horizontal')
        self.rect.y += self.direction.y * 5
        self.c_rect = pygame.Rect(self.rect.x+15, self.rect.y+30, 50, 50)
        self.collision('vertical')
        self.direction.x=0
        self.direction.y=0
        
        #print( )
        #self.rect = self.image.get_rect()
        self.rect.topleft = [self.rect.x,self.rect.y]
        
   
    

    def collision(self,direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.c_rect):
                    #print(sprite.rect.colliderect(self.rect))
                    #print(self.rect.x,self.rect.y)
                    if self.direction.x > 0: # moving right
                        #print("변하기전",self.rect.x,self.rect.y)
                        self.rect.right = sprite.rect.left+15
                        #print(self.rect.x,self.rect.y)

                    if self.direction.x < 0: # moving left
                        self.rect.left = sprite.rect.right-15

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.c_rect):
                    if self.direction.y > 0: # moving down
                        self.rect.bottom = sprite.rect.top
                    if self.direction.y < 0: # moving up
                        self.rect.top = sprite.rect.bottom-30