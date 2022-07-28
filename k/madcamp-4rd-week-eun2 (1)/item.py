import pygame 
from setting import *

class item(pygame.sprite.Sprite):
	def __init__(self,pos,groups,type,items):
		super().__init__(groups)
		if (type=="longest"):	#G
			self.image = items[0]
			self.rect = self.image.get_rect(topleft = pos)
		elif (type=="needle"):	#N
			self.image = items[1]
			self.rect = self.image.get_rect(topleft = pos)
		elif (type=="fast"):	#F
			self.image = items[2]
			self.rect = self.image.get_rect(topleft = pos)
		elif (type=="longer"):	#L
			self.image = items[3]
			self.rect = self.image.get_rect(topleft = pos)
		elif (type=="many"):	#M
			self.image = items[4]
			self.rect = self.image.get_rect(topleft = pos)