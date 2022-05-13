import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
	"""A class to represent alien fleet"""
	
	def __init__(self,ai_settings,screen):
		"""Initiaize alien and set its starting position"""
		
		super(Alien,self).__init__()
		self.screen=screen
		self.ai_settings=ai_settings
		
		#Load the alien image and set its rect attribute
		self.image=pygame.image.load('images/alien.bmp')
		self.image = pygame.transform.scale(self.image,(60,40))
		self.rect = self.image.get_rect()
		
		
		#start each new alien at top left of the screen
		self.rect.y=self.rect.height
		self.rect.x=self.rect.width
		
		self.x=float(self.rect.x)
		
	def blitme(self):
		"""Draw alien at its current lcation"""
		
		self.screen.blit(self.image,self.rect)

	def update(self):
		"""move alien to right"""
		self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction )
		self.rect.x = self.x
		
		
	def check_edges(self):
		"""return true if alien is at edge of the screen"""
		
		screen_rect = self.screen.get_rect()
		if(self.rect.right >= screen_rect.right):
			return True
		elif  self.rect.left <= 0:
			return True
			
	
