# Boil.py
# Aaron Taylor
# Moose Abumeeiz
#
# This is the class for the red boil that appears as an enemy
# and shoots in random directions
# 

from pygame import *

from func import *
from const import *
from Enemy import *
from Animation import *
from time import time as cTime
from random import choice
from Tear import *

class Boil(Enemy):

	hurtDistance = 0.6
	health = 10

	def __init__(self, xy, sounds, textures):
		self.x, self.y = xy
		self.sounds = sounds

		# Split textures
		self.frames = [textures["enemies"]["boil"].subsurface(i*64-(i//4)*(64*4), (i//4)*64, 64, 64) for i in range(10)][::-1]

		# Record sound and textures for tears
		self.tearTextures = textures["tears"]
		self.tearSounds = sounds["tear"]

		# How long it takes to grow + current size
		self.size = 0
		self.advanceTime = 0.5

		# When the animation was started
		self.start = cTime()

		# Animation for grow
		self.animation = Animation(self.frames, 10, shouldLoop=False)

		# How long the boil has been full
		self.sinceFull = -1

		# How many tears the boil has active
		self.tears = []

	def hurt(self, ammount):

		# Take damage and reduce size
		if not self.dead:
			self.health -= ammount
			self.animation.setFrame(self.animation.currentIndex-ammount)

			if self.health <= 0:
				self.die()

	def render(self, surface, time, character, nodes, paths, bounds, obsticals):

		# Set current health to match animation
		self.health = self.animation.currentIndex

		if not self.dead:
			self.checkHurt(character, time) # Check for any damage

		if self.animation.currentIndex == self.animation.frameCount-1:
			# The boil is full size
			if time-self.sinceFull >= 1:
				# Ensure the boil doesnt shoot too often
				self.tears.append(Tear(choice([(1,0),(-1,0),(0,-1),(0,1)]), (GRIDX+GRATIO*self.x, GRIDY+GRATIO*self.y), (0, 0), 1, 1, 1, False, self.tearTextures, self.tearSounds))
				self.sinceFull = time

		for tear in self.tears[:]:
			# Render the boil's tear
			if not tear.render(surface, time, bounds, obsticals):
				self.tears.remove(tear)

		surface.blit(self.animation.render(time), (GRIDX+GRATIO*self.x-16, GRIDY+GRATIO*self.y-32))

		return not self.dead
