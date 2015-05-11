import xml.etree.ElementTree as xml
import os
from Room import *

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

def rWithOne(floor, possibleCoords, rooms):
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
					continue
			except:
				pass

			if newCoords in rooms:
				count += 1

		if count == 1:
			rs.append(room)

	return rs

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

	roomsWithOne = rWithOne(floor, possibleCoords, rooms)

	itemRoom = choice(roomsWithOne)
	floor[itemRoom] = Room(index, 1, chosen, d[0], textures, sounds)

	roomsWithOne = rWithOne(floor, possibleCoords, rooms)

	bossRoom = choice(roomsWithOne)
	roomsWithOne.remove(bossRoom)
	floor[bossRoom] = Room(index, 2, chosen, d[0], textures, sounds)

	return floor
