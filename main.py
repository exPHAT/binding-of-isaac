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
from Character import *
from Room import *
from Bomb import *
import os
import xml.etree.ElementTree as xml

init() # Initalize pygame
joystick.init() # Allow joystick support

jCount = joystick.get_count()
if jCount > 0:
	joysticks = [joystick.Joystick(i) for i in range(jCount)]
	joysticks[0].init() # Default to first joystick
	joystick.quit() # Deinit joystick

screen = display.set_mode((WIDTH, HEIGHT))

nextSong = ""

def loadTexture(name, directory=""):
	# Load texture and double its size

	if directory != "":
		t = image.load(os.path.join('res', 'textures', directory, name))
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
	global nextSong

	if os.name == "posix": # Mac (music is broken)
		return

	nextSong = ""

	if len(intro) > 0:
		mixer.music.load(os.path.join('res', 'music', intro))
		mixer.music.play(0) # Play music once 

		nextSong = os.path.join('res', 'music', name)
	else:
		mixer.music.load(os.path.join('res', 'music', name))
		mixer.music.play(-1)


def loadFloor(name, index, size, sounds, textures):
	d = xml.parse(os.path.join('res', 'floors', name)).getroot()

	floor = {}
	floor[(0,0)] = Room(index, 0, (0,0), d[0], textures, sounds)


	moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
	unusedRooms = [i for i in range(1, len(d))]
	possibleCoords = moves[:]
	rooms = [(0,0)]
	for i in range(size-1):
		chosen = choice(possibleCoords)
		x, y = chosen
		possibleCoords.remove(chosen)
		for m in moves:
			mx, my = m
			if (x+mx, y+my) not in rooms:
				possibleCoords.append((x+mx, y+my))

		unusedRoom = choice(unusedRooms)
		unusedRooms.remove(unusedRoom)
		rooms.append(chosen)
		floor[chosen] = Room(index, 0, chosen, d[unusedRoom], textures, sounds)

	roomsWithOne = []

	for room in possibleCoords:
		x, y = room
		count = 0
		for m in moves:
			mx, my = m
			newCoords = (x+mx, y+my)
			
			if newCoords in rooms:
				count += 1

		if count == 1:
			roomsWithOne.append(room)




	itemRoom = choice(roomsWithOne)
	roomsWithOne.remove(itemRoom)
	floor[itemRoom] = Room(index, 1, chosen, d[0], textures, sounds)

	bossRoom = choice(roomsWithOne)
	roomsWithOne.remove(bossRoom)
	floor[bossRoom] = Room(index, 2, chosen, d[0], textures, sounds)

	return floor

def loadCFont(name, width, height, total):
	f = image.load(os.path.join('res', 'fonts', name))
	digits = [transform.scale(f.subsurface(width*i, 0, width, height), (width*2, height*2)) for i in range(total)]

	return digits

def menu():
	running = True
	arrowpoint = 0
	rotate = 50
	spotlight = 0
	total = 80
	arrowlocation = [(310,147),(315,255),(330,370)]
	swap = False
	menu = "main"
	select = Rect(400,200,200,245)
	loadingimage = loadTexture("loadingimage.jpg", directory="menu")
	loadingimage.set_alpha(None)

	for x in range(0,50):
		time.wait(60)
		loadingimage.set_alpha(x)
		screen.blit(loadingimage,(0,0))
		display.flip()

	menuoverlay = loadTexture("menuoverlay.png", directory="menu")
	menuoverlay2 = loadTexture("menuoverlay2.png", directory="menu")
	mainbackground = loadTexture("mainbackground.png", directory="menu")
	file = loadTexture("file.png", directory="menu")
	issac = loadTexture("issac.png", directory="menu")
	maintitle = loadTexture("maintitle.png", directory="menu")
	arrow = loadTexture("arrow.png", directory="menu")
	selectspotlight = [None,None]
	selectspotlight[0] = loadTexture("fileselect1.png", directory="menu")
	selectspotlight[1] = loadTexture("fileselect2.png", directory="menu")
	filespotlight = [None,None]
	filespotlight[0] = loadTexture("filespotlight1.png", directory="menu")
	filespotlight[1] = loadTexture("filespotlight2.png", directory="menu")
	spotlightcry = [None,None]
	spotlightcry[0] = loadTexture("spotlightcry1.png", directory="menu")
	spotlightcry[1] = loadTexture("spotlightcry2.png", directory="menu")
	controloverlay = loadTexture("controloverlay.png", directory="menu")
	fileunselect = loadTexture("fileunselect.png", directory="menu")

	screen.blit(mainbackground,(0,0))
	display.flip()
	degrees = -1
	increase = -0.05
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
			if e.type == QUIT:
				running = False

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
					screen.blit(selectspotlight[spotlight],(320-x,total))
					screen.blit(menuoverlay2,(0,0))
					display.flip()
				continue

		if menu == "main":
			if degrees < -2:
				increase *= -1
			elif degrees > 2:
				increase *= -1            
			screen.blit(mainbackground,(0,0))
			screen.blit(spotlightcry[spotlight],(270,140))
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
				screen.blit(file,(320,total))
				screen.blit(selectspotlight[spotlight],(320,total))
				slide = screen.copy()
				screen.blit(menuoverlay2,(0,0))
			else:
				if total == 80:
					total = 75
				total += 5
				screen.blit(fileunselect,(320,total))
				screen.blit(filespotlight[spotlight],(320,total))
				slide = screen.copy()
				screen.blit(menuoverlay2,(0,0))
			
		elif menu == "selection":
			screen.blit(mainbackground,(-960,-540))
			screen.blit(arrow,arrowlocation[arrowpoint])
			slide = screen.copy()
			screen.blit(menuoverlay2,(0,0))
			running = False
			
			
		clock.tick(60)
		display.flip()

	return 0, "YOLOSWAG"

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

