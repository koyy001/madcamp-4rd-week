# small network game that has differnt blobs
# moving around the screen

import contextlib

from cv2 import RETR_LIST
with contextlib.redirect_stdout(None):
    import pygame
from client import Network
import random
import os
import pygame
from setting import *
from player import player
from balloon import balloon
from baam import baam
from item import item
from tile import tile
import time
import copy

from loginbox import *


players = {}
balloons = {}


server = Network()
server.connect()

#current_id = server.connect()
#players = server.send("get") # 처음 호출되었을 때 현재 게임 상태를 받는것
#그러면, 로그인할때 아마 처음 login을 호출한 다음에, 게임 들어갈 때 호출하는 함수는 명확히 달라야 할 것 같다

###pygame 관련 코드###    
# 1. 게임 초기화
#pygame.init()

# 2. 게임창 옵션 설정
screen = pygame.display.set_mode((900, 700))
pygame.display.set_caption(title)

# 3. 게임 내 필요한 설정
clock = pygame.time.Clock()

current_id = -3 # 처음 상태는 -3
mod = 0

#image들 받아오는 부분
intro_img = pygame.image.load("intro.jpg")
intro_img = pygame.transform.scale(intro_img, (900, 700))
login_img = pygame.image.load("login.png")
login_img = pygame.transform.scale(login_img, (900, 700))
register_img = pygame.image.load("register.png")
register_img = pygame.transform.scale(register_img, (900, 700))
balloon_img = "asset/balloon/yellow.png"


## 여기를 ㅈㄴ 고쳐야될듯
moving_sprites = pygame.sprite.Group()
obstacle_sprites = pygame.sprite.Group()
visible_sprites = pygame.sprite.Group()
over_sprites = pygame.sprite.Group()
water_sprites = pygame.sprite.Group()
item_sprites = pygame.sprite.Group()


#balloon1 = balloon(screen, "asset/balloon/yellow.png")
#now_count = balloon1.balloonCount 


m_list = [] #화면에 출력할 것들 리스트
k = 0 #???
ball_released = 0 # 내 캐릭터가 놓은 볼 개수?
now_count = 3
erased_tile=[]

#def redraw_window(players, m_list, current_id, sprites):
def redraw_window(players, balloons, current_id, sprites):
    global now_count

    screen.fill(white)
    #print(balloons)

    for i in players: ## {1: {data}, 2:{data}, ...}
        if i != current_id:
            p = player(screen, players[i]["x"], players[i]["y"], players[i]["crs"], sprites)
            moving_sprites.add(p)
    
    visible_sprites.draw(screen)
    for keyid in balloons:
        for m in balloons[keyid]:
            # 물풍선 잔여시간을 변수에 받아놓는다 (물줄기 타일 생성할때 써먹으려고)
            
            myball = balloon(screen, balloon_img, m[0], m[1], m[2]) #물풍선을 생성해서
            myball.showBalloon() #화면에 표시해주고
            if time.time() - m[2] > 3: # 만약 생성한 지 오래 지났으면 (m[2]가 생성시간)
                
                if keyid == current_id:
                    # 여기서 구현.
                    # 물풍선 터지는 위치일때, 주변에 물줄기 타일 생성,,
                    x = m[0]
                    y = m[1]
                    if time.time() - m[2] > 3:
                        
                        baam((x-64,y),[water_sprites], baam_img).baam_direction(True,False,False,False)
                        baam((x+64,y),[water_sprites], baam_img).baam_direction(False,True,False,False)
                        baam((x,y-64),[water_sprites], baam_img).baam_direction(False,False,True,False)
                        baam((x,y+64),[water_sprites], baam_img).baam_direction(False,False,False,True)

                        xx = x//64
                        yy = y//64
                        x=yy
                        y=xx
                        
                        if WORLD_MAP[x-1][y] != 'R' and WORLD_MAP[x-1][y] != 'B'and WORLD_MAP[x-1][y] != 't':
                                if (y>0) and (y<20) and (x-1>0) and (x-1<12):
                                    if (y>=9) and (y<=11):
                                        WORLD_MAP[x-1][y] = 'g'
                                    else:
                                        WORLD_MAP[x-1][y] = 'l'
                                    if ITEM_MAP[x-1][y] == 'x':
                                            item((64*y,64*(x-1)),[item_sprites], "x", items)
                        if WORLD_MAP[x+1][y] != 'R' and WORLD_MAP[x+1][y] != 'B'and WORLD_MAP[x+1][y] != 't':
                                if (y>0) and (y<20) and (x+1>0) and (x+1<12):
                                    if (y>=9) and (y<=11):
                                        WORLD_MAP[x+1][y] = 'g'
                                    else:
                                        WORLD_MAP[x+1][y] = 'l'
                                    if ITEM_MAP[x+1][y] == 'x':
                                            item((64*y,64*(x+1)),[item_sprites], "x", items)
                        if WORLD_MAP[x][y+1] != 'R' and WORLD_MAP[x][y+1] != 'B'and WORLD_MAP[x][y+1] != 't':
                                if (y+1>0) and (y+1<20) and (x>0) and (x<12):
                                    if (y+1>=9) and (y+1<=11):
                                        WORLD_MAP[x][y+1] = 'g'
                                    else:
                                        WORLD_MAP[x][y+1] = 'l'
                                    if ITEM_MAP[x][y+1] == 'x':
                                            item((64*(y+1),64*x),[item_sprites], "x", items)
                        if WORLD_MAP[x][y-1] != 'R' and WORLD_MAP[x][y-1] != 'B'and WORLD_MAP[x][y-1] != 't':
                                if (y-1>0) and (y-1<20) and (x>0) and (x<12):
                                    if (y-1>=9) and (y-1<=11):
                                        WORLD_MAP[x][y-1] = 'g'
                                    else:
                                        WORLD_MAP[x][y-1] = 'l'
                                    if ITEM_MAP[x][y-1] == 'x':
                                            item((64*(y-1),64*x),[item_sprites], "x", items)

                    balloons[keyid].remove(m)
                    now_count +=1
    water_sprites.draw(screen)
    moving_sprites.draw(screen)
    over_sprites.draw(screen)
    item_sprites.draw(screen)

    #return balloons # 사라진 벌룬 반환


