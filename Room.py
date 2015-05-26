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

	# ROOMS ARE 13 x 7

	def __init__(self, floor, variant, xy, xml, textures, sounds):
		offX = offY = 0
		if variant == 2:
			offX, offY = 234*2, 156*2

		texture = textures["floors"][floor].subsurface(Rect(offX, offY, 221*2, 143*2))
		backdrop = Surface((221*2*2, 143*2*2))


		backdrop.blit(texture, (0,0))
		backdrop.blit(transform.flip(texture, True, False), (221*2, 0))
		backdrop.blit(transform.flip(texture, False, True), (0, 143*2))
		backdrop.blit(transform.flip(texture, True, True), (221*2, 143*2))

		if xy[0] == 0 and xy[1] == 0:
			controls = textures["controls"]
			backdrop.blit(controls, (113, 203))

		backdrop.blit(textures["shading"], (0,0))
		backdrop = func.darken(backdrop, .25)
		backdrop.blit(textures["overlays"][randint(0,4)], (0,0))

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

		graph, self.nodes = make_graph({"width": 13, "height": 7, "obstacle": obsticals})
		self.paths = AStarGrid(graph)

	def parseRoomXML(self, xml):
		self.w, self.h = map(int, [xml.get('width'), xml.get('height')])
		for obj in xml: # Iterate through room objects
			attr = obj.attrib
			x, y = int(attr["x"]), int(attr["y"])

			if obj.tag == "spawn":
				
				typ = int(obj[0].get('type'))
				var = int(obj[0].get('variant'))
				subtype = int(obj[0].get('subtype'))

				if typ in [1500, -1, -1, 1496, -1]:
					self.poops.append(Poop([1500, -1, -1, 1496, -1].index(typ), (x,y), self.textures["poops"], self.sounds["pop"]))
				elif typ == 1000:
					self.rocks.append(Rock(0, (x,y), False, self.sounds["rockBreak"], self.textures["rocks"]))
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
					self.enemies.append(Fly((x, y), [self.sounds["deathBurst"]], self.textures["enemies"]["fly"]))
				elif typ == 14:
					self.enemies.append(Pooter((x, y), [self.sounds["deathBurst"]], self.textures["enemies"]["pooter"]))


	def addDoor(self, xy, variant, isOpen):
		x, y = xy
		
		
		side = [[6,7], [13, 3], [6,-1], [-1,3]].index([x,y])
		self.doors.append(Door(side, variant, isOpen, self.textures["doors"], self.sounds))

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
		ratio = 16
		x, y = currentRoom

		if self.x == x and self.y == y:
			# Isaac is in this room
			texture = self.textures["map"]["in"]
		elif self.entered:
			# Isaac has entered this room
			texture = self.textures["map"]["entered"]
		elif self.seen:
			# Isaac has seen the door to the room
			texture = self.textures["map"]["seen"]
		else:
			return

		if not detail:
			draw.rect(surface, (0,0,0), (surface.get_width()//2+(self.x-x)*ratio - 8, surface.get_height()/2-(self.y-y)*ratio - 8, 24, 24))
			return

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

		if not self.animating:
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
					if not other.render(surface, currTime, objects):
						self.other.remove(other)

			everything = objects+self.other

			for enemy in self.enemies[:]:
				if not enemy.render(surface, currTime, character, self.nodes, self.paths):
					self.enemies.remove(enemy)

			move = character.render(surface, currTime, self.levelBounds, everything, self.doors)

			return move
		else:

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
					if not other.render(surface, currTime, self.nodes, self.paths, ox=self.ax, oy=self.ay):
						self.other.remove(other)

			return [0, 0]
