import sys
from Settings import Settings
from ship import Ship
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep


def check_events(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets):
	"""respond to key and mouse events  """
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.KEYUP:
			check_keyup_events(event,ship)
		elif event.type == pygame.KEYDOWN:
			check_keydown_events(event,ai_settings,screen,ship,bullets)
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x,mouse_y = pygame.mouse.get_pos()
			check_play_button(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets,mouse_x,mouse_y)
			
def check_play_button(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets,mouse_x,mouse_y):
	"""Start a new game when player clicks on play"""
	button_clicked = play_button.rect.collidepoint(mouse_x,mouse_y)
	
	if button_clicked and not stats.game_active:
		
		#Reset the game settings
		ai_settings.initialize_dynamic_settings()
		
		#Hide the mouse cursor
		pygame.mouse.set_visible(False)
			
		#Reset the game stats:
		stats.reset_stats()
		stats.game_active = True
		
		#Reset the scoreboard images
		sb.prep_score()
		sb.prep_high_score()
		sb.prep_level()
		sb.prep_ships()
		
		#Empty the list of aliens and bullets
		aliens.empty()
		bullets.empty()
		
		#Create new fleet and center the ship
		create_fleet(ai_settings,screen,ship,aliens)
		ship.center_ship()
		
		
			

		
def check_keydown_events(event,ai_settings,screen,ship,bullets):
	"""respond to keydown events"""			
					
	if event.key == pygame.K_RIGHT:
		#move the ship to the right
		ship.moving_right =True
		
	elif event.key == pygame.K_LEFT:
		ship.moving_left = True
		
	elif event.key == pygame.K_SPACE:
		fire_bullet(event,ai_settings,screen,ship,bullets)
		
	elif event.key == pygame.K_q:
			sys.exit()
		
		
def fire_bullet(event,ai_settings,screen,ship,bullets):
	#create new bullet and add it to bullets group
	if len(bullets)<ai_settings.bullets_allowed:
		new_bullet = Bullet(ai_settings,screen,ship)
		bullets.add(new_bullet)
	
		
		
def check_keyup_events(event,ship):
	"""respond to keyup events"""
		
	if event.key == pygame.K_RIGHT:
		#move the ship to the right
		ship.moving_right =False
		
	if event.key == pygame.K_LEFT:
		ship.moving_left = False

			
def update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,play_button):
	
	"""redraw screen during each pass through the loop """
	screen.fill(ai_settings.bg_color)
	
	
	#Redraw all the bullets behind the ship and aliens:
	for bullet in bullets.sprites():
		bullet.draw_bullet()
		
	ship.blitme()
	aliens.draw(screen)
	sb.show_score()
	
	#Draw the play button if game is inacive
	if not stats.game_active:
		play_button.draw_button()
	
	#make the most recently drawn screen visible 
	pygame.display.flip()
	
	
def update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets):
	"""update the new bullets postion and get rid of old bullets"""
	#update the bullet position
	bullets.update()
		
	#Get rid of bullets that have disappeared
	for bullet  in bullets.copy():
		if bullet.rect.bottom <=0:
			bullets.remove(bullet)
	check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,aliens,bullets)		
	
				
def check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,aliens,bullets):
	"""respond to bullet alien collision"""
	#Remove any bullets and aliens that have collided.
	collisions = pygame.sprite.groupcollide(bullets,aliens,True,True)
	
	if collisions:
		for aliens in collisions.values():
			stats.score += ai_settings.alien_points * len(aliens)
			sb.prep_score()
		check_high_score(stats,sb)
	
	if len(aliens) == 0:
		#Destroy existing bullets and create  new fleet
		bullets.empty()
		ai_settings.increase_speed()
		
		#Increase level
		stats.level += 1
		sb.prep_level()
		
		create_fleet(ai_settings,screen,ship,aliens)
	
	
	
	
	
def create_fleet(ai_settings,screen,ship,aliens):
	"""Create full fleet of aliens"""
	
	#spacing between each alien is equal to one alien width
	alien = Alien(ai_settings,screen)
	number_aliens_x = get_number_aliens_x(ai_settings,alien.rect.width)
	number_rows = get_number_rows(ai_settings,ship.rect.height,alien.rect.height)
	
	
	#create an alien and find the number of aliens in a row
	for row_number in range(number_rows -2 ):
		for alien_number in range(number_aliens_x):
			create_alien(ai_settings,screen,aliens,alien_number,row_number)
	
def get_number_rows(ai_settings,ship_height,alien_height):
	"""Determine the number of rows that fit on the screen"""
	
	available_space_y = (ai_settings.screen_height-(3*alien_height) - ship_height)
	number_rows = int(available_space_y / (2*alien_height))
	return number_rows
	
	
def create_alien(ai_settings,screen,aliens,alien_number,row_number):
	#Create an alien ina row and place it in position
	alien = Alien(ai_settings,screen)
	alien_width = alien.rect.width
	alien.x = alien_width + 2*alien_width*alien_number
	alien.rect.x = alien.x
	alien.rect.y = alien.rect.height + 2*alien.rect.height * row_number
	aliens.add(alien)
	
	
def get_number_aliens_x(ai_settings,alien_width):
	"""Determine the number of aliens that fit in a row"""
	available_space = ai_settings.screen_width - 2 * alien_width
	number_aliens_x = int(available_space / (2*alien_width))
	return number_aliens_x
	
def update_aliens(ai_settings,screen,stats,sb,ship,aliens,bullets):
	"""check if the fleet  is at an edge
	update the positions of all aliens in the fleet """
	check_fleet_edges(ai_settings,aliens)
	aliens.update()
	
	#Look for alien-ship collisions
	if pygame.sprite.spritecollideany(ship,aliens):
		print("ship hit!!")
		ship_hit(ai_settings,screen,stats,sb,ship,aliens,bullets)
		
	#Look for aliens hitting the bottom of the screen
	check_aliens_bottom(ai_settings,screen,stats,sb,ship,aliens,bullets)
	
def check_fleet_edges(ai_settings,aliens):
	"""respond appropriately if any aliens have reached an edge"""
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(ai_settings,aliens)
			break
			
def change_fleet_direction(ai_settings,aliens):
	""" Drop the entire fleet and change the fleet direction"""
	for alien in aliens.sprites():
		alien.rect.y +=ai_settings.fleet_drop_speed
	ai_settings.fleet_direction *=-1
	

			
def ship_hit(ai_settings,screen,stats,sb,ship,aliens,bullets):
	"""Respond to ship being hit by alien"""
	
	if stats.ships_left > 0:
		#Decrement ships left.
		stats.ships_left-=1
		
		#Update scoreboard
		sb.prep_ships()
	
		#Empty the list of aliens and bullets
		aliens.empty()
		bullets.empty()
		
		#Create new fleet and center the ship
		create_fleet(ai_settings,screen,ship,aliens)
		ship.center_ship()
		
		#Pause
		sleep(0.5)
		
	else:
		stats.game_active = False
		pygame.mouse.set_visible(True)
	
	
	
def check_aliens_bottom(ai_settings,screen,stats,sb,ship,aliens,bullets):
	"""Check if any aliens have reached the bottom of the screen"""
	
	screen_rect =screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >=screen_rect.bottom:
			#Treat this same as ship got hit
			ship_hit(ai_settings,screen,stats,sb,ship,aliens,bullets)
			break
def check_high_score(stats,sb):
	"""Check to see if there is new high score """
	
	if stats.score > stats.high_score:
		stats.high_score = stats.score
		sb.prep_high_score()
