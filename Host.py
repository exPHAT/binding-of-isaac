# Host.py
# Aaron Taylor
# Moose Abumeeiz
#
# The host pops up at a random time and shoots a tear in the
# characters directions
# 

from pygame import *
from const import *
from Enemy import *
from time import time as cTime
from Tear import *


class Host(Enemy):

	health = 6

	def __init__(self, xy, sounds, textures):
		self.x, self.y = xy
		self.tearTextures = textures["tears"]
		self.tearSounds = sounds["tear"]
		self.frames = [textures["enemies"]["host"].subsurface(i*64, 0, 64, 128) for i in range(2)]

		self.texture = self.frames[0]

		self.sinceFull = cTime()
		self.sinceDown = cTime()
		self.shot = False
		self.canHurt = False

	def render(self, surface, time, character, nodes, paths, bounds, obsticals):

		if not self.dead:
			self.checkHurt(character, time)

		if self.canHurt: # aka is up
			self.texture = self.frames[1]

			# Handle opening, shooting and closing again
			if time-self.sinceFull >= .5 and not self.shot:
				self.shot = True
				dx, dy = character.x-(GRIDX+GRATIO*self.x), character.y-(GRIDY+GRATIO*self.y)
				dist = sqrt(dx**2+dy**2)
				self.tears.append(Tear((dx/dist, dy/dist), (GRIDX+GRATIO*self.x+16, GRIDY+GRATIO*self.y), (0, 0), 1, 1, 1, False, self.tearTextures, self.tearSounds))
			elif time-self.sinceFull >= 1:
				# Put down
				
				self.canHurt = False
				self.shot = False
				self.sinceDown = time

		else:
			# Set to down texture
			self.texture = self.frames[0]
			self.canHurt = randint(0,100) == 0 and time-self.sinceDown >= 1.5
			if self.canHurt:
				self.sinceFull = time

		# Render tears
		for tear in self.tears[:]:
			if not tear.render(surface, time, bounds, obsticals):
				self.tears.remove(tear)

		surface.blit(self.texture, (GRIDX+GRATIO*self.x-16, GRIDY+GRATIO*self.y-80))

		return not self.dead


