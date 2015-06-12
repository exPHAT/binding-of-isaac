# Explosion.py
# Aaron Taylor
# Moose Abumeeiz
#
# This class is spawned by a bomb and creates an explosion animations
# 

from pygame import *
from const import *
from Animation import *

class Explosion:
	"""Bomb explosion class"""

	def __init__(self, variant, xy, sound, textures):
		self.variant = variant
		self.x = xy[0]
		self.y = xy[1]
		self.sound = sound
		self.textures = textures[variant]

		self.frames = [self.textures.subsurface(192*i - (i//4)*768,192*(i//4), 192, 192) for i in range(12)]

		self.anim = Animation(self.frames, .45)
		sound.play() # Play explosion sound

	def render(self, surface, time, ox=0, oy=0):
		# Get frame and blit to screen
		frame = self.anim.render(time)
		if self.anim.looped:
			return False
		surface.blit(frame, ((GRIDX + GRATIO*self.x) - self.anim.width//2 + ox, (GRIDY + GRATIO*self.y) - self.anim.height//2 - 50 + oy))
		return True