from pygame import *
from time import time as cTime
from random import randint
from math import *
from Explosion import *

class Bomb:
	"""Droppable bomb class"""

	def __init__(self, parent, variant, xy, sounds, textures):
		self.variant = variant
		self.x = xy[0]
		self.y = xy[1]
		self.sounds = sounds
		self.textures = textures
		self.parent = parent

		self.bounds = Rect(0,0,0,0)

		self.fuse = 2
		self.placed = cTime()
		self.exploded = False

		self.collideable = False

		self.anim = Animation([textures[0].subsurface(0,0,64,64)], .2)

	def explode(self, objects):
		self.exploded = True
		self.anim = Explosion(0, (self.x, self.y), self.sounds[0], self.textures[1])
		self.parent.backdrop.blit(self.textures[2].subsurface(192*randint(0,1), 128*randint(0,1), 192, 128), ((GRIDX + GRATIO*self.x) - 128, (GRIDY + GRATIO*self.y) - 32))
		for ob in objects:
			if sqrt((ob.x-self.x)**2 + (ob.y-self.y)**2) < 2:
				ob.destroy()

	def render(self, surface, time, objects, ox=0, oy=0):
		if not self.exploded:
			frame = self.anim.render(time)
			surface.blit(frame, ((GRIDX + GRATIO*self.x) - self.anim.width//2+ox, (GRIDY + GRATIO*self.y) - self.anim.height//2+oy))

			if time-self.placed >= self.fuse:
				self.explode(objects)
			return True
		else:
			return self.anim.render(surface, time)

