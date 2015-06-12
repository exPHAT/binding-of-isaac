import xml.etree.ElementTree as xml
import os
from Room import *
from Gurdy import *

alph = "abcdefghijklmnopqrstuvwxyz0123456789 "

def darken(image, ammount):
	nImage = image.copy()

	ammount = int(ammount*255)

	dark = Surface(nImage.get_size())
	dark.set_alpha(ammount, RLEACCEL)
	nImage.blit(dark, (0,0))

	pa = PixelArray(nImage)
	pa.replace((0,0,0,ammount), (0,0,0,0))
	return pa.make_surface()

def parseImage(image, startX, startY, width, height, xCount, yCount, total):
	textures = []

	[textures.subsurface(i*128 - ((i//4)*128*4), 128 * (i//4 + 1), 128, 128) for i in range(12)]

	for i in range(total):
		image.subsurface(i*width - ((i//xCount)*width*xCount), i*height , width, height)

def generateSeed():
	SEED_LENGTH = 8
	characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
	charLen = len(characters)
	finalSeed = ""

	for i in range(SEED_LENGTH):
		finalSeed += characters[randint(0, SEED_LENGTH)]

	return finalSeed

def findRooms(floor, possibleCoords, rooms):
	rs = []
	moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]

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
		floor[chosen] = Room(index, 0, chosen, d[unusedRoom], textures, sounds)

	someRooms = findRooms(floor, possibleCoords, rooms)

	shuffle(someRooms)

	for room in someRooms:
		if room[1] == 1:
			itemRoom = tuple(room[0])
			break
	floor[itemRoom] = Room(index, 1, itemRoom, d[1], textures, sounds)
	if True:
		floor[itemRoom].other.append(PHD((6,3), sounds, textures["phd"]))
	else:
		floor[itemRoom].other.append(Pill((6,3), textures["pills"]))

	someRooms = findRooms(floor, possibleCoords, rooms)

	shuffle(someRooms)

	for room in someRooms:
		if room[1] == 1:
			bossRoom = tuple(room[0])
			break

	floor[bossRoom] = Room(index, 2, bossRoom, d[0], textures, sounds)
	floor[bossRoom].enemies.append(Gurdy(textures["bosses"]["gurdy"], sounds))

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

def write(text, font, alph=alph):
	width = font[0].get_width()
	height = font[0].get_height()
	writing = Surface((width*len(text), height)).convert_alpha()
	writing.fill((0,0,0,0))
	for i in range(len(text)):
		writing.blit(font[alph.index(text[i].lower())], (i*width, 0))
	return darken(writing, 0.80)
