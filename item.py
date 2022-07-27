import pygame 
from setting import *

class item(pygame.sprite.Sprite):
	def __init__(self,pos,groups,type,items):
		super().__init__(groups)
		if (type=="?"):
			self.image = items[0]
			self.rect = self.image.get_rect(topleft = pos)
		elif (type=="x"):
			self.image = items[1]
			self.rect = self.image.get_rect(topleft = pos)
		elif (type=="?"):
			self.image = items[2]
			self.rect = self.image.get_rect(topleft = pos)
		elif (type=="?"):
			self.image = items[3]
			self.rect = self.image.get_rect(topleft = pos)
		elif (type=="?"):
			self.image = items[4]
			self.rect = self.image.get_rect(topleft = pos)