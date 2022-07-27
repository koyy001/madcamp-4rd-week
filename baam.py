import pygame 
from setting import *

class baam(pygame.sprite.Sprite):
	def __init__(self,pos,groups, baam_img):
		super().__init__(groups)

		self.is_animating=False
		self.sprites = baam_img
		self.current_sprite = 0
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

        




		'''
		if (type=="left"):
			self.image = baam_img[0]
			#self.rect = self.image.get_rect(topleft = pos)
		elif (type=="right"):
			self.image = baam_img[1]
			#self.rect = self.image.get_rect(topleft = pos)
		elif (type=="up"):
			self.image = baam_img[2]
			#self.rect = self.image.get_rect(topleft = pos)
		elif (type=="down"):
			self.image = baam_img[3]
			#self.rect = self.image.get_rect(topleft = pos)
		'''


	def baam_direction(self, left,right,up,down):
		if left == True:
			self.is_animating = True 
			self.current_sprite+=self.speed    # 속도 조절하는 ㅅㄲ
			if self.current_sprite>4:
				self.current_sprite=0
				self.is_animating = False   # 이거 설정하면, 어떤 입력값이 들어왔을 때 애니메이션 동작을 한번만 수행. 이거 설정 안하면 애니메이션 동작은 영구적 수행.
			self.image = self.sprites[int(self.current_sprite)]
            
		elif right == True:
			self.is_animating = True 
			if self.current_sprite < 5:
				self.current_sprite = 5
			self.current_sprite+=self.speed    # 속도 조절하는 ㅅㄲ
			if self.current_sprite>9:
				self.current_sprite=5
				self.is_animating = False   # 이거 설정하면, 어떤 입력값이 들어왔을 때 애니메이션 동작을 한번만 수행. 이거 설정 안하면 애니메이션 동작은 영구적 수행.
			self.image = self.sprites[int(self.current_sprite)]

		elif up == True:
			self.is_animating = True 
			if self.current_sprite < 10:
				self.current_sprite = 10
			self.current_sprite+=self.speed    # 속도 조절하는 ㅅㄲ
			if self.current_sprite>14:
				self.current_sprite=10
				self.is_animating = False   # 이거 설정하면, 어떤 입력값이 들어왔을 때 애니메이션 동작을 한번만 수행. 이거 설정 안하면 애니메이션 동작은 영구적 수행.
			self.image = self.sprites[int(self.current_sprite)]

		elif down == True:
			self.is_animating = True 
			if self.current_sprite < 15:
				self.current_sprite = 15
			self.current_sprite+=self.speed    # 속도 조절하는 ㅅㄲ
			if self.current_sprite>19:
				self.current_sprite=15
				self.is_animating = False   # 이거 설정하면, 어떤 입력값이 들어왔을 때 애니메이션 동작을 한번만 수행. 이거 설정 안하면 애니메이션 동작은 영구적 수행.
			self.image = self.sprites[int(self.current_sprite)]