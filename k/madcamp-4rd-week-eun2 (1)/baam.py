import pygame 
from setting import *

class baam(pygame.sprite.Sprite):
	def __init__(self,pos,groups, baam_img, initTime):
		super().__init__(groups)

		self.is_animating=False
		self.sprites = baam_img
		self.current_sprite = 0
		self.Time = initTime
		self.image = self.sprites[int(self.current_sprite)]
		self.rect = self.image.get_rect()
		self.rect.topleft = pos
		self.c_rect = self.rect
		for i in range(len(self.sprites)):
			self.sprites[i] = pygame.transform.scale(self.sprites[i], (64,64))
        
		# player 이미지 크기
		# self.image = pygame.transform.scale(self.image, (50, 60))
		self.sx, self.sy = self.image.get_size()
        
        # default
		self.move = 5   # 아이템에 따라 달라짐
		self.is_animating = False
		self.speed = 0.2   # 아이템에 따라 달라짐


	def baam_direction(self, left,right,up,down, curTime):
		self.current_sprite = int((curTime - self.Time)*30) # 초당 30프레임 가정
		#print(self.current_sprite)
		self.current_sprite = self.current_sprite//6
		if self.current_sprite <5:
			self.current_sprite = 4 - self.current_sprite
		if self.current_sprite >5:
			self.current_sprite = 0
		if left == True:
			self.image = self.sprites[self.current_sprite%5]
            
		elif right == True:
			self.image = self.sprites[5+self.current_sprite%5]

		elif up == True:
			self.image = self.sprites[10+self.current_sprite%5]

		elif down == True:
			self.image = self.sprites[15+self.current_sprite%5]