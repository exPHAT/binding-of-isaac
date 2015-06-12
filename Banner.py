# Banner.py
# Aaron Taylor
# Moose Abumeeiz
#
# This is the class for the banner that shows up when you take a pill
# or appear on a new floor
# 

from pygame import *
from time import time as cTime
from func import *
from const import *

class Banner:
	def __init__(self, text, textures):
		self.text = text # The text to show

		self.snap = loadCFont("banner.png", 12, 10, 26) # Load the font
		self.streak = textures["streak"] # The black background behind it

		self.start = cTime() # When the banner was created
		
		# Create a surface for the text
		self.drawText = write(text, self.snap, alph="abcdefghijklmnopqrstuvwxyz ", dark=0)
	def draw(self, surface, text):
		# Draw it on the surface
		surface.blit(self.streak,(80,100))
		surface.blit(self.drawText,(WIDTH//2 - self.drawText.get_width()//2,150))

	def render(self, surface):
		self.slide = surface.copy()

		# Only allow it to show up for 3 seconds	
		if cTime() - self.start <= 3:
			self.draw(surface, self.drawText)
		else:
			return True

		return False
