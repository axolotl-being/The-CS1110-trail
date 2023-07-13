#Lewis Liu, Mohit Srivastav
#Computing IDs: Lewis Liu - ll5ts Mohit Srivastav - mvs2dq

import pygame
import gamebox
import random


camera = gamebox.Camera(800, 600)

####################
# The Title Screen #
####################

title_cards = [] ##A list containing the scrolling credit cardsfor i in range(12):
	#Credit cards below scroll right
for i in range(12):
	credit = gamebox.from_image(-(160*i), 120, 'credit_card.png')
	credit.size = [100, 120]
	credit.speedx = 2
	title_cards.append(credit)
	##SS cards below scroll left
	ss = gamebox.from_image(600 + (160*i), 500, 'ss_card.png')
	ss.size = [100, 120]
	ss.speedx = -2
	title_cards.append(ss)

game_on = False

instruction = '''
Attention ALL CS students! 
Professor Upsorn is in great danger, 
and she needs YOUR help to escape Fortnite and
get enough support for a new class. 
To do this, she needs a new desktop and new TAs. 
To help her, all she needs is your credit card number,
the three numbers on the back, the expiration month/date,
and your Social Security number!
But hurry! There's only so long before the hordes of 1110
students come and force you to take a lab section!

PRESS ANY KEY TO BEGIN
'''

def draw_title(keys):
	'''This function draws the title screen. To exit it, simply press any key.'''
	global game_on

	if keys:
		game_on = True
	keys.clear()

	to_draw = []

	background_image = gamebox.from_image(400, 300, 'headshot.jpg')
	background_image.size = [800,600]
	to_draw.append(background_image)

	title_box = gamebox.from_text(400, 30, 'HELP SAVE PROFESSOR UPSORN!!', 50, 'red', True) ##The title at the top
	to_draw.append(title_box)

	ypos = 190
	for line in instruction.split('\n'):
		to_draw.append(gamebox.from_text(400, ypos, line, 30, 'red')) ##The instructions and how they're supposed to appear
		ypos += 20

	for cards in title_cards:
		cards.move_speed()
		to_draw.append(cards)
		if cards.x > 800 and cards.speedx > 0:
			cards.x = 0
		if cards.x < 0 and cards.speedx < 0:
			cards.x = 800

	for box in to_draw:
		camera.draw(box)

#####################
# ACTUAL GAME STUFF #
#####################

############################################################ Variables affecting health/progress/etc.
progress = 0 
health = 100
dysentary = False
##################################### Variables affecting timing of some sort
tick_count = 0
number_of_days_passed = 0
#################################### Variables affecting gamestates
game_over = False #Whether game is over or not
day_over = False #Whether the prompt screen at the end of the day is shown or not
disaster = False #Whether a mid-day event fires
event_selection_number = 0
flappy = False #flappybird
shoot = False #shooter
frog = False #frogger
winning_condition = False
################################### Variables affecting collectibles
ss_card_number = 0
credit_number = 0

####################################################################### SPRITES
car = gamebox.from_image(600, 350, 'station_wagon_upsorn.png')
car.scale_by(0.75)

background = gamebox.from_color(400, 550, 'white', 1000, 150)
background.scale_by(2)

progress_bar_text = gamebox.from_text(100, 450, 'TIME', 20, 'black')
max_progress = gamebox.from_color(275, 450, 'black', 300, 10)

health_bar_text = gamebox.from_text(100, 475, 'HEALTH', 20, 'black')

grass = gamebox.from_color(400, 400, 'gray', 1000, 50)

eraser = gamebox.from_image(400, 100, 'skyline.png')
eraser.size = [1000, 550]

def draw_game(keys):


	'''This function takes the keys you press as a parameter, and runs the main portion of the game. 
	That is, the actual Oregon-Trail style portion that serves as a medium between the minigames. 
	This function is responsible for checking if you have dysentery, if an event has occurred, or if you have won. 
	It also keeps a running list of how many cards you own and your health/day progress. 
	'''