clock = pygame.time.Clock()
while True: # 전체적인 로그인 및 회원가입 과정
    if current_id >= 0: # 로그인 또는 회원가입 성공시 끝
        break
    #처음 켰을 때 화면
    button_login = button(position=(450, 300), size=(100, 50), clr=(220, 220, 220), cngclr=(255, 0, 0), func=fn_loginmod, text='Login')
    button_register = button(position=(450, 400), size=(100, 50), clr=(220, 220, 220), cngclr=(255, 0, 0), func=fn_regmod, text='Register')
    button_quit = button(position=(450, 500), size=(100, 50), clr=(220, 220, 220), cngclr=(255, 0, 0), func=fn_qmod, text='Quit')
    button_list = [button_login, button_register, button_quit]
    crash = True
    while mod == 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crash = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    for b in button_list:
                        if b.rect.collidepoint(pos):
                            mod = str(b.call_back())
        screen.blit(intro_img, (0, 0))
        for b in button_list:
            b.draw(screen)
        pygame.display.update()
        clock.tick(30)
        
    #mod = input("What will you do? (1) Login  (2) Register (3) Quit ")
    if mod == '1': #로그인화면 구성하기
        #pygame.display.set_mode((1500, 900))
        #button들과 input_box들 선언
        input_box1 = InputBox(420, 551, 170, 32)
        input_box2 = InputBox(420, 592, 170, 32)
        input_boxes = [input_box1, input_box2]
        button1 = button(position=(455, 665), size=(97, 28), clr=(220, 220, 220), cngclr=(255, 0, 0), func=fn_login, text='Login', visible = False)
        button_list = [button1]
        
        while True:
            for event in pygame.event.get():
                for box in input_boxes:
                    box.handle_event(event)
                if event.type == pygame.QUIT:
                    crash = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        pos = pygame.mouse.get_pos()
                        for b in button_list:
                            if b.rect.collidepoint(pos):
                                current_id = b.call_back(input_box1.text, input_box2.text, server)
            for box in input_boxes: # 박스 정보 업데이트하기
                box.update()
            screen.fill((30, 30, 30))
            screen.blit(login_img, (0, 0)) # 배경 띄우기
            for box in input_boxes: # 박스 그리기
                box.draw(screen)
            for b in button_list: # 버튼 그리기
                b.draw(screen)
            
            if current_id >= 0: #정상적으로 로그인 성공시
                #pygame.quit()
                break
            elif current_id == -1: # 로그인 실패시
                print("Password Wrong")
            elif current_id == -2:
                print("No ID...")
            pygame.display.update()
            clock.tick(30)
            
    elif mod == '2':
        #button들과 input_box들 선언
        input_box1 = InputBox(420, 527, 170, 32) #ID
        input_box2 = InputBox(420, 565, 170, 32) #Password
        input_box3 = InputBox(420, 603, 170, 32) #Nickname
        input_boxes = [input_box1, input_box2, input_box3]
        button1 = button(position=(454, 668), size=(97, 28), clr=(220, 220, 220), cngclr=(255, 0, 0), func=fn_register, text='Register', visible = False)
        button_list = [button1]
        
        while True:
            for event in pygame.event.get():
                for box in input_boxes:
                    box.handle_event(event)
                if event.type == pygame.QUIT:
                    crash = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        pos = pygame.mouse.get_pos()
                        print(pos)
                        for b in button_list:
                            if b.rect.collidepoint(pos):
                                current_id = b.call_back(input_box1.text, input_box2.text, input_box3.text, server)
            for box in input_boxes: # 박스 정보 업데이트하기
                box.update()
            screen.fill((30, 30, 30))
            screen.blit(register_img, (0, 0)) # 배경 띄우기
            for box in input_boxes: # 박스 그리기
                box.draw(screen)
            for b in button_list: # 버튼 그리기
                b.draw(screen)
                
            if current_id >=0 :
                #pygame.quit()
                break
            pygame.display.update()
            clock.tick(30)
        
    else:
        server.disconnect()
        quit()


    
        
