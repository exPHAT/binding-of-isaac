from pygame import *
from time import time as cTime

class Animation:
	"""Class for all animations"""

	def __init__(self, frames, interval):
		self.frames = frames
		self.frameCount = len(self.frames)
		self.interval = interval/self.frameCount

		self.lastFrame = cTime()
		self.currentIndex = -1
		self.frame = self.frames[self.currentIndex]
		self.looped = False

		self.width = self.frames[0].get_width()
		self.height = self.frames[0].get_height()

	def resize(self, percent):
		self.width = int(self.width*percent)
		self.height = int(self.height*percent)

		self.frames = [transform.scale(self.frames[i], (self.width, self.height)) for i in range(len(self.frames))]

	def setInterval(self, interval):
		self.interval = interval

	def reset(self):
		self.currentIndex = 0
		self.frame = self.frames[self.currentIndex]

	def step(self):
		self.currentIndex += 1
		if self.currentIndex >= self.frameCount:
			self.currentIndex = 0
			self.looped = True

		self.frame = self.frames[self.currentIndex]

	def render(self, time):
		if time-self.lastFrame >= self.interval:
			self.step()
			self.lastFrame = time

		return self.frame
