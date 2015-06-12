# Coin.py
# Aaron Taylor
# Moose Abumeeiz
#
# This is the class for the coin that you can pickup in a room
# 

from pygame import *
from const import *
from Animation import *
from Item import *

class Coin(Item):
	"""Pickup coin class"""

	def __init__(self, variant, xy, sounds, textures):
		self.variant = variant
		self.x = xy[0]
		self.y = xy[1]
		self.sounds = sounds
		self.textures = textures[variant]
		self.worth = [1, 5, 10][variant]

		self.bounds = Rect(GRIDX+GRATIO*self.x,GRIDY+GRATIO*self.y, 52, 52)

		self.collideable = False
		self.pickedUp = False

		# Split up textures
		self.frames = [self.textures.subsurface(i*128, 0, 128, 128) for i in range(6)]
		self.frames = [self.frames[0].copy() for i in range(16)] + self.frames
		self.anim = Animation(self.frames, 1)

	def pickup(self):
		self.pickedUp = True
		self.sounds[1].play()

	def render(self, surface, time, objects, ox=0, oy=0):
		if not self.pickedUp:
			surface.blit(self.anim.render(time), (GRIDX+GRATIO*self.x+GRATIO//2-self.anim.width//2+ox,GRIDY+GRATIO*self.y+GRATIO//2-self.anim.height//2+oy))
		return not self.pickedUp
