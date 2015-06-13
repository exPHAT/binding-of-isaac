# Game.py
# Aaron Taylor
# Moose Abumeeiz
#
# This is the main game class (not including menu)
# It is responsible for rendering the floor and the character.
# 

from pygame import *
from func import *
from Character import *
from Room import *
from Bomb import *
from time import time as cTime
from pause import *
from Pill import *
from Banner import *
from Gurdy import *
from Duke import *
import random


class Game:
	floor = {}
	floorIndex = 0
	currentRoom = (0,0)
	animatingRooms = []
	won = False
	def __init__(self, characterType, controls, seed):
		self.surface = surface
		self.characterType = characterType
		self.seed = seed
		self.controls = controls

		self.banners = []

		# Feed the seed to the random module
		random.seed(self.seed)

	def setup(self):
		# Load floor with custom data
		floor = loadFloor(["basement.xml", "basement.xml", "basement.xml", "basement.xml", "basement.xml", "basement.xml", "basement.xml"][self.floorIndex], self.floorIndex, randint(8, 12), self.sounds, self.textures)
		adjecent = [-1,0], [0, 1], [1, 0], [0, -1]
		doorPoss = [[13, 3], [6,7], [-1,3], [6,-1]]

		# Position isaac in the center of the room
		self.isaac.x, self.isaac.y = (WIDTH//2, (HEIGHT//4)*3)

		# Add a door to every room
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

		# Create a banner for the new floor
		self.floor = floor
		self.banners.append(Banner(["Basement", "Caves", "Catacombs","Necropolis","Depths","Womb","Uterus"][self.floorIndex], self.textures))

	def updateMinimap(self, currentRoom):
		# Draw the minimap

		self.minimap.fill((0,0,0,0))
		self.minimap.blit(self.textures["map"]["background"], (0, 0))
		for room in self.floor:
			self.floor[room].renderMap(self.minimap, currentRoom, False)
		for room in self.floor:
			self.floor[room].renderMap(self.minimap, currentRoom, True)

	def updateFloor(self):
		# Check if you've been in a room

		self.floor[self.currentRoom].entered = True

		for m in self.posMoves:
			mx, my = m
			x, y = self.currentRoom
			newPos = (mx+x, my+y)

			try:
				self.floor[newPos].seen = True
			except:
				pass

		self.updateMinimap(self.currentRoom)


	def run(self, screen, sounds, textures, fonts, joystick=None):
		# Run the main loop
		animatingRooms = self.animatingRooms
		currentRoom = self.currentRoom

		# Setup controls and create character
		cn = self.controls
		self.isaac = isaac = Character(self.characterType, (WIDTH//2, (HEIGHT//4)*3), [[cn[3], cn[1], cn[2], cn[0]], [cn[7], cn[5], cn[6], cn[4]]], textures, sounds, fonts)

		# Setup special stats
		if self.characterType == 0:
			isaac.pill = Pill((0,0), textures["pills"])
		elif self.characterType == 2:
			isaac.speed = 3
			isaac.damage = 1
			del isaac.hearts[-1]

		self.sounds = sounds
		self.textures = textures
		self.setup()

		floor = self.floor
		floorIndex = self.floorIndex
		clock = time.Clock()

		# Create minimap
		self.minimap = Surface((textures["map"]["background"].get_width(), textures["map"]["background"].get_height())).convert_alpha()
		self.updateMinimap(self.currentRoom)
		self.minimap.set_clip(Rect(4, 4, 100, 86))
		mWidth = self.minimap.get_width()
		mHeight = self.minimap.get_height()
		
		# Define possible moves
		self.posMoves = [[1, 0], [0, 1], [-1, 0], [0, -1]]
		posMoves = self.posMoves

		# Set the game (so we can modify stuff from the character class)
		self.isaac.game = self

		self.updateFloor()

		running = True
		while running:

			currTime = cTime()
			k = key.get_pressed() # Current down keys

			for e in event.get():
				if e.type == QUIT:
					quit() 
				elif e.type == KEYDOWN and e.key == 27:
					# Pause the game
					running = pause(screen, self.seed, textures, fonts, [self.isaac.speed, self.isaac.shotSpeed, self.isaac.damage, self.isaac.luck, self.isaac.shotRate, self.isaac.range])

				elif e.type == KEYDOWN:
					# Update key value
					isaac.moving(e.key, True, False)
	
					if e.key == self.controls[-1]:
						# Bomb key pressed
						if isaac.pickups[1].use(1):
							self.floor[self.currentRoom].other.append(Bomb(self.floor[self.currentRoom], 0, ((isaac.x-GRIDX)/GRATIO, (isaac.y-GRIDY)/GRATIO), [sounds["explosion"]], textures["bombs"], explode=True))

					elif e.key == self.controls[-2]:
						# Pill key pressed
						isaac.usePill()

				elif e.type == KEYUP:
					# Update key value
					isaac.moving(e.key, False, False)

			# Draw animating rooms (The ones that are shifting in and out of frame)
			if len(animatingRooms) > 0:
				for r in animatingRooms[:]:
					r.render(screen, isaac, currTime)
					if not r.animating:
						animatingRooms.remove(r)
			else:
				screen.fill((0,0,0))

				# Render the room
				move = self.floor[self.currentRoom].render(screen, isaac, currTime)

				if move[0] != 0 or move[1] != 0:
					old = tuple(self.currentRoom[:])

					self.currentRoom = (move[0]+self.currentRoom[0], move[1]+self.currentRoom[1])
					try:
						# Animate the room
						self.floor[self.currentRoom].animateIn(move)
						self.floor[old].animateOut(move)

						# Animate the room
						animatingRooms.append(self.floor[self.currentRoom])
						animatingRooms.append(self.floor[old])

						# Animate isaac with the room
						isaac.x += 650*(-move[0])
						isaac.y += 348*(move[1])


						# Remove tears from an animating room
						isaac.clearTears()

						# Check if you enter a boss room
						if self.floor[self.currentRoom].variant == 2 and not self.floor[self.currentRoom].entered:
							sounds["bossIntro"].play()

							# Give the correct boss index
							bossIntro(screen, self.characterType, [Gurdy, Duke].index(type(self.floor[self.currentRoom].enemies[0])), self.floorIndex)

						self.floor[self.currentRoom].entered = True

						for m in posMoves:
							mx, my = m
							x, y = self.currentRoom
							newPos = (mx+x, my+y)

							try:
								self.floor[newPos].seen = True
							except:
								pass

						self.updateMinimap(self.currentRoom)

					except:
						# That room doesnt exist
						self.currentRoom = old

			if self.floor[self.currentRoom].variant == 2:
				# Its a boss room
				try:
					# Draw the boss bar
					bossbar(screen, self.floor[self.currentRoom].enemies[0].health/100)
				except:
					pass

				if not self.won and self.floorIndex == 6 and len(self.floor[self.currentRoom].enemies) == 0:
					self.banners.append(Banner("You won", self.textures))
					self.won = True


			# DRAW MAP
			screen.blit(self.minimap, (MAPX-mWidth//2, MAPY-mHeight//2))

			# Blit all banners
			for banner in self.banners:
				if banner.render(screen):
					self.banners.remove(banner)

			if joystick != None:
				joystick.update()

			if isaac.dead:
				running = False

			display.flip()
			clock.tick(60)