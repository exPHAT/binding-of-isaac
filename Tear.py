# Tear.py
# Aaron Taylor
# Moose Abumeeiz
#
# The tear can be shot from an enemy or the main character.
# It will hurt anything of the oppisite type (enemies and good guys)
# 

from pygame import *
from const import *
from random import randint
from Animation import *

class Tear:
	"""Main tear class"""

	def __init__(self, xyv, xy, ixy, speed, damage, shotRange, friendly, textures, sounds):	
		self.xVel, self.yVel = xyv # X, Y velocity
		
		# Stats
		self.speed = int(speed*2)+4
		self.damage = damage+3
		self.friendly = friendly
		self.range = (shotRange*20)+200
		self.distance = 0

		# sounds
		self.sounds = sounds

		self.x = xy[0]
		self.y = xy[1]

		# Inherited x and y velocity
		self.iXVel = ixy[0]
		self.iYVel = ixy[1]

		self.poped = False

		self.frames = [textures[1].subsurface(Rect((i*128 - ((i)//4)*128*4), ((i//4)*128), 128, 128)) for i in range(12)]
		self.popping = Animation(self.frames, 0.24)

		self.ox = self.x
		self.oy = self.y

		offX = 0
		offY = 0

		if damage > 7:
			offX = -7
			offY = 1

		if not friendly:
			offY += 2

		# Play random shoot sound
		sounds[randint(0,1)].play()

		# Texture setup
		self.texture = textures[0].subsurface(Rect((self.damage+offX)*64, offY*64, 64, 64))
		self.width = self.texture.get_width()
		self.height = self.texture.get_height()

	def step(self):
		self.texture = self.frames[self.frameIndex]
		self.frameIndex += 1

	def pop(self, collision):
		self.poped = True
		if collision:
			self.sounds[2].play() # Play collison pop
		else:
			self.sounds[1].play() # Play normal pop
		return True

	def render(self, surface, time, bounds, obsticals):
		if self.poped:
			# Return popping tear
			frame = self.popping.render(time)
			if self.popping.looped:
				return False
			surface.blit(frame, (self.x-self.popping.width//2, self.y-self.popping.height//2))
			return True

		if abs(self.x-self.ox) < self.range and abs(self.y-self.oy) < self.range:
			dx = 0
			dy = 0

			dx += self.xVel * self.speed
			dy += self.yVel * self.speed

			# Add inherited X and Y velocity
			dx += self.iXVel
			dy += self.iYVel

			inBoundsX = bounds.collidepoint(self.x+dx, self.y)
			inBoundsY = bounds.collidepoint(self.x, self.y+dx)

			rockColX = False
			rockColY = False

			for ob in obsticals:
				# Collide with ob
				try:
					if ob.destroyed:
						continue
				except:
					pass
				# Collude with object
				rcx = ob.bounds.collidepoint(self.x+self.speed, self.y)
				rcy = ob.bounds.collidepoint(self.x, self.y+self.speed)
				if rcx or rcy:
					try:
						ob.hurt(1)
					except:
						pass

					if not ob.collideable:
						rockColX = rockColY = False
					return self.pop(True)

			if not inBoundsX or not inBoundsY:
				# Ensure tear is within level bounds
				return self.pop(True)

			# Add to x and y
			self.x += dx
			self.y += dy

			surface.blit(self.texture, (self.x-self.width//2, self.y-self.height//2))

			return True
		return self.pop(False)