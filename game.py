# small network game that has differnt blobs
# moving around the screen

import contextlib

#from cv2 import RETR_LIST
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

import cv2 
import mediapipe as mp  
from PIL import ImageFont, ImageDraw, Image
import numpy as np    

from loginbox import *


players = {}
balloons = {}
booms = []
item_map = []


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


win_img = pygame.image.load("win.png").convert_alpha()
win_img = pygame.transform.scale(win_img, (856, 158))

lose_img = pygame.image.load("lose.png").convert_alpha()
lose_img = pygame.transform.scale(lose_img, (856, 158))
#image들 받아오는 부분
intro_img = pygame.image.load("intro.jpg")
intro_img = pygame.transform.scale(intro_img, (900, 700))
login_img = pygame.image.load("login.png")
login_img = pygame.transform.scale(login_img, (900, 700))
register_img = pygame.image.load("register.png")
register_img = pygame.transform.scale(register_img, (900, 700))
balloon_img = "asset/balloon/yellow.png"

create_room_img = pygame.image.load("createroom.png")
create_room_img = pygame.transform.scale(create_room_img, (900, 700))

ready_img = pygame.image.load("asset/mapchoose/ready.png").convert_alpha()
ready_img = pygame.transform.scale(ready_img, (1000, 430))
be_img = pygame.image.load("asset/mapchoose/ready_be.png").convert_alpha() #배찌 로비 이미지
be_img = pygame.transform.scale(be_img, (65, 79))
dao_img = pygame.image.load("asset/mapchoose/ready_dao.png").convert_alpha() #다오 로비 이미지
dao_img = pygame.transform.scale(dao_img, (65, 79))
ready_on_img = pygame.image.load("asset/mapchoose/ready_on.png").convert_alpha()
ready_on_img = pygame.transform.scale(ready_on_img, (105, 19))

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
ball_max = 1
ball_cur = 0
water_power = 1

erased_tile=[]

WON = 0 # 0: not defined, 1: lose, 2: won



#def redraw_window(players, m_list, current_id, sprites):
def redraw_window(players, balloons, booms, current_id, sprites, sprites2):
    screen.fill(gray)
    #print(balloons)
    
    for i in players: ## {1: {data}, 2:{data}, ...}
        if i != current_id: 
            character = players[i]["character"]
            if character == 1:
                p = player(screen, players[i]["x"], players[i]["y"], players[i]["crs"], sprites)
            else:
                p = player(screen, players[i]["x"], players[i]["y"], players[i]["crs"], sprites2)
            
            #if players[i]["bubble"][0] == True:
            #    p.image = die_img
            if players[i]["bubble"][0] == True or players[i]["bubble"][0] == "DIE":
                my_frame = int((time.time() - players[i]["bubble"][1])*30)
                for j in range(0, 7):
                    if my_frame >= 20*j and my_frame <= 20*(j+1):
                        if character==1:
                            p.image = bubble_img[j]
                        elif character==2:
                            p.image = bubble_img2[j]
                if my_frame >= 140:
                    for j in range(7, 19):
                        if my_frame >= 140 + 5*(i-7) and my_frame <= 140 * 5*(j-6):
                            if character==1:
                                p.image = bubble_img[j]
                            elif character==2:
                                p.image = bubble_img2[j]
                if my_frame >= 200:
                    if character==1:
                        p.image = bubble_img[18]
                    elif character==2:
                        p.image = bubble_img2[18]
            
            if players[i]["bubble"][0] == "Revival":
                my_frame = int((time.time() - players[i]["bubble"][1])*30)
                for j in range(0, 9):
                    if my_frame >= 5*j and my_frame <= 5*(j+1):
                        if character==1:
                            p.image = revival_img[j]
                        elif character==2:
                            p.image = revival_img2[j]
                    if my_frame >= 45:
                        if character==1:
                            p.image = revival_img[8]
                        elif character==2:
                            p.image = revival_img2[8]
            moving_sprites.add(p)
    
    visible_sprites.draw(screen)
    for keyid in balloons:
        for m in balloons[keyid]:
            # 물풍선 잔여시간을 변수에 받아놓는다 (물줄기 타일 생성할때 써먹으려고)
            
            myball = balloon(screen, balloon_img, m[0], m[1], m[2]) #물풍선을 생성해서
            myball.showBalloon() #화면에 표시해주기
    for m in booms: #물줄기가 다 담겨있으니까
        if m[3] == 'LEFT':
            baam((m[0], m[1]), [water_sprites], baam_img, m[2]).baam_direction(True,False,False,False, time.time())
        if m[3] == 'RIGHT':
            baam((m[0], m[1]), [water_sprites], baam_img, m[2]).baam_direction(False,True,False,False, time.time())
        if m[3] == 'UP':
            baam((m[0], m[1]), [water_sprites], baam_img, m[2]).baam_direction(False,False,True,False, time.time())
        if m[3] == 'DOWN':
            baam((m[0], m[1]), [water_sprites], baam_img, m[2]).baam_direction(False,False,False,True, time.time())
        if m[3] == "CENTER":
            baam((m[0], m[1]), [water_sprites], baam_img, m[2]).center_baam(time.time())
                  

    water_sprites.draw(screen)
    item_sprites.draw(screen)
    moving_sprites.draw(screen)
    over_sprites.draw(screen)
    
    if WON == 1:
        screen.blit(lose_img, (260, 300))
    elif WON == 2:
        screen.blit(win_img, (250, 300))
    

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

