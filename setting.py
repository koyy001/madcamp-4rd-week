import pygame

# 게임창 옵션 설정
size = [1500, 900]  # 가로 : 60x25 / 세로 : 60x15
title = "crazy arcade"

# color
black = (0,0,0)
white = (255,255,255)
gray = (50, 50, 50)

tilesize = 64

# default move
left_go = False
right_go = False
up_go = False
down_go = False
space_go = False



# map tile
WORLD_MAP = [
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

ITEM_MAP = [
[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
[' ',' ','o','r','o','r','o','r','t','g','g','x','t','B','r','B','l','B','l','B',' '],
[' ',' ','R','b','R','b','R','b','t','b','g','g','t','r','o','r','o','l','l','l',' '],
[' ',' ',' ','o','r','o','r','o','l','g','g','g','l','B','b','B','b','B','b','B',' '],
[' ','x','R','b','R','b','R','b','t','g','b','g','t','o','r','o','r','o','r','o',' '],
[' ','r','o','r','o','r','o','r','l','g','g','b','l','B','b','B','b','B','b','B',' '],
[' ','l','t','l','t','l','t','l','t','g','g','g','t','l','t','l','t','l','t','l',' '],
[' ','r','o','r','o','r','o','r','l','b','b','b','l','R','R','r','r','R','R','r',' '],
[' ','B','b','B','b','B','b','B','t','g','g','g','t','o','r','o','r','o','r','o',' '],
[' ','o','r','o','r','o','r','o','l','b','g','b','l','r','o','r','o','r','o','l',' '],
[' ','B','l','B','b','B','b','B','t','g','b','g','t','b','R','b','R','b','R','l',' '],
[' ','l','l','r','o','r','o','r','l','g','g','b','l','o','r','o','r','o','l','l',' '],
[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
]
