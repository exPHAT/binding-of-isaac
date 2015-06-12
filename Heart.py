# Heart.py
# Aaron Taylor
# Moose Abumeeiz
#
# The heart can be rendered on the floor or on the HUD.
# Taking damage will result in half of a heart loss.
# 

from pygame import *
from const import *
from Animation import *
from Item import *
import func

class Heart(Item):
	"""Pickup Heart class"""

	price = 0
	
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

		# Load the font for the shop price
		self.digits = func.loadCFont("main.png", 20, 16, 36, size=1.8)

	def pickup(self):
		self.pickedUp = True
		self.sound.play()

	def render(self, surface, time, objects, ox=0, oy=0):
		# Render the heart on the ground
		if not self.pickedUp:
			# draw.rect(surface, (255,0,0), self.bounds)
			surface.blit(self.texture, (GRIDX+GRATIO*self.x-self.width//4+ox,GRIDY+GRATIO*self.y-self.height//4+oy))
			if self.price != 0:
				surface.blit(func.write(str(self.price), self.digits, dark=0), (GRIDX+GRATIO*self.x+ox-5,GRIDY+GRATIO*self.y+oy+35))
		return not self.pickedUp
