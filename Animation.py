# Animation.py
# Aaron Taylor
# Moose Abumeeiz
#
# This is the class for all animations in the game, based on time
# it will advance the frame when it is the correct time
# 

from pygame import *
from time import time as cTime

class Animation:
	"""Class to handle all animation timing"""

	def __init__(self, frames, interval, shouldLoop=True):
		self.frames = frames
		self.frameCount = len(self.frames)
		self.interval = interval/self.frameCount # Wait between frames
		self.shouldLoop = shouldLoop

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

		# Re-set the frame interval
		self.interval = interval/self.frameCount

	def setFrame(self, index):
		'Sets the current frame index'

		# Ensure changing it wont cause an error
		if index < self.frameCount:
			self.currentIndex = index
			self.frame = self.frames[self.currentIndex]

	def reset(self, time):
		'Reset animation to start'

		# Re-set the current index and re-set the current frame
		self.currentIndex = 0
		self.frame = self.frames[self.currentIndex]
		self.lastFrame = time

	def step(self):
		'Step the animation forward a frame'

		self.currentIndex += 1
		if self.currentIndex >= self.frameCount:
			# The animation has surpassed the last frame, restart it
			if self.shouldLoop:
				self.currentIndex = 0
				self.looped = True
			else:
				self.currentIndex -= 1

		self.frame = self.frames[self.currentIndex]

	def render(self, time):
		'Return the current frame'
		
		# Decide wether or not we should advance a frame
		if time-self.lastFrame >= self.interval:
			self.step()
			self.lastFrame = time

		return self.frame
