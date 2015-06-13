# func.py
# Aaron Taylor
# Moose Abumeeiz
#
# This file contains a many functions that are used throught the game
# 

import xml.etree.ElementTree as xml
import os
from Room import *
from Gurdy import *
from Heart import *
from PHD import *
from Pill import *
from Duke import *

alph = "abcdefghijklmnopqrstuvwxyz0123456789 "

def darken(image, ammount):
	"Darken the image but preseve transparency"

	nImage = image.copy()

	ammount = int(ammount*255)

	# Blit new darker surface
	dark = Surface(nImage.get_size())
	dark.set_alpha(ammount, RLEACCEL)
	nImage.blit(dark, (0,0))

	# Use pixel array to remove previously transparent pixels
	pa = PixelArray(nImage)
	pa.replace((0,0,0,ammount), (0,0,0,0))
	return pa.make_surface()

def generateSeed():
	# Create random level seed

	SEED_LENGTH = 8
	characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
	charLen = len(characters)
	finalSeed = ""

	for i in range(SEED_LENGTH):
		finalSeed += characters[randint(0, SEED_LENGTH)]

	return finalSeed

def findRooms(floor, possibleCoords, rooms):
	# Find rooms on the floor

	rs = []
	moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]

	# Find rooms that can spawn 
	for room in possibleCoords:
		x, y = room
		count = 0
		for m in moves:
			mx, my = m
			newCoords = (x+mx, y+my)
			
			try:
				if floor[newCoords].variant != 0:
					count = 0
					break
			except:
				pass

			if newCoords in rooms:
				count += 1

		rs.append([room, count])

	return rs

def loadFloor(name, index, size, sounds, textures):
	d = xml.parse(os.path.join('res', 'floors', name)).getroot()

	floor = {}
	floor[(0,0)] = Room(index, 0, (0,0), d[0], textures, sounds)

	# Create the floor
	moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
	unusedRooms = [i for i in range(2, len(d))]
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

		# Create a room at the selected spot
		floor[chosen] = Room(index, 0, chosen, d[unusedRoom], textures, sounds)

	# Spawn shop
	someRooms = findRooms(floor, possibleCoords, rooms)
	shuffle(someRooms)
	for room in someRooms:
		if room[1] == 1:
			shop = tuple(room[0])
			break
	floor[shop] = Room(index, 5, shop, d[2], textures, sounds)
	things = [
		Heart(1, (4,3), [sounds["heartIntake"], sounds["holy"]], textures["pickupHearts"]),
		Pill((6, 3), textures["pills"]),
		PHD((8,3), sounds, textures["phd"])
	]
	for i in range(len(things)):
		things[i].price = i*2+3
		floor[shop].other.append(things[i])

	# Spawn item room
	someRooms = findRooms(floor, possibleCoords, rooms)
	shuffle(someRooms)
	for room in someRooms:
		if room[1] == 1:
			itemRoom = tuple(room[0])
			break
	floor[itemRoom] = Room(index, 1, itemRoom, d[1], textures, sounds)
	if randint(0,10) == 0:
		floor[itemRoom].other.append(PHD((6,3), sounds, textures["phd"]))
	else:
		floor[itemRoom].other.append(Pill((6,3), textures["pills"]))

	# Spawn boss room
	someRooms = findRooms(floor, possibleCoords, rooms)
	shuffle(someRooms)
	for room in someRooms:
		if room[1] == 1:
			bossRoom = tuple(room[0])
			break
	floor[bossRoom] = Room(index, 2, bossRoom, d[0], textures, sounds)
	floor[bossRoom].enemies.append([Gurdy, Duke][randint(0,1)](textures, sounds))

	return floor

def loadTexture(name, dir="", double=True):
	# Load texture and double its size

	if dir != "":
		t = image.load(os.path.join('res', 'textures', dir, name))

	else:
		t = image.load(os.path.join('res','textures', name))

	w = t.get_width()
	h = t.get_height()

	if double:
		w *= 2
		h *= 2

	if False:
		return transform.scale2x(t)
	else:
		return transform.scale(t, (w, h))

def loadSound(name):
	s = mixer.Sound(os.path.join('res','sounds', name))

	return s

