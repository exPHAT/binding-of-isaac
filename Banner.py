from pygame import *
from time import time as cTime
from func import *

class Banner:
	def __init__(self, text, textures):
		self.text = text

		self.snap = loadCFont("banner.png", 12, 10, 26)
		self.streak = textures["streak"]

		self.start = cTime()

		self.drawText = write(text, self.snap, alph="abcdefghijklmnopqrstuvwxyz ")
	def draw(self, surface, text):
		surface.blit(self.streak,(80,100))
		surface.blit(self.drawText,(380,150))

	def render(self, surface):
		self.slide = surface.copy()

	
		if cTime() - self.start <= 3:
			self.draw(surface, self.drawText)
		else:
			return True

		return False
