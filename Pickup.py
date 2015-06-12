# Pickup.py
# Aaron Taylor
# Moose Abumeeiz
#
# This is the class for the HUD pickups (keys, bombs, coins)
# 

from pygame import *

class Pickup:
	"""The class for the HUD pickup counters"""

	def __init__(self, variant, textures, font):
		self.variant = variant
		self.score = 0
		self.font = font

		self.digit1 = font[0]
		self.digit2 = font[0]

		xPos = 0
		yPos = 16 * self.variant

		if variant == 2:
			xPos = 16
			yPos = 0

		self.texture = textures.subsurface(Rect(xPos*2, yPos*2, 16*2, 16*2))

	def updateDigits(self):
		# Update textures for digits

		string = str(self.score)
		if len(string) == 1:
			# Prepend with a 0
			string = "0"+string
		self.digit1 = self.font[int(string[0])]
		self.digit2 = self.font[int(string[1])]

	def add(self, ammount):
		self.score += ammount
		if self.score > 99:
			self.score = 99

		self.updateDigits()

	def use(self, ammount):
		self.score -= ammount
		if self.score < 0:
			self.score += ammount

			self.updateDigits()
			return False

		self.updateDigits()
		return True

	def render(self, surface):
		# Blit icon, digit1, and digit 2
		surface.blit(self.texture, (40, 88 + 24*self.variant))
		surface.blit(self.digit1, (68, 94 + 24*self.variant))
		surface.blit(self.digit2, (80, 94 + 24*self.variant))