############################# VARIABLES AFFECTING GAMESTATE	
	global game_over
	global flappy
	global shoot
	global frog
	global day_over
	global disaster
	global event_selection_number
	global winning_condition
############################ VARIABLES AFFECTING MAIN GAME
	global progress
	global health
	global tick_count
	global dysentary
############################# VARIABLES AFFECTING COLLECTIBLE ITEMS
	global ss_card_number
	global credit_number

	to_draw = []

	progress_bar = gamebox.from_color(275, 450, 'blue', progress, 10) ##Keeps track of how much progress you are making
	health_bar = gamebox.from_color(185, 475, 'green', health, 10) ##Keeps track of how much health you have

	ss_card_value = gamebox.from_text(700, 475, 'You have ' + str(ss_card_number) + ' SS cards', 20, 'black') ##Keeps track of SS cards
	credit_value = gamebox.from_text(700, 450, 'You have ' + str(credit_number) + ' Credit cards', 20, 'black') ##Keeps track of credit cards
	day_progress = gamebox.from_text(650, 500, 'You have been in Fortnite for ' + str(number_of_days_passed) + ' days', 20, 'black')

############################################## Background Items
	to_draw.append(eraser)
	to_draw.append(background)
	to_draw.append(grass)
############################################## Bars and signifiers of various kinds
	to_draw.append(max_progress)
	to_draw.append(progress_bar)
	to_draw.append(progress_bar_text)

	to_draw.append(health_bar)
	to_draw.append(health_bar_text)

	to_draw.append(ss_card_value)
	to_draw.append(credit_value)

	to_draw.append(day_progress)
######################################################### THE WINNING CONDITION
	if ss_card_number >= 20 and credit_number >= 17 and number_of_days_passed >= 4: #You've won if you have 20 SSN and 17 credit cards, and have passed 4 days
		winning_condition = True

############################################################### ANIMATION
	if tick_count % 10 == 0 and tick_count % 20 != 0:
		car.image = 'station_wagon_upsorn_lights.png'

	if tick_count % 20 == 0:
		car.image = 'station_wagon_upsorn.png'

	to_draw.append(car) #Drawn after animation
	
	if health <= 0: #If your health is below 0, you have died
		game_over = True
		
	else:
		progress += 1
		tick_count += 1

		dysentary_check = random.randrange(0, 1001)
		if dysentary_check % 500 == 0: # If you have dysentary, it will be noted at the end of the day
			dysentary = True

		event_check = random.randrange(1, 201)
		if event_check % 200 == 0: #Checks for disaster
			event_selection_number = random.randrange(0, 2) #Picks the random event
			disaster = True

	if progress >= 300:
		day_over = True #Initiates the end-of-day prompt
		progress = 0 #Resets Day progress at the end of the day

	for yeet in to_draw:
		yeet.move_speed()
		camera.draw(yeet)

############################
# OCCURRENCES WITHIN A DAY #
############################
event_selection = ['Oh no! A large river is in your way! You have to ford it to get away from the storm!',
'Oh no! 12 year old Fortnite gamers want your cards! Flap past for 10 seconds using SPACE!']

mingigame_countdown = 120

def oh_no(keys):
	'''This function serves as a stopgap between any mid-day minigame and the main game.
	It displays a statement based on what even you have picked, and goes to the game from there'''
	global ss_card_number
	global credit_number
	global flappy
	global frog
	global health
	global event_selection_number
	global mingigame_countdown
	global disaster

	to_draw = []

	task = gamebox.from_text(400, 300, event_selection[event_selection_number], 20, 'grey')
	to_draw.append(task)

	mingigame_countdown -= 1
	if mingigame_countdown == 0: #Displays the promt for 100 ticks

		if event_selection_number == 0: #If the frogger prompt is there, do that
			mingigame_countdown = 120
			frog = True
			disaster = False

		elif event_selection_number == 1: #If the flappy prompt is there, do that
			mingigame_countdown = 120 #Resets the minigame counter delay
			flappy = True
			disaster = False

	for box in to_draw:
		camera.draw(box)

	camera.display()