sprites2 = []
sprites2.append(pygame.image.load('asset/character2/down_1.png').convert_alpha())
sprites2.append(pygame.image.load('asset/character2/down_2.png').convert_alpha())
sprites2.append(pygame.image.load('asset/character2/down_3.png').convert_alpha())
sprites2.append(pygame.image.load('asset/character2/down_4.png').convert_alpha())
sprites2.append(pygame.image.load('asset/character2/up_1.png').convert_alpha())
sprites2.append(pygame.image.load('asset/character2/up_2.png').convert_alpha())
sprites2.append(pygame.image.load('asset/character2/up_3.png').convert_alpha())
sprites2.append(pygame.image.load('asset/character2/up_4.png').convert_alpha())
sprites2.append(pygame.image.load('asset/character2/left_1.png').convert_alpha())
sprites2.append(pygame.image.load('asset/character2/left_2.png').convert_alpha())
sprites2.append(pygame.image.load('asset/character2/left_3.png').convert_alpha())
sprites2.append(pygame.image.load('asset/character2/left_4.png').convert_alpha())
sprites2.append(pygame.image.load('asset/character2/right_1.png').convert_alpha())
sprites2.append(pygame.image.load('asset/character2/right_2.png').convert_alpha())
sprites2.append(pygame.image.load('asset/character2/right_3.png').convert_alpha())
sprites2.append(pygame.image.load('asset/character2/right_4.png').convert_alpha())

baam_img = []
baam_img.append(pygame.image.load('asset/balloon/baam/left/0.png').convert_alpha())
baam_img.append(pygame.image.load('asset/balloon/baam/left/1.png').convert_alpha())
baam_img.append(pygame.image.load('asset/balloon/baam/left/2.png').convert_alpha())
baam_img.append(pygame.image.load('asset/balloon/baam/left/3.png').convert_alpha())
baam_img.append(pygame.image.load('asset/balloon/baam/left/4.png').convert_alpha())
baam_img.append(pygame.image.load('asset/balloon/baam/left/5.png').convert_alpha())
baam_img.append(pygame.image.load('asset/balloon/baam/right/0.png').convert_alpha())
baam_img.append(pygame.image.load('asset/balloon/baam/right/1.png').convert_alpha())
baam_img.append(pygame.image.load('asset/balloon/baam/right/2.png').convert_alpha())
baam_img.append(pygame.image.load('asset/balloon/baam/right/3.png').convert_alpha())
baam_img.append(pygame.image.load('asset/balloon/baam/right/4.png').convert_alpha())
baam_img.append(pygame.image.load('asset/balloon/baam/right/5.png').convert_alpha())
baam_img.append(pygame.image.load('asset/balloon/baam/up/0.png').convert_alpha())
baam_img.append(pygame.image.load('asset/balloon/baam/up/1.png').convert_alpha())
baam_img.append(pygame.image.load('asset/balloon/baam/up/2.png').convert_alpha())
baam_img.append(pygame.image.load('asset/balloon/baam/up/3.png').convert_alpha())
baam_img.append(pygame.image.load('asset/balloon/baam/up/4.png').convert_alpha())
baam_img.append(pygame.image.load('asset/balloon/baam/up/5.png').convert_alpha())
baam_img.append(pygame.image.load('asset/balloon/baam/down/0.png').convert_alpha())
baam_img.append(pygame.image.load('asset/balloon/baam/down/1.png').convert_alpha())
baam_img.append(pygame.image.load('asset/balloon/baam/down/2.png').convert_alpha())
baam_img.append(pygame.image.load('asset/balloon/baam/down/3.png').convert_alpha())
baam_img.append(pygame.image.load('asset/balloon/baam/down/4.png').convert_alpha())
baam_img.append(pygame.image.load('asset/balloon/baam/down/5.png').convert_alpha())
baam_img.append(pygame.image.load('asset/balloon/baam/center/1.jpg'))
baam_img.append(pygame.image.load('asset/balloon/baam/center/2.jpg'))

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

