# -*- coding: utf-8 -*-
"""
main server script for running agar.io server

can handle multiple/infinite connections on the same
local network
"""
import socket
from _thread import *
import pickle
import time
import random
import math
import json
import copy

# setup sockets
S = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
S.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Set constants
PORT = 80
MASS_LOSS_TIME = 7

W, H = 800, 800

HOST_NAME = socket.gethostname()
SERVER_IP = socket.gethostbyname(HOST_NAME)

DEFAULT_WORLD_MAP = [
[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
[' ','l','o','r','o','r','o','r','t','g','g','b','t','B','r','B','l','B','l','B',' '],
[' ','l','R','b','R','b','R','b','t','b','g','g','t','r','o','r','o','l','l','l',' '],
[' ','l','l','o','r','o','r','o','l','g','g','g','l','B','b','B','b','B','b','B',' '],
[' ','b','R','b','R','b','R','b','t','g','b','g','t','o','r','o','r','o','r','o',' '],
[' ','r','o','r','o','r','o','r','l','g','g','b','l','B','b','B','b','B','b','B',' '],
[' ','l','t','l','t','l','t','l','t','g','g','g','t','l','t','l','t','l','t','l',' '],
[' ','r','o','r','o','r','o','r','l','b','b','b','l','R','R','r','r','R','R','r',' '],
[' ','B','b','B','b','B','b','B','t','g','g','g','t','o','r','o','r','o','r','o',' '],
[' ','o','r','o','r','o','r','o','l','b','g','b','l','r','o','r','o','r','o','l',' '],
[' ','B','l','B','b','B','b','B','t','g','b','g','t','b','R','b','R','b','R','l',' '],
[' ','l','l','r','o','r','o','r','l','g','g','b','l','o','r','o','r','o','l','l',' '],
[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
]
FIELD_MAP = [ # 블럭이 없을 때 필드
[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
[' ','1','1','1','1','1','1','1','1','2','2','2','1','1','1','1','1','1','1','1',' '],
[' ','1','1','1','1','1','1','1','1','2','2','2','1','1','1','1','1','1','1','1',' '],
[' ','1','1','1','1','1','1','1','1','2','2','2','1','1','1','1','1','1','1','1',' '],
[' ','1','1','1','1','1','1','1','1','2','2','2','1','1','1','1','1','1','1','1',' '],
[' ','1','1','1','1','1','1','1','1','2','2','2','1','1','1','1','1','1','1','1',' '],
[' ','1','1','1','1','1','1','1','1','2','2','2','1','1','1','1','1','1','1','1',' '],
[' ','1','1','1','1','1','1','1','1','2','2','2','1','1','1','1','1','1','1','1',' '],
[' ','1','1','1','1','1','1','1','1','2','2','2','1','1','1','1','1','1','1','1',' '],
[' ','1','1','1','1','1','1','1','1','2','2','2','1','1','1','1','1','1','1','1',' '],
[' ','1','1','1','1','1','1','1','1','2','2','2','1','1','1','1','1','1','1','1',' '],
[' ','1','1','1','1','1','1','1','1','2','2','2','1','1','1','1','1','1','1','1',' '],
[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
]

ITEM_MAP = [ # 아이템 위치
[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
[' ','l','M','L','o','r','L','r','t','g','g','x','t','B','M','B','l','B','l','B',' '],
[' ','l','R','M','R','b','R','M','t','b','g','g','t','r','o','L','F','l','l','l',' '],
[' ','l','l','o','L','F','r','o','l','g','g','g','l','B','N','B','G','B','M','B',' '],
[' ','L','R','b','R','b','R','G','t','g','M','g','t','L','r','o','M','o','F','F',' '],
[' ','r','F','F','N','r','o','M','l','g','g','L','l','B','b','B','b','B','b','B',' '],
[' ','l','t','l','t','l','t','l','t','g','g','g','t','l','t','l','t','l','t','l',' '],
[' ','F','o','r','o','r','o','r','l','N','b','M','l','R','R','r','r','R','R','L',' '],
[' ','B','G','B','b','B','M','B','t','g','g','g','t','o','M','F','L','o','r','o',' '],
[' ','o','M','L','r','o','L','o','l','b','g','G','l','L','o','r','o','F','o','l',' '],
[' ','B','l','B','b','B','b','B','t','g','M','g','t','N','R','b','R','M','R','l',' '],
[' ','l','l','L','o','F','L','r','l','g','g','b','l','F','F','o','r','o','l','l',' '],
[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
]

##전체 변수들
players = {}
balloons = {}
booms = {}
maps = {}
items = {}
room_ready = {}
_id = 0
connections = 0

###로그인 데이터 불러오기#######
with open('server/data.json') as f:
    userdata = json.load(f)
print(userdata)

# try to connect to server
try:
    S.bind((SERVER_IP, PORT)) #서버에 연결하는 코드
except socket.error as e:
    print(str(e))
    print("[SERVER] Server could not start")
    quit()

S.listen()  # listen for connections

print(f"[SERVER] Server Started with local ip {SERVER_IP}")


def threaded_client(conn, _id): #로그인 실패해도 일단 id는 주어지는걸로
    global players
    global balloons
    global connections
    global room_ready
    username = ""
    nickname = ""
    current_id = _id
    room = 0
    game_started = False
    while True: # 로그인 성공할때가지 반복
        data = conn.recv(64) # 64 byte만큼의 데이터를 읽어옴
        #data = pickle.loads(data)
        data = data.decode("utf-8")
        #print(data)

        if data.split(" ")[0] == "login":
            split_data = data.split(" ")
            username = split_data[1]
            password = split_data[2]
            #dictionary들이 들어있는 userdata를 찾아보자
            if username in userdata:
                if userdata[username][0] == password:
                    print("[Log] username " + username + " login succeed") # 로그인 시작헀다고 띄우고
                    #players[current_id] = {"username": username, "nickname": userdata[username][1], "x": int(float(random.random()*1000)), "y": int(float(random.random()*600)), "crs": 0} # 유저 정보 저징
                    #balloons[current_id] = []
                    #print(players[current_id])
                    conn.send(str.encode(str(current_id)))
                    break
                else:
                    print("Wrong password")
                    conn.send(str.encode("-1"))
                    continue
            else:
                print("No ID")
                conn.send(str.encode("-2"))
                continue    
        elif data.split(" ")[0] == "register":
            split_data = data.split(" ")
            username = split_data[1]
            password = split_data[2]
            nickname = split_data[3]
            userdata[username] = [password, nickname] # 저장작업
            with open("data.json", "w") as f:
                json.dump(userdata, f)
            #players[current_id] = {"username": username, "nickname": nickname, "x": int(float(random.random()*1000)), "y": int(float(random.random()*600)), "crs": 0}
            #balloons[current_id] = []
            conn.send(str.encode(str(current_id)))
            break
    
    while True: # 스레드별로 무한 반복문 시작
        try:
            #print(players)
            data = conn.recv(2048)
            if not data:
                break
            
            if room <= 0:
                data = pickle.loads(data)
                if data.split(" ")[0] == "create":
                    print("A")
                    split_data = data.split(" ")
                    #새 룸 코드 만들어 부여하기
                    room = int(float(random.random() * 1000000))+1 # 6자리 랜덤 정수.. 나중에 안겹치게 할 수 있도록 합시다
                    players[room] = {}
                    #players[room][current_id] = {"username": username, "nickname": nickname, "x": int(float(random.random()*1000)), "y": int(float(random.random()*600)), "crs": 0}
                    players[room][current_id] = {"username": username, "nickname": nickname, "x": 0, "y": 0, "crs": 0, "ball_max": 1, "ball_cur" : 0, "water_power": 1, "bubble": (False, None),"player_speed":5, "needle_item":0}
                    balloons[room] = {}
                    balloons[room][current_id] = []
                    booms[room] = []
                    maps[room] = copy.deepcopy(DEFAULT_WORLD_MAP)
                    items[room] = copy.deepcopy(ITEM_MAP)
                    room_ready[room] = {} # 준비 여부 체크
                    room_ready[room][current_id] = (False, "be") # be: 배찌, da: 다오
                    
                    ##
                    send_data = pickle.dumps(room) 
                elif data.split(" ")[0] == "enter": #enter room 식으로 넘어올 예정
                    split_data = data.split(" ")
                    room = int(split_data[1])
                    if room in players:
                        #players[room][current_id] = {"username": username, "nickname": nickname, "x": int(float(random.random()*1000)), "y": int(float(random.random()*600)), "crs": 0}
                        players[room][current_id] = {"username": username, "nickname": nickname, "x": 0, "y": 0, "crs": 0, "ball_max": 1, "ball_cur" : 0, "water_power": 1, "bubble": (False, None), "player_speed":5, "needle_item":0}
                        balloons[room][current_id] = []
                        room_ready[room][current_id] = [False, "be"] # 바뀌어야 하므로 list로 씁시다
                    else:
                        room = -1
                        print("no room")
                    send_data = pickle.dumps(room)
                conn.send(send_data)
            else:
                # 매번 풍선 터지는 거 체크: x, y, 시간, 방향을 넣어주자
                for keyid in balloons[room]:
                    for m in balloons[room][keyid]:
                        if time.time() - m[2] > 3:
                            dir = [[1, 0], [0, 1], [-1, 0], [0, -1]]
                            giv = ['LEFT', 'UP', 'RIGHT', 'DOWN']
                            avl = [True, True, True, True] # 각 방향으로 물줄기를 더 틀 수 있는가?
                            pw = players[room][keyid]["water_power"]
                            x = m[0]
                            y = m[1]

                            booms[room].append((x, y, time.time(), 'CENTER'))

                            #power만큼 4방향 물줄기 구현하는 코드
                            for i in range(pw):
                                for j in range(4):
                                    if avl[j] == True:
                                        newx = m[0] + (i+1)*64*dir[j][0] # 물줄기가 실제로 놓일 위치
                                        newy = m[1] + (i+1)*64*dir[j][1]
                                        idx_x = newy//64 # 물줄기의 좌표상 위치
                                        idx_y = newx//64
                                        if idx_x<0 or idx_x>12 or idx_y < 0 or idx_y > 20:
                                            avl[j] = False
                                        elif maps[room][idx_x][idx_y]== 'R' or maps[room][idx_x][idx_y] == 'B' or maps[room][idx_x][idx_y] == 't': #아예 막히는애들은 안됨
                                            avl[j] = False # 물줄기 막기
                                        elif maps[room][idx_x][idx_y]== 'o' or maps[room][idx_x][idx_y]== 'r' or maps[room][idx_x][idx_y]== 'b': # 터지는 블럭들
                                            avl[j] = False
                                            booms[room].append((newx, newy, time.time(), giv[j])) # x좌표, y좌표, 생성시간, 방향을 넣어줌
                                            maps[room][idx_x][idx_y] = FIELD_MAP[idx_x][idx_y] # 박스가 터졌으니까 필드로 바꿔줘야겠져?
                                        elif maps[room][idx_x][idx_y]== '1' or maps[room][idx_x][idx_y]== '2': # 아이템위에 물줄기 닿은 경우
                                            items[room][idx_x][idx_y] = 'U'
                                        else:
                                            booms[room].append((newx, newy, time.time(), giv[j]))                                            
                            players[room][keyid]["ball_cur"] -= 1
                            balloons[room][keyid].remove(m)
                # 매번 물줄기 시간 체크
                for m in booms[room]:
                    if time.time() - m[2] > 0.7:
                        booms[room].remove(m)
                #print(type(data))
                #data = data.decode("utf-8")
                data = pickle.loads(data)
                #print(data)
                if type(data) == str:
                    if data.split(" ")[0] == "move":
                        split_data = data.split(" ")
                        x = int(float(split_data[1]))
                        y = int(float(split_data[2]))
                        crs = float(split_data[3])
                        players[room][current_id]["x"] = x
                        players[room][current_id]["y"] = y
                        players[room][current_id]["crs"] = crs
                    if data.split(" ")[0] == "item": # 먹은 아이템 위치
                        split_data = data.split(" ")
                        x = int(float(split_data[1]))
                        y = int(float(split_data[2]))
                        items[room][x][y] = "U"
                    
                else:
                    if data[0] == "ball": # ball 리스트를 업데이트 하기
                        balloons[room][current_id] = data[1]
                        players[room][current_id]["ball_cur"] = data[2]
                    if data[0] == "bubble": # 사람이 맞아버림
                        players[room][current_id]["bubble"] = data[1]
                    if data[0] == "longer": # "물약 아이템 먹음"
                        x = data[1][0]
                        y = data[1][1]
                        items[room][x][y] = 'U'
                        if (players[room][current_id]["water_power"]<5):
                            players[room][current_id]["water_power"] += 1
                    if data[0] == "many": # "물풍선 아이템 먹음"
                        x = data[1][0]
                        y = data[1][1]
                        items[room][x][y] = 'U'
                        players[room][current_id]["ball_max"] += 1
                    if data[0] == "longest": # "그 보라색 아이템 먹음"
                        x = data[1][0]
                        y = data[1][1]
                        items[room][x][y] = 'U'
                        players[room][current_id]["water_power"] =5
                    if data[0] == "fast": # "스케이트 먹음"
                        x = data[1][0]
                        y = data[1][1]
                        items[room][x][y] = 'U'
                        if players[room][current_id]["player_speed"]<10:
                            players[room][current_id]["player_speed"] +=2
                    if data[0] == "needle": # "바늘 아이템 먹음"
                        x = data[1][0]
                        y = data[1][1]
                        items[room][x][y] = 'U'
                        players[room][current_id]["needle_item"] +=1
                    if data[0] == "revival": # "바늘 아이템 씀" 부활하는 기능은 아직 안만듦
                        if players[room][current_id]["needle_item"]>0:
                            players[room][current_id]["needle_item"] -=1


                send_data = pickle.dumps((players[room], balloons[room], booms[room], maps[room], items[room])) # 이용자들의 데이터를 돌려줌
                #send_data = pickle.dumps(players) # 이용자들의 데이터를 돌려줌~
                conn.send(send_data)
        except Exception as e:
            print(e)
            break
        time.sleep(0.001)
    
    #When user disconnects
    print("[DISCONNECT] Name:", username, ", Client Id:", current_id, "disconnected")
    connections -= 1
    del players[room][current_id]
    conn.close

print("[GAME] Setting up level")
print("[SERVER] Waiting for connections")


# Keep looping to accept new connections
while True:
	
	host, addr = S.accept()
	print("[CONNECTION] Connected to:", addr)

	# start game when a client on the server computer connects
	if addr[0] == SERVER_IP:
		print("[STARTED] Game Started")

	# increment connections start new thread then increment ids
	connections += 1
	start_new_thread(threaded_client,(host,_id))
	_id += 1

# when program ends
print("[SERVER] Server offline")
