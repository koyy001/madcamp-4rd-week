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

from loginbox import *



players = {}
def main(): # main 루프가 들어있는 함수
    global players
    server = Network()
    server.connect()
    
    #current_id = server.connect()
    #players = server.send("get") # 처음 호출되었을 때 현재 게임 상태를 받는것
    #그러면, 로그인할때 아마 처음 login을 호출한 다음에, 게임 들어갈 때 호출하는 함수는 명확히 달라야 할 것 같다
    
    ###pygame 관련 코드###    
    current_id = -3 # 처음 상태는 -3
    mod = 0
    intro_img = pygame.image.load("intro.jpg")
    intro_img = pygame.transform.scale(intro_img, (900, 700))
    login_img = pygame.image.load("login.png")
    login_img = pygame.transform.scale(login_img, (900, 700))
    register_img = pygame.image.load("register.png")
    register_img = pygame.transform.scale(register_img, (900, 700))
    
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
        
            
    players = server.send("get")
    
    run = True
    while run:
        player = players[current_id]
        data = "1"
        players = server.send(data)
        
        pygame.display.set_mode((1500, 900))
        screen.fill((30, 30, 30))
        
        
        font = pygame.font.Font(None,60)  #폰트 설정
        screentext = "Game Window"
        screentext = font.render(screentext,True,(255,255, 255))
        screen.blit(screentext, (400, 500))
        pygame.display.update()
        clock.tick(30)
        
        #print('received data: ', players)
        #for event in pygame.event.get():
        #    if(event.type) == pygame.QUIT:
        #        run = False
        #redraw_window(players, balls, game_time, player["score"])
        #pygame.display.update()
    server.disconnect()
    #pygame.quit()
    quit()


# get users name

## 로그인을 구현해봅시당
## 1: 로그인, 2:회원가입을 입력받아
## 로그인이면 id password를 서버에 넘기고 로그인 성공 여부 확인
## 겹치는거 여부는 어케 할지 생각해봅시다
## 회원가입이면 id password nickname을 서버에 넘겨서 새로운 데이터 생성
## 



# make window start in top left hand corner
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,30)

# setup pygame window
#WIN = pygame.display.set_mode((W,H))
#pygame.display.set_caption("Blobs")

# start game
main()