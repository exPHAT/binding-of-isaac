from pygame import *
from const import *
from Animation import *

class Heart:
	"""Pickup Heart class"""

	def __init__(self, variant, xy, sound, textures):
		self.variant = variant
		self.x = xy[0]
		self.y = xy[1]
		self.sound = sound[[0,1,0][variant]]
		self.textures = textures

		self.health = 2

		self.bounds = Rect(GRIDX+GRATIO*self.x,GRIDY+GRATIO*self.y, 32, 32)

		self.texture = self.textures.subsurface(0,64*variant,64,64)

		self.width = self.texture.get_width()
		self.height = self.texture.get_height()

		self.collideable = False
		self.pickedUp = False

	def pickup(self):
		self.pickedUp = True
		self.sound.play()

	def render(self, surface, time, ox=0, oy=0):
		if not self.pickedUp:
			# draw.rect(surface, (255,0,0), self.bounds)
			surface.blit(self.texture, (GRIDX+GRATIO*self.x-self.width//4+ox,GRIDY+GRATIO*self.y-self.height//4+oy))
		return not self.pickedUp
