# main.py
# Aaron Taylor
# Moose Abumeeiz
#
# The main file for our final project. This is a replica of
# the popular game The Binding of Isaac: Rebirth.
#
# TODO:
# Enemy knockback
# Boss
# Items
# Special controls - After menu
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

def showSymbol(screen, length, index, textures):
	start = cTime()
	texture = textures["loading"][index]
	w = texture.get_width()
	h = texture.get_height()
	running = True
	while running:
		for e in event.get():
			if e.type == QUIT or e.type == KEYDOWN and e.key == 27:
				quit()

		screen.fill((0,0,0))
		screen.blit(texture, (WIDTH//2-w//2,HEIGHT//2-h//2))

		display.flip()

		if cTime() - start >= length:
			running = False

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
	},
	"bosses": {
		"gurdy": loadTexture("gurdy.png", dir="bosses"),
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
}

# Load fonts
fonts = {
	"main": loadCFont("main.png", 20, 16, 36, size=1.8),
	"pickups": loadCFont("pickup.png", 10, 12, 10),
	"ticks": loadCFont("ticks.png", 4, 17 , 8),
}

running = True
while running:
	playMusic("titleScreenLoop.ogg", intro="titleScreenIntro.ogg")
	characterType, floorSeed = menu(screen, jController, sounds,nextSong, changeSong)

	# Floor setup
	seed(floorSeed)

	currTime = 0

	clock = time.Clock()

	playMusic("titleScreenJingle.ogg")
	showSymbol(screen, 4, randint(0, 55), textures)

	playMusic("basementLoop.ogg", intro="basementIntro.ogg")

	game = Game(characterType, floorSeed)
	game.run(screen, sounds, textures, fonts, joystick=jController)

quit()
