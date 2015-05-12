from pygame import *
from const import GRATIO

import func

class Door:
	"""The main door class"""

	# DOOR TYPES:
	#
	# 0 - Normal door
	# 1 - Treasure door
	# 2 - Boss door
	# 3 - Devil door
	# 4 - Angel door

	# ROOMS ARE 13 x 7

	def __init__(self, side, variant, isOpen, texture, sounds):
		self.side = side
		self.variant = variant
		self.texture = func.darken(texture[variant], .25)
		self.sounds = sounds

		self.isOpen = isOpen
		self.x = -1
		self.y = -1

		if variant != 3 and variant != 4:
			# Rotate the door texture to be the correct orrientation
			self.doorFrame = transform.rotate(self.texture.subsurface(0, 0, 64*2, 48*2), -(180 - (90*self.side)))
			self.doorBack  = transform.rotate(self.texture.subsurface(64*2, 0, 64*2, 48*2), -(180 - (90*self.side)))
			self.lDoor     = transform.rotate(self.texture.subsurface(0, 48*2, 64*2, 48*2), -(180 - (90*self.side)))
			self.rDoor     = transform.rotate(self.texture.subsurface(64*2, 48*2, 64*2, 48*2), -(180 - (90*self.side)))

		else:

			sounds[["devilRoomAppear", "angelRoomAppear"][variant-3]].play()

			self.doorFrame = transform.rotate(self.texture, -(180 - (90*self.side)))
			self.doorBack  = Surface((0,0))
			self.lDoor     = Surface((0,0))
			self.rDoor     = Surface((0,0))

		self.x = [7, 14, 7, -1][self.side]
		self.y = [8, 4, -1, 4][self.side]

		self.xOff = [0, 6, 0, 48][self.side]
		self.yOff = [-48, -52, -6, -52][self.side]

		if side == 0:
			self.rect = Rect(468,436,22,32)
		elif side == 1:
			self.rect = Rect(806,252,32,22)
		elif side == 2:
			self.rect = Rect(470,68,22,32)
		elif side == 3:
			self.rect = Rect(122,251,32,22)


	def close(self):
		if self.isOpen:
			self.isOpen = False
			self.sounds["doorClose"].stop()
			self.sounds["doorClose"].play()

	def open(self):
		if not self.isOpen:
			self.isOpen = True
			self.sounds["doorOpen"].stop()
			self.sounds["doorOpen"].play()

	def step(self):
		pass

	def render(self, surface, ox=0, oy=0):
		width = self.doorFrame.get_width()
		height = self.doorFrame.get_height()

		xy = (((142 + (self.x*GRATIO)-(width//2)-GRATIO//2) + self.xOff) + ox, ((89 + (self.y*GRATIO)-(height//2)+GRATIO//2)+self.yOff) + oy)

		surface.blit(self.doorBack, xy)

		if not self.isOpen:
			surface.blit(self.lDoor, xy)
			surface.blit(self.rDoor, xy)

		surface.blit(self.doorFrame, xy)

