# main.py
# Aaron Taylor
# Moose Abumeeiz
#
# The main file for our final project. This is a replica of
# the popular game The Binding of Isaac: Rebirth.

from const import *
from pygame import *
from time import time as cTime
from random import *
from func import *
from Game import *
import os

init() # Initalize pygame
joystick.init() # Allow joystick support

jCount = joystick.get_count()
if jCount > 0:
	joysticks = [joystick.Joystick(i) for i in range(jCount)]
	joysticks[0].init() # Default to first joystick
else:
	print("Joystick not detected.")
	joystick.quit() # Deinit joystick

screen = display.set_mode((WIDTH, HEIGHT))

nextSong = ""
changeSong = -1

def loadTexture(name, dir=""):
	# Load texture and double its size

	if dir != "":
		t = image.load(os.path.join('res', 'textures', dir, name))
		return t

	t = image.load(os.path.join('res','textures', name))

	if False:
		return transform.scale2x(t)
	else:
		return transform.scale(t, (t.get_width()*2, t.get_height()*2))

def loadSound(name):
	s = mixer.Sound(os.path.join('res','sounds', name))

	return s

def playMusic(name, intro=""):
	global nextSong, changeSong

	if os.name == "posix": # Mac (music is broken)
		return

	nextSong = ""
	changeSong = -1

	if len(intro) > 0:
		intro = os.path.join('res', 'music', intro)
		mixer.music.load(intro)
		mixer.music.play(0) # Play music once 

		nextSong = os.path.join('res', 'music', name)
		changeSong = mixer.Sound(intro).get_length() - 0.05

	else:
		mixer.music.load(os.path.join('res', 'music', name))
		mixer.music.play(-1)



def loadCFont(name, width, height, total):
	f = image.load(os.path.join('res', 'fonts', name))
	digits = [transform.scale(f.subsurface(width*i, 0, width, height), (width*2, height*2)) for i in range(total)]

	return digits

def generateSeed():
	SEED_LENGTH = 8
	characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
	charLen = len(characters)
	finalSeed = ""

	for i in range(SEED_LENGTH):
		finalSeed += characters[randint(0, SEED_LENGTH)]

	return finalSeed

def menu():
	global nextSong, changeSong

	loaded = False
	running = True
	arrowpoint = 0
	rotate = 50
	spotlight = 0
	total = 80
	arrowlocation = [(310,147),(315,255),(330,370)]
	swap = False
	menu = "main"
	select = Rect(400,200,200,245)

	menuoverlay = loadTexture("menuoverlay.png", dir="menu")
	menuoverlay2 = loadTexture("menuoverlay2.png", dir="menu")



	mainbackground = loadTexture("mainbackground.png", dir="menu")
	file = loadTexture("file.png", dir="menu")
	issac = loadTexture("issac.png", dir="menu")
	maintitle = loadTexture("maintitle.png", dir="menu")
	arrow = loadTexture("arrow.png", dir="menu")
	selectspotlight = [None,None]
	selectspotlight[0] = loadTexture("fileselect1.png", dir="menu")
	selectspotlight[1] = loadTexture("fileselect2.png", dir="menu")

	selectAnimation = Animation([loadTexture("fileselect1.png", dir="menu"),
	loadTexture("fileselect2.png", dir="menu")], .3)

	filespotlightAnimation = Animation([loadTexture("filespotlight1.png", dir="menu"),
		loadTexture("filespotlight2.png", dir="menu")], .3)

	spotlightAnimation = Animation([loadTexture("spotlightcry1.png", dir="menu"),
								loadTexture("spotlightcry2.png", dir="menu")], .3)

	controloverlay = loadTexture("controloverlay.png", dir="menu")
	# fileunselect = loadTexture("fileunselect.png", dir="menu")
	fileunselect = darken(file, .5)

	screen.blit(mainbackground,(0,0))
	display.flip()
	degrees = -1
	increase = -0.05
	frame2 = 0

	playMusic("titleScreenLoop.ogg", intro="titleScreenIntro.ogg")

	clock = time.Clock()

	while running:
		frame = time.get_ticks()
		mb = mouse.get_pressed()
		kd = key.get_pressed()
		mx,my = mouse.get_pos()
		currTime = cTime()

		for e in event.get():
			if e.type == QUIT:
				running = False
				quit()

			if not loaded:
				break

			if e.type == KEYDOWN and menu == "selection" and e.key == 273:
				arrowpoint -= 1

			elif e.type == KEYDOWN and menu == "selection" and e.key == 274:
				arrowpoint += 1

			if arrowpoint > 2:
				arrowpoint = 0

			elif arrowpoint < 0:
				arrowpoint = 2

			if menu == "selection" and e.type == KEYDOWN and e.key == 27:     
				menu = "file"
				for x in range(0,960,70):
					screen.blit(mainbackground,(-960+x,-540))
					screen.blit(slide,(0+x,0))
					screen.blit(menuoverlay2,(0,0))
					display.flip()
				continue

			elif menu == "main" and e.type == KEYDOWN and e.key == 32:
				menu = "file"
				for x in range(0,540,40):
					screen.blit(mainbackground,(0,0-x))
					screen.blit(slide,(0,0-x))
					screen.blit(menuoverlay,(0,0))
					screen.blit(controloverlay,(0,540-x))
					display.flip()
				continue

			elif  menu == "file" and e.type == KEYDOWN and e.key == 27:          
				menu = "main"
				for x in range(0,540,40):
					screen.blit(mainbackground,(0,-540+x))
					screen.blit(slide,(0,0+x))
					screen.blit(menuoverlay,(0,0))
					screen.blit(controloverlay,(0,0+x))
					display.flip()
				continue

			elif menu == "file" and e.type == KEYDOWN and e.key == 32:
				menu = "selection"
				for x in range(0,960,70):
					screen.blit(mainbackground,(0-x,-540))
					screen.blit(slide,(0-x,0))
					screen.blit(file,(320-x,total))
					screen.blit(selectAnimation.render(currTime), (380-x,total+150))
					screen.blit(menuoverlay2,(0,0))
					display.flip()
				continue
			elif menu == "selection" and e.type == KEYDOWN and e.key == 32:
				if arrowpoint == 0:
					running = False

		if menu == "main":
			if degrees < -2:
				increase *= -1
			elif degrees > 2:
				increase *= -1            
			screen.blit(mainbackground,(0,0))
			screen.blit(spotlightAnimation.render(currTime), (270,140))
			rottitle = transform.rotate(maintitle, degrees)
			screen.blit(rottitle,(90,50))
			degrees += increase
			slide = screen.copy()
			screen.blit(menuoverlay,(0,0))
			
		elif menu == "file":
			screen.blit(mainbackground,(0,-540)) 
			if select.collidepoint(mx,my):
				if total == 15:
					total = 20
				total -= 5
				screen.blit(file,(320,total))
				screen.blit(selectAnimation.render(currTime), (380,total+150))
				slide = screen.copy()
				screen.blit(menuoverlay2,(0,0))
			else:
				if total == 80:
					total = 75
				total += 5
				screen.blit(fileunselect,(320,total))
				screen.blit(filespotlightAnimation.render(currTime),(320,total))
				slide = screen.copy()
				screen.blit(menuoverlay2,(0,0))
			
		elif menu == "selection":
			screen.blit(mainbackground,(-960,-540))
			screen.blit(arrow,arrowlocation[arrowpoint])
			slide = screen.copy()
			screen.blit(menuoverlay2,(0,0))
			
		if nextSong != "" and changeSong != -1:
			if mixer.music.get_pos()/1000 >= changeSong:
				mixer.music.load(nextSong)
				mixer.music.play(-1)
				nextSong = ""
				changeSong = -1

		clock.tick(60)
		display.flip()

		loaded = True
	return 0, generateSeed()

