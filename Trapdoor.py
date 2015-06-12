# Trapdoor.py
# Aaron Taylor
# Moose Abumeeiz
#
# The trapdoor will spawn when there are no enemies in the boss room
# 

from pygame import *
from func import *
from const import *

class Trapdoor:
	x = 6
	y = 3

	destroyed = False
	collideable = False

	def __init__(self, texture):
		self.texture = texture.subsurface(0,0, 128, 128)
		self.bounds = Rect(GRIDX+GRATIO*self.x-35+10,GRIDY+GRATIO*self.y-35, 70, 70)

	def render(self, surface, time, objects, ox=0, oy=0):
		surface.blit(self.texture, (GRIDX+GRATIO*self.x-64+10++ox,GRIDY+GRATIO*self.y-64+oy))
		return True