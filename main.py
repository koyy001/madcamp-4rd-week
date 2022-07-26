import pygame
import random
from setting import *
from player import player
from tile import tile
from balloon import balloon
import copy
import time

# 1. 게임 초기화
pygame.init()

# 2. 게임창 옵션 설정
screen = pygame.display.set_mode(size)
pygame.display.set_caption(title)

# 3. 게임 내 필요한 설정
clock = pygame.time.Clock()

# sprite group setup
visible_sprites = pygame.sprite.Group()
obstacle_sprites = pygame.sprite.Group()

moving_sprites = pygame.sprite.Group()
over_sprites = pygame.sprite.Group()
player1 = player((0,0),[visible_sprites],obstacle_sprites)
moving_sprites.add(player1)

balloon1 = balloon(screen, "asset/balloon/yellow.png")
now_count = balloon1.balloonCount


tile_img = []
tile_img.append(pygame.image.load('asset/tile/land.png').convert_alpha())
tile_img.append(pygame.image.load('asset/tile/tree_under.png').convert_alpha())
tile_img.append(pygame.image.load('asset/tile/redBlock.png').convert_alpha())
tile_img.append(pygame.image.load('asset/tile/orangeBlock.png').convert_alpha())
tile_img.append(pygame.image.load('asset/tile/redHouse_under.png').convert_alpha())
tile_img.append(pygame.image.load('asset/tile/box.png').convert_alpha())
tile_img.append(pygame.image.load('asset/tile/blueHouse_under.png').convert_alpha())
tile_img.append(pygame.image.load('asset/tile/road.png').convert_alpha())
tile_img.append(pygame.image.load('asset/tile/tree_up.png').convert_alpha())
tile_img.append(pygame.image.load('asset/tile/redHouse_up.png').convert_alpha())
tile_img.append(pygame.image.load('asset/tile/blueHouse_up.png').convert_alpha())

tile_img[0]= pygame.transform.scale(tile_img[0], (64, 64))
tile_img[1]= pygame.transform.scale(tile_img[1], (64, 64))
tile_img[2]= pygame.transform.scale(tile_img[2], (64, 64))
tile_img[3]= pygame.transform.scale(tile_img[3], (64, 64))
tile_img[4]= pygame.transform.scale(tile_img[4], (64, 64))
tile_img[5]= pygame.transform.scale(tile_img[5], (64, 64))
tile_img[6]= pygame.transform.scale(tile_img[6], (64, 64))
tile_img[7]= pygame.transform.scale(tile_img[7], (64, 64))
tile_img[8]= pygame.transform.scale(tile_img[8], (64, 108))
tile_img[9]= pygame.transform.scale(tile_img[9], (64, 94))
tile_img[10]= pygame.transform.scale(tile_img[10], (64, 94))

m_list = []
k = 0
ball_released = 0

# 타일 깔아주기

for row_index,row in enumerate(WORLD_MAP):
    for col_index, col in enumerate(row):
        x = col_index * tilesize
        y = row_index * tilesize
        if col == 'l':
            tile((x,y),[visible_sprites], "land", tile_img)
        elif col == 'o':
            tile((x,y),[visible_sprites,obstacle_sprites], "orangeBlock", tile_img)
        elif col == 'r':
            tile((x,y),[visible_sprites,obstacle_sprites], "redBlock", tile_img)
        elif col == 'R':
            tile((x,y),[visible_sprites,obstacle_sprites], "redHouse_under", tile_img)
        elif col == 'b':
            tile((x,y),[visible_sprites,obstacle_sprites], "box", tile_img)
        elif col == 't':
            tile((x,y),[visible_sprites,obstacle_sprites], "tree_under", tile_img)
        elif col == 'B':
            tile((x,y),[visible_sprites,obstacle_sprites], "blueHouse_under", tile_img)
        elif col == 'g':
            tile((x,y),[visible_sprites], "road", tile_img)

for row_index,row in enumerate(WORLD_MAP):
    for col_index, col in enumerate(row):
        x = col_index * tilesize
        y = row_index * tilesize
        if col == 'R':
            tile((x,y),[over_sprites], "redHouse_up",tile_img)
        elif col == 't':
            tile((x,y),[over_sprites], "tree_up",tile_img)
        elif col == 'B':
            tile((x,y),[over_sprites], "blueHouse_up",tile_img)
            

# 4. 메인 이벤트
SB = 0
while SB == 0:

    # 4-1. FPS 설정 
    clock.tick(60)

    # 4-2. 각종 입력 감지
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            SB = 1
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                left_go = True
            elif event.key == pygame.K_RIGHT:
                right_go = True
            elif event.key == pygame.K_UP:
                up_go = True
            elif event.key == pygame.K_DOWN:
                down_go = True
            elif event.key == pygame.K_SPACE:
                space_go = True
                #player1.animate()

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                left_go = False
            elif event.key == pygame.K_RIGHT:
                right_go = False
            elif event.key == pygame.K_UP:
                up_go = False 
            elif event.key == pygame.K_DOWN:
                down_go = False 
            elif event.key == pygame.K_SPACE:
                space_go = False 
                
                
    # 4-3. 입력, 시간에 따른 변화
    player1.change_location(left_go, right_go, up_go, down_go)
    
    if space_go == True and ball_released == 0:
        if (now_count>0):
            balloon1_copy=copy.copy(balloon1)
            balloon1_copy.initTime = time.time()
            balloon1_copy.x = round(player1.x + player1.sx/2 - balloon1_copy.bx/2)
            balloon1_copy.y = player1.y + 10
            m_list.append(balloon1_copy)
            ball_released = 1
            now_count-=1
    k += 1

    if space_go == False:
        ball_released = 0

    # 스크린 리셋하기
    screen.fill(gray)

    # 타일 그리기
    visible_sprites.draw(screen)
    
    # 물풍선 그리기
    for m in m_list:
        m.showBalloon()
        if time.time() - m.initTime > 3:
            m_list.remove(m)
            now_count +=1
	
    # player 그리기
    moving_sprites.draw(screen)
    
    # 입체적 타일 그리기
    over_sprites.draw(screen)

    #visible_sprites.draw(screen)
    print(over_sprites)
    # 4-5. 업데이트
    pygame.display.flip()

# 5. 게임 종료
pygame.quit()