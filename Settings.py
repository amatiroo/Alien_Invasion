class Settings():
	
	""" A class to store all settings related to alien invasion"""
	
	def __init__(self):
		"""initialize the settings"""
		
		#Screen settings
		
		self.screen_width = 1200
		self.screen_height = 600
		self.bg_color = (255,255,255)
		
		#Ship settings
		self.ship_left = 2
		
		
		#Bullet Settings
		self.bullet_height =10
		self.bullet_width = 3
		self.bullet_color = 255,0,0
		self.bullets_allowed = 5
		
		#Alien settings
		self.fleet_drop_speed=50
		
		#Scoring
		self.alien_points =50
		
		
		#How quickly game speeds up
		self.speed_up_scale = 1.5
		
		#How quickly the alien point value increase
		self.score_scale =1.5
		
		
		self.initialize_dynamic_settings()
		

	def initialize_dynamic_settings(self):
		"""Initialize the settings that change throughout the game"""
		
		self.ship_speed_factor = 1
		self.bullet_speed_factor = 1
		self.alien_speed_factor = 0.1
		#fleet_direction of 1 represents right , and -1 represents left
		self.fleet_direction =1

	def increase_speed(self):
		"""Increase speed settings"""
		self.ship_speed_factor *= self.speed_up_scale
		self.bullet_speed_factor *= self.speed_up_scale
		self.alien_speed_factor *= self.speed_up_scale
		self.alien_points = int(self.alien_points * self.score_scale)
		print(self.alien_points)
		
		
		
