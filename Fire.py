# Fire.py
# Aaron Taylor
# Moose Abumeeiz
#
# This is the class for the fires in each room.
# They can have a diffrent base hurt isaac.
# 

from pygame import *
from random import randint
from const import *
from Animation import *


class Fire:
	def __init__(self, variant, xy, sounds, textures):
		self.variant = variant
		self.x = xy[0]
		self.y = xy[1]
		self.sounds = sounds
		self.textures = textures

		# Random base
		self.randVar = randint(0,2)

		self.collideable = False

		self.destroyed = False
		self.bounds = Rect(GRIDX+GRATIO*self.x-16-4, GRIDY+GRATIO*self.y-16-5, 64+4, 64)

		self.health = 4

		# Get frames for flame
		self.fireFrames = [self.textures[0].subsurface(Rect(96*i, 0, 96, 104)) for i in range(6)]

		xMod = 0
		yMod = 0

		if self.randVar == 1:
			xMod = 64*2
		elif self.randVar == 2:
			yMod = 64*2

		# Wood animation frames
		self.woodFrames = [self.textures[1].subsurface(Rect((64*i - (i//2)*128)+xMod, (i//2)*64+yMod, 64, 64)) for i in range(4)]

		self.fire = Animation(self.fireFrames, .4)
		self.wood = Animation(self.woodFrames, .4)

		# Define dead wood and fire frames
		self.deadWood = self.woodFrames[1]
		self.deadFire = Surface((0,0))

	def destroy(self):
		self.destroyed = True
		self.sounds[1].play() # Extinguish sound
		self.health = 0

	def hurt(self, ammount):
		self.health -= 1

		if self.health == 0:
			self.destroy()
		elif self.health < 0:
			self.health = 0
		else:
			self.fire.resize(0.8) # Decrease flame size

	def render(self, surface, time, ox=0, oy=0):
		
		if self.health > 0:
			wood = self.wood.render(time)
			fire = self.fire.render(time)
		else:
			wood = self.deadWood
			fire = self.deadFire

		surface.blit(wood, ((GRIDX + self.x*GRATIO + GRATIO//2 - self.wood.width//2 - 12)+ox, (GRIDY + self.y*GRATIO + GRATIO//2 - self.wood.height//2)+oy))
		surface.blit(fire, ((GRIDX + self.x*GRATIO + GRATIO//2 - self.fire.width//2 - 12)+ox, (GRIDY + self.y*GRATIO + GRATIO//2 - self.fire.height//1.2 - 2)+oy))
