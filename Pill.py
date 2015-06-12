# Pill.py
# Aaron Taylor
# Moose Abumeeiz
#
# The pill has a 50/50 chance of being positive or negative.
# It will display a banner when taken
# 

from pygame import *
from random import *
from const import *
from Item import *
from PHD import *
import func

class Pill(Item):
	tWidth = 64
	def __init__(self, xy, texture):
		self.x, self.y = xy
		self.texture = texture.subsurface(randint(0,2)*64, randint(0,2)*64, 64, 64)
		self.bounds = Rect(GRIDX+GRATIO*self.x,GRIDY+GRATIO*self.y, 32, 64)
		self.digits = func.loadCFont("main.png", 20, 16, 36, size=1.8)

	def use(self, character):
		# Choose random affect and wether its positive or negative
		
		hasPHD = sum([1 if type(item) == PHD else 0 for item in character.items]) > 0
		self.stats = [0]*6
		self.stats[randint(0,5)] = 1 if randint(0,1) or hasPHD else -1

		return not self.pickedUp