die_img = pygame.image.load('asset/character/die.png').convert_alpha()
die_img= pygame.transform.scale(die_img, (64, 64))

bubble_img = []
bubble_img.append(pygame.image.load('asset/bubble/0.png').convert_alpha())
bubble_img.append(pygame.image.load('asset/bubble/1.png').convert_alpha())
bubble_img.append(pygame.image.load('asset/bubble/2.png').convert_alpha())
bubble_img.append(pygame.image.load('asset/bubble/3.png').convert_alpha())
bubble_img.append(pygame.image.load('asset/bubble/4.png').convert_alpha())
bubble_img.append(pygame.image.load('asset/bubble/5.png').convert_alpha())
bubble_img.append(pygame.image.load('asset/bubble/6.png').convert_alpha())
bubble_img.append(pygame.image.load('asset/bubble/7.png').convert_alpha())
bubble_img.append(pygame.image.load('asset/bubble/8.png').convert_alpha())
bubble_img.append(pygame.image.load('asset/bubble/9.png').convert_alpha())
bubble_img.append(pygame.image.load('asset/bubble/10.png').convert_alpha())
bubble_img.append(pygame.image.load('asset/bubble/11.png').convert_alpha())
bubble_img.append(pygame.image.load('asset/bubble/12.png').convert_alpha())
bubble_img.append(pygame.image.load('asset/bubble/13.png').convert_alpha())
bubble_img.append(pygame.image.load('asset/bubble/14.png').convert_alpha())
bubble_img.append(pygame.image.load('asset/bubble/15.png').convert_alpha())
bubble_img.append(pygame.image.load('asset/bubble/16.png').convert_alpha())
bubble_img.append(pygame.image.load('asset/bubble/17.png').convert_alpha())
bubble_img.append(pygame.image.load('asset/bubble/18.png').convert_alpha())
for i in range(0, 19):
    bubble_img[i] = pygame.transform.scale(bubble_img[i], (80, 80))
    