####################
# THE DAILY PROMPT #
####################

cured = False

def daily_prompt(keys):
	'''This function defines the daily end-of-day prompt that is given just like in Oregon Trail. 
	If you have dysentery, you can cure it. After/if you don't have dysentery, you can either keep going or scavenge'''
	global day_over
	global ss_card_number
	global credit_number
	global shoot
	global dysentary
	global health
	global number_of_days_passed
	global cured
	
	question = 'DAY ' + str(number_of_days_passed + 1) + ' has finished. |Would you like to scavenge then move on? [1] |Would you like to immediately keep going? [2]' 
	
	to_draw = []

	ypos = 150
	for line in question.split('|'):
		ypos += 100
		to_draw.append(gamebox.from_text(400, ypos, line, 40, 'grey'))

	if dysentary:
		to_draw.append(gamebox.from_text(400, 100, 'YOU HAVE CONTRACTED DYSENTERY, -40 HEALTH UNLESS CURED', 30, 'brown'))
		to_draw.append(gamebox.from_text(400, 130, 'CURE IT OR IT WILL AFFECT YOU EVERY DAY!', 40, 'brown'))
		to_draw.append(gamebox.from_text(400, 550, 'Would you like to cure dysentery for 8 Credit Cards? [3]', 40, 'grey'))
		
	if cured:
		to_draw.append(gamebox.from_text(400, 100, 'CURED!', 40, 'green'))

	if pygame.K_1 in keys:

		if dysentary:
			health -= 40
		shoot = True
		day_over = False

		number_of_days_passed += 1

		cured = False

	elif pygame.K_2 in keys:
		if dysentary:
			health -= 40		

		day_over = False

		number_of_days_passed += 1

		cured = False

	elif dysentary:
		if pygame.K_3 in keys:
			if credit_number >= 8:
				if dysentary:
					credit_number -= 8
					dysentary = False
					cured = True

	for box in to_draw:
		camera.draw(box)

	camera.display()

#####################
# VARIOUS MINIGAMES #
#####################

birb = gamebox.from_image(300, 300,'station_wagon_upsorn.png')
birb.size = [100, 50]
block_higher = gamebox.from_image(800, 75, "barrier.jpg")
block_higher.size = [100, 400]
block_higher.rotate(180)
block_lower = gamebox.from_image(800, 625, "barrier.jpg")
block_lower.size = [100, 400]
border_top = gamebox.from_color(400, -100, 'grey' , 800, 100)
border_bottom = gamebox.from_color(400, 700, 'grey' , 800, 100)
flappy_time = 0
flappy_on = True
flappy_timer = 0

def draw_flappy(keys):
   '''Draws the flappy-bird minigame'''
   global flappy_on, flappy_time, health, flappy, flappy_timer

   #make the blocks scroll
   block_lower.speedx = -15
   block_higher.speedx = -15
   block_lower.move_speed()
   block_higher.move_speed()

   camera.draw(block_lower)
   camera.draw(block_higher)

   #make the blocks cycle and randomize the location
   if flappy_on:

   	if int(block_higher.x) < 0:
   	    height = random.randint(-200, 200)
   	    block_higher.move(900, height)
   	    block_lower.move(900, height)

   #make the character jump
   	if pygame.K_SPACE in keys:
   	    birb.speedy = -17
   	birb.speedy += 2
   	birb.move_speed()
   	camera.draw(birb)

   #collision detection
   	camera.draw(border_top)
   	camera.draw(border_bottom)

   	if birb.touches(block_lower) or birb.touches(block_higher) or birb.touches(border_top) or birb.touches(border_bottom):
   	    flappy_on = False

   	#record how much flappy_time has elapsed
   	flappy_time += 1/30

   elif flappy_on == False: #stops when the game ends
       #display the score
       flappy_timer += 1
       camera.draw(gamebox.from_text(400, 300, "Your score was " + str(int(flappy_time)) + ".", 24, "red"))
       if flappy_time < 10:
       	camera.draw(gamebox.from_text(400, 350, "-20 health from surviving less than 10 seconds against n00bs", 24, 'red'))
       else:
       	camera.draw(gamebox.from_text(400, 350, "+5 health from looting the 12-year-olds you murdered in cold blood", 24, 'red'))
       if flappy_timer == 100:
       	if flappy_time < 10:
       		health -= 20
       	else:
       		health += 5
       	
       	flappy_timer = 0
       	flappy_time = 0
       	height = random.randint(-200, 200)
       	block_higher.x = 1000
       	block_lower.x = 1000
       	birb.center = (300, 300)
       	flappy_on = True       	
       	flappy = False
   keys.clear() #continual inputs are a no-no

   camera.draw(gamebox.from_text(400, 50, "Press Space to flap upwards! Don't touch the Fortnite players trying to steal your cards, and survive for at least 10 seconds!", 20, 'purple'))

