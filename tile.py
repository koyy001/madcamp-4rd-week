import pygame 
from setting import *

class tile(pygame.sprite.Sprite):
	def __init__(self,pos,groups,type,tile_img):
		super().__init__(groups)
		if (type=="land"):
			self.image = tile_img[0]
			self.rect = self.image.get_rect(topleft = pos)
		elif (type=="tree_under"):
			self.image = tile_img[1]
			self.rect = self.image.get_rect(topleft = pos)
		elif (type=="redBlock"):
			self.image = tile_img[2]
			self.rect = self.image.get_rect(topleft = pos)
		elif (type=="orangeBlock"):
			self.image = tile_img[3]
			self.rect = self.image.get_rect(topleft = pos)
		elif (type=="redHouse_under"):
			self.image = tile_img[4]
			self.rect = self.image.get_rect(topleft = pos)
		elif (type=="box"):
			self.image = tile_img[5]
			self.rect = self.image.get_rect(topleft = pos)
		elif (type=="blueHouse_under"):
			self.image = tile_img[6]
			self.rect = self.image.get_rect(topleft = pos)
		elif (type=="road"):
			self.image = tile_img[7]
			self.rect = self.image.get_rect(topleft = pos)
		elif (type=="tree_up"):
			self.image = tile_img[8]
			self.rect = self.image.get_rect(topleft = (pos[0],pos[1] - tilesize/2 - 11))
		elif (type=="redHouse_up"):
			self.image = tile_img[9]
			self.rect = self.image.get_rect(topleft = (pos[0],pos[1] - tilesize/2 + 11))
		elif (type=="blueHouse_up"):
			self.image = tile_img[10]
			self.rect = self.image.get_rect(topleft = (pos[0],pos[1] - tilesize/2 + 11))
            