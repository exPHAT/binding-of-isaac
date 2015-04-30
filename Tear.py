from pygame import *
from const import *
from random import randint
from Animation import *

class Tear:
	"""Main tear class"""

	def __init__(self, direction, xy, ixy, speed, damage, shotRange, friendly, textures, sounds):
		self.direction = direction
		self.speed = int(speed*2)+4
		self.damage = damage+3
		self.friendly = friendly
		self.range = (shotRange*20)+200
		self.distance = 0

		self.sounds = sounds

		self.x = xy[0]
		self.y = xy[1]

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
			frame = self.popping.render(time)
			if self.popping.looped:
				return False
			surface.blit(frame, (self.x-self.popping.width//2, self.y-self.popping.height//2))
			return True

		if abs(self.x-self.ox) < self.range and abs(self.y-self.oy) < self.range:
			dx = 0
			dy = 0

			if self.direction == 0:
				# Down
				dy += self.speed
			elif self.direction == 1:
				# Right
				dx += self.speed
			elif self.direction == 2:
				# Up
				dy -= self.speed
			elif self.direction == 3:
				# Left
				dx -= self.speed

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
				return self.pop(True)

			self.x += dx
			self.y += dy

			surface.blit(self.texture, (self.x-self.width//2, self.y-self.height//2))

			return True
		return self.pop(False)