######################################################################################################################################################

bullets = [
	gamebox.from_image(-300, 300, 'python.png'),
	]

car_shooter = gamebox.from_image(750, 300, 'station_wagon_upsorn.png')
car_shooter.scale_by(0.5)

background_shooter = gamebox.from_image(400, 300, 'shooter_background.png')
background_shooter.size = [800, 600]

obstacles_ssn = []
obstacles_cc = []

counter = 0

def draw_shoot(keys):
	'''draws the scavenging minigame'''

	global counter
	global ss_card_number
	global credit_number
	global shoot

	if counter >= 510: ##Ends the game after 500 ticks (or 17 seconds)

		camera.draw(gamebox.from_text(400, 300, 'SCAVENGE TIME IS NO MORE!', 40, 'red'))
		camera.draw(gamebox.from_text(400, 450, 'you have collected ' + str(ss_card_number) + ' SSN cards and ' + str(credit_number) + ' credit cards', 40, 'red'))
		counter += 1

		for bullet in bullets:
			bullets.remove(bullet)
		for obs in obstacles_cc:
			obstacles_cc.remove(obs)
		for obs in obstacles_ssn:
			obstacles_ssn.remove(obs)
		car_shooter.center = (750, 300)
		if counter >= 570: #Delays the ending screen from leaving too soon
			counter = 0
			shoot = False

	else:

		if counter % 25 == 0 and counter % 50 != 0: ##Spawns SSN cards every other 50 ticks
			object_count = random.randrange(0, 3)

			for i in range(0, object_count):

				credit_card_sprite = gamebox.from_image(random.randrange(0, 400), 0, 'ss_card.png')
				credit_card_sprite.size = [75, 100]
				obstacles_ssn.append(credit_card_sprite)

		if counter % 50 == 0: ##Spawns credit cards every other 50 ticks

			object_count = random.randrange(0, 3)

			for i in range(0, object_count):

				ssn_card_sprite = gamebox.from_image(random.randrange(0, 400), 0, 'credit_card.png')
				ssn_card_sprite.size = [75, 100]
				obstacles_cc.append(ssn_card_sprite)

		camera.clear('black')

		for bullet in bullets:
			bullet.move_speed()

		if pygame.K_UP in keys:
			car_shooter.y += -5

		if pygame.K_DOWN in keys:
			car_shooter.y += 5

		if pygame.K_SPACE in keys:

			bullets.append(
				gamebox.from_image(-300, 300, 'python.png'),
				)

			bullets[-1].speedx = -30

			bullets[-1].center = car_shooter.center

			car_shooter.image = 'station_wagon_upsorn_lights.png'

			keys.remove(pygame.K_SPACE)

		else:

			car_shooter.image = 'station_wagon_upsorn.png'

		for bullet in bullets:
			if int(bullet.x) < 0:
				bullets.remove(bullet)


		for bullet in bullets:
			for obs in obstacles_ssn:
				if bullet.touches(obs):
					ss_card_number += 1
					obstacles_ssn.remove(obs)
					bullets.remove(bullet)
		camera.draw(background_shooter)
		
		for bullet in bullets:
			for obs in obstacles_cc:
				if bullet.touches(obs):
					credit_number += 1 ##Keeps track of the number of cards you have
					obstacles_cc.remove(obs)
					bullets.remove(bullet)
			camera.draw(bullet)
		
		camera.draw(gamebox.from_text(400, 50, 'time left:' + str(510 - counter), 30, 'white'))		

			

		for obs in obstacles_ssn:

			obs.y += random.randrange(30, 40)
			obs.x += random.randrange(10, 20)
			camera.draw(obs)

		for obs in obstacles_cc:

			obs.y += random.randrange(30, 40) ##Constantly changing speeds makes it harder to shoot the objects
			obs.x += random.randrange(10, 20)
			camera.draw(obs)

		counter += 1

		camera.draw(car_shooter)
		camera.draw(gamebox.from_text(550, 75, 'Press Space to fire missiles to hit the cards, and UP/DOWN to move up/down', 20, 'grey'))