#players, balloons = server.send("get")

items = []
items.append(pygame.image.load('asset/item/1.png').convert_alpha())
items.append(pygame.image.load('asset/item/2.png').convert_alpha())
items.append(pygame.image.load('asset/item/3.png').convert_alpha())
items.append(pygame.image.load('asset/item/4.png').convert_alpha())
items.append(pygame.image.load('asset/item/5.png').convert_alpha())

for i in range(len(items)):
    items[i] = pygame.transform.scale(items[i], (64,64))

sprites = []
sprites.append(pygame.image.load('asset/character/down_1.png').convert_alpha())
sprites.append(pygame.image.load('asset/character/down_2.png').convert_alpha())
sprites.append(pygame.image.load('asset/character/down_3.png').convert_alpha())
sprites.append(pygame.image.load('asset/character/down_4.png').convert_alpha())
sprites.append(pygame.image.load('asset/character/up_1.png').convert_alpha())
sprites.append(pygame.image.load('asset/character/up_2.png').convert_alpha())
sprites.append(pygame.image.load('asset/character/up_3.png').convert_alpha())
sprites.append(pygame.image.load('asset/character/up_4.png').convert_alpha())
sprites.append(pygame.image.load('asset/character/left_1.png').convert_alpha())
sprites.append(pygame.image.load('asset/character/left_2.png').convert_alpha())
sprites.append(pygame.image.load('asset/character/left_3.png').convert_alpha())
sprites.append(pygame.image.load('asset/character/left_4.png').convert_alpha())
sprites.append(pygame.image.load('asset/character/right_1.png').convert_alpha())
sprites.append(pygame.image.load('asset/character/right_2.png').convert_alpha())
sprites.append(pygame.image.load('asset/character/right_3.png').convert_alpha())
sprites.append(pygame.image.load('asset/character/right_4.png').convert_alpha())

baam_img = []
baam_img.append(pygame.image.load('asset/balloon/baam/left/1.png').convert_alpha())
baam_img.append(pygame.image.load('asset/balloon/baam/left/2.png').convert_alpha())
baam_img.append(pygame.image.load('asset/balloon/baam/left/3.png').convert_alpha())
baam_img.append(pygame.image.load('asset/balloon/baam/left/4.png').convert_alpha())
baam_img.append(pygame.image.load('asset/balloon/baam/left/5.png').convert_alpha())
baam_img.append(pygame.image.load('asset/balloon/baam/right/1.png').convert_alpha())
baam_img.append(pygame.image.load('asset/balloon/baam/right/2.png').convert_alpha())
baam_img.append(pygame.image.load('asset/balloon/baam/right/3.png').convert_alpha())
baam_img.append(pygame.image.load('asset/balloon/baam/right/4.png').convert_alpha())
baam_img.append(pygame.image.load('asset/balloon/baam/right/5.png').convert_alpha())
baam_img.append(pygame.image.load('asset/balloon/baam/up/1.png').convert_alpha())
baam_img.append(pygame.image.load('asset/balloon/baam/up/2.png').convert_alpha())
baam_img.append(pygame.image.load('asset/balloon/baam/up/3.png').convert_alpha())
baam_img.append(pygame.image.load('asset/balloon/baam/up/4.png').convert_alpha())
baam_img.append(pygame.image.load('asset/balloon/baam/up/5.png').convert_alpha())
baam_img.append(pygame.image.load('asset/balloon/baam/down/1.png').convert_alpha())
baam_img.append(pygame.image.load('asset/balloon/baam/down/2.png').convert_alpha())
baam_img.append(pygame.image.load('asset/balloon/baam/down/3.png').convert_alpha())
baam_img.append(pygame.image.load('asset/balloon/baam/down/4.png').convert_alpha())
baam_img.append(pygame.image.load('asset/balloon/baam/down/5.png').convert_alpha())

for i in range(len(baam_img)):
    baam_img[i] = pygame.transform.scale(baam_img[i], (64,64))

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


if balloon_img[-3:] == "png":
    balloon_img = pygame.image.load(balloon_img).convert_alpha()
