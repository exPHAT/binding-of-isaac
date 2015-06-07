from pygame import *
from const import *
from Animation import *

class Item:
	"""Main item class"""

	collideable = False
	pickedUp = False
	stats = [0, 0, 0, 0, 0, 0]

	def __init__(self, stats, xy, sounds, textures):
		self.stats = stats
		self.x = xy[0]
		self.y = xy[1]
		self.sounds = sounds
		self.textures = textures

		self.bounds = Rect(GRIDX+GRATIO*self.x,GRIDY+GRATIO*self.y, 32, 64)

		self.texture = self.textures.subsurface(0,0,32,64)

	def pickup(self):
		self.pickedUp = True
		# self.sounds[1].play()

	def render(self, surface, time, objects, ox=0, oy=0):
		if not self.pickedUp:
			surface.blit(self.texture, (GRIDX+GRATIO*self.x+ox,GRIDY+GRATIO*self.y+oy))
		return not self.pickedUp
