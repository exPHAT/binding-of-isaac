# Room.py
# Aaron Taylor
# Moose Abumeeiz
#
# This room class supports animation in and out,
# it will show the background and will be responsible for rendering
# everything within it.
# 

from pygame import *
from const import *
from random import *
from Rock import *
from Poop import *
from Fire import *
from Door import *
from Tear import *
from Explosion import *
from Coin import *
from Key import *
from Fly import *
from Pooter import *
from Heart import *
from Bomb import *
from Pill import *
from Trapdoor import *
from Maw import *
from Boil import *
from Host import *

import func

class Room:
	"""The main floor class"""

	# ROOM TYPES:
	#
	# 0 - Normal room
	# 1 - Treasure room
	# 2 - Boss room
	# 3 - Devil room
	# 4 - Angel room
	# 5 - Shop

	# ROOMS ARE 13 x 7

	lcx = -1
	lcy = -1

	def __init__(self, floor, variant, xy, xml, textures, sounds):
		offX = offY = 0
		if variant == 2:
			offX, offY = 234*2, 156*2

		if variant == 5:
			texture = textures["floors"][-1].subsurface(Rect(offX, offY, 221*2, 143*2))
		else:
			texture = textures["floors"][floor].subsurface(Rect(offX, offY, 221*2, 143*2))

		backdrop = Surface((221*2*2, 143*2*2))

		# Form the texture to each of the 4 corners of the room
		backdrop.blit(texture, (0,0))
		backdrop.blit(transform.flip(texture, True, False), (221*2, 0))
		backdrop.blit(transform.flip(texture, False, True), (0, 143*2))
		backdrop.blit(transform.flip(texture, True, True), (221*2, 143*2))

		# Show tutorial controls if its the first room
		if floor == 0 and xy[0] == 0 and xy[1] == 0:
			controls = textures["controls"]
			backdrop.blit(controls, (113, 203))

		# Add gorgeous lighting
		backdrop.blit(textures["shading"], (0,0))
		backdrop = func.darken(backdrop, .25)
		backdrop.blit(textures["overlays"][randint(0,4)], (0,0))

		# Setup x and y
		self.x, self.y = xy
		self.w, self.h = 0,0

		self.variant = variant

		self.entered = False
		self.seen = False

		self.floor = floor
		self.backdrop = backdrop
		self.sounds = sounds
		self.textures = textures

		self.animating = False
		self.ax, self.ay = 0, 0
		self.aDirection = -1
		self.sx, self.sy = 0,0

		self.levelBounds = Rect(GRIDX, GRIDY, WIDTH-(154*2), HEIGHT-(96*2))

		self.enemies = []
		self.rocks = []
		self.poops = []
		self.fires = []
		self.doors = []
		self.other = [] # Other stuff that doesnt have special properties

		self.parseRoomXML(xml) # Build the room based on the xml

		obsticals = []

		for o in self.rocks+self.fires+self.poops:
			obsticals.append([o.x, o.y])

		# Setup room for path finding
		graph, self.nodes = make_graph({"width": 13, "height": 7, "obstacle": obsticals})
		self.paths = AStarGrid(graph)
		self.hadEnemies = len(self.enemies) > 0
		self.spawnedItem = False

	def parseRoomXML(self, xml):
		self.w, self.h = map(int, [xml.get('width'), xml.get('height')])
		for obj in xml: # Iterate through room objects
			attr = obj.attrib
			x, y = int(attr["x"]), int(attr["y"])

			if obj.tag == "spawn":
				
				typ = int(obj[0].get('type'))
				var = int(obj[0].get('variant'))
				subtype = int(obj[0].get('subtype'))

				# Spawn the correct item for the type
				if typ in [1500, -1, -1, 1496, -1]:
					self.poops.append(Poop([1500, -1, -1, 1496, -1].index(typ), (x,y), self.textures["poops"], self.sounds["pop"]))
				elif typ == 1000:
					self.rocks.append(Rock(randint(0,2), (x,y), False, self.sounds["rockBreak"], self.textures["rocks"]))
				elif typ == 33:
					self.fires.append(Fire(0, (x,y), [self.sounds["fireBurn"], self.sounds["steam"]], self.textures["fires"]))
				elif typ == 5 and var == 10:
					self.other.append(Heart([1,3,6].index(subtype), (x,y), [self.sounds["heartIntake"], self.sounds["holy"]], self.textures["pickupHearts"]))
				elif typ == 5 and var == 20:
					self.other.append(Coin(subtype-1, (x,y), [self.sounds["coinDrop"], self.sounds["coinPickup"]], self.textures["coins"]))
				elif typ == 5 and var == 30:
					self.other.append(Key(0, (x, y), [self.sounds["keyDrop"], self.sounds["keyPickup"]], self.textures["keys"]))
				elif typ == 5 and var == 40:
					self.other.append(Bomb(self, 0, (x, y), [self.sounds["explosion"]], self.textures["bombs"], explode=False))
				elif typ == 13:
					self.enemies.append(Fly((x,y), [self.sounds["deathBurst"]], self.textures["enemies"]["fly"]))
				elif typ == 14:
					self.enemies.append(Pooter((x, y), [self.sounds["deathBurst"]], self.textures["enemies"]["pooter"]))
				elif typ == 26:
					self.enemies.append(Maw((x, y), [self.sounds["deathBurst"]], self.textures["enemies"]["maw"]))
				elif typ == 27:
					self.enemies.append(Host((x, y), self.sounds, self.textures))
				elif typ == 30:
					self.enemies.append(Boil((x, y), self.sounds, self.textures))

	def addDoor(self, xy, variant, isOpen):
		x, y = xy
		
		
		side = [[6,7], [13, 3], [6,-1], [-1,3]].index([x,y])
		self.doors.append(Door(self.floor, side, variant, isOpen, self.textures["doors"], self.sounds))

	def addOther(self, xy):
		self.other.append(Explosion(0, xy, self.sounds["explosion"], self.textures["explosions"]))

	def animateOut(self, direction):
		# animate the room out

		self.animating = True

		if direction[1] == -1:
			self.aDirection = 0
		elif direction[0] == -1:
			self.aDirection = 1
		elif direction[1] == 1:
			self.aDirection = 2
		elif direction[0] == 1:
			self.aDirection = 3

	def animateIn(self, direction):
		# Animate the room in

		self.animating = True

		if direction[1] == -1:
			self.aDirection = 0
		elif direction[0] == -1:
			self.aDirection = 1
		elif direction[1] == 1:
			self.aDirection = 2
		elif direction[0] == 1:
			self.aDirection = 3

		self.ax, self.ay = [0, -1, 0, 1][self.aDirection]*WIDTH, [1, 0, -1, 0][self.aDirection]*HEIGHT
		self.sx,self.sy = self.ax, self.ay

	def step(self, currTime):
		pass

	def renderMap(self, surface, currentRoom, detail):
		ratio = 16 # Pixel to size ratio
		x, y = currentRoom

		if self.x == x and self.y == y:
			# Isaac is in this room
			texture = self.textures["map"]["in"]
		elif self.entered:
			# Isaac has  this room
			texture = self.textures["map"]["entered"]
		elif self.seen:
			# Isaac has seen the door to the room
			texture = self.textures["map"]["seen"]
		else:
			return

		if not detail:
			draw.rect(surface, (0,0,0), (surface.get_width()//2+(self.x-x)*ratio - 8, surface.get_height()/2-(self.y-y)*ratio - 8, 24, 24))
			return

		# Draw special symbol
		surface.blit(texture, (surface.get_width()//2+(self.x-x)*ratio - 4, surface.get_height()/2-(self.y-y)*ratio - 4))
		if self.variant == 1 or self.variant == 2 and not self.x == x and self.y == y:
			surface.blit(self.textures["map"][["item", "boss"][self.variant-1]], (surface.get_width()//2+(self.x-x)*ratio - 4, surface.get_height()/2-(self.y-y)*ratio - 4))


	def render(self, surface, character, currTime):

		if len(self.enemies) > 0:
			for door in self.doors:
				door.close()

		else:
			for door in self.doors:
				door.open()

			if self.hadEnemies and len(self.other) == 0 and randint(0,5) == 0 and not self.spawnedItem:
				typ = randint(0,2)
				self.spawnedItem = True

				# Random spawn
				if typ == 0:
					self.other.append(Coin(0, (6,2), [self.sounds["coinDrop"], self.sounds["coinPickup"]], self.textures["coins"]))
				elif typ == 1:
					self.other.append(Bomb(self, 1, (6,2), [self.sounds["explosion"]], self.textures["bombs"], explode=False))
				elif typ == 2:
					self.other.append(Key(0, (6, 2), [self.sounds["keyDrop"], self.sounds["keyPickup"]], self.textures["keys"]))

			# Create trapdoor in empty boss room
			if self.variant == 2 and self.floor < 6 and not Trapdoor in list(map(type, self.other)):
				self.other.append(Trapdoor(self.textures["trapdoor"]))

		if not self.animating:
			# Render stationary room

			surface.blit(self.backdrop, (38,-16))

			for door in self.doors:
				door.render(surface)

			for rock in self.rocks:
				rock.render(surface)

			for poop in self.poops:
				poop.render(surface)

			for fire in self.fires:
					fire.render(surface, currTime)

			objects = self.rocks + self.poops + self.fires

			for other in self.other[::-1]:
					if not other.render(surface, currTime, objects+self.enemies):
						self.other.remove(other)

			everything = objects+self.other

			# Character x and y
			cx, cy = int((character.x-GRIDX)/GRATIO), int((character.y-GRIDY)/GRATIO)
			
			if cx != self.lcx or cy != self.lcy:
				self.lcx, self.lcy = cx, cy
				for enemy in self.enemies:
					enemy.pathFind((cx,cy), self.nodes, self.paths)

			for enemy in self.enemies[:]:
				if not enemy.render(surface, currTime, character, self.nodes, self.paths, self.levelBounds, objects):
					self.enemies.remove(enemy)

			move = character.render(surface, currTime, self.levelBounds, everything, self.doors)

			return move
		else:
			# Render moving room

			moveDistance = 40 # How far the canvas should move
			self.ax += [0, 1, 0, -1][self.aDirection]*moveDistance
			self.ay += [-1, 0, 1, 0][self.aDirection]*moveDistance

			if abs(self.sx - self.ax) >= WIDTH or abs(self.sy - self.ay) >= HEIGHT:
				self.animating = False
				self.ax, self.ay = 0, 0
				self.sx, self.sy = 0, 0
			else:
				surface.blit(self.backdrop, (38+self.ax,-16+self.ay))

				for door in self.doors:
					door.render(surface, ox=self.ax, oy=self.ay)

				for rock in self.rocks:
					rock.render(surface, ox=self.ax, oy=self.ay)

				for poop in self.poops:
					poop.render(surface, ox=self.ax, oy=self.ay)

				for fire in self.fires:
					fire.render(surface, currTime, ox=self.ax, oy=self.ay)

				objects = self.rocks + self.poops + self.fires

				for other in self.other[::-1]:
					if not other.render(surface, currTime, objects, ox=self.ax, oy=self.ay):
						self.other.remove(other)

			return [0, 0]
