from pygame import *
from const import GRATIO, GRIDX, GRIDY


class Rock:
	"""Main level rock class"""

	def __init__(self, variant, xy, special, textures):
		self.variant = variant
		self.x = xy[0]
		self.y = xy[1]
		self.special = special

		self.collideable = True

		self.texture = textures.subsurface(Rect((variant*64), 0, 64, 64))
		self.bounds = Rect(GRIDX+GRATIO*self.x-16-4, GRIDY+GRATIO*self.y-16-5, 64+4, 64)

		# self.texture = textures[variant] if not special else textures[0] # TODO: SPECIAL INDEX

		self.tWidth = self.texture.get_width()
		self.tHeight = self.texture.get_height()
		self.destroyed = False

	def destroy(self):
		if self.special:
			# TODO: TAKE CARE OF DROPS
			pass

		self.destroyed = True

	def hurt(self, ammount):
		pass

	def render(self, surface, ox=0, oy=0):
		surface.blit(self.texture, ((GRIDX + self.x*GRATIO - 16)+ox, (GRIDY + self.y*GRATIO - 16)+oy))