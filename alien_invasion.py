import sys
import pygame
from Settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import ScoreBoard



def run_game():
	#Initialize game and create a screen object .
	pygame.init()
	ai_settings = Settings()
	screen = pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
	
	#Make a ship , group to store bullets and alien fleet group.
	ship = Ship(ai_settings,screen)
	bullets = Group()
	aliens = Group()
	gf.create_fleet(ai_settings,screen,ship,aliens)	
	
	#Create an instance to store game statistics and create scoreboard
	
	stats = GameStats(ai_settings)
	sb = ScoreBoard(ai_settings,screen,stats)
	
	#set background color
	bg_color = (255,255,255)
	
	#Make the Play button
	play_button = Button(ai_settings,screen,"Play")
	
	#start with main loop for game
	
	
	while True:
		#Watch for keyboard and mouse events
		gf.check_events(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets)
		if stats.game_active:
			ship.update()
			gf.update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets)	
			gf.update_aliens(ai_settings,screen,stats,sb,ship,aliens,bullets)
		gf.update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,play_button)

run_game()
