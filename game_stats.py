class GameStats():
	"""Track statistics for alien invasion"""
	
	def __init__(self,ai_settings):
		"""Initialize statistics"""
		
		self.ai_settings=ai_settings
		self.reset_stats()
		
		#start alien invasion in an inactive state
		self.game_active = False
		
		#High Score should never be reset
		self.high_score = 0
		
		
	def reset_stats(self):
		"""Initialize the stats that can change during game"""
		self.ships_left = self.ai_settings.ship_left
		self.score=0
		self.level = 1
		
		
		
		
