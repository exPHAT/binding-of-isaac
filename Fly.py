from pygame import *
from const import *
from Enemy import *
from Animation import *
from math import *

class Fly(Enemy):
	"""Simple enemy fly class"""

	isFlying = False
	dank = False

	def __init__(self, xy, sounds, textures):
		self.x, self.y = xy

		self.sounds = sounds

		self.frames = [textures.subsurface(i*64, 0, 64, 64) for i in range(2)]
		self.deathFrames = [textures.subsurface(i*128 - ((i//4)*128*4), 128 * (i//4 + 1), 128, 128) for i in range(12)]

		self.anim = Animation(self.frames, 0.04)

		self.health = 2
		self.speed = 1.5/GRATIO
		self.hurtDistance = 0.8

	def die(self):
		if not self.dead:
			self.anim = Animation(self.deathFrames, 0.24)
			self.dead = True
			self.sounds[-1].play() # Play death sound

	def render(self, surface, time, character, nodes, paths):

		self.cx, self.cy = ix, iy = (character.x-GRIDX)/GRATIO, (character.y-GRIDY)/GRATIO
		dx, dy = (self.cx-self.x), (self.cy-self.y)

		if not self.dead:
			if not self.dank:
				self.pathFind((ix, iy), nodes, paths)
				self.dank = True
			self.move()

			for t in character.tears:
				tx = (t.x-GRIDX)/GRATIO
				ty = (t.y-GRIDY)/GRATIO
				dist = sqrt((tx-self.x)**2+(ty-self.y)**2)
				if dist < self.hurtDistance and not t.poped:
					t.pop(True)
					# TAKE DAMAGE HERE
					self.die()

			if abs(dx) < 0.8 and abs(dy) < 0.8:
				fx, fy = (GRIDX+GRATIO*self.x, GRIDY+GRATIO*self.y)

				character.hurt(1, fx, fy, time)



			frame = self.anim.render(time)
		else:
			frame = self.anim.render(time)
			if self.anim.looped:
				return False

		surface.blit(frame, (GRIDX+GRATIO*self.x-self.anim.width//2, GRIDY+GRATIO*self.y-self.anim.height//2))
		return True