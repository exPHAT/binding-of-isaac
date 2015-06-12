# Pooter.py
# Aaron Taylor
# Moose Abumeeiz
#
# The pooter will follow the user similarly to a fly
# 

from pygame import *
from const import *
from Enemy import *
from Animation import *
from math import *

class Pooter(Enemy):
	"""Simple enemy fly class"""

	hurtDistance = 0.6
	health = 12

	def __init__(self, xy, sounds, textures):
		self.x, self.y = xy

		self.sounds = sounds

		self.frames = [textures.subsurface(i*64, 0, 64, 64) for i in range(2)]
		# self.deathFrames = [textures.subsurface(i*128 - ((i//4)*128*4), 128 * (i//4 + 1), 128, 128) for i in range(12)]

		self.anim = Animation(self.frames, 0.04)

		self.health = 2

	def die(self):
		if not self.dead:
			# self.anim = Animation(self.deathFrames, 0.24)
			self.dead = True
			self.sounds[-1].play() # Play death sound

	def render(self, surface, time, character, nodes, paths, bounds, obsticals):
		speed = 1.5/GRATIO

		ix, iy = (character.x-GRIDX)/GRATIO, (character.y-GRIDY)/GRATIO
		dx, dy = (ix-self.x), (iy-self.y)


		# X and Y ratios
		dist = sqrt(dx**2+dy**2)
		rx = dx/dist
		ry = dy/dist

		hurtDistance = 0.8

		if not self.dead:

			# Add to x and y
			self.x += speed*rx
			self.y += speed*ry

			self.checkHurt(character, time)


			frame = self.anim.render(time)
		else:
			frame = self.anim.render(time)
			if self.anim.looped:
				return False

		surface.blit(frame, (GRIDX+GRATIO*self.x-self.anim.width//2, GRIDY+GRATIO*self.y-self.anim.height//2))
		return True # Should remain in enemies list