def loadCFont(name, width, height, total, size=2):
	# Load custom font

	f = image.load(os.path.join('res', 'fonts', name))
	digits = [transform.scale(f.subsurface(width*i, 0, width, height), list(map(int,(width*size, height*size)))) for i in range(total)]
	space = Surface((width, height)).convert_alpha()
	space.fill((0,0,0,0))
	digits.append(space)

	return digits

def createSave(index, characterIndex, seed):
	f = open("save-%i.dat"%(index+1), "w+")
	f.write(str(characterIndex)+"\n"+seed)
	f.close()

def readSave(index):
	f = open("save-%i.dat"%(index+1), "r")
	data = f.read().split("\n")
	f.close()
	return int(data[0]), data[1]

def deleteSave(index):
	try:
		os.remove("save-%i.dat"%(index+1))
	except:
		pass

def write(text, font, alph=alph, dark=.8):
	# Create surface with special font

	width = font[0].get_width()
	height = font[0].get_height()
	writing = Surface((width*len(text), height)).convert_alpha()
	writing.fill((0,0,0,0))
	for i in range(len(text)):
		writing.blit(font[alph.index(text[i].lower())], (i*width, 0))
	return darken(writing, dark)



# BOSS INTRO

face = [None,None,None]
spot = [None,None,None,None,None,None,None]
title = [None,None,None]
bosstitle = [None,None,None]
bossface = [None,None,None]

frame = loadTexture("frame.png", dir="bossIntro")
spot[0] = loadTexture("spot1.png", dir="bossIntro")
spot[1] = loadTexture("spot2.png", dir="bossIntro")
spot[2] = loadTexture("spot3.png", dir="bossIntro")
spot[3] = loadTexture("spot4.png", dir="bossIntro")
spot[4] = loadTexture("spot5.png", dir="bossIntro")
spot[5] = loadTexture("spot6.png", dir="bossIntro")
spot[6] = loadTexture("spot7.png", dir="bossIntro")
bossspot = loadTexture("bossspot.png", dir="bossIntro")
face[1] = loadTexture("issacportrait.png", dir="bossIntro")
face[2] = loadTexture("eveportrait.png", dir="bossIntro")
face[0] = loadTexture("lazarusportrait.png", dir="bossIntro")
title[1] = loadTexture("titleissac.png", dir="bossIntro")
title[2] = loadTexture("titleeve.png", dir="bossIntro")
title[0] = loadTexture("titlelazarus.png", dir="bossIntro")
bosstitle[0] = loadTexture("titlegurdy.png", dir="bossIntro")
bosstitle[1] =  loadTexture("titledukeofflies.png", dir="bossIntro")
bossface[0] = loadTexture("gurdy.png", dir="bossIntro")
bossface[1] = loadTexture("dukeofflies.png", dir="bossIntro")
vs = loadTexture("vs.png", dir="bossIntro")

def bossIntro(screen, char,boss,floor):
	# Slide in character + boss
	for i in range(0,380,14):
		screen.blit(frame,(0,0))
		screen.blit(spot[floor],(-340+i,390))
		screen.blit(bossspot,(860-i,340))
		screen.blit(bossface[boss],(900-i,60))
		screen.blit(face[char],(-275+i,300))
		display.flip()
		
	# Slide in text
	copy = screen.copy()
	for i in range(0,500,16):
		screen.blit(copy,(0,0))
		screen.blit(title[char],(-400+i,10))
		screen.blit(vs,(-390+i,90))
		screen.blit(bosstitle[boss],(-400+i,170))
		display.flip()

	# Slower slide in
	for i in range(0,180,4):
		screen.blit(copy,(0,0))
		screen.blit(title[char],(100+i,10))
		screen.blit(vs,(110+i,90))
		screen.blit(bosstitle[boss],(100+i,170))
		display.flip()

	# Stall for a bit
	for i in range(0, 20):
		display.flip()

	copy = screen.copy()
	screen.blit(copy,(0,0))

# Textures for boss bar
emptybar = loadTexture("emptybar.png", dir="healthBar")
skull = loadTexture("skull.png", dir="healthBar")
fullbar = loadTexture("fullbar.png", dir="healthBar")

def bossbar(screen, health):
	# Draw boss bar with correc health
	
    if health == 1:
        screen.blit(fullbar,(350,-30))
    elif health <= 0:
        screen.blit(emptybar,(350,-30))
    else:
        screen.blit(emptybar,(350,-30))
        draw.rect(screen,(255,0,0),Rect(380,38,int(200*health)+45,16))
        screen.blit(skull,(364,20))

