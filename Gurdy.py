from pygame import *
from const import *
from func import *
from Animation import *
from Enemy import *

class Gurdy(Enemy):
	x = 6
	y = 3

	health = 10
	hurtDistance = 2

	def __init__(self, texture, sounds):
		self.body = texture.subsurface(0, 0, 284, 320)
		self.head = texture.subsurface(0, 768, 84, 104)
		self.sounds = sounds

		emergeFrames = [texture.subsurface(i*84, 672, 84, 104) for i in range(3)]+[self.head]

		self.emerge = Animation(emergeFrames, .3)
		self.demarge = Animation(emergeFrames[::-1], .3)


	def die(self):
		self.dead = True

	def render(self, surface, time, character, nodes, paths, bounds, obsticals):
		# Draw body
		surface.blit(self.body, (GRIDX+GRATIO*self.x-284/2, GRIDY+GRATIO*self.y-320/2))

		# Blit head
		surface.blit(self.emerge.render(time), (GRIDX+GRATIO*self.x-284/4 + 30, GRIDY+GRATIO*self.y-320/4 - 40))

		self.checkHurt(character, time)

		return not self.dead