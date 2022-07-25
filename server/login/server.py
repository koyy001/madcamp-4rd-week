# -*- coding: utf-8 -*-
"""
main server script for running agar.io server

can handle multiple/infinite connections on the same
local network
"""
import socket
from _thread import *
import pickle as pickle
import time
import random
import math
import json

# setup sockets
S = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
S.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Set constants
PORT = 80
MASS_LOSS_TIME = 7

W, H = 800, 800

HOST_NAME = socket.gethostname()
SERVER_IP = socket.gethostbyname(HOST_NAME)

players = {}
_id = 0
connections = 0

###로그인 데이터 불러오기#######
with open('data.json') as f:
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
    current_id = _id
    while True: # 로그인 성공할때가지 반복
        data = conn.recv(64) # 64 byte만큼의 데이터를 읽어옴
        data = data.decode("utf-8")
        print(data)

        if data.split(" ")[0] == "login":
            split_data = data.split(" ")
            username = split_data[1]
            password = split_data[2]
            #dictionary들이 들어있는 userdata를 찾아보자
            if username in userdata:
                if userdata[username][0] == password:
                    print("[Log] username " + username + " login succeed") # 로그인 시작헀다고 띄우고
                    players[current_id] = {"username": username, "password": password, "nickname": userdata[username][1]} # 유저 정보 저징
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
            players[current_id] = {"username": username, "password": password, "nickname": nickname}
            conn.send(str.encode(str(current_id)))
            break
    
    while True: # 스레드별로 무한 반복문 시작
        try:
            data = conn.recv(32)
            if not data:
                break
            
            data = data.decode("utf-8")
            send_data = pickle.dumps((players)) # 이용자들의 데이터를 돌려줌~
            conn.send(send_data)
        except Exception as e:
            print(e)
            break
        time.sleep(0.001)
    
    #When user disconnects
    print("[DISCONNECT] Name:", username, ", Client Id:", current_id, "disconnected")
    connections -= 1
    del players[current_id]
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
