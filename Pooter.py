from pygame import *
from const import *
from Enemy import *
from Animation import *
from math import *

class Pooter(Enemy):
	"""Simple enemy fly class"""

	def __init__(self, xy, sounds, textures):
		self.x, self.y = xy

		self.sounds = sounds

		self.frames = [textures.subsurface(i*64, 0, 64, 64) for i in range(2)]
		# self.deathFrames = [textures.subsurface(i*128 - ((i//4)*128*4), 128 * (i//4 + 1), 128, 128) for i in range(12)]

		self.anim = Animation(self.frames, 0.04)

		self.health = 2

	def die(self):
		if not self.dead:
			# self.anim = Animation(self.deathFrames, 0.24)
			self.dead = True
			self.sounds[-1].play() # Play death sound

	def render(self, surface, time, character, obsticals):
		speed = 1.5/GRATIO

		ix, iy = (character.x-GRIDX)/GRATIO, (character.y-GRIDY)/GRATIO


		dx, dy = (ix-self.x), (iy-self.y)

		something = sqrt(dx**2+dy**2)

		rx = dx/something
		ry = dy/something

		hurtDistance = 0.8

		if not self.dead:

			self.x += speed*rx
			self.y += speed*ry

			for t in character.tears:
				tx = (t.x-GRIDX)/GRATIO
				ty = (t.y-GRIDY)/GRATIO
				dist = sqrt((tx-self.x)**2+(ty-self.y)**2)
				if dist < 0.6 and not t.poped:
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