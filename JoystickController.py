# JoystickController.py
# Aaron Taylor
# Moose Abumeeiz
#
# Takes input from the joystick and simulates key presses for
# the corrisponding control 
# 

from pygame import *

class JoystickController:
	"""Custom Joystick event class"""

	def __init__(self, stick, thresh, leftStick=[115, 100, 119, 97], rightStick=[274, 275, 273, 276]):
		self.stick = stick
		self.thresh = thresh
		self.keys = leftStick,rightStick

		self.axis = [0, 0, 0, 0]

		#[[115, 100, 119, 97], [274, 275, 273, 276], [], [], 0, 0]

	def fixKeys(self):
		pass

	def getAxis(self, index):
		# Get stick 
		pos = round(self.stick.get_axis(index), 1)

		if abs(pos) < self.thresh:
			return 0

		elif pos >= self.thresh:
			return 1

		elif pos <= -self.thresh:
			return -1

	def update(self):
		newAxis = [self.getAxis(i) for i in range(4)]

		print(newAxis)

		if newAxis[0] != self.axis[0]:
			# change in joystick 1 X
			a = newAxis[0]

			# EMULATE ALL THE EVENTS
			if a == 0:
				self.createKeyEvent(self.keys[0][3], False)
				self.createKeyEvent(self.keys[0][1], False)
			elif a < 0:
				self.createKeyEvent(self.keys[0][3], True)
			else:
				self.createKeyEvent(self.keys[0][1], True)
		elif newAxis[1] != self.axis[1]:
			# change in joystick 1 Y
			a = newAxis[1]

			# MOAR EVENTS
			if a == 0:
				self.createKeyEvent(self.keys[0][0], False)
				self.createKeyEvent(self.keys[0][2], False)
			elif a < 0:
				self.createKeyEvent(self.keys[0][2], True)
			else:
				self.createKeyEvent(self.keys[0][0], True)

		elif newAxis[3] != self.axis[3]:
			# change in joystick 1 X
			a = newAxis[3]

			# OMG EVENTS
			if a == 0:
				self.createKeyEvent(self.keys[1][0], False)
				self.createKeyEvent(self.keys[1][2], False)
			elif a < 0:
				self.createKeyEvent(self.keys[1][2], True)
			else:
				self.createKeyEvent(self.keys[1][0], True)


		self.axis = newAxis


	def createKeyEvent(self, key, down):
		evnt = event.Event(KEYDOWN if down else KEYUP, {
			'key': key,
			'unicode': '',
		})

		event.post(evnt) # Create event
