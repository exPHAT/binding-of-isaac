# Gurdy.py
# Aaron Taylor
# Moose Abumeeiz
#
# This is the first boss, Gurdy. He just sits there and takes your bullets
# 

from pygame import *
from const import *
from func import *
from Animation import *
from Enemy import *

class Gurdy(Enemy):
	x = 6
	y = 3

	health = 100
	hurtDistance = 2

	def __init__(self, textures, sounds):
		self.body = textures["bosses"]["gurdy"].subsurface(0, 0, 284, 320)
		self.head = textures["bosses"]["gurdy"].subsurface(0, 768, 84, 104)
		self.sounds = sounds

		self.tearTextures = textures["tears"]
		self.tearSounds = sounds["tear"]

		self.textures = textures

		self.lastShot = -1

	def die(self):
		self.dead = True

	def render(self, surface, time, character, nodes, paths, bounds, obsticals):
		# Draw body
		surface.blit(self.body, (GRIDX+GRATIO*self.x-284/2, GRIDY+GRATIO*self.y-320/2))

		# Blit head
		surface.blit(self.head, (GRIDX+GRATIO*self.x-284/4 + 30, GRIDY+GRATIO*self.y-320/4 - 40))

		if time-self.lastShot >= .4:
			self.lastShot = time
			dx = character.x-(GRIDX+GRATIO*self.x)
			dy = character.y-(GRIDY+GRATIO*self.y)
			dist = sqrt(dx**2+dy**2)

			self.tears.append(Tear((dx/dist, dy/dist), ((GRIDX+GRATIO*self.x),(GRIDY+GRATIO*self.y)), (0,0), 1, 1, 1, False, self.tearTextures, self.tearSounds))

		for tear in self.tears[:]:
			if not tear.render(surface, time, bounds, obsticals):
				self.tears.remove(tear)

		self.checkHurt(character, time)

		return not self.dead