# Bomb.py
# Aaron Taylor
# Moose Abumeeiz
#
# Bombs can be dropped or picked up, they will hurt enemies in range
# 

from pygame import *
from time import time as cTime
from random import randint
from math import *
from Explosion import *
from Animation import *
from Item import *

class Bomb(Item):
	"""Droppable bomb class"""

	collideable = False
	pickedUp = False
	exploded = False
	fuse = 2

	def __init__(self, parent, variant, xy, sounds, textures, explode=False):
		self.variant = variant
		self.x = xy[0]
		self.y = xy[1]
		self.sounds = sounds
		self.textures = textures
		self.parent = parent # So we can stain the room floor

		if not explode:
			self.bounds = Rect(GRIDX+GRATIO*self.x,GRIDY+GRATIO*self.y, 32, 64)
		else:
			# You cant collide with a bomb that will explode
			self.bounds = Rect(0,0,0,0)

		# Should the bomb explode
		self.shouldExplode = explode
		self.placed = cTime()

		self.anim = Animation([textures[0].subsurface(0,0,64,64)], .2)

	def explode(self, objects):
		# Explode bomb, draw the stain on the background
		self.exploded = True
		self.anim = Explosion(0, (self.x, self.y), self.sounds[0], self.textures[1])
		self.parent.backdrop.blit(self.textures[2].subsurface(192*randint(0,1), 128*randint(0,1), 192, 128), ((GRIDX + GRATIO*self.x) - 128, (GRIDY + GRATIO*self.y) - 32))
		for ob in objects:
			if sqrt((ob.x-self.x)**2 + (ob.y-self.y)**2) < 2:
				# Try to hur the enemy, if its not an entity, destroy it
				try:
					ob.destroy()
				except:
					ob.hurt(8)

	def pickup(self):
		if not self.shouldExplode:
			self.pickedUp = True


	def render(self, surface, time, objects, ox=0, oy=0):
		if self.pickedUp:
			return False

		if not self.shouldExplode:
			surface.blit(self.anim.render(time), ((GRIDX + GRATIO*self.x) - self.anim.width//2+ox, (GRIDY + GRATIO*self.y) - self.anim.height//2+oy))
			return True

		if not self.exploded:
			# render the  normal bomb

			frame = self.anim.render(time)
			surface.blit(frame, ((GRIDX + GRATIO*self.x) - self.anim.width//2+ox, (GRIDY + GRATIO*self.y) - self.anim.height//2+oy))

			if time-self.placed >= self.fuse:
				self.explode(objects)
			return True
		else:
			# Render the explosion
			return self.anim.render(surface, time)

