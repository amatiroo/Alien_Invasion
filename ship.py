import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
	
	def __init__(self,ai_settings,screen):
		"""Initialize the ship position"""
		super(Ship,self).__init__()
		
		
		self.screen =screen
		
		#Movement flag 
		self.moving_right=False
		self.moving_left=False
		
		#Load the ship image and get its rect 
		self.image = pygame.image.load('images/ship.bmp').convert_alpha()
		self.image = pygame.transform.scale(self.image,(60,40))
		self.rect = self.image.get_rect()
		self.screen_rect = screen.get_rect()
		
		#Start each new ship at the bottom of screen
		self.rect.centery = self.screen_rect.centery
		self.rect.bottom = self.screen_rect.bottom
		
		#ship settings
		self.ai_settings = ai_settings
		
		#store ship speed factor 
		self.center = float(self.rect.centerx)
		
		
	def blitme(self):
		"""Draw the ship at its current location"""
		
		self.screen.blit(self.image,self.rect)
	
	def update(self):
		"""update ships position based on the movement flag"""
		#update ships center value not the rect
		if self.moving_right and self.rect.right < self.screen_rect.right:
			self.center +=self.ai_settings.ship_speed_factor
		if self.moving_left and self.rect.left > 0:
			self.center -=self.ai_settings.ship_speed_factor
			
		#update rect object from self center
		self.rect.centerx = self.center
			
	def center_ship(self):
		"""Center ship on the screen"""
		
		self.center = self.screen_rect.centerx
		
		
			
		
