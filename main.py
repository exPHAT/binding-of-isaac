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
from JoystickController import *
import os

init() # Initalize pygame
joystick.init() # Allow joystick support

jController = None

jCount = joystick.get_count()
if jCount > 0:
	joysticks = [joystick.Joystick(i) for i in range(jCount)]
	joysticks[0].init() # Default to first joystick
	jController = JoystickController(joysticks[0], 0.5)

else:
	print("Joystick not detected.")
	joystick.quit() # Deinit joystick

screen = display.set_mode((WIDTH, HEIGHT))

nextSong = ""
changeSong = -1

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

	# return finalSeed
	return "EGAAHBBI"

def menu():
	global nextSong, changeSong

	running = True 
	arrowpoint = 0
	rotate = 50
	spotlight = 0
	total1 = 50
	total2 = 50
	total3 = 50
	space = 1
	arrowselectionlocation = [(335,120),(350,245),(350,380)]
	swap = False
	menu = "main"
	filepoint = 0

	menuoverlay = loadTexture("menuoverlay.png", dir="menu", double=False)
	menuoverlay2 = loadTexture("menuoverlay2.png", dir="menu", double=False)
	mainbackground = loadTexture("mainbackground.png", dir="menu").convert()
	delete = loadTexture("delete.png", dir="menu")
	unselectdelete = darken(delete,0.5)
	file = [None,None,None]
	unselectfile = [None,None,None]
	file[0] = loadTexture("file1.png", dir="menu")
	unselectfile[0] = darken(file[0],0.5)
	file[1] = loadTexture("file2.png", dir="menu")
	unselectfile[1] = darken(file[1],0.5)
	file[2] = loadTexture("file3.png", dir="menu")
	unselectfile[2] = darken(file[2],0.5)
	maintitle = loadTexture("maintitle.png", dir="menu")
	arrow = loadTexture("arrow.png", dir="menu")
	filespotlight = [None,None]
	filespotlight[0] = loadTexture("filespotlight1.png", dir="menu")
	filespotlight[1] = loadTexture("filespotlight2.png", dir="menu")
	spotlightcry = [None,None]
	spotlightcry[0] = loadTexture("spotlightcry1.png", dir="menu")
	spotlightcry[1] = loadTexture("spotlightcry2.png", dir="menu")
	controloverlay = loadTexture("controloverlay.png", dir="menu")

	screen.blit(mainbackground,(0,0))
	display.flip()
	degrees = 0
	increase = -0.0
	frame2 = 0

	clock = time.Clock()

	while running:
		frame = time.get_ticks()
		mb = mouse.get_pressed()
		kd = key.get_pressed()
		mx,my = mouse.get_pos()

		if (frame - frame2) > 120:
			spotlight += 1
			frame2 = frame
			if spotlight > 1:
				spotlight = 0
		for e in event.get():
			if e.type == QUIT or (e.type == KEYDOWN and e.key == 27 and menu == "main"):
				running = False
				quit()

			if e.type == KEYDOWN and menu == "selection" and e.key == 273:
				arrowpoint -= 1
			elif e.type == KEYDOWN and menu == "selection" and e.key == 274:
				arrowpoint += 1

			if arrowpoint > 2:
				arrowpoint = 0
			elif arrowpoint < 0:
				arrowpoint = 2

			if e.type == KEYDOWN and menu == "file" and e.key == 276:
				filepoint -= 1
			elif e.type == KEYDOWN and menu == "file" and e.key == 275:
				filepoint += 1

			if e.type == KEYDOWN and menu == "file" and e.key == 273:
				space -= 1
			elif e.type == KEYDOWN and menu == "file" and e.key == 274:
				space += 1

			if e.type == KEYDOWN and menu == "file" and e.key == 32 and space == 0:
				print("delete" , filepoint)

			if e.type == KEYDOWN and menu == "selection" and e.key == 32 and arrowpoint == 1:
				running = False

			if space > 1:
				space = 0
			elif space < 0:
				space = 1


			if filepoint > 2:
				filepoint = 0
			elif filepoint < 0:
				filepoint = 2

			if menu == "selection" and e.type == KEYDOWN and e.key == 27:     
				menu = "file"
				sounds["pageTurn"].stop()
				sounds["pageTurn"].play()
				for x in range(0,960,70):
					screen.blit(mainbackground,(-960+x,-540))
					screen.blit(slide,(0+x,0))
					screen.blit(menuoverlay2,(0,0))
					display.flip()
				continue

			elif menu == "main" and e.type == KEYDOWN and e.key == 32:
				menu = "file"
				sounds["pageTurn"].stop()
				sounds["pageTurn"].play()
				for x in range(0,540,40):
					screen.blit(mainbackground,(0,0-x))
					screen.blit(slide,(0,0-x))
					screen.blit(menuoverlay,(0,0))
					screen.blit(controloverlay,(0,540-x))
					display.flip()
				continue

			elif  menu == "file" and e.type == KEYDOWN and e.key == 27:          
				menu = "main"
				sounds["pageTurn"].stop()
				sounds["pageTurn"].play()
				for x in range(0,540,40):
					screen.blit(mainbackground,(0,-540+x))
					screen.blit(slide,(0,0+x))
					screen.blit(menuoverlay,(0,0))
					screen.blit(controloverlay,(0,0+x))
					display.flip()
				continue

			elif menu == "file" and e.type == KEYDOWN and e.key == 32 and space == 1:
				menu = "selection"
				sounds["pageTurn"].stop()
				sounds["pageTurn"].play()
				for x in range(0,960,70):
					screen.blit(mainbackground,(0-x,-540))
					screen.blit(slide,(0-x,0))
					screen.blit(unselectfile[0],(-20-x,total1-5))
					screen.blit(unselectfile[1],(280-x,total2-5))
					screen.blit(unselectfile[2],(580-x,total3-5))
					screen.blit(filespotlight[spotlight],(45-x,total1))
					screen.blit(filespotlight[spotlight],(325-x,total2))
					screen.blit(filespotlight[spotlight],(635-x,total3))
					screen.blit(menuoverlay2,(0,0))
					display.flip()
				continue

		if menu == "main":
			if degrees < -1:
				increase *= -1
			elif degrees > 0:
				increase *= -1            
			screen.blit(mainbackground,(0,0))
			screen.blit(spotlightcry[spotlight],(260,100))
			rottitle = transform.rotate(maintitle,degrees)
			screen.blit(rottitle, (475-rottitle.get_width()//2,145-rottitle.get_height()//2))
			degrees += increase
			slide = screen.copy()
			screen.blit(menuoverlay,(0,0))
			
		elif menu == "file":
			screen.blit(mainbackground,(0,-540)) 
			if filepoint == 0:
				total1 -= 5
				screen.blit(file[0],(-20,total1))
				screen.blit(filespotlight[spotlight],(45,total1))
				if total1 == 15:
					total1 = 20
			else:
				total1 += 5
				screen.blit(unselectfile[0],(-20,total1))
				screen.blit(filespotlight[0],(45,total1))
				if total1 == 55:
					total1 = 50

			if filepoint == 1:
				total2 -= 5
				screen.blit(file[1],(280,total2))
				screen.blit(filespotlight[spotlight],(325,total2))
				if total2 == 15:
					total2 = 20
			else:
				total2 += 5
				screen.blit(unselectfile[1],(280,total2))
				screen.blit(filespotlight[0],(325,total2))
				if total2 == 55:
					total2 = 50

			if filepoint == 2:
				total3 -= 5
				screen.blit(file[2],(580,total3))
				screen.blit(filespotlight[spotlight],(635,total3))
				if total3 == 15:
					total3 = 20
			else:
				total3 += 5
				screen.blit(unselectfile[2],(580,total3))
				screen.blit(filespotlight[0],(635,total3))
				if total3 == 55:
					total3 = 50

			if space == 0:
				screen.blit(delete,(180,380))
			elif space == 1:
				screen.blit(unselectdelete,(180,380))
							
			
			
			
			slide = screen.copy()
			screen.blit(menuoverlay2,(0,0))
			
		elif menu == "selection":
			screen.blit(mainbackground,(-960,-540))
			screen.blit(arrow,arrowselectionlocation[arrowpoint])
			slide = screen.copy()
			screen.blit(menuoverlay2,(0,0))


		if nextSong != "" and changeSong != -1:
			if mixer.music.get_pos()/1000 >= changeSong:
				mixer.music.load(nextSong)
				mixer.music.play(-1)
				nextSong = ""
				changeSong = -1
			

		if jController != None:
			jController.update()
			
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
	"character": darken(loadTexture("character.png"), .1),
	"floors": [loadTexture("basement.png"),
			loadTexture("caves.png")],
	"controls": loadTexture("controls.png"),
	"doors": [loadTexture("door.png"),
			loadTexture("treasure_door.png"),
			loadTexture("boss_door.png"),
			loadTexture("devil_door.png"),
			loadTexture("angel_door.png")],
	"controls": loadTexture("controls.png"),
	"rocks": darken(loadTexture("rocks.png"), .1),
	"poops": loadTexture("poops.png"),
	"tears": [loadTexture("tears.png"), loadTexture("tear_pop.png")],
	"fires": [loadTexture("fire_top.png"), loadTexture("fire_bottom.png")],
	"bombs": [loadTexture("bombs.png"), [loadTexture("explosion.png")], loadTexture("smut.png")],
	"coins": [loadTexture("penny.png"), loadTexture("nickel.png"), loadTexture("dime.png")],
	"keys": loadTexture("keys.png"),
	"pickupHearts": loadTexture("pickup_hearts.png"),
	"overlays": [loadTexture("%i.png"%i, dir="overlays") for i in range(5)],
	"shading": loadTexture("shading.png"),
	"map": {
		"background": loadTexture("minimap.png").subsurface(0, 0, 112, 102),
		"in": loadTexture("minimap.png").subsurface(113, 0, 16, 16),
		"entered": loadTexture("minimap.png").subsurface(113, 16, 16, 16),
		"seen": loadTexture("minimap.png").subsurface(113, 32, 16, 16),
		"item": loadTexture("minimap.png").subsurface(113, 48, 16, 16),
		"boss": loadTexture("minimap.png").subsurface(113, 64, 16, 16),
	},
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
	"doorOpen": loadSound("doorOpen.wav"),
	"doorClose": loadSound("doorClose.wav"),
	"deathBurst": loadSound("deathBurst.wav"),
	"pageTurn": loadSound("pageTurn.wav"),
}

# Load fonts
fonts = {
	"main": loadCFont("main.png", 20, 16, 26),
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
	game.run(screen, sounds, textures, fonts, joystick=jController)


quit()
