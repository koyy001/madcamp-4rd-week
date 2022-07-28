import pygame
import time
# from time import time, localtime

class balloon:

    def __init__(self, screen, balloon_img):
        
        self.x=0
        self.y=0
        self.initTime = time.time()

        # 스크린
        self.screen=screen

        # balloon의 이미지를 불러오는 함수
        if balloon_img[-3:] == "png":
            self.image = pygame.image.load(balloon_img).convert_alpha()
        else :
            self.image = pygame.image.load(balloon_img)

        # balloon 이미지 크기    
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.bx, self.by = self.image.get_size()
        
        # default
        self.balloonCount = 3
        self.move = 0


    # 해당 player의 balloon 개수를 조절해주는 함수
    def change_balloon_count(self, item):
        if item == 1:
            self.balloonCount+=1


    # 물풍선을 screen에 띄우는 함수
    def showBalloon(self):
        self.screen.blit(self.image, (self.x,self.y))

        # tm = localtime(time())
        # print("second:", tm.tm_sec)
        # now_time = tm.tm_sec
        # if (tm.tm_sec+3)