bubble_img2 = []
bubble_img2.append(pygame.image.load('asset/bubble2/0.png').convert_alpha())
bubble_img2.append(pygame.image.load('asset/bubble2/1.png').convert_alpha())
bubble_img2.append(pygame.image.load('asset/bubble2/2.png').convert_alpha())
bubble_img2.append(pygame.image.load('asset/bubble2/3.png').convert_alpha())
bubble_img2.append(pygame.image.load('asset/bubble2/4.png').convert_alpha())
bubble_img2.append(pygame.image.load('asset/bubble2/5.png').convert_alpha())
bubble_img2.append(pygame.image.load('asset/bubble2/6.png').convert_alpha())
bubble_img2.append(pygame.image.load('asset/bubble2/7.png').convert_alpha())
bubble_img2.append(pygame.image.load('asset/bubble2/8.png').convert_alpha())
bubble_img2.append(pygame.image.load('asset/bubble2/9.png').convert_alpha())
bubble_img2.append(pygame.image.load('asset/bubble2/10.png').convert_alpha())
bubble_img2.append(pygame.image.load('asset/bubble2/11.png').convert_alpha())
bubble_img2.append(pygame.image.load('asset/bubble2/12.png').convert_alpha())
bubble_img2.append(pygame.image.load('asset/bubble2/13.png').convert_alpha())
bubble_img2.append(pygame.image.load('asset/bubble2/14.png').convert_alpha())
bubble_img2.append(pygame.image.load('asset/bubble2/15.png').convert_alpha())
bubble_img2.append(pygame.image.load('asset/bubble2/16.png').convert_alpha())
bubble_img2.append(pygame.image.load('asset/bubble2/17.png').convert_alpha())
bubble_img2.append(pygame.image.load('asset/bubble2/18.png').convert_alpha())
bubble_img2.append(pygame.image.load('asset/bubble2/19.png').convert_alpha())
bubble_img2.append(pygame.image.load('asset/bubble2/20.png').convert_alpha())
bubble_img2.append(pygame.image.load('asset/bubble2/21.png').convert_alpha())
bubble_img2.append(pygame.image.load('asset/bubble2/22.png').convert_alpha())
bubble_img2.append(pygame.image.load('asset/bubble2/23.png').convert_alpha())
bubble_img2.append(pygame.image.load('asset/bubble2/24.png').convert_alpha())
bubble_img2.append(pygame.image.load('asset/bubble2/25.png').convert_alpha())
bubble_img2.append(pygame.image.load('asset/bubble2/26.png').convert_alpha())
for i in range(0, 27):
    bubble_img2[i] = pygame.transform.scale(bubble_img2[i], (80, 80))

revival_img = []
revival_img.append(pygame.image.load('asset/bubble/revival/0.png').convert_alpha())
revival_img.append(pygame.image.load('asset/bubble/revival/1.png').convert_alpha())
revival_img.append(pygame.image.load('asset/bubble/revival/2.png').convert_alpha())
revival_img.append(pygame.image.load('asset/bubble/revival/3.png').convert_alpha())
revival_img.append(pygame.image.load('asset/bubble/revival/4.png').convert_alpha())
revival_img.append(pygame.image.load('asset/bubble/revival/5.png').convert_alpha())
revival_img.append(pygame.image.load('asset/bubble/revival/6.png').convert_alpha())
revival_img.append(pygame.image.load('asset/bubble/revival/7.png').convert_alpha())
revival_img.append(pygame.image.load('asset/bubble/revival/8.png').convert_alpha())
for i in range(0, 9):
    revival_img[i] = pygame.transform.scale(revival_img[i], (80, 80))

revival_img2 = []
revival_img2.append(pygame.image.load('asset/bubble2/revival/0.png').convert_alpha())
revival_img2.append(pygame.image.load('asset/bubble2/revival/1.png').convert_alpha())
revival_img2.append(pygame.image.load('asset/bubble2/revival/2.png').convert_alpha())
revival_img2.append(pygame.image.load('asset/bubble2/revival/3.png').convert_alpha())
revival_img2.append(pygame.image.load('asset/bubble2/revival/4.png').convert_alpha())
revival_img2.append(pygame.image.load('asset/bubble2/revival/5.png').convert_alpha())
revival_img2.append(pygame.image.load('asset/bubble2/revival/6.png').convert_alpha())
revival_img2.append(pygame.image.load('asset/bubble2/revival/7.png').convert_alpha())
revival_img2.append(pygame.image.load('asset/bubble2/revival/8.png').convert_alpha())
for i in range(0, 9):
    revival_img2[i] = pygame.transform.scale(revival_img2[i], (80, 80))



if balloon_img[-3:] == "png":
    balloon_img = pygame.image.load(balloon_img).convert_alpha()
else :
    balloon_img = pygame.image.load(balloon_img)
#balloon1 = balloon(screen, balloon_img)
#now_count = balloon1.balloonCount


room = 0 # 0: Lobby, else: n번 룸

game_started = False
room_ready = {}


#### 손가락 인식 관련 상수####
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
mp_drawing_styles = mp.solutions.drawing_styles


# 손가락 캡처창
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,30)

