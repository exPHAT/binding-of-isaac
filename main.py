# main.py
# Aaron Taylor
# Moose Abumeeiz
#
# The main file for our final project. This is a replica of
# the popular game The Binding waof Isaac: Rebirth.
# 

from const import *
from pygame import *
from time import time as cTime
from random import *
from func import *
from Game import *
from menu import *
from JoystickController import *
import os

init() # Initalize pygame
joystick.init() # Allow joystick support

# Joystick controller
jController = None

# If there is a joystick, initialize with JoystickController
jCount = joystick.get_count()
if jCount > 0:
	joysticks = [joystick.Joystick(i) for i in range(jCount)]
	joysticks[0].init() # Default to first joystick
	jController = JoystickController(joysticks[0], 0.5)

else:
	joystick.quit() # Deinit joystick module

# Create display
screen = display.set_mode((WIDTH, HEIGHT))

# Current song setup
nextSong = ""
changeSong = -1

def playMusic(name, intro=""):
	"Plays music with possible intro"

	global nextSong, changeSong

	if os.name == "posix": # Mac (music is broken)
		return

	# Reset variables
	nextSong = ""
	changeSong = -1

	# If there is an intro, load and play it, set next songs
	if len(intro) > 0:
		intro = os.path.join('res', 'music', intro)
		mixer.music.load(intro)
		mixer.music.play(0) # Play music once 

		nextSong = os.path.join('res', 'music', name)
		changeSong = mixer.Sound(intro).get_length() - 0.05

	else:
		# Just play the song normally
		mixer.music.load(os.path.join('res', 'music', name))
		mixer.music.play(-1)

def showSymbol(screen, length, index, textures):
	"Show loading screen symbol"

	start = cTime()
	texture = textures["loading"][index]
	w = texture.get_width()
	h = texture.get_height()
	running = True
	while running:
		for e in event.get():
			if e.type == QUIT or e.type == KEYDOWN and e.key == 27:
				quit()

		# Draw the centered texture
		screen.fill((0,0,0))
		screen.blit(texture, (WIDTH//2-w//2,HEIGHT//2-h//2))

		display.flip()

		# Only run for a certian ammount of time
		if cTime() - start >= length:
			running = False

# Setup display
display.set_caption("The Binding of Isaac: Rebirth")
display.set_icon(image.load(os.path.join('res','textures', 'icon.png')))

# Load all needed textures
textures = {
	"hearts": loadTexture("hearts.png"),
	"pickups": loadTexture("pickups.png"),
	"character": [darken(loadTexture(["lazarus.png", "isaac.png", "eve.png"][i]), .1) for i in range(3)],
	"floors": [loadTexture("basement.png"),
			loadTexture("caves.png"),
			loadTexture("catacombs.png"),
			loadTexture("depths.png"),
			loadTexture("necropolis.png"),
			loadTexture("womb.png"),
			loadTexture("utero.png"),
			loadTexture("shop.png"),
			],
	"controls": loadTexture("controls.png"),
	"doors": [[loadTexture("door.png"), loadTexture("dark_door.png"), loadTexture("red_door.png")],
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
	"loading": [loadTexture("%i.png"%(i+1), dir="loading") for i in range(56)],
	"pauseCard": loadTexture("pauseCard.png", dir="pause"),
	"seedCard": loadTexture("seedcard.png", dir="pause"),
	"arrow": loadTexture("arrow.png", dir="pause", double=False),
	"pills": loadTexture("pills.png"),
	"trapdoor": loadTexture("trap_door.png"),
	"phd": loadTexture("phd.png"),
	"streak": loadTexture("streak.png"),
	"map": {
		"background": loadTexture("minimap.png").subsurface(0, 0, 112, 102),
		"in": loadTexture("minimap.png").subsurface(113, 0, 16, 16),
		"entered": loadTexture("minimap.png").subsurface(113, 16, 16, 16),
		"seen": loadTexture("minimap.png").subsurface(113, 32, 16, 16),
		"item": loadTexture("minimap.png").subsurface(113, 48, 16, 16),
		"boss": loadTexture("minimap.png").subsurface(113, 64, 16, 16),
	},
	
	"enemies": {
		"fly": loadTexture("fly.png", dir="enemies"),
		"pooter": loadTexture("pooter.png", dir="enemies"),
		"maw": loadTexture("maw.png", dir="enemies"),
		"boil": loadTexture("boil.png", dir="enemies"),
		"host": loadTexture("host.png", dir="enemies"),
	},
	"bosses": {
		"gurdy": loadTexture("gurdy.png", dir="bosses"),
		"duke": loadTexture("duke.png", dir="bosses"),
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
	"error": loadSound("error.wav"),
	"selectLeft": loadSound("selectLeft.wav"),
	"selectRight": loadSound("selectRight.wav"),
	"bossIntro": loadSound("bossIntro.wav"),
}

# Load fonts
fonts = {
	"main": loadCFont("main.png", 20, 16, 36, size=1.8),
	"pickups": loadCFont("pickup.png", 10, 12, 10),
	"ticks": loadCFont("ticks.png", 4, 17 , 8),
}

# Begin main loop
running = True
while running:
	# Start by playing the title screen music
	playMusic("titleScreenLoop.ogg", intro="titleScreenIntro.ogg")

	# Begin menu
	characterType, controls, floorSeed = menu(screen, jController, sounds,nextSong, changeSong)

	# Floor setup
	seed(floorSeed)

	# Define current time
	currTime = 0

	# Define clock (mainly for FPS)
	clock = time.Clock()

	# Play the choir noise when the user chooses a level
	# and show the random symboly 
	playMusic("titleScreenJingle.ogg")
	showSymbol(screen, 4, randint(0, 55), textures)

	# Play the normal game music
	playMusic("basementLoop.ogg", intro="basementIntro.ogg")

	# Start game
	game = Game(characterType, controls, floorSeed)
	game.run(screen, sounds, textures, fonts, joystick=jController)

quit()
