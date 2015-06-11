from pygame import *
from math import *
from const import *
from func import *

def pause(screen, seed, textures, fonts, stats):
	running = True
	arrowpoint = 0
	pausecard = textures["pauseCard"]
	ticker = fonts["ticks"]
	digitstwo = fonts["main"]
	seedcard = textures["seedCard"]
	arrow = textures["arrow"]
	arrowlocation = [(350,375),(380,420)]
	seed = list(seed.upper())
	speed, shotspeed, damage, luck, firerate, distance = stats
	clock = time.Clock()

	slide = darken(screen.copy(), .6)
	for i in range(0,960,50):
		clock.tick(60)
		screen.blit(slide,(0,0))
		screen.blit(pausecard,(250-960+i,50))
		screen.blit(seedcard,(170-960+i,50))
		display.flip()


	while running:
		for e in event.get():
			if e.type == QUIT:
				quit()
			elif (e.type == KEYDOWN and e.key == 27) or (e.type == KEYDOWN and e.key == 32 and arrowpoint == 0):
				running = False
			elif e.type == KEYDOWN and e.key == 32 and arrowpoint == 1:
				return False
					
			if e.type == KEYDOWN and e.key == 273:
				arrowpoint -= 1
			elif e.type == KEYDOWN and e.key == 274:
				arrowpoint += 1

			if arrowpoint > 1:
				arrowpoint = 0
			elif arrowpoint < 0:
				arrowpoint = 1

		screen.blit(slide,(0,0)) 
		screen.blit(pausecard,(250,50))
		screen.blit(seedcard,(170,50))
		screen.blit(write(seed[0:4],digitstwo),((200,150)))
		screen.blit(write(seed[4:],digitstwo),((195,115)))
		screen.blit(arrow,(arrowlocation[arrowpoint]))
		for i in range(speed):
			screen.blit(ticker[i],(429+(i*8),193))
		for i in range(distance):
			screen.blit(ticker[i],(545+(i*8),193))
		for i in range(firerate):
			screen.blit(ticker[i],(429+(i*8),225))
		for i in range(damage):
			screen.blit(ticker[i],(429+(i*8),260))
		for i in range(shotspeed):
			screen.blit(ticker[i],(545+(i*8),225))
		for i in range(luck):
			screen.blit(ticker[i],(545+(i*8),260))

		clock.tick(60)               

		display.flip()

	for i in range(0,960,50):
		clock.tick(60)
		screen.blit(slide,(0,0))
		screen.blit(pausecard,(250+i,50))
		screen.blit(seedcard,(170+i,50))
		display.flip()
	return True     
