import pygame
import random
from setting import *
from player import player
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

moving_sprites = pygame.sprite.Group()
player1 = player(screen,"asset/balloon/pink.png",0,0)
moving_sprites.add(player1)

balloon1 = balloon(screen, "asset/balloon/yellow.png")
now_count = balloon1.balloonCount

m_list = []
k = 0
ball_released = 0



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

    # 4-4. 그리기
    screen.fill(white)

    for m in m_list:
        m.showBalloon()
        if time.time() - m.initTime > 3:
            m_list.remove(m)
            now_count +=1
	
    # player1.show()
    moving_sprites.draw(screen)
    # moving_sprites.update()

    # 4-5. 업데이트
    pygame.display.flip()

# 5. 게임 종료
pygame.quit()