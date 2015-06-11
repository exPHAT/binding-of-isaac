from pygame import *

from func import *
from const import *
from Enemy import *
from Animation import *
from time import time as cTime
from random import randint
from Tear import *

class Boil(Enemy):

	hurtDistance = 0.6
	health = 10

	def __init__(self, xy, sounds, textures):
		self.x, self.y = xy
		self.sounds = sounds
		self.frames = [textures["enemies"]["boil"].subsurface(i*64-(i//4)*(64*4), (i//4)*64, 64, 64) for i in range(10)][::-1]

		self.tearTextures = textures["tears"]
		self.tearSounds = sounds["tear"]

		self.size = 0

		self.advanceTime = 0.5

		self.start = cTime()

		self.animation = Animation(self.frames, 10, shouldLoop=False)

		self.sinceFull = -1

		self.tears = []

	def hurt(self, ammount):
		if not self.dead:
			self.health -= ammount
			self.animation.setFrame(self.animation.currentIndex-ammount)

			if self.health <= 0:
				self.die()

	def render(self, surface, time, character, nodes, paths, bounds, obsticals):

		self.health = self.animation.currentIndex

		if not self.dead:
			self.checkHurt(character, time)

		if self.animation.currentIndex == self.animation.frameCount-1:
			# The boil is full size
			if time-self.sinceFull >= 1:
				self.tears.append(Tear((randint(-1,1), randint(-1,1)), (GRIDX+GRATIO*self.x, GRIDY+GRATIO*self.y), (0, 0), 1, 1, 1, False, self.tearTextures, self.tearSounds))
				self.sinceFull = time

		for tear in self.tears[:]:
			if not tear.render(surface, time, bounds, obsticals):
				self.tears.remove(tear)

		surface.blit(self.animation.render(time), (GRIDX+GRATIO*self.x-16, GRIDY+GRATIO*self.y-32))

		return not self.dead