display.set_caption("The Binding of Isaac: Rebirth")
display.set_icon(image.load(os.path.join('res','textures', 'isaac.png')))

# Load all needed textures
textures = {
	"hearts": loadTexture("hearts.png"),
	"pickups": loadTexture("pickups.png"),
	"character": loadTexture("character.png"),
	"floors": [loadTexture("basement.png")],
	"controls": loadTexture("controls.png"),
	"doors": [loadTexture("door.png"),
			loadTexture("treasure_door.png"),
			loadTexture("boss_door.png"),
			loadTexture("devil_door.png"),
			loadTexture("angel_door.png")],
	"controls": loadTexture("controls.png"),
	"rocks": loadTexture("rocks.png"),
	"poops": loadTexture("poops.png"),
	"tears": [loadTexture("tears.png"), loadTexture("tear_pop.png")],
	"fires": [loadTexture("fire_top.png"), loadTexture("fire_bottom.png")],
	"bombs": [loadTexture("bombs.png"), [loadTexture("explosion.png")], loadTexture("smut.png")],
	"coins": [loadTexture("penny.png"), loadTexture("nickel.png"), loadTexture("dime.png")],
	"keys": loadTexture("keys.png"),
	"pickupHearts": loadTexture("pickup_hearts.png"),
	"enemies": {
		"fly": loadTexture("fly.png"),
		"pooter": loadTexture("pooter.png"),

	}
}

# Load all sounds we need
sounds = {
	"pop": loadSound("pop.wav"),
	"explosion": loadSound("explosion.wav"),
	"hurt": [loadSound("hurt1.wav"), loadSound("hurt2.wav")],
	"tear": [loadSound("tear1.wav"), loadSound("tear2.wav"), loadSound("tearPop.wav"), loadSound("tearSplat.wav")],
	"unlock": loadSound("unlock.wav"),
	"devilRoomAppear": loadSound("devilRoomAppear.wav"),
	"angelRoomAppear": loadSound("angelRoomAppear.wav"),
	"coinDrop": loadSound("coinDrop.wav"),
	"coinPickup": loadSound("coinPickup.wav"),
	"fireBurn": loadSound("fireBurning.wav"),
	"steam": loadSound("steam.wav"),
	"keyDrop": loadSound("keyDrop.wav"),
	"keyPickup": loadSound("keyPickup.wav"),
	"heartIntake": loadSound("heartIntake.wav"),
	"holy": loadSound("holy.wav"),
	"rockBreak": loadSound("rockBreak.wav"),
}

# Load fonts
fonts = {
	"pickups": loadCFont("pickup.png", 10, 12, 10)
}

running = True
while running:
	characterType, floorSeed = menu()

	# Floor setup

	seed(floorSeed)

	currTime = 0

	clock = time.Clock()

	playMusic("basementLoop.ogg", intro="basementIntro.ogg")

	game = Game(characterType, floorSeed)
	game.run(screen, sounds, textures, fonts)


quit()
