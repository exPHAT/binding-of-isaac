from pygame import *
from time import time as cTime

class Animation:
	"""Class for all animations"""

	def __init__(self, frames, interval):
		self.frames = frames
		self.frameCount = len(self.frames)
		self.interval = interval/self.frameCount # Wait between frames

		self.lastFrame = cTime() # Creation time
		self.currentIndex = -1 # There will be an step right away, counter act it
		self.frame = self.frames[self.currentIndex] # Start off current frame
		self.looped = False # Has made a complete loop

		# Assume all images are the same size
		self.width = self.frames[0].get_width()
		self.height = self.frames[0].get_height()

	def resize(self, percent):
		'Resize all frames'

		# Create new height
		self.width = int(self.width*percent)
		self.height = int(self.height*percent)

		# Resize all frames
		self.frames = [transform.scale(self.frames[i], (self.width, self.height)) for i in range(len(self.frames))]
		self.frame = self.frames[self.currentIndex] # Set new frame incase no step

	def setInterval(self, interval):
		'Change animation interval'

		self.interval = interval/self.frameCount

	def reset(self):
		'Reset animation to start'

		self.currentIndex = 0
		self.frame = self.frames[self.currentIndex]

	def step(self):
		'Step the animation forward a frame'

		self.currentIndex += 1
		if self.currentIndex >= self.frameCount:
			self.currentIndex = 0
			self.looped = True

		self.frame = self.frames[self.currentIndex]

	def render(self, time):
		'Return the current frame'
		
		if time-self.lastFrame >= self.interval:
			self.step()
			self.lastFrame = time

		return self.frame
