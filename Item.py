from pygame import *
from const import *
from Animation import *

class Item:
	"""Main item class"""

	collideable = False
	pickedUp = False

	tWidth = 32
	tHeight = 64

	def __init__(self, xy, sounds, textures):
		self.x = xy[0]
		self.y = xy[1]
		self.sounds = sounds
		self.textures = textures

		self.bounds = Rect(GRIDX+GRATIO*self.x,GRIDY+GRATIO*self.y, 32, 64)

		self.texture = self.textures.subsurface(0, 0, self.tWidth, self.tHeight)

	def pickup(self):
		self.pickedUp = True
		# self.sounds[1].play()

	def renderCorner(self, surface):
		surface.blit(self.texture, (30, HEIGHT-64))

	def render(self, surface, time, objects, ox=0, oy=0):
		if not self.pickedUp:
			surface.blit(self.texture, (GRIDX+GRATIO*self.x+ox-self.tWidth//4,GRIDY+GRATIO*self.y+oy-self.tHeight//4))
		return not self.pickedUp
