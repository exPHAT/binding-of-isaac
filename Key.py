# Key.py
# Aaron Taylor
# Moose Abumeeiz
#
# The class for the key that you can pickup.
# The key can be used to unlock rooms such as item rooms and shops.
# 

from pygame import *
from const import *
from Animation import *
from Item import *

class Key(Item):
	"""Pickup Key class"""

	collideable = False
	pickedUp = False

	def __init__(self, variant, xy, sounds, textures):
		self.variant = variant
		self.x = xy[0]
		self.y = xy[1]
		self.sounds = sounds
		self.textures = textures

		self.bounds = Rect(GRIDX+GRATIO*self.x,GRIDY+GRATIO*self.y, 32, 64)

		self.texture = self.textures.subsurface(0,0,32,64)

	def pickup(self):
		self.pickedUp = True
		self.sounds[1].play()

	def render(self, surface, time, objects, ox=0, oy=0):
		if not self.pickedUp:
			# draw.rect(surface, (255,0,0), self.bounds)
			surface.blit(self.texture, (GRIDX+GRATIO*self.x+ox,GRIDY+GRATIO*self.y+oy))
		return not self.pickedUp