cap = cv2.VideoCapture(0) # cap으로 비디오 캡처
SB =0

initialize = False # 처음에 init 했는가?

with mp_hands.Hands(
    min_detection_confidence = 0.5,
    min_tracking_confidence = 0.5) as hands:
    



    while SB == 0:
        if room == 0: # 참가 or 방 생성 화면
            clock.tick(30)
            pygame.display.set_mode((900, 700))
            input_box1 = InputBox(543, 565, 170, 32) #ID
            input_boxes = [input_box1]
            button_c = button(position=(247, 607), size=(140, 88), clr=(220, 220, 220), cngclr=(255, 0, 0), func=fn_create, text='CreateRoom', visible = False)
            button_e = button(position=(575, 633), size=(290, 30), clr=(220, 220, 220), cngclr=(255, 0, 0), func=fn_enter, text='EnterRoom', visible = False)
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
                            print(pos)
                            if button_c.rect.collidepoint(pos):
                                room = button_c.call_back(server)
                            if button_e.rect.collidepoint(pos):
                                room = button_e.call_back(server, input_box1.text)
                for box in input_boxes: # 박스 정보 업데이트하기
                    box.update()
                screen.fill((30, 30, 30))
                screen.blit(create_room_img, (0, 0)) # 배경 띄우기
                for box in input_boxes: # 박스 그리기
                    box.draw(screen)
                for b in button_list: # 버튼 그리기
                    b.draw(screen)
                    
                if room >0 :
                    #pygame.quit()
                    break
                pygame.display.update()
            
        else:
            
            if game_started == False: # 준비창
                players, room_ready, game_started = server.send("get")
                
                clock.tick(30)
                pygame.display.set_mode((1000, 430))
                button_ready = button(position=(750, 350), size=(470, 130), clr=(220, 220, 220), cngclr=(255, 0, 0), func=fn_ready, text='Ready', visible = False)
                button_character_b = button(position=(250, 270), size=(500, 90), clr=(220, 220, 220), cngclr=(255, 0, 0), func=fn_ready, text='', visible = False)
                button_character_d = button(position=(250, 380), size=(500, 90), clr=(220, 220, 220), cngclr=(255, 0, 0), func=fn_ready, text=' ', visible = False)
            
                button_list = [button_ready,button_character_b,button_character_d]
                #button_chr = button(position=(454, 468), size=(97, 28), clr=(220, 220, 220), cngclr=(255, 0, 0), func=fn_enter, text='EnterRoom', visible = True)
                while game_started == False:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            crash = False
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            if event.button == 1:
                                pos = pygame.mouse.get_pos()
                                print(pos)
                                if button_ready.rect.collidepoint(pos):
                                    players, room_ready, game_started = button_ready.call_back(server)
                                elif button_character_b.rect.collidepoint(pos):
                                    print("배찌선택")
                                    character=1
                                    data = "character " + str(1)
                                    players, room_ready, game_started = server.send(data)
                                elif button_character_d.rect.collidepoint(pos):
                                    print("다오선택")
                                    character=2
                                    data = "character " + str(2)
                                    players, room_ready, game_started = server.send(data)
                    screen.fill((30, 30, 30))
                    screen.blit(ready_img, (0, 0)) # 배경 띄우기
                    if game_started == True:
                        break
                    players, room_ready, game_started = server.send("")
                    
                    myfont = pygame.font.SysFont("Sans", 17, bold = True) 
                    ready_idx = 0
                    roomcode_text = myfont.render(str(room), True, (0, 0, 0))
                    screen.blit(roomcode_text, (160, 19))
                    for people in players:
                            if players[people]["character"]==1:
                                screen.blit(be_img, (38+120*ready_idx, 85))
                            elif players[people]["character"]==2:
                                screen.blit(dao_img, (38+120*ready_idx, 85))
                            ready_idx +=1
                    ready_idx=0
                    for keys in room_ready: # 사람별로 준비창 등등 띄울 예정
                        nickname_text = myfont.render(players[keys]["nickname"], True, (0, 0, 0))
                        text_rect = nickname_text.get_rect(center = (70 + 120*ready_idx, 181))
                        screen.blit(nickname_text, text_rect)
                        if room_ready[keys][0] == True:
                            screen.blit(ready_on_img, (19+120*ready_idx, 195))
                        ready_idx +=1
                        
                        
                    
                    for b in button_list: # 버튼 그리기
                        b.draw(screen)
                    pygame.display.update()
            else:
                
                if initialize == False:
                    players, balloons, booms, WORLD_MAP, item_map = server.send("get")
                    initialize = True
                clock.tick(30) # FPS 설정            
                
                
                ## cv 관련 부분
                success, image = cap.read()
                if not success:
                    print("Empty Camera")
                    continue
                
                image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
                image.flags.writeable = False
                results = hands.process(image)
                
                # Draw the hand annotations on the image.
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                image_height, image_width, _ = image.shape
                
                
                # 플레이어 데이터 받아올 부분인데... 나중에 고치자
                player1 = players[current_id]
                ball_max = player1["ball_max"]
                ball_cur = player1["ball_cur"]
                water_power = player1["water_power"]
                player_speed = player1["player_speed"]
                needle_item = player1["needle_item"]
                character = player1["character"]
                ssprites=sprites
                if character==2:
                    ssprites=sprites2
                #print(players)
                player1 = player(screen, player1["x"], player1["y"], player1["crs"], ssprites)
                player1.move=player_speed

                obstacle_sprites = pygame.sprite.Group() # 매번 sprite group 새로 만들기
                visible_sprites = pygame.sprite.Group()
                over_sprites = pygame.sprite.Group()
                moving_sprites = pygame.sprite.Group()
                water_sprites = pygame.sprite.Group()
                item_sprites = pygame.sprite.Group()
                moving_sprites.add(player1)
                
                for row_index,row in enumerate(WORLD_MAP):
                    for col_index, col in enumerate(row):
                        x = col_index * tilesize
                        y = row_index * tilesize
                        if col == 'l' or col == '1':
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
                        elif col == 'g' or col == '2':
                            tile((x,y),[visible_sprites], "road", tile_img)

                        
                recent_items = []
                for row_index,row in enumerate(WORLD_MAP):
                    for col_index, col in enumerate(row):
                        x = col_index * tilesize
                        y = row_index * tilesize
                        if col == '1' or col == '2':
                            col = item_map[row_index][col_index]
                            if col == 'N':
                                item((x,y),[item_sprites], "needle",items)
                            elif col == 'M':
                                item((x,y),[item_sprites], "many",items)
                            elif col == 'L':
                                item((x,y),[item_sprites], "longer",items)
                            elif col == 'G':
                                item((x,y),[item_sprites], "longest",items)
                            elif col == 'F':
                                item((x,y),[item_sprites], "fast",items)
                            recent_items.append((x,y,col))



                            
                for i in recent_items:
                    itemrect = pygame.Rect(i[0], i[1], 64, 64)
                    if itemrect.colliderect(player1.c_rect):
                        if i[2] == 'L':
                            data = ("longer", (i[1]//64, i[0]//64))
                            players, balloons, booms, WORLD_MAP, item_map = server.send(data)
                        elif i[2] == 'M':
                            data = ("many", (i[1]//64, i[0]//64))
                            players, balloons, booms, WORLD_MAP, item_map = server.send(data)
                        elif i[2] == 'G':
                            data = ("longest", (i[1]//64, i[0]//64))
                            players, balloons, booms, WORLD_MAP, item_map = server.send(data)
                        elif i[2] == 'F':
                            data = ("fast", (i[1]//64, i[0]//64))
                            players, balloons, booms, WORLD_MAP, item_map = server.send(data)
                        elif i[2] == 'N':
                            data = ("needle", (i[1]//64, i[0]//64))
                            players, balloons, booms, WORLD_MAP, item_map = server.send(data)
                
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
                
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:

                    # 엄지가 일자로 펴져 있는 경우
                        thumb_finger_state = 0
                        if hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_CMC].y * image_height > hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP].y * image_height:
                            if hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP].y * image_height > hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].y * image_height:
                                if hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].y * image_height > hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y * image_height:
                                    thumb_finger_state = 1

                    # 검지가 일자로 펴져 있는 경우
                        index_finger_state = 0
                        if hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].y * image_height > hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].y * image_height:
                            if hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].y * image_height > hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP].y * image_height:
                                if hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP].y * image_height > hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_height:
                                    index_finger_state = 1

                        # 중지가 일자로 펴져 있는 경우
                        middle_finger_state = 0
                        if hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y * image_height > hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y * image_height:
                            if hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y * image_height > hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_DIP].y * image_height:
                                if hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_DIP].y * image_height > hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y * image_height:
                                    middle_finger_state = 1

                        # 약지가 일자로 펴져 있는 경우
                        ring_finger_state = 0
                        if hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP].y * image_height > hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP].y * image_height:
                            if hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP].y * image_height > hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_DIP].y * image_height:
                                if hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_DIP].y * image_height > hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y * image_height:
                                    ring_finger_state = 1

                        # 소지가 일자로 펴져 있는 경우
                        pinky_finger_state = 0
                        if hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP].y * image_height > hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP].y * image_height:
                            if hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP].y * image_height > hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_DIP].y * image_height:
                                if hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_DIP].y * image_height > hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y * image_height:
                                    pinky_finger_state = 1



                        # 방향
                        # hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP] : 8번 관절
                        # hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP] : 5번 관절
                        # hand_landmarks.landmark[mp_hands.HandLandmark.WRIST] : 0번 관절
                        x1 = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x
                        y1 = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y
                        x2 = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x
                        y2 = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
                        xm = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].x
                        ym = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].y


                        # 방향키로 넘어갈 조건
                        arrow = 0
                        if abs(x1-xm)/2<abs(xm-x2):
                            arrow = 1
                        elif abs(y1-ym)/2<abs(ym-y2):
                            arrow = 1

                        text = ""

                        keys = ""
                        # 주먹
                        if index_finger_state == 0 and middle_finger_state == 0 and ring_finger_state == 0 and pinky_finger_state == 0 and arrow == 0:
                            text = "주먹"
                            if players[current_id]["bubble"][0] == True:
                                data = ("revival", (1, 1))    # 바늘써서 부활
                                players, balloons, booms, WORLD_MAP, item_map = server.send(data)  
                        # 보
                        elif thumb_finger_state == 1 and index_finger_state == 1 and middle_finger_state == 1 and ring_finger_state == 1 and pinky_finger_state == 1:
                            text = "보"
                            space_go = True
                            right_go = False
                            left_go = False
                            up_go = False
                            down_go = False
                        # 오른쪽 방향
                        elif 0<(abs(y2-y1))/(x2-x1)<1:
                            text = "오른쪽"
                            right_go = True
                            space_go = False
                            left_go = False
                            up_go = False
                            down_go = False
                        # 왼쪽 방향
                        elif 0>(abs(y2-y1))/(x2-x1)>-1:
                            text = "왼쪽"
                            left_go = True
                            space_go = False
                            right_go = False
                            up_go = False
                            down_go = False
                        # 위쪽 방향
                        elif (y2-y1)/(abs(x2-x1))<-1:
                            text = "위"
                            up_go = True
                            space_go = False
                            right_go = False
                            left_go = False
                            down_go = False
                        # 아래쪽 방향
                        elif (y2-y1)/(abs(x2-x1))>1:
                            text = "아래"
                            down_go = True
                            space_go = False
                            right_go = False
                            left_go = False
                            up_go = False

                        # 손가락 위치 확인한 값을 사용하여 1,2,3,4,5 중 하나를 출력 해줍니다.
                        font = ImageFont.truetype("fonts/gulim.ttc", 80)
                        image = Image.fromarray(image)
                        draw = ImageDraw.Draw(image)
                        
                        w, h = font.getsize(text)

                        x = 50
                        y = 50

                        draw.rectangle((x, y, x + w, y + h), fill='black')
                        draw.text((x, y),  text, font=font, fill=(255, 255, 255))
                        image = np.array(image)


                        # 손가락 뼈대를 그려줍니다.
                        mp_drawing.draw_landmarks(
                            image,
                            hand_landmarks,
                            mp_hands.HAND_CONNECTIONS,
                            mp_drawing_styles.get_default_hand_landmarks_style(),
                            mp_drawing_styles.get_default_hand_connections_style())
                
                cv2.imshow('MediaPipe Hands', image)
                if cv2.waitKey(5) & 0xFF == 27:
                    break
                
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
                        elif event.key == pygame.K_a:
                            if players[current_id]["bubble"][0] == True:
                                data = ("revival", (1, 1))    # 바늘써서 부활
                                players, balloons, booms, WORLD_MAP, item_map = server.send(data)    
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
                
                down_go = False
                right_go = False
                left_go = False
                up_go = False
                
                data = "move " + str(player1.x) + " " + str(player1.y) + " " + str(player1.current_sprite)

                #players, balloons, booms, WORLD_MAP, item_map = server.send(data)
                
                
                
                for i in booms:
                    waterrect = pygame.Rect(i[0], i[1], 64, 64)
                    if waterrect.colliderect(player1.c_rect):
                        if players[current_id]["bubble"][0] == False:
                            players[current_id]["bubble"] = (True, time.time())
                            data = ("bubble", players[current_id]["bubble"])
                #players, balloons, booms, WORLD_MAP, item_map = server.send(data)
                
                if players[current_id]["bubble"][0] == True or players[current_id]["bubble"][0] == "DIE":
                    my_frame = int((time.time() - players[current_id]["bubble"][1])*30)
                    for i in range(0, 7):
                        if my_frame >= 20*i and my_frame <= 20*(i+1):
                            if character == 1:
                                player1.image = bubble_img[i]
                            elif character == 2:
                                player1.image = bubble_img2[i]
                    if my_frame >= 140:
                        players[current_id]["bubble"] = ("DIE", players[current_id]["bubble"][1]) 
                        data = ("die", players[current_id]["bubble"])
                        WON = 1 # 1: die
                        for i in range(7, 19):
                            if my_frame >= 140 + 5*(i-7) and my_frame <= 140 * 5*(i-6):
                                if character == 1:
                                    player1.image = bubble_img[i]
                                elif character == 2:
                                    player1.image = bubble_img2[i]
                    if my_frame >= 200:
                        if character == 1:
                            player1.image = bubble_img[i]
                        elif character == 2:
                            player1.image = bubble_img2[i]
                if players[current_id]["bubble"][0] == "Revival":
                    my_frame = int((time.time() - players[current_id]["bubble"][1])*30)
                    for i in range(0, 9):
                        if my_frame >= 5*i and my_frame <= 5*(i+1):
                            if character == 1:
                                player1.image = revival_img[i]
                            elif character == 2:
                                player1.image = revival_img2[i]
                        if my_frame >= 45:
                            if character == 1:
                                player1.image = revival_img[8]
                            elif character == 2:
                                player1.image = revival_img2[8]
                            players[current_id]["bubble"] = (False, None) 
                            data = ("revived", players[current_id]["bubble"])
                        
                    #player1.image = die_img
                players, balloons, booms, WORLD_MAP, item_map = server.send(data)
                
                pls = len(players)
                aliv = player_speed
                for keys in players:
                    if players[keys]["bubble"][0] == "DIE":
                        pls -= 1
                
                if pls == 1 and WON != 1:
                    WON = 2 # 승리
                    
                    
                data = ""
                
                #print(now_count)
                if space_go == True and ball_released == 0 and players[current_id]["bubble"][0] == False: # 캐릭터가 물풍선에 갇히면 못놓게
                    if ball_cur < ball_max:
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
                        ball_cur +=1
                        players[current_id]["ball_cur"] = ball_cur
                        data = ("ball", balloons[current_id], ball_cur) # m_list 자체를 걍 건네줘버리기
                        players, balloons, booms, WORLD_MAP, item_map = server.send(data)
                    
                k += 1
                
                if space_go == False:
                    ball_released = 0
                    
                    #데이터 넘길때 move x y crs 넘기기
                space_go = False # cv 할때..
                screen.fill(white)
                #redraw_window(players, m_list, current_id, sprites)
                redraw_window(players, balloons, booms, current_id, sprites, sprites2)
                
                
                
                #업데이트
                pygame.display.update()
        
server.disconnect()
pygame.quit()
quit()