####################################################################################################################################################

river = gamebox.from_color(400, 300, 'blue', 800, 350)
upsorn = gamebox.from_image(400, 500, 'headshot.png')
upsorn.size = [40, 40]
log0 = gamebox.from_color(400, 500, 'grey', 200, 50)  # make sure log0 is the same as the background
log1 = gamebox.from_color(500, 450, 'brown', 200, 50)
log2 = gamebox.from_color(300, 400, 'brown', 200, 50)
log3 = gamebox.from_color(200, 350, 'brown', 200, 50)
log4 = gamebox.from_color(450, 300, 'brown', 200, 50)
log5 = gamebox.from_color(700, 250, 'brown', 200, 50)
log6 = gamebox.from_color(620, 200, 'brown', 200, 50)
log7 = gamebox.from_color(550, 150, 'brown', 200, 50)
logs = [log1, log2, log3, log4, log5, log6, log7]
logspeed1 = random.randint(-30, -15)
frog_timer = 0 


for i in range(0, len(logs)):
	logs[i].speedx = random.randint(-50, 0)

def draw_frog(keys):
   '''draws the frogger minigame'''

   global logspeed, health, frog, frog_timer

   if not upsorn.touches(river) or upsorn.touches(log1) or upsorn.touches(log2) or upsorn.touches(log3) or upsorn.touches(log4) or upsorn.touches(log5) or upsorn.touches(log6) or upsorn.touches(log7) or upsorn.touches(log0):

     camera.clear('grey')
     camera.draw(river)
     camera.draw(log0)

   # character movement
     if pygame.K_SPACE in keys:
         upsorn.move(0, -50)

   # set log speeds and scroll them

     camera.draw(log1)
     for log in logs:

       #log.speedx = random.randint(-30, -15)

         if int(log.x) < 0:
             log.move(900, 0)
           #log.speedx = random.randint(-30,-15)

         log.move_speed()
         camera.draw(log)
   # hit detection
   # also have upsorn start and end on an invisible solitary log
     for log in logs:
         if upsorn.touches(log):
             upsorn.speedx = log.speedx
             upsorn.center = log.center
             upsorn.move_speed()

     camera.draw(gamebox.from_text(400, 50, "Press SPACE to move forwards! Don't hit the river!", 30, 'black'))

   # if frog is on log, set speed of the frog to the log
   # have the frog loop as well
     if int(upsorn.x) < 0 :
         upsorn.move(900, 0)

     camera.draw(upsorn)
   elif upsorn.touches(river):
       camera.draw(gamebox.from_text(400, 300, 'YOU SUNK! -20 health', 90, 'red'))
       frog_timer += 1
       if frog_timer == 40:
       	health -= 20
       	frog = False
       	frog_timer = 0
       	upsorn.center = (400, 500)
   keys.clear()

   if upsorn.y < 0:
       camera.draw(gamebox.from_text(400, 300, 'YOU FORDED THE RIVER!', 90, 'green'))
       camera.draw(gamebox.from_text(400, 350, '+5 health from the replenishing waters', 40, 'green'))
       frog_timer += 1
       if frog_timer == 70:
       	frog = False
       	frog_timer = 0
       	upsorn.center = (400, 500)
       	health += 5
