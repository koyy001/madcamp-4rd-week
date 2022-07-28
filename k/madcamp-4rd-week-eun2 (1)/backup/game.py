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
    
    while True:
        mod = input("What will you do? (1) Login  (2) Register (3) Quit ")
        if mod == '1':
            while True:
                username = input("Please enter your name ")
                if 0 < len(username) and len(username) < 20:
                    break;
                else:
                    print("username should be 1~19 characters")
            while True:
                password = input("Please enter your password")
                if 0 < len(password) and len(password) < 20:
                    break;
                else:
                    print("password should be 1~19 characters")
            data = "login " + username + " " + password # login username password 꼴로 줘서 split할 예정
            loginsuccess = server.login(data) # login함수를 따로 구현, 리턴으로 currentid를 받아옴
            print(loginsuccess)
            if loginsuccess>=0:
                current_id = loginsuccess # 현재 id 체크
                break;
            elif loginsuccess == -1:
                print("Password Wrong....")
                continue # 처음 과정부터 다시 실행
            else:
                print("No ID...")
                continue # 처음 과정부터 다시 실행
                
        elif mod == '2':
            while True:
                username = input("Please enter your name")
                if 0 < len(username) and len(username) < 20:
                    break;
                else:
                    print("username should be 1~19 characters")
            while True:
                password = input("Please enter your password")
                if 0 < len(password) and len(password) < 20:
                    break;
                else:
                    print("password should be 1~19 characters")
            while True:
                nickname = input("Please enter your nickname")
                if 0 < len(nickname) and len(nickname) < 20:
                    break;
                else:
                    print("nickname should be 1~19 characters")
            data = "register " + username + " " + password + " " + nickname
            loginsuccess = server.login(data) # login함수를 따로 구현, 리턴으로 currentid를 받아옴
            current_id = loginsuccess # 현재 id 체크
            print(loginsuccess)
            print("회원가입 성공")
            break
            
        else:
            server.disconnect()
            quit()
        
            
    players = server.send("get")
    
    run = True
    while run:
        player = players[current_id]
        data = "1"
        players = server.send(data)
        print('received data: ', players)
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