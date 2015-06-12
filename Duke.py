# Duke.py
# Aaron Taylor
# Moose Abumeeiz
#
# This is the first boss, Gurdy. He just sits there and takes your bullets
# 

from pygame import *
from const import *
from func import *
from Animation import *
from Enemy import *
from Fly import *

class Duke(Enemy):
	x = 6
	y = 3

	health = 100
	hurtDistance = 1.3

	def __init__(self, textures, sounds):
		self.texture = textures["bosses"]["duke"].subsurface(0, 128, 160, 128)
		self.sounds = sounds
		self.textures = textures

		self.frames = [
			textures["bosses"]["duke"].subsurface(160, 128, 160, 128),
			textures["bosses"]["duke"].subsurface(160, 0, 160, 128),
			textures["bosses"]["duke"].subsurface(0, 0, 160, 128)
		]

		self.tearTextures = textures["tears"]
		self.tearSounds = sounds["tear"]

		self.animation = Animation(self.frames, 0.5)

		self.textures = textures

		self.lastShot = -1

		self.flies = []
		self.animating = False

	def die(self):
		self.dead = True

	def render(self, surface, time, character, nodes, paths, bounds, obsticals):

		# Blit head
		if not self.dead:
			if not self.animating:
				surface.blit(self.texture, (GRIDX+GRATIO*self.x-284/4 +10, GRIDY+GRATIO*self.y-320/4))
			else:
				surface.blit(self.animation.render(time), (GRIDX+GRATIO*self.x-284/4 + 10, GRIDY+GRATIO*self.y-320/4))

			dx = character.x-(GRIDX+GRATIO*self.x)
			dy = character.y-(GRIDY+GRATIO*self.y)
			dist = sqrt(dx**2+dy**2)

			self.x += (dx/dist)/60
			self.y += (dy/dist)/60
		
			if time-self.lastShot >= 3:
				self.lastShot = time
				self.animating = False
				self.flies.append(Fly((self.x+randint(-1, 1), self.y), [self.sounds["deathBurst"]], self.textures["enemies"]["fly"]))
			elif time-self.lastShot >= 2.5:
				self.animation.reset(time)
				self.animating = True

			self.checkHurt(character, time)

		for fly in self.flies[:]:
			if not fly.render(surface, time, character, nodes, paths, bounds, obsticals):
				self.flies.remove(fly)

		if len(self.flies) > 0:
			return True

		return not self.dead