####################
# GAME OVER SCREEN #
####################

###########################################################################Winning and losing screens
win_counter = 0
def draw_winner(keys): #This is our favorite screen by far. It is our proudest creation
	'''Draws the winning screen. The amount of fun that is to be had on this screen is large'''
	global win_counter
	win_counter += 1
	to_draw = []

	now_thats_epic = gamebox.from_image(600, 300, 'epic_win.png')
	now_thats_epic.size = [800, 600]
	
	trump = gamebox.from_image(100, 300, 'winning.png')
	trump.size = [200, 600]

	borat = gamebox.from_image(700, 300, 'borat.png')
	borat.size = [200, 600]

	victory_royale = gamebox.from_image(400, 300, 'ultimate.png')
	victory_royale.size = [400, 600]

	message = gamebox.from_text(400, 50, 'UPSORN HAS RETURNED TO THE MOTHERLAND AND ESCAPED FORTNITE!', 30, 'green')
	weegee = gamebox.from_image(200, 450, 'yeet.png')
	weegee2 = gamebox.from_image(600, 450, 'yeet.png') #Make this the epic gamer win

	if win_counter % 25 in range(-10, 10):
		victory_royale.image = 'ultimate_2.png'
		weegee.image = 'yeet.png'
		weegee2.image = 'yeet.png'
	else:
		victory_royale.image = 'ultimate.png'
		weegee.image = 'yeet_start.png'
		weegee2.image = 'yeet_start.png'

	to_draw.append(now_thats_epic)
	to_draw.append(trump)
	to_draw.append(borat)
	to_draw.append(victory_royale)
	to_draw.append(message)
	to_draw.append(gamebox.from_text(400, 75, 'WITH YOUR HELP, SHE HAS STOLEN MANY IDENTITIES!', 30, 'green'))
	to_draw.append(weegee)
	to_draw.append(weegee2)

	for box in to_draw:
		camera.draw(box)

	camera.display()


def draw_game_over(keys): 
	'''if the game is over from losing health, you come here'''
	
	to_draw = []

	game_over_screen = gamebox.from_image(400, 300, 'dysentary.png')
	game_over_screen.size = [800, 600]
	to_draw.append(game_over_screen)
	game_over_text = gamebox.from_text(400, 50, 'WASTED', 50, 'red')
	to_draw.append(game_over_text)

	for box in to_draw:
		camera.draw(box)

	camera.display()

########################################################## THE THREE FUNCTIONS THAT RUN ALL THE GAMESTATES

def main_game(keys):
    '''If the title is not on, draw the game'''
    if not game_on:
        draw_title(keys) #### Draws the title screen first
    elif game_on:
    	draw_game(keys)

    camera.display()

def minigame_drawer(keys):
	'''This function checks to see what minigame to play when it is invoked'''
	if flappy and not frog and not shoot:
		draw_flappy(keys)
	elif shoot and not flappy and not frog:
		draw_shoot(keys)
	elif frog and not shoot and not flappy:
		draw_frog(keys)

	camera.display()


#################################################### THE BIG BOI FUNCTION ITSELF
def when_to_run(keys):
	'''This is the big boi function of the game. It checks all the conditions and runs the respective functions for the game to run. 
	The main game is run by the absence of everything else'''
	camera.clear('black')
	if winning_condition: #First it checks if you've won
		draw_winner(keys)
	elif game_over: #Then it checks if the game is over
		draw_game_over(keys)
	elif day_over: #Then it checks if the day is over and you need a prompt
		daily_prompt(keys)
	elif disaster: # If in the day, and there is a disaster, a disaster occurs
		oh_no(keys)
	elif flappy or frog or shoot: #If any of the minigames are on run the minigame function
		minigame_drawer(keys)	
	elif not flappy and not frog and not shoot and not game_over and not winning_condition: #Checks if any of the minigames are on, if not, then the main game runs
		main_game(keys)


gamebox.timer_loop(30, when_to_run) #This is the expression that runs the game on 30fps using the when_to_run function