else :
    balloon_img = pygame.image.load(balloon_img)
#balloon1 = balloon(screen, balloon_img)
#now_count = balloon1.balloonCount


room = 0 # 0: Lobby, else: n번 룸

SB =0
while SB == 0:
    if room == 0: # 참가 or 방 생성 화면
        clock.tick(60)
        pygame.display.set_mode((900, 700))
        input_box1 = InputBox(420, 527, 170, 32) #ID
        input_boxes = [input_box1]
        button_c = button(position=(454, 668), size=(97, 28), clr=(220, 220, 220), cngclr=(255, 0, 0), func=fn_create, text='CreateRoom', visible = True)
        button_e = button(position=(454, 468), size=(97, 28), clr=(220, 220, 220), cngclr=(255, 0, 0), func=fn_enter, text='EnterRoom', visible = True)
        button_list = [button_c, button_e]

        while True:
            for event in pygame.event.get():
                for box in input_boxes:
                    box.handle_event(event)
                if event.type == pygame.QUIT:
                    crash = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        pos = pygame.mouse.get_pos()
                        if button_c.rect.collidepoint(pos):
                            room = button_c.call_back(server)
                        if button_e.rect.collidepoint(pos):
                            room = button_e.call_back(server, input_box1.text)
            for box in input_boxes: # 박스 정보 업데이트하기
                box.update()
            screen.fill((30, 30, 30))
            screen.blit(register_img, (0, 0)) # 배경 띄우기
            for box in input_boxes: # 박스 그리기
                box.draw(screen)
            for b in button_list: # 버튼 그리기
                b.draw(screen)
                
            if room >0 :
                #pygame.quit()
                break
            pygame.display.update()
        
    else:
        players, balloons = server.send("get")
        clock.tick(60) # FPS 설정            
        
        
        # 플레이어 데이터 받아올 부분인데... 나중에 고치자
        player1 = players[current_id]
        #print(players)
        player1 = player(screen, player1["x"], player1["y"], player1["crs"], sprites)
        obstacle_sprites = pygame.sprite.Group() # 매번 sprite group 새로 만들기
        visible_sprites = pygame.sprite.Group()
        over_sprites = pygame.sprite.Group()
        moving_sprites = pygame.sprite.Group()
        water_sprites = pygame.sprite.Group()
        moving_sprites.add(player1)
        
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
        
        #m_list = balloons[current_id] # 이번에 추가된거
        
        data = "1"
        
        pygame.display.set_mode((1350, 830))
        
        #상하좌우 키 부분: 나중에 손가락으로 대치하면 되는데
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
            
        
        #입력, 시간에 따른 변화
        player1.change_location(left_go, right_go, up_go, down_go, obstacle_sprites)
        
        data = "move " + str(player1.x) + " " + str(player1.y) + " " + str(player1.current_sprite)

        players, balloons = server.send(data)
        
        #print(now_count)
        if space_go == True and ball_released == 0:
            if now_count > 0:
                #balloon1_copy = copy.copy(balloon1)
                #balloon1_copy.initTime = time.time()
                #balloon1_copy.x = round(player1.x + player1.sx/2 - balloon1_copy.bx/2)
                #balloon1_copy.y = player1.y + 10
                ballinitTime = time.time()
                ballx = round(player1.x + player1.sx/2 - 30)
                bally = player1.y + 10

                # 물풍선을 타일 안에 넣어주는 알고리즘
                if (ballx%64!=0):
                    j=0
                    while(j!=-1):
                        if (64*j<ballx) and (ballx<64*(j+1)) :
                            if abs(64*j-ballx)<abs(64*(j+1)-ballx):
                                ballx=64*j
                            else:
                                ballx=64*(j+1)
                            j=-1
                        else :
                            j+=1
                if (bally%64!=0):
                    j=0
                    while(j!=-1):
                        if (64*j<bally) and (bally<64*(j+1)) :
                            if abs(64*j-bally)<abs(64*(j+1)-bally):
                                bally=64*j
                            else:
                                bally=64*(j+1)
                            j=-1
                        else :
                            j+=1
                #m_list.append(balloon1_copy)
                balloons[current_id].append((ballx, bally, ballinitTime))
                
                ball_released = 1
                now_count -=1
        k += 1
        
        if space_go == False:
            ball_released = 0
            
            #데이터 넘길때 move x y crs 넘기기
        
        screen.fill(white)
        #redraw_window(players, m_list, current_id, sprites)
        redraw_window(players, balloons, current_id, sprites)
        
        data = ("ball", balloons[current_id]) # m_list 자체를 걍 건네줘버리기
        players, balloons = server.send(data)
        
        #업데이트
        pygame.display.update()
        
server.disconnect()
pygame.quit()
quit()