# Isaac
isaac = Character(WIDTH//2, (HEIGHT//4)*3, [[115, 100, 119, 97], [274, 275, 273, 276]], 1, 1, textures, sounds, fonts)


# Game music
playMusic("titleScreenLoop.ogg", intro="titleScreenIntro.ogg")


characterType, floorSeed = menu()

# Floor setup

seed(floorSeed)

floorIndex = 0
currentRoom = (0,0)
floor = loadFloor("basement.xml", floorIndex, randint(8, 12), sounds, textures)

adjecent = [-1,0], [0, 1], [1, 0], [0, -1]
doorPoss = [[13, 3], [6,7], [-1,3], [6,-1]]

for coord in floor:
	for i in range(len(adjecent)):
		diffX = adjecent[i][0]
		diffY = adjecent[i][1]

		coordX = coord[0]
		coordY = coord[1]

		try:
			room = floor[(diffX + coordX, diffY + coordY)]
			if room.variant != 0:
				room.addDoor(doorPoss[i], room.variant, True)
			else:
				room.addDoor(doorPoss[i], floor[coord].variant, True)
		except:
			pass


animatingRooms = []

currTime = 0

clock = time.Clock()

running = True
while running:
	# Main loop

	currTime = cTime()
	k = key.get_pressed() # Current down keys

	for e in event.get():
		if e.type == QUIT or k[K_ESCAPE]: 
			running = False

		elif e.type == KEYDOWN:
			isaac.moving(e.key, True, False)
			if e.unicode == "p":
				isaac.hurt(1, currTime)
			elif e.unicode == "e":
				if isaac.pickups[1].use(1):
					floor[currentRoom].other.append(Bomb(floor[currentRoom], 0, ((isaac.x-GRIDX)/GRATIO, (isaac.y-GRIDY)/GRATIO), [sounds["explosion"]], textures["bombs"], explode=True))
			elif e.unicode == "t":
				isaac.pickups[1].add(3)
			elif e.unicode == "h":
				isaac.hurt(1, 0, 0, currTime)
			# else:
			# 	print(e)

		elif e.type == KEYUP:
			isaac.moving(e.key, False, False)

		elif jCount > 0 and e.type == JOYAXISMOTION:
			rounded = round(e.value, 2)
			isaac.moving(e.axis, rounded, True)

	if len(animatingRooms) > 0:
		for r in animatingRooms[:]:
			r.render(screen, isaac, currTime)
			if not r.animating:
				animatingRooms.remove(r)
	else:
		screen.fill((0,0,0))
		move = floor[currentRoom].render(screen, isaac, currTime)
		if move[0] != 0 or move[1] != 0:
			old = tuple(currentRoom[:])

			currentRoom = (move[0]+currentRoom[0], move[1]+currentRoom[1])
			try:
				floor[currentRoom].animateIn(move)
				floor[old].animateOut(move)

				animatingRooms.append(floor[currentRoom])
				animatingRooms.append(floor[old])

				isaac.x += 650*(-move[0])
				isaac.y += 338*(move[1])

				isaac.clearTears()
			except:
				currentRoom = old

	if isaac.dead:
		running = False

	if nextSong != "":
		if not mixer.music.get_busy():
			mixer.music.load(nextSong)
			mixer.music.play(-1)

	# print(round(clock.get_fps(), 1), end="\r")

	display.flip()
	clock.tick(60)

quit()
