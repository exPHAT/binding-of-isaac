# Maw.py
# Aaron Taylor
# Moose Abumeeiz
#
# Maw follows the user just like a fly. Just with a diffrent texture
# 

from pygame import *
from const import *
from func import *
from Fly import *

class Maw(Fly):
	hurtDistance = 1
	health = 12
	isFlying = False

	def __init__(self, xy, sounds, textures):
		self.x, self.y = xy

		self.sounds = sounds

		self.frames = [textures.subsurface(0, 0, 64, 64)]
		self.deathFrames = [textures.subsurface(0,0,0,0) for i in range(1)]

		# Create his still animation
		self.anim = Animation(self.frames, 0.04)

		self.speed = 1.5/GRATIO